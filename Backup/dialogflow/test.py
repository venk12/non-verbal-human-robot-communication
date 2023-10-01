# import detect_intent as detect
# import speech_recog as listen

# print("Program works!..")
# content=listen.main()
# print(content)
# detect.detect_intent_texts(content)

import time
import detect_intent as detect
import speech_recog as listen
# from speech_to_text import listen_and_transcribe
import re


while True:
    content = listen.main()
    print(content)
    print("Now sending the transcribed text to dialogflow...")
    # detected_intent = detect.detect_intent_texts(content)
    # print(detected_intent)
    # for c in content:
    #     if re.search(r"\b(exit|quit)\b", c, re.I):
    #         print("Exiting the program..")
    #         break
