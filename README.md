# Video to Tag Converter

This web application converts spoken content from videos into text and generates relevant tags using OpenAI's GPT-3 API.

## Getting Started

Follow these steps to set up and run the project locally:

### Prerequisites

- Python 3
- [Virtualenv](https://pypi.org/project/virtualenv/)

### Installation

1. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    - For Windows:

        ```bash
        venv\Scripts\activate
        ```

    - For macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Run the Application

```bash
python app.py
```

Visit http://localhost:5000/index in your browser to access the application.


# Set OpenAI GPT-3 API Key
Make sure to set your OpenAI GPT-3 API key in the app.py file:
# Set your OpenAI GPT-3 API key
openai.api_key = 'your OpenAI GPT-3 API key'


# Usage
1. Access the web application at http://localhost:5000/index.
2. Upload a video file for conversion.
3. Receive the converted text and generated tags.


# Acknowledgments
This project utilizes Flask, MoviePy, SpeechRecognition, and OpenAI's GPT-3 API.
