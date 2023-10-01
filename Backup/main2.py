import re
import sys
import queue
import pyaudio
from google.cloud import speech
from google.oauth2 import service_account
import dialogflow_v2 as dialogflow

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Create a function for speech recognition
def speech_recognition():
    def create_speech_recognizer(service_account_json_path):
        # Load service account credentials for Google Cloud Speech-to-Text
        credentials = service_account.Credentials.from_service_account_file(
            service_account_json_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        # Create a SpeechClient with the credentials
        client = speech.SpeechClient(credentials=credentials)

        return client

    class MicrophoneStream:
        """Opens a recording stream as a generator yielding the audio chunks."""

        def __init__(self: object, rate: int = RATE, chunk: int = CHUNK) -> None:
            """The audio -- and generator -- is guaranteed to be on the main thread."""
            self._rate = rate
            self._chunk = chunk

            # Create a thread-safe buffer of audio data
            self._buff = queue.Queue()
            self.closed = True

        def __enter__(self: object) -> object:
            self._audio_interface = pyaudio.PyAudio()
            self._audio_stream = self._audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self._rate,
                input=True,
                frames_per_buffer=self._chunk,
                stream_callback=self._fill_buffer,
            )

            self.closed = False

            return self

        def __exit__(
            self: object,
            type: object,
            value: object,
            traceback: object,
        ) -> None:
            """Closes the stream, regardless of whether the connection was lost or not."""
            self._audio_stream.stop_stream()
            self._audio_stream.close()
            self.closed = True
            self._buff.put(None)
            self._audio_interface.terminate()

        def _fill_buffer(
            self: object,
            in_data: object,
            frame_count: int,
            time_info: object,
            status_flags: object,
        ) -> object:
            """Continuously collect data from the audio stream into the buffer."""
            self._buff.put(in_data)
            return None, pyaudio.paContinue

        def generator(self: object) -> object:
            """Generates audio chunks from the stream of audio data in chunks."""
            while not self.closed:
                chunk = self._buff.get()
                if chunk is None:
                    return
                data = [chunk]

                while True:
                    try:
                        chunk = self._buff.get(block=False)
                        if chunk is None:
                            return
                        data.append(chunk)
                    except queue.Empty:
                        break

                yield b"".join(data)

    def listen_print_loop(responses: object) -> str:
        """Iterates through server responses and prints them."""
        num_chars_printed = 0
        transcript = []

        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            new_transcript = result.alternatives[0].transcript

            overwrite_chars = " " * (num_chars_printed - len(new_transcript))

            if not result.is_final:
                sys.stdout.write(new_transcript + overwrite_chars + "\r")
                sys.stdout.flush()
                num_chars_printed = len(new_transcript)
            else:
                print(new_transcript + overwrite_chars)
                num_chars_printed = 0

                transcript.append(new_transcript)

        return transcript

    def main():
        """Transcribe speech from audio stream."""
        language_code = "en-US"

        client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code,
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=config, interim_results=True
        )

        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_generator
            )

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            transcript = listen_print_loop(responses)
            return transcript

    if __name__ == "__main__":
        return main()

# Create a function for interacting with Dialogflow
def detect_intent(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.intent.display_name


if __name__ == "__main__":
    # Replace with your Google Cloud service account JSON key file path
    service_account_json_path = "dialogflow/google_service_key.json"

    # Replace with your Dialogflow project ID
    dialogflow_project_id = "probable-summer-395414"

    # Replace with a unique session ID for each interaction
    session_id = '11111'

    # Start speech recognition
    transcript = speech_recognition()

    # Check for the "over" stop word in the transcript
    if "over" in transcript:
        # Send the transcribed text to Dialogflow for intent detection
        intent = detect_intent(
            dialogflow_project_id, session_id, transcript[0], "en-US"
        )

        # Print the detected intent
        print("Detected Intent:", intent)