import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


def access_to_sheets(xk):
    scope = ['https://spreadsheets.google.com/feeds']
    row = 2
    cell = 1
    cred = ServiceAccountCredentials.from_json_keyfile_name('client.json', scope)
    client = gspread.authorize(cred)
    sheet = client.open("Internet Faults").sheet1
    time = sheet.update_cell(row, cell, xk)
    day = sheet.update_cell(row, cell, xk)
    print(time)
    print(day)

def main():
    access_to_sheets(datetime.now().time())


if __name__ == "__main__":
    main()