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


def exam_reputation(inn: int = 5021013384):
    mandatory_certificate = sheet_data(link="1NG2gg8YmPmW3g5qWNz_c08e4q0SJGxV3let9BVIxfh8",
                                       list="'Обязательные СС'!A:Q",
                                       path="lab-reestr-6aa81a2d3150.json")
    for one_mandatory_certificate in mandatory_certificate:
        status_mandatory_certificate = one_mandatory_certificate[0]
        inn_manufacture_mandatory_certificate = one_mandatory_certificate[15]
        try:
            name_manufacture_mandatory_certificate = one_mandatory_certificate[16]
            if inn_manufacture_mandatory_certificate == str(inn):
                print(
                    f"status: {status_mandatory_certificate}, inn: {inn_manufacture_mandatory_certificate}, name: {name_manufacture_mandatory_certificate}")
        except:
            pass


if __name__ == '__main__':
    exam_reputation(inn=5021013384)
