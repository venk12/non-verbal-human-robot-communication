import speech_recognition as sr
import time

# Initialize the recognizer
r = sr.Recognizer()

def listen_and_transcribe():
    pause_threshold = 1.0  # 1 second pause threshold
    pause_detected = False
    statement = ""

    with sr.Microphone() as source:
        print("Now Listening...")
        
        while True:
            try:
                audio = r.listen(source, timeout=None, phrase_time_limit=None)
                text = r.recognize_google(audio)
                print("You said:", text)

                # Append the recognized text to the statement
                statement += " " + text

                # Reset the pause timer
                pause_start_time = time.time()
                pause_detected = False

            except sr.UnknownValueError:
                # Speech was unintelligible
                pass
            except sr.RequestError as e:
                print(f"Error with the request: {e}")

            # Check for a pause
            if not pause_detected and time.time() - pause_start_time >= pause_threshold:
                print("Pause detected. End of statement.")
                break

    return statement.strip()