# qualtrics-project

This Python command line tool will download responses from a specified Qualtrics survey and input them into a Google Sheet. I chose Python for this project as it is a modern and versatile language with many useful libraries written for it.

### Usage

1. Clone the repository and use the following command to install all dependencies
```
pip install -r requirements.txt
```
2. Create config.py in the same directory to hold your keys, using the following structure
```
api_key = 'YOUR_API_KEY_HERE'
datacenter = 'YOUR_DATACENTER_HERE' 
survey_id = 'YOUR_SURVEY_ID_HERE'
```
3. Obtain and include in the directory the Google Service Account key for gspread, credentials.json
4. Run the following to trigger an update to the survey dashboard: https://docs.google.com/spreadsheets/d/1FnzyRnJBWo0j_eyh3ia0wX11Fbhl-NBAJMu01Y3Z3tc (you may need to request access)
```
python start.py 
```

### Built With

* [Qualtrics API](https://api.qualtrics.com/)
* [gspread](https://gspread.readthedocs.io/en/latest/)

### Current Limitations

* Cannot yet specify alternative Google Sheets to use for results.
* Gspread clears all other sheets from the spreadsheet when script is run. If we want to perform manipulation on the data, it would have to be from a separate spreadsheet. Useful: https://support.google.com/docs/answer/3093340
* Tested only with Python 3

### Acknowlegments
* https://api.qualtrics.com/guides/docs/Guides/Common%20Tasks/getting-survey-responses-via-the-new-export-apis.md
* https://gist.github.com/PurpleBooth/109311bb0361f32d87a2
* https://medium.com/knerd/best-practices-for-python-dependency-management-cc8d1913db82
