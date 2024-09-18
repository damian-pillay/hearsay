import azure.cognitiveservices.speech as speechsdk
from recorder import Recorder
from dotenv import load_dotenv
import os

load_dotenv()

class AzureSpeechClient:
    def __init__(self) -> None:
        self.key = os.environ["AZURE_SPEECH_KEY"]
        self.region =os.environ["AZURE_SPEECH_REGION"]
        
        self.speech_config = speechsdk.SpeechConfig(
            subscription= self.key,
            region=self.region,
            speech_recognition_language="en-US"
        )

        self.audio_mic_config = speechsdk.audio.AudioConfig(
            use_default_microphone=True
        )

        self.user_dialogue = ""
        self.pronunciation_result = {}
        self.recorder = Recorder()
        self.input = self.recorder.output_file
        self.output = "./sound/tutor_response.wav"

    def transcription(self):
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_mic_config)

        print("Speak into your microphone.")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            self.user_dialogue = speech_recognition_result.text
            print(self.user_dialogue)
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    # def analyse(self):
    #     self.recorder.start()
    #     self.transcription()
    #     self.recorder.stop()
    #     self.pronunciation_assessment(self.user_dialogue)


    def pronunciation_assessment(self, reference):
        """Performs one-shot pronunciation assessment asynchronously with input from wav file"""
        
        print("\n-------------- PRONUNCIATION ASSESSMENT ---------------\n")
        # Creates an instance  of a speech config with specified subscription key and service region.
        # Replace with your own subscription key and service region (e.g., "westus").
        config = self.speech_config

        # The pronunciation assessment service has a longer default end silence timeout (5 seconds) than normal STT
        config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "3000")
        audio_config = speechsdk.audio.AudioConfig(filename=self.input)

        reference_text = ""
        pronunciation_config = speechsdk.PronunciationAssessmentConfig(
            reference_text=reference_text,
            grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
            granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
            enable_miscue=True)
        pronunciation_config.enable_prosody_assessment()

        # Create a speech recognizer, also specify the speech language
        recognizer = speechsdk.SpeechRecognizer(speech_config=config, language="en-US", audio_config=audio_config)

        reference_text = reference
        pronunciation_config.reference_text = reference_text
        pronunciation_config.apply_to(recognizer)

        result = recognizer.recognize_once_async().get()

        # Check the result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print('Recognized: {}'.format(result.text))
            print('  Pronunciation Assessment Result:')

            pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
            pronunciation = {}

            print('    Accuracy score: {}, Prosody score: {}, Pronunciation score: {}, Completeness score : {}, FluencyScore: {}'.format(
                pronunciation_result.accuracy_score, pronunciation_result.prosody_score, pronunciation_result.pronunciation_score,
                pronunciation_result.completeness_score, pronunciation_result.fluency_score
            ))
            print('  Word-level details:')
            for idx, word in enumerate(pronunciation_result.words):
                print('    {}: word: {}, accuracy score: {}, error type: {};'.format(
                    idx + 1, word.word, word.accuracy_score, word.error_type
                ))
                pronunciation[word.word] = word.accuracy_score
                if pronunciation[word.word] >= 90:
                    pronunciation[word.word] = 100

            self.pronunciation_result = {
                "response": reference,
                "accuracy": pronunciation_result.accuracy_score,
                "pronunciation": pronunciation,
            }

        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))

    def speak(self, text):
  
        tts_speech_config = speechsdk.SpeechConfig(
            subscription=self.key,
            region=self.region,
            )
        
        tts_audio_config = speechsdk.audio.AudioOutputConfig(filename=self.output)

        # The neural multilingual voice can speak different languages based on the input text.
        tts_speech_config.speech_synthesis_voice_name="en-US-SaraNeural"

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=tts_speech_config, audio_config=tts_audio_config)

        # Get text from the console and synthesize to the default speaker.
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("\nSpeech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
