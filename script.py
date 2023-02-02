###########################################################################
#
# NAME: Account Link Reconcile Utility
# VERSION: 1.0
#
# AUTHOR:  Tim CHONG
#
# COMMENT:
# This script will bulk Link Accounts from a CSV file using REST API.
#
# SUPPORTED VERSIONS:
# CyberArk PVWA v11.6 and above
#
#
###########################################################################

import requests
import urllib3
import csv
import ast
import sys
import ipaddress

class Logger(object): # Create log for the results
    def __init__(self, filename='results.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
     # redirect std err, if necessary

print ('###########################################################################\n#\n# NAME: Account Link Reconcile Utility\n# VERSION: 1.0\n#\n# AUTHOR:  Tim CHONG\n#\n# COMMENT:\n# This script will bulk Link Accounts from a CSV file using REST API.\n#\n# SUPPORTED VERSIONS:\n# CyberArk PVWA v11.6 and above\n#\n#\n###########################################################################\n')

def readPerfReviewCSVToDict(csvPath):
    reader = csv.DictReader(open(csvPath, 'r'))

    perfReviewsDictionary = []
    for line in reader:
        perfReviewsDictionary.append(line)

    perfReviewsDictionaryWithCommentsSplit = []
    for item in perfReviewsDictionary:
        itemId = item["Account_Name"]
        itemName = item["ExtraPass3Name"]
        itemSafe = item["ExtraPass3Safe"]
        perfReviewsDictionaryWithCommentsSplit.append({'Account_Name':itemId, 'ExtraPass3Name':itemName, 'ExtraPass3Safe':itemSafe})

    return perfReviewsDictionaryWithCommentsSplit

def ipEntered(): # check input ip address only
    while True:
        try:
            val = input("Please enter your CyberArk ip address :")
            return ipaddress.ip_address(val)
        except ValueError:
            print("Not a valid IP address")

while True:
    try:
        csv_name = input('Enter your csv file name(name.csv): ')
        dict_list = readPerfReviewCSVToDict(csv_name)
    except FileNotFoundError:
        print('CSV File '+ csv_name +' not found!')
        continue
    break

cyberarkurl = str(ipEntered())
adminusername = input("Enter CyberArk Admin username: ")
adminupassword = input("Enter CyberArk Admin password: ")


adminaccount = {
"username": adminusername,
"password": adminupassword,
"concurrentSession": True
}
s = 0
f = 0
e = 0

tokenurl = 'https://'+cyberarkurl+'/PasswordVault/API/auth/Cyberark/Logon/' 
token = requests.post(tokenurl ,json = adminaccount,verify=False)
print('Your seesion token is: '+ token.text)
seesiontoken = input("Enter your token: ")

sys.stdout = Logger(stream=sys.stdout)

Headers = { 
    "Authorization" : seesiontoken,
    "Content-Type" : "application/json"
}

for a in dict_list:
    try:
        searchurl = 'https://'+cyberarkurl+'/passwordvault/api/accounts?search='+a['Account_Name']
        go2 = requests.get(searchurl,headers=Headers,verify=False) 
        dict1 = str(go2.json())
        dict2 = dict1.replace("{'value': [",'')
        dict3 = dict2.replace("], 'count': 1}",'')
        dict4 = ast.literal_eval(dict3)  #string to dict 
        ExtraPass3Folder_patch = [
        { "op": "add", "path": "/platformAccountProperties/ExtraPass3Folder", "value": "Root"} #Add Root to Folder
        ]
        ExtraPass3Safe_patch = [
        { "op": "add", "path": "/platformAccountProperties/ExtraPass3Safe", "value": a['ExtraPass3Safe']} #Add ExtraPass3Safe
        ]
        ExtraPass3Name_patch = [
        { "op": "add", "path": "/platformAccountProperties/ExtraPass3Name", "value": a['ExtraPass3Name']} #Add ExtraPass3Name
        ]
        patchurl = 'https://'+cyberarkurl+'/PasswordVault/api/Accounts/'+dict4['id']
        # Patch method https://cyberark-customers.force.com/s/article/Add-Reconcile-and-Login-Accounts-to-an-Account-using-V10-REST-API
        go = requests.patch(patchurl,json=ExtraPass3Folder_patch,headers=Headers,verify=False) 
        go = requests.patch(patchurl,json=ExtraPass3Safe_patch,headers=Headers,verify=False) 
        go = requests.patch(patchurl,json=ExtraPass3Name_patch,headers=Headers,verify=False)
        if go.status_code == 200:
            print(a['Account_Name']+' Successful to Link Reconcile Account to '+a['ExtraPass3Name'])
            s = s+ 1
        else:
            print(go.text)
            print('Failed !')
            f = f + 1
    except(SyntaxError):
        print(a['Account_Name']+' Failed to Reconcile! Account name if is correct ?')
        e = e + 1

print('\nAll Reconcile account Completed ! ' +str(s)+ ' Successful '+str(f)+' Failed '+str(e)+' Error!\nPress Enter to continue...')  
input("")
