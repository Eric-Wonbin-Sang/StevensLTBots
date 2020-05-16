import gspread
from oauth2client.service_account import ServiceAccountCredentials

from General import Constants

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(Constants.google_sheets_json, scope)
client = gspread.authorize(credentials)


def get_google_sheets(doc_name):
    return client.open(doc_name)
