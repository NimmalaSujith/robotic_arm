import speech_recognition as sr
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print('Clearing background noise...Please wait')
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("waiting for your message...")
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio)
    print('Done recording')