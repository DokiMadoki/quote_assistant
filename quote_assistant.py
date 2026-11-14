import os
import time
from dotenv import load_dotenv
import json
from llm import ask
from pathlib import Path
load_dotenv()

base_dir = Path(__file__).resolve().parent

    
def calling(messages, temperature = 0.7, max_tokens = 1500):

    result = ask(messages, temperature, max_tokens)
    if result:
        print(result[0])
        print(f"Finish Reason is {result[1]}")
        print(f"Prompt Tokens is {result[2]}")
        print(f"Completion Tokens is {result[3]}")
    else:
        print("Error: The Model returned a ratelimit, Try again after some time")


