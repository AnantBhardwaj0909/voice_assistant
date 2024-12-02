from decouple import config
from datetime import datetime
import pyttsx3
import  keyboard
from conv import random_text
from random import choice
import os
import requests
import imdb
import subprocess as sp
import speech_recognition as sr
from online import find_my_ip
import wolframalpha
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound
from online import get_live_matches,get_minister_info,search_on_google,search_on_wikipedia,youtube,send_email,get_news,weather_forcast
engine = pyttsx3.init()
engine.setProperty('volume', 2.0)
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[8].id)
USER=config('USER')
HOSTNAME=config('HOSTNAME')

def speak(text, speed_factor=1.5):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")

    audio = AudioSegment.from_file("response.mp3")
    faster_audio = audio.speedup(playback_speed=speed_factor)

    faster_audio.export("response_fast.mp3", format="mp3")
    playsound("response_fast.mp3")

speak("Hello! I am your assistant.", speed_factor=1.6)

def greet_me():
    hour = datetime.now().hour
    if hour>=6 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<=16:
        speak("Good Afternoon")
    elif hour>=16 and hour<=18:
        speak("Good Evening")
    speak(f"I am {HOSTNAME}. How may I help you? {USER}")
from pynput import keyboard

listening = True

def start_listening():
    global listening
    listening = True
    print("Start listening")

def pause_listening():
    global listening
    listening = False
    print("Pause listening")

def on_press(key):
    try:
        if key == keyboard.Key.cmd and key.char == 'p':
            pause_listening()
        elif key == keyboard.Key.cmd and key.char == 's':
            start_listening()
    except AttributeError:
        pass  # Handle special keys here if needed

# Start listening for key presses
listener = keyboard.Listener(on_press=on_press)
listener.start()
# keyboard.add_hotkey('command+p', pause_listening)
# keyboard.add_hotkey('command+s', start_listening)
# def take_command():
#     r=sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Adjusting for ambient noise, please wait...")
#         r.adjust_for_ambient_noise(source, duration=1)
#         print("Listening...")
#         r.pause_threshold = 1
#         audio = r.listen(source)
#     try:
#         print("Recognizing...")
#         queri = r.recognize_google(audio, language='en-in')
#         print(f"User said: {queri}\n")
#         if not 'stop' in queri or 'exit' in queri:
#              speak(choice(random_text))
#         else:
#             hour=datetime.now().hour
#             if hour>=21 and hour<6:
#                 speak("Good Night Sir,take care")
#             else:
#                 speak("Have a nice day")
#             exit()
#
#     except Exception:
#         # speak("sorry I couldn't recognize your command, please Repeat")
#         print("Say that again please...")
#         queri='None'
#     return queri
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio)
            if 'exit' in query.lower():
                hour = datetime.now().hour
                if hour >= 21 or hour < 6:
                    speak("Good night, take care.")
                else:
                    speak("Have a nice day!")
                exit()
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio. Returning None.")
            return 'None'
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return 'None'

if __name__ == '__main__':
    # speak("hi I am Jarvis")
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            print(f"User said (raw): {query}")
            if "hello" in query:
                speak("I am Great Sir,How may I help you?")
            elif "open terminal" in query:
                speak("Opening Terminal")
                sp.run(["open", "-a", "Terminal"])
            elif "open camera" in query:
                speak("Opening camera")
                sp.run(["open", "/System/Applications/Photo Booth.app"])

            elif "open notepad" in query:
                speak("Opening TextEdit for you")
                sp.run(["open", "-a", "TextEdit"])
            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(f"Your IP Address is {ip_address}.")
                print(f"Your IP Address is {ip_address}")

            elif "open youtube" in query:
                speak("What do you want to play on YouTube?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak("What do you want to search on Google?")
                search_query = take_command().lower()
                search_on_google(search_query)

            elif "wikipedia" in query:
                speak("What do you want to search on Wikipedia?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to Wikipedia: {results}")
                speak("I am printing it on the terminal for your reference.")
                print("\n")
                print(results)
            elif "send an email" in query:
                speak("On what email address do you want to send sir?. Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message ?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")
            elif "give me the news" in query:
                speak("I am reading out the latest headlines of today, sir.")
                url = "https://api.currentsapi.services/v1/latest-news"
                params = {
                    'apiKey': '3zH-be-E_I8RWepW93E0R6W9Vo5LoBwSFSP9WBzae75dR3Bs',
                    'category': 'business',  # You can filter by category such as 'sports', 'technology', etc.
                    'country': 'IN'  # Use country code 'IN' for India
                }

                response = requests.get(url, params=params)
                data = response.json()

                if 'news' in data:
                    for article in data['news'][:6]:
                        speak(article['title'])
                        print(article['title'])
                else:
                    speak("No news available")

            elif "tell me the weather" in query or "weather report" in query:
                speak("Tell me the name of your city")
                city = take_command()
                if city:
                    speak(f"Getting weather report for your city {city}")
                    weather, temp, feels_like = weather_forcast(city)  # You need to define this function
                    speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                    speak(f"Also, the weather report talks about {weather}")
                    speak("For your convenience, I am printing it on the screen, sir.")
                    print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")
                else:
                    speak("I couldn't hear the city name. Please try again.")

            elif "movie" in query:
                movies_db=imdb.IMDb()
                speak("Please tell me about movie name")
                text = take_command().lower()
                movie = movies_db.search_movie(text)
                speak("Searching for"+text)
                speak("I found the following movies:")
                for movie in movie:
                    title = movie['title']
                    year = movie['year']
                    speak(f"{title} {year}")

                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)

                    rating = movie_info.get('rating', 'Rating not available')

                    cast = movie_info.get('cast', [])
                    actor_names = [actor['name'] for actor in cast[:5]]

                    plot = movie_info.get('plot outline', movie_info.get('plot summary', 'Plot not available'))

                    speak(
                        f"{title} was released in {year} and has IMDb rating of {rating}. It has a cast of {', '.join(actor_names)}. "
                        f"The plot summary of the movie is {plot}")

                    # Print the details on the terminal
                    print(f"{title} was released in {year} and has IMDb rating of {rating}.")
                    print(f"It has a cast of {', '.join(actor_names)}.")
                    print(f"The plot summary of the movie is {plot}")


            elif "calculate" in query:
                app_id = "XHAW44-T6YV69UARW"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index('calculate')
                text = " ".join(query.split()[ind + 1:])
                result = client.query(text)
                try:
                    ans = next(result.results).text
                    speak(f"The answer is {ans}")
                    print(f"The answer is {ans}")
                except StopIteration:
                    speak("Sorry, I couldn't find that.")
                    print("Sorry, I couldn't find that.")

            elif "what is" in query or "who is" in query or "which is" in query:
                try:
                    minister_info = get_minister_info(query)

                    if minister_info and "Sorry, no relevant information found in our database." not in minister_info:
                        speak(minister_info)
                        print(minister_info)
                    else:
                        app_id = "XHAW44-T6YV69UARW"
                        client = wolframalpha.Client(app_id)


                        ind = query.lower().index('what is') if 'what is' in query.lower() else \
                            query.lower().index('who is') if 'who is' in query.lower() else \
                                query.lower().index('which is') if 'which is' in query.lower() else None

                        if ind is not None:
                            text = query.split()[ind + 2:]
                            res = client.query(" ".join(text))
                            try:
                                ans = next(res.results).text

                                if len(ans) > 200:
                                    ans = ans[:200] + "..."

                                speak(f"The answer is: {ans}")
                                print(f"The answer is: {ans}")
                            except StopIteration:
                                speak("Sorry, I couldn't find that from WolframAlpha.")
                                print("Sorry, I couldn't find that from WolframAlpha.")
                        else:
                            speak("Sorry, I couldn't understand your query. Please try again.")
                            print("Sorry, I couldn't understand your query.")
                except Exception as e:
                    speak(f"An error occurred: {str(e)}")
                    print(f"An error occurred: {str(e)}")

            elif "live cricket matches" in query:
                live_matches = get_live_matches()
                speak("Live Cricket Matches:")
                for match in live_matches:
                    speak(match)
                    print(match)

            elif "indian cricket team" in query:
                cricket_team = [
                    "Captain: Rohit Sharma",
                    "Vice-Captain: Hardik Pandya",
                    "Coach: Rahul Dravid",
                    "Key Players: Virat Kohli, Jasprit Bumrah, KL Rahul, Mohammed Shami, Ravindra Jadeja"
                ]
                speak("Indian Cricket Team Information:")
                for member in cricket_team:
                    speak(member)
                    print(member)

                else:
                    speak("Sorry, I couldn't understand your query.")
                    print("Sorry, I couldn't understand your query.")
            # news_headlines = get_news()
                # news_text = "\n".join(news_headlines)
                # speak(news_text)
                # speak("I am printing it on screen, sir.")
                # print(news_text)
                #
            # elif "subscribe" in query:
            #     speak("Let me guide you to subscribe to our channel.")
            #     guide_subscribe()