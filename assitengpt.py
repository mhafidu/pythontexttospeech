import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import requests
import json
from takeData import takeData

data = None
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

def get_name():
    speak("What's your name?")
    name = takeCommand()
    speak(f"Hello, {name}. How can I help you?")

def get_time():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")

def search_youtube(query):
    speak("Searching YouTube...")
    query = query.replace("search youtube for", "")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def search_google(query):
    speak("Searching Google...")
    query = query.replace("search google for", "")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_stock_price(ticker):
    url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey=your_api_key"
    response = requests.get(url)
    data = json.loads(response.text)
    speak(f"The current stock price of {ticker} is {data[0]['price']:.2f} USD")
def speakData(data) :
    speak(data)
    


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

if __name__ == "__main__":
    greet()
    get_name()

    while True:
        query = takeCommand().lower()
        data = takeData(query)
        print(data[1])
    
        if "what's the time" in query:
            get_time()  
        elif query in data[1].lower():
            speakData(data[2])
        elif "search youtube for" in query:
            search_youtube(query)
        elif "search google for" in query:
            search_google(query)
        elif "what's the stock price of" in query:
            ticker = query.split()[-1]
            get_stock_price(ticker)
        elif "exit" in query or "bye" in query:
            speak("Goodbye!")
            exit()
