import requests
import json

def getSFW(bot_id):
    url = f"https://citeifmttmdotbcsotyh.supabase.co/rest/v1/media?bot_id=eq.{bot_id}"

    payload = {}
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    jsonValue = json.loads(response_text)
    print("PICTURES")
    print(jsonValue)
   
    return jsonValue

