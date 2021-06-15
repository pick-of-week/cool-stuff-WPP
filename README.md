# Weekly Product Shop

This repository contains the files needed for the backend
for a weekly product shop using chinabrands as a supplier.
This repository also uses the Goole Sheets API.

**API docs for [chinabrands][1]**  
**API docs for [Google Sheets API][2] & [Google Sheets Api w/ Python][3]**


[1]: <https://www.chinabrands.com/api/#/> (Api Docs for Chinabrands)
[2]: <https://developers.google.com/sheets/api> (Api Docs for Google Sheets)
[3]: <https://developers.google.com/sheets/api/quickstart/python> (Api Docs for Google Sheets and Python)

# Api Setup

To setup chinabrands API go to `Backend/settings/apiSettings.py` and refer to
**[chinabrands docs][1]** 

To setup google sheets api, first go to **[Google Sheets Docs][2]** and **[Google Sheets Docs w/ Python][3]** and follow the instructions. Then go to `Backend/settings/apiSettings.py` to configure your sheet url and sheet name.

# Variables Setup
To setup the variables for this program go to `Backend/settings/vars.py`. 
The variables are self-explanitory.
