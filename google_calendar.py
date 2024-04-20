import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account
import googleapiclient.discovery

# Функція для отримання списку подій з веб-сторінки


def get_events_from_website(url):
    events = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Розбираємо HTML сторінку і дістаємо дані про події
        
        for event_elem in soup.find_all(class_='event'):
            event_title = event_elem.find(class_='event-title').text.strip()
            event_date = event_elem.find(class_='event-date').text.strip()
            event_description = event_elem.find(
                class_='event-description').text.strip()
            events.append({'title': event_title, 'date': event_date,
                          'description': event_description})
    return events

# Функція для додавання подій до Google Календаря


def add_events_to_google_calendar(events):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # Шлях до файлу з автентифікаційними ключами
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=credentials)

    calendar_id = 'primary'  # ID календаря

    for event in events:
        event_obj = {
            'summary': event['title'],
            'description': event['description'],
            'start': {'date': event['date']},
            'end': {'date': event['date']}
        }

        # Додаємо подію до календаря
        service.events().insert(calendarId=calendar_id, body=event_obj).execute()


# Отримуємо список подій з веб-сторінки
events = get_events_from_website('https://www.edu.goit.global/uk/calendar')

# Додаємо події до Google Календаря
add_events_to_google_calendar(events)

print("Події успішно додані до Google Календаря!")
