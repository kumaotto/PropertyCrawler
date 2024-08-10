# SUUMO crawler and notify someone

## Overview

- Enable the noticing of new candidate houses
- Notify the person you’re considering living with to facilitate a smooth decision-making process

## Features

- Notify new house adjust your condition
- Notify when someone reacts to new bot message
    - If your future cohabitant reacts to the messages, you'll receive a notification.
- List your favorite house
    - If you react with a specific icon, the bot will pin the message.
    - And the reacted properties will be listed in a spreadsheet for easier management. (Also remove unreacted properties)

## Usage
### Enabling the Functionality for Writing to a Spreadsheet

To enable the functionality for writing to a spreadsheet, follow these steps to create `credentials.json` (make sure to rename it to `credentials.json`). Place the created `credentials.json` in the root of your project.  
[Google Sheets API Quickstart for Python](https://developers.google.com/sheets/api/quickstart/python?hl=en)

### How to Post a Message to Slack

1. **Copy `.env.example`:**
```shell
   cp .env.example .env
```

1. **Create a token on Slack and fill out the `.env` file**

Steps:

1. Log in to Slack API: Go to the Slack API page and select your app.
2. OAuth & Permissions Page: From the left-hand menu, select "OAuth & Permissions."
3. Bot Token Scopes: Go to the "Bot Token Scopes" section and add the scopes required by your app. For example, to post messages, you need the following scopes:
- chat:write (Posting messages)
- channels:read (Reading channel information)
4. Regenerate OAuth Token: After adding the scopes, click the "Reinstall App" button in the "OAuth Tokens for Your Workspace" section to generate a new token.
