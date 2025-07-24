# CalendarAutomation

🔧 Setup Instructions: Google Calendar API
To use this project with your own Google Calendar, you'll need to create your own credentials.json file. This allows your app to securely access your Google account.

🔐 Step 1: Create a Google Cloud Project
Go to the Google Cloud Console.

Click the project dropdown at the top and select "New Project".

Give your project a name (e.g., My Calendar App) and click Create.

📦 Step 2: Enable the Google Calendar API
Visit the Calendar API Library page.

Select your project (if prompted).

Click "Enable".

🔑 Step 3: Create OAuth 2.0 Credentials
Go to the Credentials Page.

Click "Create Credentials" > "OAuth client ID".

If prompted, configure the OAuth consent screen:

Set the user type to External.

Fill in required fields (app name, email, etc.) and save.

Choose:

Application type: Desktop app

Name: Anything (e.g., My Calendar App)

Click Create.

Click "Download JSON" – this is your credentials.json file.

Save it to the root of this project folder.

✅ Step 4: Run the Script
Make sure dependencies are installed:

bash
Copy
Edit
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
Run the script:

bash
Copy
Edit
python quickstart.py
A browser window will open asking you to sign in and authorize access to your calendar.

📁 .gitignore Reminder
This project ignores sensitive files like:

pgsql
Copy
Edit
credentials.json
token.json
❗ Do not share or commit these files. They contain private API credentials and personal tokens.