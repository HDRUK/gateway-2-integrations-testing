# Introduction

The Private Apps feature enables Developers to create a Private App and corresponding ClientID which is used as a token to authenticate requests made to the Gateway API. This guide offers step-by-step instructions for setting up and managing Private Apps on the Gateway. 

## How to Create a new Private App

_Please note that HDR UK cannot create Private Apps on behalf of users._

### Step 1: Sign into the Gateway

Sign in to the Gateway with your preferred login provider. Make sure you have a ‘team’ set up on the Gateway. If you are not a member of an existing ‘team’ you may need to ask a Team Admin to add you  to the team (see documentation [here](https://www.healthdatagateway.org/en/support/team-management) on how to manage ‘team’ on the Gateway). If you need assistance with this step, contact the HDR UK Technology Team using the link below. 

[https://hdruk.atlassian.net/servicedesk/customer/portal/7/group/14/create/29](https://hdruk.atlassian.net/servicedesk/customer/portal/7/group/14/create/29)


### Step 2: Access the Gateway Private App management page

Providing you have the necessary roles (Team Admin or Developer), you can access the feature by following these steps: 

- Navigate to your Team Management page by clicking on your name in the top-right corner of the window, and selecting the your ’team’ from the dropdown list. 
- In the menu on the left-hand side, select Integrations > Private Apps. 
- Click on the Create Private App button to initiate the process (Fig 1) 

![](https://github.com/HDRUK/gateway-2-integrations-testing/assets/69473770/4dd0dbc8-10ae-46a0-b567-9c98c3367987)
_Fig 1: How to create a new Private App_

### Step 3: Enter Private App details

To create a new Private App you will need to enter the following information (Fig 2):

- Public App name: Name of the App you wish to create. 
- Description: A brief description of the App. 
- Notification contacts: Gateway user accounts for relevant notification recipients. 

After completing the required fields, click the Save & Continue button to proceed to the permissions page.

![image](https://github.com/HDRUK/gateway-2-integrations-testing/assets/69473770/5667e21e-576d-4aec-9a96-92448c4375fc)
_Fig 2: App info_


### Step 4: Define permissions

Use the permissions matrix (Fig 3) to assign the appropriate permissions for secure integration. Your App will only be allowed to use APIs for the permissions you have defined. App permissions are the responsibility of your ‘team’.  

If you have any questions about defining Private App permissions, please contact the HDR UK Technology Team using the URL below. 

[https://hdruk.atlassian.net/servicedesk/customer/portal/7/group/14/create/29](https://hdruk.atlassian.net/servicedesk/customer/portal/7/group/14/create/29)

![image](https://github.com/HDRUK/gateway-2-integrations-testing/assets/69473770/6146a122-e2fb-4daf-a514-f69d2008e178)
_Fig 3: Permissions matrix_

We recommend only assigning permissions that the App will need and suggest a minimal permissions approach, for example: if an App is going to be managing Datasets we would recommend `datasets.create`,  `datasets.read`,  `datasets.update`,  and `datasets.delete`. There would be no need to grant the App permissions to manage Tools or Data Uses in this instance. 

Once the desired permissions are set, click the Save & Finish button to complete the Private App setup. 

**Please note, at the current time, only functionality for Datasets has been enabled on the Gateway.**

### Step 5: Authentication Keys

Click on the newly created App entry. The AppID and ClientID will be accessible in the Authentication tab after completing the App setup (Fig 4). Both the AppID and Client ID are crucial as any requests to an authenticated Gateway API endpoint will require these to validate the request. Please see the documentation _link_ which demonstrates how to make an authenticated API request to the Gateway. 

![image](https://github.com/HDRUK/gateway-2-integrations-testing/assets/69473770/2c0ec13f-bbe8-4a07-94ee-adc9b8c5620a)
_Fig 4: Authentication_