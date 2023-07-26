import requests
from requests.api import head
from requests.auth import HTTPBasicAuth
import json
from http import HTTPStatus
import time
import getpass

def getTransitionId(issueType):
    if issueType == "Inquiry":
        return "111"
    else:
        return "701"


def closeIssue(issue, issueType, s):
    issueUrl = "https://jira.rakuten-it.com/jira/rest/api/2/issue/%s/transitions" %issue

    data = {
                "update" : {
                "comment" : [{
                        "add" : {
                                "body" : '''This ticket’s status hasn’t changed in the last three days, so we will change the status to “closed”. 
                                If you need anything else, please raise a new request.
                                https://confluence.rakuten-it.com/confluence/display/id/ID+Client+Support+Ticket+Creation.
                                Sorry for the inconvenience.
                                Best regards,
                                Operation Support Team'''
                                }
                        }]
                },
            "transition" : {
                "id" : ""
            }
        }
    data["transition"]["id"] = getTransitionId(issueType)

    dataJsonFormat = json.dumps(data)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    result = s.post(issueUrl, data = dataJsonFormat, headers = headers)
    
    if 200 < result.status_code <= 299:
        return  "Success", result.status_code
    else:
        return "Failure", result.status_code

proxies = {
    "http":"",
    "https":""
}

username = input("Enter your INTRA Username:")
passwd = getpass.getpass(prompt="Enter your INTRA Password:")

auth = HTTPBasicAuth(username,passwd)

totalIssues = 0
successfullyClosed = 0

with requests.Session() as s:
    s.proxies=proxies
    s.auth = auth
    result=s.get('https://jira.rakuten-it.com/jira/rest/api/2/search?jql=filter%3D195443')
    if result.status_code == HTTPStatus.OK:
        json_result = json.loads(result.text)
        totalIssues = json_result["total"]
        if json_result["total"] < 1:
            print("No tickets to close")
        else:
            for issue in json_result["issues"]:
                print("issue: %s" %issue["key"], end="|")
                print(" type: "+ issue["fields"]["issuetype"]["name"], end="|")

                status, reponse_code = closeIssue(issue["key"],issue["fields"]["issuetype"]["name"] , s)

                print(" Status: "+ status+ "| Response_code:"+ str(reponse_code))

                if status == "Success":
                    successfullyClosed +=1
                time.sleep(2)
    else:
        print("Unsuccessfully response code :"+ result.status_code + " when getting all issues.")

print("========================================")
print("Total issues: ", totalIssues)
print("Successfully Closed: ", successfullyClosed)
print("========================================")
