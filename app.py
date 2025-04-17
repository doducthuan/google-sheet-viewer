from flask import Flask, render_template, request
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import logging
import string

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1VtyjW-OHHgyD6gOeSxfYsPdb14mZiL1hI3MUm4CfriI'

def get_column_letter(n):
    """Convert column number to letter (1 -> A, 2 -> B, etc.)"""
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = string.ascii_uppercase[remainder] + result
    return result

def get_sheets_list():
    """Get list of all sheets in the spreadsheet"""
    try:
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
        return sheets
    except Exception as e:
        logger.error(f"Error getting sheets list: {str(e)}")
        return []

def get_google_sheets_data(sheet_name):
    """Get data from specific sheet in Google Sheets"""
    try:
        logger.info(f"Attempting to read data from sheet: {sheet_name}")
        creds = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheet_properties = next((s['properties'] for s in spreadsheet['sheets'] 
                               if s['properties']['title'] == sheet_name), None)
        
        if not sheet_properties:
            return [], 0, 0
        
        grid_properties = sheet_properties['gridProperties']
        max_rows = grid_properties['rowCount']
        max_cols = grid_properties['columnCount']
        
        range_name = f"{sheet_name}!A1:{get_column_letter(max_cols)}{max_rows}"
        logger.info(f"Fetching data from range: {range_name}")
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=range_name).execute()
        values = result.get('values', [])
        
        for row in values:
            while len(row) < max_cols:
                row.append('')
        
        while len(values) < max_rows:
            values.append([''] * max_cols)
        
        logger.info(f"Retrieved {len(values)} rows of data from {sheet_name}")
        return values, max_rows, max_cols
    except Exception as e:
        logger.error(f"Error accessing Google Sheets: {str(e)}")
        return [], 0, 0

@app.route('/')
def index():
    sheet_name = request.args.get('sheet', '')
    sheets = get_sheets_list()
    
    if not sheet_name and sheets:
        sheet_name = sheets[0] 
    
    data, max_rows, max_cols = get_google_sheets_data(sheet_name) if sheet_name else ([], 0, 0)
    column_headers = [get_column_letter(i+1) for i in range(max_cols)]
    
    logger.info(f"Rendering template with {len(data)} rows of data from {sheet_name}")
    return render_template('index.html', 
                         data=data, 
                         sheets=sheets, 
                         current_sheet=sheet_name,
                         column_headers=column_headers,
                         max_rows=max_rows,
                         max_cols=max_cols)

if __name__ == '__main__':
    app.run(debug=True) 