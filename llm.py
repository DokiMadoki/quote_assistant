import os
import time
from dotenv import load_dotenv
import json
import requests
from pathlib import Path
load_dotenv()

base_dir = Path(__file__).resolve().parent
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print(f"There is no OpenRouter key in your .env file")
    exit(1)

def ask(messages, temperature=0, max_tokens=2000, tools=None):
    attempt=3
    while attempt > 0:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
        }
         
        payload = {
            "model": "nvidia/nemotron-3.5-super-vl:free", 
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if tools:
            payload["tools"] = tools
        timeout = 200
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        except requests.exceptions.RequestException as error:
            print(f"Error Occured: {error}")
            exit(1)
        if response.status_code == 429:
            print(f"Retrying in 5 seconds")
            attempt-=1
            time.sleep(5)
            continue

        elif response.status_code == 200:
            data=response.json()
            print("Data Received")
            answer = data["choices"][0]["message"]["content"]
            finish_reason = data["choices"][0]["finish_reason"]
            prompt_tokens = data["usage"]["prompt_tokens"]
            completion_tokens = data["usage"]["completion_tokens"]
            message = data["choices"][0]["message"]
            return answer, finish_reason, prompt_tokens, completion_tokens, message
        
            
        else:
            print(f"There was no response {response.status_code}")
            print(f"Response Error is {response.text}")
            break