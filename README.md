# Voice Assistant Using GEMINI Pro LLM

## Overview

This project showcases a voice assistant powered by the GEMINI Pro LLM, Azure Cognitive Services, and Porcupine wake word detection. The assistant listens for a specific wake word ("Jarvis") and responds to user queries with accurate and contextually appropriate answers. This system is designed for deployment on a rover bot used to scout around industrial areas and perform tasks with precision.

## Features

- **Wake Word Detection**: Utilizes Porcupine for detecting the wake word "Jarvis".
- **Speech Recognition**: Converts spoken language into text using Azure Cognitive Services.
- **Text Generation**: Generates responses using Google's GEMINI Pro LLM.
- **Speech Synthesis**: Converts text responses back to speech using Azure Cognitive Services.
- **Safety Filters**: Includes safety settings to block harmful content categories.

## Setup

### Prerequisites

- Python 3.7 or higher
- [Porcupine](https://picovoice.ai/platform/porcupine/) access key
- Azure Cognitive Services subscription key
- Google GEMINI Pro API key

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Adarshgurazada/Voice-Assistant-Using-GEMINI.git
    cd Voice-Assistant-Using-GEMINI
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your API keys:

    ```env
    PORCUPINE=your_porcupine_key
    AZURE=your_azure_key
    GOOGLE_API=your_google_api_key
    ```

## Usage

1. Run the main script:

    ```bash
    python main.py
    ```

2. The assistant will listen for the wake word "Jarvis". Once detected, it will prompt you to ask a question.

3. Speak your query, and the assistant will process it, generate a response, and speak it back to you.

## Code Explanation

### Importing Libraries

- **pyaudio**: For audio input and output.
- **pvporcupine**: For wake word detection.
- **azure.cognitiveservices.speech**: For speech recognition and synthesis.
- **google.generativeai**: For text generation using GEMINI Pro LLM.
- **dotenv**: For loading environment variables.

### Initializing Services

- **Porcupine**: Configured to detect the wake word "Jarvis".
- **Azure Cognitive Services**: Configured for both speech recognition and synthesis.
- **GEMINI Pro LLM**: Configured with generation and safety settings.

### Main Loop

- Continuously listens for the wake word using Porcupine.
- Upon detecting the wake word, prompts the user for a query.
- Converts the user's spoken query to text.
- Sends the text to GEMINI Pro for a response.
- Converts the generated response back to speech and plays it.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.


## Contact

For any inquiries or feedback, please reach out to [adarsh.gurazada@gmail.com].
