import os
import re
import json
import requests
from fake_useragent import UserAgent

class Cerebras_Unofficial:
    def __init__(self, cookies:str):
        self.cookies = cookies
        self.config_file_path = os.path.join(os.path.expanduser("~"), "CerebrasUnofficial.json")
        try:
            # Check if the config file exists
            if not os.path.exists(self.config_file_path):
                # If the file doesn't exist, create a new empty JSON file
                with open(self.config_file_path, 'w') as config_file:
                    json.dump({}, config_file)  # Creating an empty JSON structure
                print(f"New config file created at {self.config_file_path}")
            else:
                with open(self.config_file_path, 'r') as f:
                    api_key = json.load(f)["data"]["GetMyDemoApiKey"]
                    self.api_key = api_key
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error encountered: {e}")
            print(self.refresh_api_key())
            self.__init__(self.cookies)

    def refresh_api_key(self) -> str:
        """
        Refreshes the API key by making a request to the Cerebras API endpoint.

        This method sends a POST request to the Cerebras API to obtain a new demo API key.
        The response is then saved to a JSON configuration file located in the user's home directory.
        If the request is successful, the new API key is stored and a success message is returned.
        In case of any errors, appropriate error messages are printed and the method retries the request.

        Returns:
            str: A message indicating the result of the API key refresh operation.
        """
        headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': str(self.cookies),
        'dnt': '1',
        'origin': 'https://inference.cerebras.ai',
        'priority': 'u=1, i',
        'referer': 'https://inference.cerebras.ai/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': UserAgent().random
        }

        json_data = {
            'operationName': 'GetMyDemoApiKey',
            'variables': {},
            'query': 'query GetMyDemoApiKey {\n  GetMyDemoApiKey\n}',
        }
        try:
            response = requests.post('https://inference.cerebras.ai/api/graphql', headers=headers, json=json_data)
            response.raise_for_status()
            if response.status_code == 200 and response.ok:
                # Writing to a JSON file with human-readable date format
                with open(self.config_file_path, 'w') as json_file:
                    json.dump(response.json(), json_file, indent=4)
                return "\033[1;93mAPI key updated successfully!\n\033[0m"
            else:
                print(f"\033[1;91mUnexpected response status: {response.status_code}. Please check the API endpoint or your request parameters.\033[0m")
                return "\033[1;91mFailed to update API key due to unexpected response.\n\033[0m"
        except FileNotFoundError:
            print(f"\033[1;91m{self.config_file_path} not found, creating a new file.\033[0m")
            with open(self.config_file_path, 'w') as json_file:
                json.dump(response.json(), json_file, indent=4)
            print(f"\033[1;92mNew file created and data written successfully to {self.config_file_path}\033[0m")
            return "\033[1;93mAPI key updated successfully!\n\033[0m"
        except requests.exceptions.RequestException as e:
            print(f"🔄 Demo API key refresh failed due to network error: {e}. Retrying... 🔄")
            print(self.refresh_api_key())
        except Exception as e:
            print(f"🔄 Demo API key refresh failed due to an unexpected error: {e}. Retrying... 🔄")
            print(self.refresh_api_key())
    
    def chat(self, message: str, system_prompt: str = "You are a helpful assistant.", model:str = "llama3.1-8b", temperature: int = 0.7, max_tokens: str = 1000000000, timeout: int = None, stream:bool = False) -> str:
        """
        Sends a chat message to the model and returns the response.

        Parameters:
            - message (str): The user message to send to the model.
            - system_prompt (str, optional): The system prompt to provide context to the model. Defaults to "You are a helpful assistant."
            - model (str, optional): The model to use. Defaults to 'llama3.1-8b'. Available Models: llama3.1-8b, llama3.1-70b
            - temperature (int, optional): The temperature to use for the model's response. Defaults to 0.7.
            - max_tokens (str, optional): The maximum number of tokens to generate. Defaults to 1000000000.
            - timeout (int, optional): The timeout for the request. Defaults to None.
            - stream (bool, optional): Whether to stream the response. Defaults to False.

        Returns:
            - str: The response from the model.
        """
        headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {self.api_key}',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://inference.cerebras.ai',
        'priority': 'u=1, i',
        'referer': 'https://inference.cerebras.ai/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': str(UserAgent().random),
        'x-stainless-arch': 'unknown',
        'x-stainless-lang': 'js',
        'x-stainless-os': 'Unknown',
        'x-stainless-package-version': '1.5.0',
        'x-stainless-retry-count': '0',
        'x-stainless-runtime': 'browser:chrome',
        'x-stainless-runtime-version': '131.0.0',
        }
        json_data = {
            'messages': [
                {
                    'content': system_prompt,
                    'role': 'system',
                },
                {
                    'content': message,
                    'role': 'user',
                },
            ],
            'model': model,
            'stream': True,
            'temperature': temperature,
            'top_p': 1,
            'max_completion_tokens': max_tokens,
        }
        try:
            response = requests.post('https://api.cerebras.ai/v1/chat/completions', headers=headers, json=json_data, stream=True, timeout=None)
            if response.status_code==401:
                print("🚨 Alert: Your demo API key has expired. 🕰️ Reinitializing the system To Generate New Demo Api Key... 🔄")
                print(self.refresh_api_key())
                self.__init__(self.cookies)
                return self.chat(message, system_prompt, model, temperature, max_tokens, timeout, stream)
            if response.status_code==200 and response.ok:
                streaming_text = ""
                for value in response.iter_lines(decode_unicode=True, chunk_size=1000):
                    modified_value = re.sub("data: ", "", value)
                    try:
                        json_modified_value = json.loads(modified_value)
                        if json_modified_value["choices"][0]["delta"]["content"] != None:
                            if stream:print(json_modified_value["choices"][0]["delta"]["content"], end="")
                            streaming_text += json_modified_value["choices"][0]["delta"]["content"]
                    except:continue
                return streaming_text
            else:
                return f"🚨 Alert: Received unexpected status code {response.status_code}. Please check the request and try again."
        except Exception as e:
            return f"🚨 An error occurred: {e}"

if __name__ == "__main__":
    AI = Cerebras_Unofficial('__Host-authjs.csrf-token=XXXXXXXXXXX')
    print(AI.chat("Hi"))