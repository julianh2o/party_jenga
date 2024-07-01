import json
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def spreadsheet_to_objects(spreadsheet):
    if not spreadsheet:
        return []

    headers = spreadsheet[0]
    data_rows = spreadsheet[1:]

    list_of_objects = [
        {headers[col]: row[col] for col in range(len(headers))}
        for row in data_rows
    ]

    return list_of_objects

def fetchSheet(docid,sheet):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(docid)
    worksheet = spreadsheet.worksheet(sheet)
    return worksheet.get_all_values()

docid = "1ggqWR4aNg1k6kfZ2-RwNR6ksvlHd_J80EuznuN712kQ"
sheet = "Rules"

data = fetchSheet(docid,sheet)
with open('rules.tsv', 'w', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
    for line in data:
        writer.writerow(line)
