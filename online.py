from idlelib import query
import  requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
from google.oauth2.credentials import Credentials
import wolframalpha
# Initialize the Llama model for other queries (e.g., minister info)
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
def get_live_matches():

    hardcoded_matches = [
        "India vs Australia, 2nd ODI at Wankhede Stadium.",
        "England vs South Africa, T20I series final."
    ]
    try:
        url = "https://cricapi.com/api/matches"
        params = {
            "apikey": "ff54a75a-ddac-47e4-891c-d8c9cf407047"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            matches = data.get("matches", [])
            live_matches = [
                f"{match['team-1']} vs {match['team-2']} on {match['date']}"
                for match in matches if match.get("matchStarted")
            ]
            return live_matches if live_matches else hardcoded_matches
        else:
            return hardcoded_matches
    except Exception:
        return hardcoded_matches

def get_minister_info(query):
    qa_database = [
        {"keywords": ["education minister", "minister of education"],
         "answer": "Dharmendra Pradhan: Minister of Education."},
        {"keywords": ["prime minister of india"], "answer": "Narendra Modi: Prime Minister of India."},
        {"keywords": ["home minister", "minister of home affairs"], "answer": "Amit Shah: Minister of Home Affairs."},
        {"keywords": ["finance minister", "minister of finance"], "answer": "Nirmala Sitharaman: Minister of Finance."},
        {"keywords": ["defence minister", "minister of defence"], "answer": "Rajnath Singh: Minister of Defence."},
        {"keywords": ["commerce minister", "minister of commerce and industry"],
         "answer": "Piyush Goyal: Minister of Commerce and Industry."},
        {"keywords": ["railway minister", "minister of railways"], "answer": "Ashwini Vaishnaw: Minister of Railways."},
        {"keywords": ["women and child development minister"],
         "answer": "Smriti Irani: Minister of Women and Child Development."},
        {"keywords": ["petroleum minister", "minister of petroleum and natural gas"],
         "answer": "Hardeep Singh Puri: Minister of Petroleum and Natural Gas."},
        {"keywords": ["health minister", "minister of health and family welfare"],
         "answer": "Mansukh Mandaviya: Minister of Health and Family Welfare."},
        {"keywords": ["president of the united states"], "answer": "Joe Biden: President of the United States."},
        {"keywords": ["vice president of the united states"],
         "answer": "Kamala Harris: Vice President of the United States."},
        {"keywords": ["president of china"], "answer": "Xi Jinping: President of China."},
        {"keywords": ["president of russia"], "answer": "Vladimir Putin: President of Russia."},
        {"keywords": ["prime minister of uk", "prime minister of the united kingdom"],
         "answer": "Rishi Sunak: Prime Minister of the United Kingdom."},
        {"keywords": ["president of france"], "answer": "Emmanuel Macron: President of France."},
        {"keywords": ["chancellor of germany"], "answer": "Olaf Scholz: Chancellor of Germany."},
        {"keywords": ["prime minister of japan"], "answer": "Fumio Kishida: Prime Minister of Japan."},
        {"keywords": ["prime minister of australia"], "answer": "Anthony Albanese: Prime Minister of Australia."},
        {"keywords": ["prime minister of canada"], "answer": "Justin Trudeau: Prime Minister of Canada."},
        {"keywords": ["president of ukraine"], "answer": "Volodymyr Zelenskyy: President of Ukraine."},
        {"keywords": ["prime minister of israel"], "answer": "Benjamin Netanyahu: Prime Minister of Israel."},
        {"keywords": ["crown prince of saudi arabia"], "answer": "Mohammed bin Salman: Crown Prince of Saudi Arabia."},
        {"keywords": ["president of turkey"], "answer": "Recep Tayyip Erdoğan: President of Turkey."},
        {"keywords": ["prime minister of thailand"], "answer": "Narongsak Osottanakorn: Prime Minister of Thailand."},
        {"keywords": ["former prime minister of new zealand"],
         "answer": "Jacinda Ardern: Former Prime Minister of New Zealand."},
        {"keywords": ["ceo of meta"], "answer": "Mark Zuckerberg: CEO of Meta."},
        {"keywords": ["ceo of tesla", "ceo of spacex", "ceo of twitter"],
         "answer": "Elon Musk: CEO of Tesla, SpaceX, and Twitter."},
        {"keywords": ["ceo of alphabet", "ceo of google"], "answer": "Sundar Pichai: CEO of Alphabet Inc."},
        {"keywords": ["ceo of microsoft"], "answer": "Satya Nadella: CEO of Microsoft."},
        {"keywords": ["ceo of apple"], "answer": "Tim Cook: CEO of Apple."},
        {"keywords": ["chairman of reliance industries"], "answer": "Mukesh Ambani: Chairman of Reliance Industries."},
        {"keywords": ["chairman of adani group"], "answer": "Gautam Adani: Chairman of Adani Group."},
        {"keywords": ["governor of rbi", "reserve bank governor"],
         "answer": "Shaktikanta Das: Governor of the Reserve Bank of India."},
        {"keywords": ["managing director of imf"], "answer": "Kristalina Georgieva: Managing Director of the IMF."},
        {"keywords": ["president of the european commission"],
         "answer": "Ursula von der Leyen: President of the European Commission."},
        {"keywords": ["director general of who"], "answer": "Tedros Adhanom Ghebreyesus: Director-General of the WHO."},
        {"keywords": ["president of the world bank"], "answer": "David Malpass: President of the World Bank."},
        {"keywords": ["un secretary-general"], "answer": "Antonio Guterres: UN Secretary-General."},
        {"keywords": ["president of the european central bank"],
         "answer": "Christine Lagarde: President of the European Central Bank."},
        {"keywords": ["governor of bank of england"], "answer": "Andrew Bailey: Governor of the Bank of England."},
        {"keywords": ["chairman of us federal reserve"], "answer": "Jay Powell: Chairman of the US Federal Reserve."},
        {"keywords": ["co-founder of google"], "answer": "Larry Page and Sergey Brin: Co-founders of Google."},
        {"keywords": ["founder of amazon"], "answer": "Jeff Bezos: Founder of Amazon."},
        {"keywords": ["ceo of berkshire hathaway"], "answer": "Warren Buffett: CEO of Berkshire Hathaway."},
        {"keywords": ["chairman of lvmh"], "answer": "Bernard Arnault: Chairman of LVMH."},
        {"keywords": ["media executive", "philanthropist"],
         "answer": "Oprah Winfrey: Media Executive and Philanthropist."},
        {"keywords": ["nobel peace prize laureate"], "answer": "Malala Yousafzai: Nobel Peace Prize Laureate."},
        {"keywords": ["climate activist"], "answer": "Greta Thunberg: Climate Activist."},
        {"keywords": ["leader of catholic church"], "answer": "Pope Francis: Leader of the Catholic Church."},
        {"keywords": ["spiritual leader of tibetan buddhism"],
         "answer": "Dalai Lama: Spiritual Leader of Tibetan Buddhism."},
        {"keywords": ["former president of usa"], "answer": "Barack Obama: Former President of the United States."},
        {"keywords": ["former us secretary of state"], "answer": "Hillary Clinton: Former US Secretary of State."},
        {"keywords": ["former chancellor of germany"], "answer": "Angela Merkel: Former Chancellor of Germany."},
        {"keywords": ["co-founder of microsoft"], "answer": "Bill Gates: Co-founder of Microsoft."},
        {"keywords": ["indian cricketer"], "answer": "Virat Kohli: Indian Cricketer."},
        {"keywords": ["former indian cricketer"], "answer": "Sachin Tendulkar: Former Indian Cricketer."},
        {"keywords": ["olympic athlete", "usain bolt"], "answer": "Usain Bolt: Olympic Athlete."},
        {"keywords": ["professional tennis player", "novak djokovic"],
         "answer": "Novak Djokovic: Professional Tennis Player."},
        {"keywords": ["professional tennis player", "rafael nadal"],
         "answer": "Rafael Nadal: Professional Tennis Player."},
        {"keywords": ["singer", "songwriter", "taylor swift"], "answer": "Taylor Swift: Singer and Songwriter."},
        {"keywords": ["singer", "performer", "beyoncé"], "answer": "Beyoncé: Singer and Performer."},
        {"keywords": ["space entrepreneur", "elon musk"], "answer": "Elon Musk: Space Entrepreneur."},
        {"keywords": ["founder of alibaba", "jack ma"], "answer": "Jack Ma: Founder of Alibaba."},
        {"keywords": ["first lady of china", "peng liyuan"], "answer": "Peng Liyuan: First Lady of China."},
        {"keywords": ["president of south africa", "cyril ramaphosa"],
         "answer": "Cyril Ramaphosa: President of South Africa."},
        {"keywords": ["prime minister of spain", "pedro sánchez"], "answer": "Pedro Sánchez: Prime Minister of Spain."},
        {"keywords": ["president of mexico", "andrés manuel lópez obrador"],
         "answer": "Andrés Manuel López Obrador: President of Mexico."},
        {"keywords": ["prime minister of ethiopia", "abiy ahmed"], "answer": "Abiy Ahmed: Prime Minister of Ethiopia."},
        {"keywords": ["president of syria", "bashar al-assad"], "answer": "Bashar al-Assad: President of Syria."},
        {"keywords": ["president of iran", "ebrahim raisi"], "answer": "Ebrahim Raisi: President of Iran."},
        {"keywords": ["prime minister of bangladesh", "sheikh hasina"],
         "answer": "Sheikh Hasina: Prime Minister of Bangladesh."},
        {"keywords": ["former prime minister of sri lanka", "mahinda rajapaksa"],
         "answer": "Mahinda Rajapaksa: Former Prime Minister of Sri Lanka."},
        {"keywords": ["economist", "writer", "jacques attali"], "answer": "Jacques Attali: Economist and Writer."},
        {"keywords": ["linguist", "philosopher", "noam chomsky"], "answer": "Noam Chomsky: Linguist and Philosopher."},
        {"keywords": ["historian", "author", "yuval noah harari"],
         "answer": "Yuval Noah Harari: Historian and Author."},
        {"keywords": ["author", "activist", "arundhati roy"], "answer": "Arundhati Roy: Author and Activist."},
        {"keywords": ["author", "salman rushdie"], "answer": "Salman Rushdie: Author."},
        {"keywords": ["indian industrialist", "ratan tata"], "answer": "Ratan Tata: Indian Industrialist."},
        {"keywords": ["founder of infosys", "narayana murthy"], "answer": "Narayana Murthy: Founder of Infosys."},
        {"keywords": ["chairperson of biocon", "kiran mazumdar-shaw"],
         "answer": "Kiran Mazumdar-Shaw: Chairperson of Biocon."},
        {"keywords": ["actor", "amitabh bachchan"], "answer": "Amitabh Bachchan: Actor."},
        {"keywords": ["actor", "shah rukh khan"], "answer": "Shah Rukh Khan: Actor."},
        {"keywords": ["actress", "deepika padukone"], "answer": "Deepika Padukone: Actress."},
        {"keywords": ["actress", "activist", "priyanka chopra"], "answer": "Priyanka Chopra: Actress and Activist."},
        {"keywords": ["film director", "rajkumar hirani"], "answer": "Rajkumar Hirani: Film Director."},
        {"keywords": ["film director", "zoya akhtar"], "answer": "Zoya Akhtar: Film Director."},
        {"keywords": ["comedian", "actor", "vir das"], "answer": "Vir Das: Comedian and Actor."},
        {"keywords": ["indian badminton player", "p. v. sindhu"], "answer": "P. V. Sindhu: Indian Badminton Player."},
        {"keywords": ["olympic gold medalist", "neeraj chopra", "javelin"],
         "answer": "Neeraj Chopra: Olympic Gold Medalist in Javelin."},
        {"keywords": ["boxer", "politician", "mary kom"], "answer": "Mary Kom: Boxer and Politician."}
    ]
    if query:
        query_lower = query.lower()

        for entry in qa_database:
            for keyword in entry["keywords"]:
                if keyword in query_lower:
                    info = entry["answer"]

                    print(info)

                    user_response = input("Do you want me to tell you more? (yes/no): ").lower()

                    if user_response == "yes":
                        name = info.split(":")[0]
                        try:
                            url = "https://en.wikipedia.org/w/api.php"
                            params = {
                                "action": "query",
                                "format": "json",
                                "prop": "extracts",
                                "exintro": True,
                                "explaintext": True,
                                "titles": name
                            }
                            response = requests.get(url, params=params)
                            if response.status_code == 200:
                                data = response.json()
                                page = next(iter(data["query"]["pages"].values()))
                                extract = page.get("extract", "Wikipedia information not found.")
                                # Truncate to only the first 2 lines
                                truncated_extract = "\n".join(extract.splitlines()[:2])
                                return f"{info}\n\nAdditional Info from Wikipedia:\n{truncated_extract}"
                            else:
                                return f"{info}\n\nError fetching Wikipedia data. Status Code: {response.status_code}"
                        except Exception as e:
                            return f"{info}\n\nError fetching Wikipedia data: {str(e)}"
                    else:
                        return "Okay, let me know if you need more information later."

        return "Sorry, no relevant information found in our database."

    else:
        return "\n".join([entry["answer"] for entry in qa_database])
def get_wolfram_answer(query):
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
            return ans
        except StopIteration:
            return "Sorry, I couldn't find that from WolframAlpha."
    else:
        return "Sorry, I couldn't understand your query. Please try again."

def send_email(receiver_add, subject, message):
    try:
        creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file('/Users/anantbhardwaj/Downloads/Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        service = build('gmail', 'v1', credentials=creds)

        mime_message = MIMEText(message)
        mime_message['To'] = receiver_add
        mime_message['Subject'] = subject
        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        send_message = service.users().messages().send(
            userId="me",
            body={'raw': encoded_message}
        ).execute()

        print(f"Email sent successfully: {send_message['id']}")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
# EMAIL="anantbhardwaj296@gmail.com"
# PASSWORD=""

def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address['ip']

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)


def get_news():
    news_headlines = []

    url = "https://api.currentsapi.services/v1/latest-news"

    params = {
        'apiKey': '3zH-be-E_I8RWepW93E0R6W9Vo5LoBwSFSP9WBzae75dR3Bs',
        'category': 'general',
        'country': 'IN'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if 'news' in data:
            articles = data['news']
            for article in articles[:6]:
                news_headlines.append(article['title'])  
        else:
            news_headlines.append("No news found.")

    except Exception as e:
        print(f"Error fetching news: {e}")
        news_headlines.append("Error fetching news.")

    return news_headlines

def weather_forcast(city):
    res=requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=f4692b1ee1a2dd6486106858e08f3ffc"
    ).json()
    weather = res['weather'][0]['main']
    temperature = res['main']['temp']
    feels_like = res['main']['feels_like']
    return weather,f"{temperature}°C", f"{feels_like}°C"
