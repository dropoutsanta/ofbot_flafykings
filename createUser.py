import requests
import json

url = "https://citeifmttmdotbcsotyh.supabase.co/rest/v1/users"

def createUser(userId, username, first_name, last_name, language_code):
    payload = json.dumps({
    "user_id": userId,
    "username": username,
    "first_name": first_name,
    "last_name": last_name,
    "language_code": language_code
    })
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)