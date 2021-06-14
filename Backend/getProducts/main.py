#IMPORT START
import requests as req
import json
import re
import gspread
import hashlib
from settings.apiSettings import *
from settings.vars import *
import logging
import os
from datetime import date
#IMPORT END

#CONSTANTS
SUCCESS = ["TOKEN GRABBER RAN SUCCESSFULLY", "DATA WRITTEN TO CSV SUCCESSFULLY", "CSV WRITTEN TO GOOGLE SHEETS SUCCESSFULLY"]
INFO = "WRITING DATA TO CSV"
DEL = "| "
FCOLTXT = "wp #| "
NLINECHAR = "\n"
RECHAR = " "

#DEFINE LOGGING VARS
today = date.today()
date = today.strftime("%d-%m-%Y")
appname = "POW"


#LOGGING SETUP START
filename = f'Logs/{date}-{appname}.log'
logging.basicConfig(filename=filename, level=logging.DEBUG, format="%(levelname)s @ %(asctime)s: %(message)s")
#LOGGING SETUP END

#GET TOKEN START
def get_token():

    json_data = json.dumps(chinabrandsTokenAuthData)

    signature = hashlib.md5((json_data + chinabrandsClientSecret).encode(encodingCodec)).hexdigest()

    response = req.post(chinabrandsLoginURL, data={'signature': signature, 'data': json_data})
    saved = str(response.text)
    saved2 = saved.split(':')
    saved3 = saved2[3].split(',')
    saved4 = str(saved3[0].replace('"', ''))

    return saved4
    logging.info(SUCCESS[0])

#GET TOKEN END

#TWO VALUES FOR PRODUCT LIST START
def produceStr(list, strOut):
    n = 0
    for i in list:
        if n != len(list) - 1:
            strOut += str(i) + DEL
        else:
            strOut += str(i)
        n += 1

    return strOut
#TWO VALUES FOR PRODUCT LIST END


#VARS START
url = chinabrandsInventoryUrl
info_url = chinabrandsInfoUrl
codec = encodingCodec
token = get_token()
items = itemCount
num2 = productNum
f = open('products.csv', 'w')
productList = []
headersList = []
productStr = ""
headerStr = ""
delimiter = csvDelimiter
#VARS END

#GET INFO START

for p in items:
    #define data
    data = {'token' : token, 'type' : 0, 'per_page' : 1, 'page_number' : 1}

    #request and save data
    response = req.post(url, data=data)
    saved = str(response.text)
    #print(saved)

    #split data
    mylist = saved.split(":")
    saved_sn = str(mylist[10]).split(',')
    sn = str(saved_sn[0]).replace('"', "")

    #get data from data above
    more_data = {'token' : token, 'goods_sn' : json.dumps(sn)}
    info_response = req.post(info_url, data=more_data)

    #save and split
    info = info_response.text
    infoJsonFormatPrint = json.dumps(json.loads(info), indent=4)
    infoJsonFormatWrite = json.loads(infoJsonFormatPrint)

    dictOfDict = infoJsonFormatWrite["msg"][0]
    for key in dictOfDict.keys():
        headersList.append(key)

    for values in dictOfDict.values():
        productList.append(values)


    headerStr = FCOLTXT + produceStr(headersList,headerStr) + NLINECHAR
    productStr = str(num2) + DEL + re.sub(NLINECHAR, " ", produceStr(productList, productStr))

    #print(productList)

    #print(produceStr(productList, productStr))

    if p == 1:
        f.write(headerStr)
        f.write(productStr)

    else: f.write(productStr + NLINECHAR)

    num2 += 1
    logging.info(INFO)


f.close()
logging.info(SUCCESS[1])
#GET INFO END

#UPLOAD CSV START
scope = googleSheetScope

client = gspread.service_account(filename="coolstuffwpp-9409dc01a700.json", scopes=scope)
content = open('products.csv', 'r').read()

spreadsheet = client.open_by_url(googleSheetURL)
dataSheet = spreadsheet.worksheet(googleSheetName)
body = {
    "requests": [
        {
            "pasteData": {
                "data": content,
                "delimiter": delimiter,
                "coordinate": {
                    "sheetId": dataSheet.id
                }
            }
        }
    ]
}

spreadsheet.batch_update(body)
logging.info(SUCCESS[2])
#UPLOAD CSV END
