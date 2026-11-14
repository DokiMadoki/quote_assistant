import json
from llm import ask
from pricing import calculate_quote
from extract import extract_event

system = {"role": "system", "content": "You are a catering quote assistant. Use calculate_quote to find the price and dont invent it yourself."}


tools = [{
    "type": "function",
    "function": {
    "name": "calculate_quote",
    "description": "Use this to calculate a quote after the customer gives you the details.",
    "parameters": { 
        "type": "object",
        "properties": {
            "guest_count": {"type": "integer", "description": "Number of Guests"},
            "food_preference": {"type": "string", "enum": ["veg", "non-veg", "mixed"]}
        },
        "required": ["guest_count", "food_preference"]
    }
    }
}]

text = "Hey, I want a quotation for a marriage, 500 people and a veg menu"
text2 = "Hey I want a quotation for a birthday party on friday, non veg menu"
def quote_chat(text):
    message =[system, {"role": "user", "content": text}]

    result = ask(message, 0, 2000, tools)

    if result[1] == "tool_calls":
        tool_call = result[4]["tool_calls"][0]

        # tool_call=json.loads(temp).strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        if tool_call["function"]["name"] == "calculate_quote":
            try:
                arguments = json.loads(tool_call["function"]["arguments"])
            except json.JSONDecodeError:
                print(f"LLM call didnt return proper format")
                exit(1)
            food_preference = arguments.get("food_preference")
            guest_count = arguments.get("guest_count")
            quote = calculate_quote(guest_count, food_preference)
            print(quote)
            message.append(result[4])
            message.append({"role": "tool", "tool_call_id": tool_call["id"], "content": json.dumps(quote)})
            result2= ask(message, 0, 2000, tools)
            print(result2)
    else:
        print(result)

# quote_chat(text)
quote_chat(text2)