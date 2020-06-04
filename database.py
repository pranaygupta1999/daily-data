'''
Abstraction for all the read write operation on the database
'''

from datetime import date, datetime
import dateutil.parser
import requests
import json
import xlwt 
from xlwt import Workbook, Worksheet, Style
import os


dataUrl:str  = 'https://assignment-machstatz.herokuapp.com/excel'
database_file:str = './datafile.json'
excel_file_name:str = "excel_data.xls"
latestDataUpdate:date = date.today()
date_format = "%d-%m-%Y"

def load_data():
    r = requests.get(dataUrl)
    data = r.json()
    with open(database_file, 'w+') as f:
        json.dump(data, f, indent=4)
    latestDataUpdate = date.today()



def _read_data_from_date(input_date:date)->json:
    response:dict = {
            "totalWeight": 0, 
            "totalLength": 0 ,
            "totalQuantity": 0
        }
    
    if not os.path.isfile('./datafile.json'):
        load_data()

    with open(database_file, 'r') as data_file :
        json_array:list = json.load(data_file)
        for item in json_array:
            item:dict = item
            iso_date_zulu:date = dateutil.parser.isoparse( item.get("DateTime") ).date()
            if iso_date_zulu == input_date:
                response["totalWeight"]+= item["Weight"]
                response["totalLength"]+= item["Length"]
                response["totalQuantity"]+=item["Quantity"]
    return json.dumps(response)

def read(date_string:str)->json:
    input_date:date = datetime.strptime(date_string, date_format).date()
    if input_date >= latestDataUpdate:
        print("Reloading the database")
        load_data()
        
    return _read_data_from_date(input_date)

def _process_sheet_data()->dict:
    
    load_data()
    sheet_data:dict = dict()
    with open(database_file, 'r') as data_file :
        json_array:list = json.load(data_file)
        for item in json_array:
            item:dict = item
            iso_date_zulu:date = dateutil.parser.isoparse( item.get("DateTime") ).date()
            date_key = iso_date_zulu.strftime(date_format)
            if date_key not in sheet_data:
                sheet_data[date_key] = []
                sheet_data[date_key].append( [ item["DateTime"], item["Length"], item["Quantity"], item["Weight"] ] )
            else:
                sheet_data[date_key].append( [ item["DateTime"], item["Length"], item["Quantity"], item["Weight"] ] )
    return sheet_data

def _write_to_excel():
    sheet_data:dict = _process_sheet_data()
    wb:Workbook.Workbook = Workbook()
    for date_key, data_array in sheet_data.items():
        sheet:Worksheet.Worksheet = wb.add_sheet(date_key)
        sheet.write(0,0, "DateTime", xlwt.easyxf('font: bold 1') )
        sheet.write(0,1, "Length", xlwt.easyxf('font: bold 1') )
        sheet.write(0,2, "Quantity", xlwt.easyxf('font: bold 1') )
        sheet.write(0,3, "Weight", xlwt.easyxf('font: bold 1') )
        for i in range(len(data_array)):
            for j in range(len(data_array[i])):
                sheet.write(i+1,j, data_array[i][j] )
    
    wb.save(excel_file_name)

def get_excel_file():
    # if(excel_file_not_updated):
    print("Preparing the excel file")
    _write_to_excel()
    print("Excel file created")
    return excel_file_name



        