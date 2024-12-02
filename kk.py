# # # import subprocess
# # # # subprocess.run(['ls'], shell=True)  # Works on macOS or Linux
# # # import requests
# # # result = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=9a5628bf03af4ec3b092343e7ddfe8b9")
# # # # result = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=9a5628bf03af4ec3b092343e7ddfe8b9")
# # # print(result.json())  # Debug the response
# # import requests
# #
# # url = "https://api.currentsapi.services/v1/latest-news"
# # params = {
# #     'apiKey': '3zH-be-E_I8RWepW93E0R6W9Vo5LoBwSFSP9WBzae75dR3Bs',
# #     'category': 'business',  # You can filter by category such as 'sports', 'technology', etc.
# #     'country': 'IN'  # Use country code 'IN' for India
# # }
# #
# # response = requests.get(url, params=params)
# # data = response.json()
# #
# # if 'news' in data:
# #     for article in data['news']:
# #         print(article['title']
# #         )
# import requests
#
# def get_global_figure_info(query):
#     # Dictionary of notable figures and their roles
#     figures = {
#         "Narendra Modi": "Prime Minister of India.",
#         "Rishi Sunak": "Prime Minister of the United Kingdom.",
#         "Joe Biden": "President of the United States.",
#         "Elon Musk": "CEO of Tesla, SpaceX, and Twitter.",
#         "Kamala Harris": "Vice President of the United States.",
#         "Xi Jinping": "President of China.",
#         "Vladimir Putin": "President of Russia.",
#         "Greta Thunberg": "Climate Activist.",
#         "Malala Yousafzai": "Nobel Peace Prize Laureate.",
#         "Lionel Messi": "Professional Footballer.",
#     }
#
#     if query:
#         # Preprocess the query
#         query = query.lower()
#         query_words = set(query.split())
#
#         best_match = None
#         max_role_match_count = 0
#         max_name_match_count = 0
#
#         for name, role in figures.items():
#             name_words = set(name.lower().split())
#             role_words = set(role.lower().split())
#
#             # Count how many query words match the role
#             role_match_count = len(query_words.intersection(role_words))
#             # Count how many query words match the name
#             name_match_count = len(query_words.intersection(name_words))
#
#             # Prioritize role matches over name matches for better relevance
#             if role_match_count > max_role_match_count or (
#                 role_match_count == max_role_match_count and name_match_count > max_name_match_count
#             ):
#                 best_match = f"{name}: {role}"
#                 max_role_match_count = role_match_count
#                 max_name_match_count = name_match_count
#
#         # If a match is found, fetch additional info from Wikipedia
#         if best_match:
#             name = best_match.split(":")[0]
#             try:
#                 # Fetch Wikipedia info
#                 url = "https://en.wikipedia.org/w/api.php"
#                 params = {
#                     "action": "query",
#                     "format": "json",
#                     "prop": "extracts",
#                     "exintro": True,
#                     "explaintext": True,
#                     "titles": name
#                 }
#                 response = requests.get(url, params=params)
#                 if response.status_code == 200:
#                     data = response.json()
#                     page = next(iter(data["query"]["pages"].values()))
#                     extract = page.get("extract", "Wikipedia information not found.")
#                     truncated_extract = "\n".join(extract.splitlines()[:2])  # Truncate to first 2 lines
#                     return f"{best_match}\n\nAdditional Info from Wikipedia:\n{truncated_extract}"
#                 else:
#                     return f"{best_match}\n\nError fetching Wikipedia data. Status Code: {response.status_code}"
#             except Exception as e:
#                 return f"{best_match}\n\nError fetching Wikipedia data: {str(e)}"
#
#         # If no match is found
#         return "Sorry, I couldn't find relevant information for your query."
#
# # Example usage
# query = "Who is the Prime Minister of the UK?"
# print(get_global_figure_info(query))
#
# query = "Who is the Prime Minister of India?"
# print(get_global_figure_info(query))
# import openai

from gtts import gTTS
import speech_recognition as sr

def test_microphone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source)
        print("Say something:")
        audio = r.listen(source)
        print("Recognizing...")
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
        except Exception as e:
            print(f"Error: {e}")

test_microphone()