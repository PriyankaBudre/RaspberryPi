import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
#from ecapture import ecapture as ec
#import wolframalpha
import json
import requests


engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

engine.setProperty('rate', 90) # Speed percent


def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning")
        print("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
        print("Good Afternoon")
    else:
        speak("Good Evening")
        print("Good Evening")
        
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone(device_index=4) as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

print("Loading your AI personal assistant")
speak("Hey Priyanka, I am your AI personal assistant. My name is Robo")
wishMe()

if __name__=='__main__':


    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        if statement==0:
            continue 
            
        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('your personal assistant is shutting down,Good bye')
            print('your personal assistant is shutting down,Good bye')
            break
        
        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)


