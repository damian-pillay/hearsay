# HearSay

HearSay is your personal AI assistant for real-time speech feedback. The app leverages advanced speech recognition and synthesis technologies to provide immediate feedback on your spoken English, helping you improve your pronunciation and grammar in an interactive and engaging manner.

## Features

- **Real-Time Speech Feedback**: Provides near-instant feedback on grammar and pronunciation (4 - 8 seconds). The performance is highly optimized to ensure a smooth experience, with speed primarily limited by Azure's speech services.
- **Personalized Learning**: Tailored responses and suggestions based on individual speech patterns.
- **Interactive Interface**: User-friendly interface built with Streamlit for seamless interaction.
- **Speech-to-Text Conversion**: Accurate transcription of spoken language (Up to 30 seconds) using Azure Speech SDK.
- **Text-to-Speech Synthesis**: Converts AI-generated responses into natural-sounding speech.
- **Grammar & Pronunciation Assessment**: Detailed evaluation of grammar and pronunciation accuracy with actionable feedback.
- **Audio Playback**: Allows users to listen to the AI’s responses, for better clarity on pronunciation

## Tech Stack

- **Streamlit**: A powerful framework for building interactive web applications with Python. Used for creating the user interface and managing real-time interactions.
- **Azure Speech SDK**: Provides robust speech recognition and synthesis capabilities. Utilized for converting speech to text and generating spoken responses.
- **OpenAI GPT-4**: Employed for generating conversational responses and providing personalized feedback based on user input.
- **Python**: The primary programming language used for application development, leveraging libraries such as PyAudio for audio recording and processing.
- **dotenv**: Manages environment variables and API keys securely.
- **PyAudio**: Facilitates audio recording functionality, capturing user input for analysis.
- **Wave**: Handles the saving and processing of audio files in WAV format.

## Usage

To run the application, follow these steps:

1. **Clone the Repository**
   First, clone the project repository to your local machine:
   
   ```bash
   git clone https://github.com/damian-pillay/hearsay
   ```

2. **Open the Project**
   Open the project in a Python IDE, preferably Visual Studio Code (VSCode)

3. **Install Requirements**
   Ensure all the required libraries are installed by running:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application** 
    Once the dependencies are installed, start the app with the following command:

    ```bash
    python -m streamlit run main.py
    ```

    The application will open in your browser, running locally

5. **Use the Application**
   Click the "Say Something" button to start speaking. Once you stop or after 30 seconds, the app will automatically process your speech and provide detailed feedback on your pronunciation and grammar.

## Overall Approach

Developing **HearSay** involved a comprehensive approach to creating a seamless and effective speech feedback system. The core of the application revolves around integrating multiple technologies to provide real-time analysis and feedback. The Streamlit framework was chosen for its ease of use and ability to create interactive web applications quickly. Azure Cognitive Services was selected for its advanced speech recognition and synthesis capabilities, which are crucial for accurate speech-to-text transcription and pronunciation assessment. OpenAI’s GPT-4 model was used to generate intelligent and contextually relevant feedback based on user input.

The application was designed to be user-friendly and responsive, providing almost immediate feedback to enhance the learning experience. By combining these technologies, **HearSay** offers a robust tool for improving English language skills through interactive and personalized feedback.

## Step-By-Step Process Overview

**1. Initialization**
- **Streamlit** initializes the web app interface with a title, description, and a “Say Something” button.
- **AzureSpeechClient** and **Tutor** classes are set up to handle speech recognition, pronunciation assessment, and AI responses.

**2. Button Click**
- When the “Say Something” button is pressed, Streamlit triggers the audio recording and transcription functions.
- A sound effect is played to indicate the start of the process.

**3. Simultaneous Recording and Transcription**
- **Recording**: The `Recorder` class starts recording audio via a separate thread.
- **Transcription**: Simultaneously, the `AzureSpeechClient` begins transcribing the recorded audio.
- **Stop Recording**: Recording is stopped once the transcription process is complete. The recorded audio chunks are then converted and saved into a wave audio file.

**4. Pronunciation Assessment**
- The transcription result is used as the reference text.
- The saved audio file path is used as input for the pronunciation assessment.
- The `AzureSpeechClient` analyzes the pronunciation and compares it to the reference text, generating feedback.

**5. AI Tutor Interaction**
- The pronunciation assessment results are passed to the `Tutor` class.
- The AI Tutor generates a response based on the feedback and assessment results.

**6. Text-to-Speech**
- The AI Tutor's response is converted to speech using Azure's Text-to-Speech API.
- The generated audio is saved into a wav file.

**7. Display Results**
- The user’s message and the AI Tutor’s response are displayed in the Streamlit app.
- The audio of the AI Tutor’s response is played using the Streamlit `st.audio` component.
- relevant data is printed into the IDE terminal to denote every step of the process.

## Challenges and Limitations

**1. Initial Implementation**: One struggle during development was the initial implementation phase. I first experimented with Google Cloud Platform (GCP) for its real-time speech-to-text capabilities, but it lacked pronunciation assessment features. I initially attempted to use confidence scores associated with each word, but these scores did not accurately reflect pronunciation quality. As a result, I abandoned this approach and switched to using Azure, which provided the necessary pronunciation assessment features.

**2. Audio Playback Issues**: One of the significant challenges faced was ensuring reliable audio playback in the Streamlit application when using HTML and JavaScript. While audio playback via widgets worked seamlessly, achieving consistent playback through custom HTML and JavaScript for sound effects—an approach that worked in previous projects—proved difficult. This issue may be related to threading or how the audio components interact within the Streamlit framework. After multiple attempts, the compromise was to allow audio playback only on the first button press to ensure stability.

**3. Pronunciation Assessment Accuracy**: While Azure’s pronunciation assessment service provides valuable insights, there were challenges in fine-tuning the feedback to be both accurate and user-friendly. Ensuring that the feedback was constructive and not overly critical was a key focus. To address this, I formatted the data into a JSON file containing only the relevant information and used this JSON as a prompt for ChatGPT-4 to generate the desired feedback.

**4. Chat-GPT Prompt Engineering**: Another challenge was ensuring that ChatGPT-4 adhered to my prompt engineering for phonetic guidance. The model was inconsistent in providing phonetic guidance and struggled to differentiate between ranges of pronunciation scores. Specifically, it did not always disregard scores above 90, as requested, and sometimes provided feedback for scores between 90 and 100. To address this, I adjusted the pronunciation assessment function to round scores 90 or more, to 100 for consistency and to simplify the feedback process.

**5. Integration Complexity**: Combining various technologies and ensuring they work seamlessly together posed integration challenges. Managing API interactions, audio processing, and real-time feedback required careful coordination and troubleshooting. Some Azure APIs lacked comprehensive documentation, which necessitated extensive consultation on Reddit, StackOverflow, and through AI assistance to achieve the desired functionality Audio processing, specifically converting audio to WAV format, proved more complex than anticipated. This process needed to occur simultaneously with transcription, adding a layer of difficulty to ensure accurate and timely pronunciation assessment.

**6. Performance Considerations**: Handling real-time audio processing and feedback can be resource-intensive. I had to ensure certain processes occurred in a specific order or simultaneously to optimize performance. The current system is well-optimized, providing a smooth user experience, though performance is ultimately constrained by the speed of Azure Speech Services and OpenAI's GPT-4.

**7. Unique Instances For Cloud Deployment**: One challenge encountered was optimizing the project for different session states. The goal was to create unique audio files for each instance of the application. However, the cleanup function for WAV files did not work as intended upon exiting the application. To address this, I decided to simplify the approach by allowing only one instance of the application to run at a time. This was achieved by using a consistent session ID for all instances, which avoided the need for file cleanup. The original code for handling unique session states is still present in the project but is not actively used in the current implementation.

**8. Cloud Deployment and Dockerization**: Dockerization of the application introduced additional challenges. Necessary libraries and newer versions of dependencies had to be included in the Docker image. Furthermore, Docker containers do not support direct access to user hardware, such as microphones. This limitation prevented the app from being deployed and hosted in a Docker container, necessitating a localhost-only deployment.

Despite these challenges, the project successfully delivers a functional and engaging tool for improving English language skills, showcasing the power of modern AI and cloud-based services.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
