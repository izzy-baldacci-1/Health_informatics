import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and summary of the events for the day.
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

  try:

    #### CONNECTION CREATION ####
    #creates the object which will be called upon to get events() as a list()
    service = build("calendar", "v3", credentials=creds)

    ##### DEFINE THE START AND END TIMES ####
    now = dt.datetime.today() 
    start_of_day = dt.datetime.combine(now, dt.time.min).isoformat() + ".00000Z"
    end_of_day = dt.datetime.combine(now, dt.time.max).isoformat() + "Z"
    #print(start_of_day)
    #print(end_of_day)

    print("Getting the events of the day")
    calendars = service.calendarList().list().execute()
    calendars_list = calendars.get("items", [])
    print([calendars_list[i]['id'] for i in range(len(calendars_list))])
    #print(calendars_list)

    events_result = (
        service.events()
        .list(
            calendarId='c_5ab6b2f16494dee5470fe3cff5859686adb59f324ce85016935bf74bc7b3edb5@group.calendar.google.com',
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    print(events[0]['summary'])
    print(f'You have {len(events)} events today!')

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    else:
      for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])
      return [event['summary'] for event in events]

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  todays_description = main()
  print(todays_description)


