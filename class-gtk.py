import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']


def main():
    win = class_gtk()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    
def api():
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('classroom', 'v1', credentials=creds)

        # Call the Classroom API
        results = service.courses().list(pageSize=100).execute()
        courses = results.get('courses', [])

        if not courses:
            print('No courses found ):')
            return
        # Prints the names of the first 10 courses.
        print('Courses:')
        for course in courses:
            print(course['name'])

    except HttpError as error:
        print('An error occurred: %s' % error)
    return courses

class class_gtk(Gtk.Window):
    def __init__(self):
       super().__init__(title="Class")
       #self.button = Gtk.Button(label="button")
       #self.button.connect("clicked", self.on_button_clicked)
       self.grid = Gtk.Grid()
       #self.grid.attach(self.button, 0, 0, 1, 1)
       self.add(self.grid)

       self.course = {}
       self.courses = api()
       self.add_course_buttons()

       vscrollbar = Gtk.Scrollbar(orientation=Gtk.Orientation.VERTICAL)
       self.grid.attach(vscrollbar, 2, 0, 1, 50)

    def on_button_clicked(self, widget):
        pass

    def add_course_buttons(self):
        for y, course in enumerate(self.courses, 1):
            name = course['name']
            self.course[name] = Gtk.Button(label=name)
            self.course[name].connect("clicked", self.on_button_clicked)
            self.grid.attach(self.course[name], 1, y, 1, 1)

if __name__ == '__main__':
    main()
