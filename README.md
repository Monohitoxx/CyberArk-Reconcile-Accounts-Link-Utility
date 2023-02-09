# CyberArk-Reconcile-Accounts-Link-Utility
This script will bulk Link Accounts from a CSV file using REST API.

# Language
Python

# Support Version:
CyberArk PVWA v11.6 and above

# CyberArk REST API Document:
https://cyberark-customers.force.com/s/article/Add-Reconcile-and-Login-Accounts-to-an-Account-using-V10-REST-API

# Requirement 
- Install requests library first
> pip install requests

## How to use
1. Ready Your csv file and put it in the same directory of script , format as below table :

	| Account_Name       | ExtraPass3Safe          | ExtraPass3Name          |
	|--------------------|-------------------------|-------------------------|
	| Link_Accounts_Name | Reconcile_Accounts_Safe | Reconcile_Accounts_Name |

2. Add the Properties to the Platform

	In "**Administration** -> **Platform Management**" select the platform that is used for the accounts.  
	Select **Edit** to edit the platform.  
	Expand "**UI & Workflows**"   -> Expand **Properties**  
	Right click on "**Optional**" and select "**Add Property**" to add Optional Properties to the platform. Add the following three properties:

> 	Name - **ExtraPass3Folder**, DisplayName - Reconcile Account Folder  
> 	Name - **ExtraPass3Name**, DisplayName - Reconcile Account Name  
> 	Name - **ExtraPass3Safe**. DisplayName - Reconcile Account Safe

3.  Run and Follow the script instructions 
4.  Your can check result in result.log file when you completed
