import speech_recognition as sr

def voice_to_text(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    return r.recognize_google(audio)




# PS D:\Coding> cd D:\Coding
# PS D:\Coding> python -m Chatbot.app