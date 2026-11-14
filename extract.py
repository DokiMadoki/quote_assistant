from llm import ask
import json
system_prompt = """Your role is to give an output that is a JSON. Reply with only the JSON object and no other text
You wont invent any facts and only use the information you get from the user imput. If the user input is off topic reply None.
a Missing info is a null and not an invented fact or a guess. This is the format of the JSON
event_type: Some type of string like "Wedding", "Reception" or null
guest_count: Some integer or null
food_preference: "veg" , "non-veg", "mixed" or null
date: a string as the customer wrote or null
location: a string of the location the customer wrote or null
menu_items: A list of strings or null
"""

expected_keys =["event_type", "guest_count", "food_preference", "date", "location", "menu_items"]
system = {"role": "system", "content": system_prompt}


def extract_event(messages):
    result = ask(messages)
    if result is None:
        print(f"The LLM call didnt return an answer.")
        return None
    elif result[0] is None:
        print(f"The LLM call ran out of token limit")
        return None
    else:
        temp = result[0].strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            info = json.loads(temp)

        except json.JSONDecodeError:
            print(f"json decode error")
            return None
    if not isinstance(info, dict):
        print(f"LLM call returned a JSON list instead of a JSON object")
        return None
    for expected_key in expected_keys:
        if expected_key not in info:
            print(f"Missing Key: {expected_key}")
            return None

    if not isinstance(info["guest_count"], int) and info["guest_count"] is not None:
        print(f"Guest Count needs to be an int")
        return None
    return info
if __name__ == "__main__":
    data = extract_event(messages)
    print(data)

    texts = ["Hi, I need a quotation for catering, It is a marriage on the 4th of novemeber in chennai. we want a pure veg menu of idly, vada, dosai and sweet. We are expecting 500 guests",
    "Hello, I need a quotation for a reception, on 3 july at Pondicherry. non veg menu perhaps chicken biryani and chicken 65",
    "need food for my daughter’s bday, around 80 ppl, saturday",
    "I need food for a party next sunday. for 100 people, Think of a Mutton Biryani and for vegetarians Mushroom biryani",
    "What is the Weather Today?"]

    def run_inputs(texts):
        for text in texts:
            messages = [system, {"role": "user", "content": text}]
            data = extract_event(messages)
            return data

    run_inputs(texts)