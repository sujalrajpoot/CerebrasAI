
# Cerebras Unofficial API

This repository provides an interface for interacting with the CerebrasAI API. It includes functionality for initializing the Cerebras environment, refreshing API keys, and generating AI responses using the Cerebras model.

# Table of Contents

- Features
- Installation
- Usage
- Project Structure
- Requirements
- Troubleshooting
- Contributing
- License

# Features
- API Key Management: Refreshes and updates the demo API key by fetching cookies and making an authenticated request to the Cerebras platform.
- Text Generation: Interact with Cerebras AI models to generate text completions, including streaming responses.
- Progress Tracking: Progress bars and terminal spinners for long-running operations.
- Error Handling: Built-in mechanisms to handle any type of error (e.g., connection issues, missing dependencies, invalid input) and provide meaningful error messages or fallback options.
# Installation

### Step 1: Clone the Repository
```
git clone https://github.com/sujalrajpoot/cerebras-unofficial-api.git
cd cerebras-unofficial-api
```

### Step 2: Install the required dependencies
- Ensure you have Python installed. Then, install the required Python packages:
```
pip install -r requirements.txt
```

# Usage
- You can initialize the CerebrasUnofficial class with cookies.

```python
from cerebras_unofficial import Cerebras_Unofficial

if __name__ == "__main__":
   AI = Cerebras_Unofficial('your_cookies')
   print(AI.chat("Hi"))
```


# Project Files Structure
- `cerebras_unofficial.py`: The main code file containing the `Cerebras_Unofficial` class with all functionalities.
- `requirements.txt`: Lists all the dependencies required for the project.
- `Test.py`: A script to demonstrate the usage of the `Cerebras_Unofficial` class.
- `ReadMe.md`: Documentation file providing an overview of the project, installation instructions, and usage examples.

# Requirements

- Python 3.8+
- Requests
- Fake UserAgent

# Troubleshooting
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
I'm a skilled full stack Python developer with expertise in object-oriented programming and website reverse engineering. With a strong background in programming and a passion for creating interactive and engaging web experiences, I specialize in crafting dynamic websites and applications. I'm dedicated to transforming ideas into functional and user-friendly digital solutions. Explore my portfolio to see my work in action.