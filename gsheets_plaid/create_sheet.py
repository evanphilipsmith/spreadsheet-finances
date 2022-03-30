import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from gsheets_plaid.initialization import CONFIG

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_creds(scopes: list[str]) -> Credentials:
    """Load or create credentials for Google Sheets API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(CONFIG.get('GOOGLE_TOKEN_FILENAME')):
        creds = Credentials.from_authorized_user_file(CONFIG.get('GOOGLE_TOKEN_FILENAME'), scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CONFIG.get('GOOGLE_CREDENTIAL_FILENAME'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(CONFIG.get('GOOGLE_TOKEN_FILENAME'), 'w') as token:
            token.write(creds.to_json())
    return creds

creds = get_creds(SCOPES)
gsheets_service = build('sheets', 'v4', credentials=creds)

def get_spreadsheet_id(verbose: str = False) -> str:
    """Get the spreadsheet ID, or create a new one
    """
    spreadsheet_id = None
    if (os.path.exists(CONFIG.get('GOOGLE_SHEETS_CONFIG_FILENAME'))):
        if verbose:
            print('Found an existing spreadsheet...')
        with open(CONFIG.get('GOOGLE_SHEETS_CONFIG_FILENAME')) as config_file:
            config = json.load(config_file)
        spreadsheet_id = config.get("spreadsheetId")
    else:
        if verbose:
            print('Creating a new spreadsheet...')
        spreadsheet = {'properties': {'title': 'Finance Tracker'}}
        result = gsheets_service.spreadsheets().create(body=spreadsheet).execute()
        spreadsheet_id = result.get("spreadsheetId")
        with open(CONFIG.get('GOOGLE_SHEETS_CONFIG_FILENAME'), 'w') as config_file:
            json.dump({"spreadsheetId": spreadsheet_id}, config_file)
    return spreadsheet_id


def main():
    """Print the spreadsheet ID.
    """
    spreadsheet_id = get_spreadsheet_id()
    print(spreadsheet_id)


if __name__ == '__main__':
    main()
