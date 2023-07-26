import requests
from requests.api import head
from requests.auth import HTTPBasicAuth
import json
from http import HTTPStatus
import time
import getpass
def closeIssue(issue, s):
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
                "id" : "701"
            }
        }

    dataJsonFormat = json.dumps(data)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    result = s.post(issueUrl, data = dataJsonFormat, headers = headers)
    if 200 < result.status_code <= 299:
        return True
    else:
        print("Unsuccessful response code %i for issue %s" %(result.status_code,issue))
        return False
    

proxies = {
    "http":"",
    "https":""

}
username = input("Enter username in following format firstname.lastname :")
passwd = getpass.getpass(prompt="Enter intra password:")

auth = HTTPBasicAuth(username,passwd)

with requests.Session() as s:
    s.proxies=proxies
    s.auth = auth
    result=s.get('https://jira.rakuten-it.com/jira/rest/api/2/search?jql=filter%3D195443')
    if result.status_code == HTTPStatus.OK:
        json_result = json.loads(result.text)
        if json_result["total"] < 1:
            print("No tickets to close")
        else:
            for issue in json_result["issues"]:
                print("issue: %s" %issue["key"])
                closeIssue(issue["key"], s)
                time.sleep(1)
    else:
        print("Unsuccessfully response code :"+ result.status_code + " when getting all issues.")
