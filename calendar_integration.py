import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

CALENDAR_ID = "3a1773ac22fdcc8632d114dd38affc3b05dfe4ae3018628e6357c952c95e3744@group.calendar.google.com"
TIMEZONE = "Asia/Kolkata"


def getCreds():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
    
  return creds


def addEvent(start_time, end_time, title):
  creds = getCreds() 
  service = build("calendar", "v3", credentials=creds)

  event = {
    'summary': title,
    'start': {
      'dateTime': start_time.isoformat(),
      'timeZone': TIMEZONE,
    },
    'end': {
      'dateTime': end_time.isoformat(),
      'timeZone': TIMEZONE,
    },
  }
  created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
  print(f"Event created: {created_event.get('htmlLink')}")

#testing
if __name__ == "__main__":
  creds = getCreds()
  if creds == None:
    print("Google Calendar setup failed")
  else:
    print("Calendar setup is working")
