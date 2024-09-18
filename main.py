import streamlit.components.v1 as components
from azuremanager import AzureSpeechClient
from pprint import pprint
from tutor import Tutor
import streamlit as st
import base64
import os

# Convert button sound effect to base64 for html embedding
with open("./sound/button.wav", "rb") as audio_file:
    BUTTON = base64.b64encode(audio_file.read()).decode("ascii")

def cleanup_wav_files():
    '''Deletes wav files associated with current session state'''
    for wav_file in st.session_state.get('wav_files', []):
        if os.path.exists(wav_file):
            os.remove(wav_file)
            print(f"Deleted {wav_file}")

def main():
# -------------------- Initialize Back End --------------------- #

    client = AzureSpeechClient()
    tutor = Tutor()
    
# -------------------- Initialize Front End -------------------- #
    
    # Display "HearSay" title on webpage
    st.markdown("""<h1 style='text-align: center; color: white; font-size: 6rem; white-space: nowrap; '>Hear<span style='color: #4CAF50;'>Say</span></h1>""", unsafe_allow_html=True)

    # Display info about application below title
    st.markdown("<h2 style='text-align: center; color: white; font-size: 1.4rem;  '>Your Personal AI Assistant for Real-Time Speech Feedback</h2>", unsafe_allow_html=True)

    # Style Streamlit Button
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50; /* Custom background color */
        color: white; /* Custom text color */
        padding: 10px 20px; /* Custom padding */
        font-size: 1rem; /* Custom font size */
        border: none; /* Remove border */
        border-radius: 4px; /* Rounded corners */
        cursor: pointer; /* Pointer cursor on hover */
        display: block;
        margin: 0 auto; /* Center horizontally */
    }
    .stButton>button:hover {
        background-color: #45a049; /* Custom hover background color */
    }
    .stButton>button:active {
        background-color: grey; /* Turn grey when clicked */
        color: white; /* Custom text color */
    }
    </style>
    """, unsafe_allow_html=True)

    # Remove anchor tags from markdown elements
    st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

    # Initialize wav file for specific user instance
    if 'wav_files' not in st.session_state:
        
        # session_id = str(time.time())  # Unique session ID based on timestamp (Used for keeping track of unique instances)
        session_id = 1                   # Made session ID default to 1 since previous approach was not working

        st.session_state['wav_files'] = [
            f"./sound/user_response_{session_id}.wav",
            f"./sound/tutor_response_{session_id}.wav"
        ]

    # Initialize button and display it below title and info
    speak = st.button("Say Something", type="primary")

    # Do this when "speak" button is pressed
    if speak:
        
        print("\n# ------------------- NEW REQUEST ------------------- #\n")
        
        
        #Play base64 button sound effect       
        functionality = f"""<audio id="audio" src="data:audio/mp3;base64,{BUTTON}" autoplay></audio>"""
        components.html(functionality, height=0)  

        # ---------------------------------------------- NOTE -------------------------------------------------- #
        # I debugged many times but could not get the sound to play as intended
        # Right now it only plays on the first instance of the button press
        # i have used the exact same functionality in other projects, but for some reason, it does not work here.
        # i suspect it might be something to do with the way recorder class handles its threading
        # I decided not to change the recorder class, since that functionality is more important than this button

        client.recorder.output_file = st.session_state['wav_files'][0]
        # Start recording
        client.recorder.start()

        # Transcribe mic input, simultaneously whilst recording
        client.transcription()

        # Display user message in chat message container
        with st.chat_message(name="user", avatar="./avatars/student.png"):
            st.markdown(client.user_dialogue)

        # Stop recording
        client.recorder.stop()

        # Do pronounciation assessment on recorded data with transcribed data as reference text input
        client.output = st.session_state['wav_files'][1]
        client.input = st.session_state['wav_files'][0]
        client.pronunciation_assessment(reference=client.user_dialogue)

        # Show new results to console
        # The previous function displays the assessment as it happens, the new results is formatted differently
        print("\n---------------- AI ASSESSMENT AND TTS ----------------\n")
        pprint(client.pronunciation_result)

        # Use the pronunciation results as prompt for the ai tutor
        prompt = client.pronunciation_result
        response = tutor.get_response(f"{prompt}")

        # Convert tutor response from text to speech
        client.speak(response)

        with st.chat_message(name="assistant", avatar="./avatars/tutor.png"):
            st.markdown(response)

        # Play the audio using st.audio
        tutor_tts = st.session_state['wav_files'][1]
        with open(tutor_tts, "rb") as audio_file:
            st.audio(audio_file.read(), format='audio/wav')

        # atexit.register(cleanup_wav_files) # triggers wav clean up

if __name__ == "__main__":
    main()