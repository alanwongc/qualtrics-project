# Alan Wong

# updated 7/14/20

# Using the API solution guide found at 
# https://api.qualtrics.com/guides/docs/Guides/Common%20Tasks/getting-survey-responses-via-the-new-export-apis.md
# to download responses for a specified survey into a zip file

import requests
import zipfile
import json
import io, os
import sys
import re
import config

#Python API to manipulate Google Sheets: https://gspread.readthedocs.io/
import gspread 

gclient = gspread.service_account(filename='credentials.json')

#specify name of the Google Sheet that has been provided access
sheet = gclient.open("survey-response-dashboard")

# Set Qualtrics API environment variables
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

    # retrieve name of downloaded results file saved to MyQualtricsDownload
    fn = (zipfile.ZipFile(io.BytesIO(requestDownload.content)).namelist()[0])

    # read content and pass to gspread import_csv API
    with open(f'MyQualtricsDownload/{fn}', 'r') as f:
        content = f.read()
        gclient.import_csv(sheet.id, content)


def main():
    
    print()
    try:
      apiToken = os.environ['APIKEY']
      dataCenter = os.environ['DATACENTER']
    except KeyError:
      print("set environment variables APIKEY and DATACENTER")
      sys.exit(2)

    try:
        # Take in survey ID and file format as command line arguments
        #surveyId=sys.argv[1]
        #fileFormat=sys.argv[2]

        # Hard code the survey ID and file format instead for easier testing
        surveyId = 'SV_6ES6BtNDjQ3UMJf'
        fileFormat = 'csv'

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