---
title: What is a private app
description: What a private app is and why you need one to call the Gateway API.
tags:
  - api
  - auth
---

# Private Apps

## What is a Private App

Private apps allow you to use the Gateway’s APIs to access specific data from your Gateway Team. You can define what features/services each Private App is able to access from the management page. Two access tokens will be generated called the "AppID" and “ClientID”, both of which must be sent with each request to the Gateway APIs. 

Private Apps are perfect for users who want to programmatically interact with the features and data on the Gateway and how you interact with the Gateway APIs is entirely in your control. 


## Glossary

|Term|Description|
|------|-------------|
|Private App|An application/service/ETL tool that is developed by a user who wants to be able to programmatically interact with the Gateway. |
|AppID and ClientID |Tokens that are generated when creating a new Private App. Each Private App will have a unique AppID and ClientID that needs to be sent with each API request to authenticate and approve the action. |
|Team Admin/Developer |A role that can be assigned to a user when they are part of a ‘team’ on the Gateway. Please see the documentation [here](https://www.healthdatagateway.org/about/how-to-manage-teams-on-the-gateway) on roles and permissions on the Gateway. |
|Authenticated API Endpoint |While a lot of the Gateway APIs are accessible without authentication, any endpoint changing data requires authentication. The ClientID acts as an authentication token. |