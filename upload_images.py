import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

def upload_images(images):

    SCOPES = ["https://www.googleapis.com/auth/drive"]

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
                'google_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials= creds)
        response = service.files().list(
            q= "name='Samir_CasinoImages' and mimeType='application/vnd.google-apps.folder'",
            spaces = 'drive'
        ).execute()

    #if folder is not created Create a New Folder
        if not response["files"]:
            file_metadata= {
                "name"    : "Samir_CasinoImages",
                "mimeType": "application/vnd.google-apps.folder"
            }
            file      = service.files().create(body=file_metadata,fields="id").execute()
            folder_id = file.get('id') 

        
        else:
            folder_id = response['files'][0]['id']

        file_metadata = {
            "name": '2be4473b-897c-4996-80e4-86c55fa64172.png',
            "parents": [folder_id]
        }

        #Upload Images
        media = MediaFileUpload(fr"screenshots\{images}.png")
        upload_file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields="id").execute()
        print(f"Backed up successfully: screenshots\{images}.png")

    except HttpError as e :
        print(f"Error {str(e)}")




