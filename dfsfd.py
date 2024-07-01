import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print('D')
    audio = r.listen(source)

    print('Done recording')
