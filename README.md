
# CerebrasAI

This repository provides an interface for interacting with the CerebrasAI API. It includes functionality for initializing the Cerebras environment, copying Chrome user data, refreshing API keys, and generating AI responses using the Cerebras model.

# Table of Contents

- Features
- Installation
- Usage
- Project Structure
- Requirements
- How It Works
- Troubleshooting
- Contributing
- License

# Features

- Model Initialization: Initialize the CerebrasAI class with any supported model (llama3.1-8b, llama3.1-70b).
- Copy Chrome User Data: Automatically copies required Chrome user data for cookie-based authentication.
- API Key Management: Refreshes and updates the demo API key by fetching cookies and making an authenticated request to the Cerebras platform.
- Text Generation: Interact with Cerebras AI models to generate text completions, including streaming responses.
- Progress Tracking: Progress bars and terminal spinners for long-running operations.
- Error Handling: Built-in mechanisms to handle any type of error (e.g., connection issues, missing dependencies, invalid input) and provide meaningful error messages or fallback options.
# Installation

### Step 1: Clone the Repository
```
git clone https://github.com/sujalrajpoot/CerebrasAI.git
cd CerebrasAI
```

### Step 2: Install the required dependencies
- Ensure you have Python installed. Then, install the required Python packages:
```
pip install -r requirements.txt
```

# Usage

### Step 1: Initialization
- You can initialize the CerebrasAI class with a specific model. Available models include llama3.1-8b and llama3.1-70b:

```python
from cerebras_ai import CerebrasAI

# Initialize with default model
ai = CerebrasAI()

# Initialize with a specific model
ai = CerebrasAI(model="llama3.1-70b")
```

### Generate AI Response
- You can ask questions to the AI using the ask method, which sends a message to the AI model and returns a response:

```python
response = ai.ask("What is the meaning of life?")
print(response)
```

# Project Structure
- cerebras_ai.py: The main code file containing the CerebrasAI class with all functionalities.
- requirements.txt: Contains all the dependencies required for the project.
- config.json: This file is generated automatically and stores the 
### API key and related information.

# Requirements

- Python 3.7+
- Chrome WebDriver
- Selenium
- tqdm
- yaspin
- Cerebras SDK
- Requests
- Fake UserAgent
# How It Works
- Initialization: The class is initialized with the model. It checks for existing config files and copies Chrome user data if required.
- Cookie Fetching: The class uses Selenium to open a headless Chrome session, fetch the necessary cookies, and extract the demo API key.
- Asking Questions: Once the API key is set, users can interact with Cerebras models by asking questions using the ask method.

# Troubleshooting
- Chrome WebDriver Error: Ensure that you have the correct version of Chrome WebDriver installed. You can download it from here.
- API Key Expiration: If your demo API key expires, the program will automatically refresh it, but ensure that your Chrome user data is up-to-date.

# Contributing
- Feel free to modify and adjust the content as necessary based on your specific project needs! Let me know if you'd like any changes or additions.

# License

[MIT](https://choosealicense.com/licenses/mit/)
# Hi, I'm Sujal Rajpoot! 👋
## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://sujalrajpoot.netlify.app/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sujal-rajpoot-469888305/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/sujalrajpoot70)


## 🚀 About Me
I'm a skilled Python programmer and experienced web developer. With a strong background in programming and a passion for creating interactive and engaging web experiences, I specialize in crafting dynamic websites and applications. I'm dedicated to transforming ideas into functional and user-friendly digital solutions. Explore my portfolio to see my work in action.
