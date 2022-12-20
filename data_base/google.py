from googleapiclient import discovery
from google.oauth2 import service_account
import os


def sheet_data(link, list, path):
    """ Считываем данные с Google Sheets.
    link - ссылка на гугл таблицу;
    list - название листа в таблице;
    path - наименование json файла необходимого для работы с таблицей"""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    secret_file = os.path.join(os.getcwd(), path)
    spreadsheet_id = link
    range_name = list
    credentials = service_account.Credentials.from_service_account_file(
        secret_file, scopes=scopes
    )
    service = discovery.build("sheets", "v4", credentials=credentials)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name,
    ).execute()
    return values.get('values')
