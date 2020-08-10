# Alan Wong

# updated 8/9/20

# Makes use of the Qualtrics API solution guide found at 
# https://api.qualtrics.com/guides/docs/Guides/Common%20Tasks/getting-survey-responses-via-the-new-export-apis.md
# to download responses for a specified survey into a zip file

import requests
import zipfile
import json
import io, os
import sys
import re
import config

# Set up and use gspread to manipulate Google Sheets: https://gspread.readthedocs.io/
import gspread 

gclient = gspread.service_account(filename='credentials.json')

# Specify name of the Google Sheet that has been provisioned for gspread
sheet = gclient.open("survey-response-dashboard")

# Look for the Qualtrics API environment variables stored in config.py
os.environ['APIKEY'] = config.api_key
os.environ['DATACENTER'] = config.datacenter

def exportSurvey(apiToken,surveyId, dataCenter, fileFormat):

    surveyId = surveyId
    fileFormat = fileFormat
    dataCenter = dataCenter 

    # Setting static parameters
    requestCheckProgress = 0.0
    progressStatus = "inProgress"
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(dataCenter, surveyId)
    headers = {
    "content-type": "application/json",
    "x-api-token": apiToken,
    }

    # Step 1: Creating Data Export
    downloadRequestUrl = baseUrl
    downloadRequestPayload = '{"format":"' + fileFormat + '"}'
    downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
    progressId = downloadRequestResponse.json()["result"]["progressId"]
    #print(downloadRequestResponse.text)


    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while progressStatus != "complete" and progressStatus != "failed":
        print ("progressStatus=", progressStatus)
        requestCheckUrl = baseUrl + progressId
        requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
        requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
        print("Download is " + str(requestCheckProgress) + " complete")
        progressStatus = requestCheckResponse.json()["result"]["status"]


    #step 2.1: Check for error
    if progressStatus is "failed":
        raise Exception("export failed")

    fileId = requestCheckResponse.json()["result"]["fileId"]


    # Step 3: Downloading file
    requestDownloadUrl = baseUrl + fileId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)


    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall("MyQualtricsDownload")
    print('Complete')


    # Step 5: Upload to Google Sheet

    # store the name of the just downloaded file from MyQualtricsDownload
    fn = (zipfile.ZipFile(io.BytesIO(requestDownload.content)).namelist()[0])

    # handle, read, and pass file to the gspread import_csv function
    with open(f'MyQualtricsDownload/{fn}', 'r') as f:
        content = f.read()
        gclient.import_csv(sheet.id, content)
        print(f'{fn} posted to https://docs.google.com/spreadsheets/d/1FnzyRnJBWo0j_eyh3ia0wX11Fbhl-NBAJMu01Y3Z3tc')


def main():
    
    print()
    try:
      apiToken = os.environ['APIKEY']
      dataCenter = os.environ['DATACENTER']
    except KeyError:
      print("set environment variables APIKEY and DATACENTER")
      sys.exit(2)

    try:
        fileFormat = 'csv'

        # specify the survey ID in the config file
        surveyId = config.survey_id
        

    except IndexError:
        print ("usage: surveyId fileFormat")
        sys.exit(2)

    if fileFormat not in ["csv", "tsv", "spss"]:
        print ('fileFormat must be either csv, tsv, or spss')
        sys.exit(2)
 
    r = re.compile('^SV_.*')
    m = r.match(surveyId)
    if not m:
       print ("survey Id must match ^SV_.*")
       sys.exit(2)

    exportSurvey(apiToken, surveyId,dataCenter, fileFormat)
 
if __name__== "__main__":
    main()