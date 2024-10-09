import os
import time
import json
import requests
from tqdm import tqdm
from yaspin import yaspin
from datetime import datetime
from selenium import webdriver
from fake_useragent import UserAgent
from cerebras.cloud.sdk import Cerebras
from cerebras.cloud.sdk import AuthenticationError

class CerebrasAI:
    def __init__(self, model: str = 'llama3.1-8b'):
        """
        # Initializes the CerebrasAI class with the given model.

        # Args:
            - model (str, optional): The model to use. Defaults to 'llama3.1-8b'. Available Models: llama3.1-8b, llama3.1-70b
        """
        with yaspin(text="Initializing Required Path Variables...", color="cyan") as spinner:
            # current file path
            home_dir = os.path.expanduser("~")
            current_file_path = os.path.dirname(os.path.realpath(__file__))
            self.source_folder = os.path.join(home_dir, 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
            self.destination_folder = current_file_path + "/chromedata"
            if not os.path.exists(self.destination_folder):
                spinner.stop()
                print("\033[1;91m*********************************** 🚨 Destination folder not found in required path. 📁 Automatically copying to default location... 🔄 ************************************\033[0m")
                print("\033[1;91m******************************* 🚫 This process may take a few moments. Please do not attempt to interact with the system until it completes. *******************************\033[0m")
                self.copy_with_progress(self.source_folder, self.destination_folder)
            self.config_file_path = os.path.join(current_file_path, "config.json")
            # Check if the config file exists
            if not os.path.exists(self.config_file_path):
                # If the file doesn't exist, create a new empty JSON file
                with open(self.config_file_path, 'w') as config_file:
                    json.dump({}, config_file)  # Creating an empty JSON structure
                spinner.stop()
                print(f"New config file created at {self.config_file_path}")
            spinner.stop()

        with yaspin(text="Initializing AI...", color="magenta") as spinner:
            with open(self.config_file_path, 'r') as f:
                api_key = json.load(f)["user"]["demoApiKey"]
            self.api_key = api_key
            self.client = Cerebras(api_key=self.api_key)
            self.model = model
            spinner.stop()

    def get_total_size(self, folder) -> int:
        """
        - Returns the total size of all files in the given folder and its subfolders.
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total_size += os.path.getsize(fp)
                except PermissionError:
                    # Skip files that we don't have permission to access
                    continue
        return total_size

    def copy_with_progress(self, source_folder, destination_folder) -> None:
        """
        # Copies a folder and all its contents to a destination folder, with a progress bar.

        - param source_folder: The folder to copy from
        - param destination_folder: The folder to copy to
        - return: None
        """

        total_size = self.get_total_size(source_folder)
        copied_size = 0

        # Create destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        # Progress bar setup
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Copying", ncols=100)

        # Walk through the source folder
        for dirpath, dirnames, filenames in os.walk(source_folder):
            # Create corresponding destination directory
            dest_dir = dirpath.replace(source_folder, destination_folder, 1)
            os.makedirs(dest_dir, exist_ok=True)

            for file in filenames:
                source_file = os.path.join(dirpath, file)
                dest_file = os.path.join(dest_dir, file)

                try:
                    # Copy the file in chunks to track progress
                    with open(source_file, 'rb') as sf, open(dest_file, 'wb') as df:
                        while True:
                            buffer = sf.read(1024 * 1024)  # Read in chunks of 1MB
                            if not buffer:
                                break
                            df.write(buffer)
                            copied_size += len(buffer)
                            progress_bar.update(len(buffer))
                except PermissionError:
                    # Skip files that we don't have permission to copy
                    # print(f"Skipping file due to permission error: {source_file}")
                    continue
        progress_bar.close()

    def refresh_api_key(self) -> str:
        """
        - Refreshes the demo API key by using Selenium to open a headless Chrome session and fetch the cookies.
        - Then it uses the cookies to fetch the API key from the /api/auth/session endpoint.
        - The API key is then written to the config file in human-readable format.

        - If the refresh fails, it will retry the process.
        """
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={self.destination_folder}")
        options.add_argument('--profile-directory=Default')
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        driver.get("https://inference.cerebras.ai")

        print("\033[1;96mFetching Required Cookies...\033[0m")

        cookies = driver.get_cookies()
        driver.quit()

        cookies_dict = {item['name']: item['value'] for item in cookies}
        print(f"Required Cookies Dictionary: \033[1;95m{cookies_dict}\033[0m\n") 
        print("\033[1;92mRequired Cookies Fetched Successfully.\033[0m")

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://inference.cerebras.ai',
            'Referer': 'https://inference.cerebras.ai/',
            'user-agent': UserAgent().random
        }

        try:
            url = "https://inference.cerebras.ai/api/auth/session"

            payload = {}

            response = requests.request("GET", url, headers=headers, cookies=cookies_dict, data=payload, timeout=None)

            data = response.json()

            # Convert ISO format datetime to readable format
            def convert_to_readable_format(iso_datetime):
                return datetime.fromisoformat(iso_datetime.replace('Z', '')).strftime('On %d-%m-%Y At %I:%M:%S')

            # Update specific fields with readable format
            data['expires'] = convert_to_readable_format(data['expires'])
            data['createdAt'] = convert_to_readable_format(data['createdAt'])
            data['updatedAt'] = convert_to_readable_format(data['updatedAt'])

            # Convert nested 'user' timestamps as well
            data['user']['createdAt'] = convert_to_readable_format(data['user']['createdAt'])
            data['user']['updatedAt'] = convert_to_readable_format(data['user']['updatedAt'])

            try:
                # Writing to a JSON file with human-readable date format
                with open(self.config_file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
            except FileNotFoundError:
                print(f"\033[1;91m{self.config_file_path} not found, creating a new file.\033[0m")
                with open(self.config_file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                print(f"\033[1;92mNew file created and data written successfully to {self.config_file_path}\033[0m")
                
            print("\033[1;93mAPI key updated successfully!\n\033[0m")
                
            with open(self.config_file_path, 'r') as json_file:
                data = json.load(json_file)

            createdAt = data['createdAt']
            expires = data['expires']
            user = data['user']
            user_name = user['name']
            demo_api_key = user['demoApiKey']

            print(f"\033[1;95mHello {user_name}, Your API key is {demo_api_key}. It was generated {createdAt} and will expire {expires}.\033[0m")

        except Exception as E:
            print(f"🔄 Demo API key refresh failed due to {E}. Retrying... 🔄")
            self.refresh_api_key()
    
    def ask(self, message: str, system_prompt: str = "You are a helpful assistant.", temperature: int = 0.7, max_tokens: str = 1000000000, timeout: int = None, stream:bool = True) -> str:
        """
        # Ask CerebrasAI a question
        
        Args
            - message (str): The question to ask
            - system_prompt (str, optional): The system prompt to use. Defaults to "You are a helpful assistant."
            - temperature (int, optional): The temperature of the response. Defaults to 0.7
            - max_tokens (str, optional): The maximum number of tokens to generate. Defaults to 1000000000
            - timeout (int, optional): The timeout in seconds. Defaults to None
            - stream (bool, optional): Whether to stream the response in real time. Defaults to True

        # Returns
            - str: The response from CerebrasAI
        """
        try:
            messages = [{'content': system_prompt, 'role': 'system'}, {'content': message, 'role': 'user'}]
            start_time = time.time()
            response = self.client.chat.completions.create(messages=messages, model=self.model, temperature=temperature, max_tokens=max_tokens, timeout=timeout).choices[0].message.content
            taken_time = time.time()-start_time
            if stream:
                print("CerebrasAI: ", end="", flush=True)
                for chunk in response:print(f"\033[1;93m{chunk}", end="", flush=True)
                print(f"\nTime Taken: {taken_time:.2f} Seconds.\033[0m\n")
                return None
            return response
        except AuthenticationError:
            print("\033[1;91m🚨 Alert: Your demo API key has expired. 🕰️ Reinitializing the system To Generate New Demo Api Key... 🔄\033[0m")
            self.__init__(self.model)
            self.refresh_api_key()
            self.__init__(self.model)
            return self.ask(message, system_prompt, temperature, max_tokens, timeout)
        except Exception as response_error:
            return str(response_error)

if __name__ == "__main__":
    AI = CerebrasAI()
    while True:
        query = input("You: ")
        if not query.strip():continue
        start_time = time.time()
        response = AI.ask(query, stream=False)
        if response is not None:print(f"\033[1;93mCerebrasAI: {response}, Time Taken: {time.time()-start_time:.2f} Seconds.\033[0m\n")