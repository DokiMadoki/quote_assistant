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
message =[system]
if __name__ == "__main__":
    print("Hi, I am your Quotation Assistant. Please tell me the details of your event!")
    user_message=input()
    message.append({"role": "user", "content": user_message})
def run_turn(messages):
    limit=5
    while limit > 0:
        result = ask(messages, 0, 2000, tools)
        if result is None:
            print("Our services seem to be busy, Please try again later")
            exit(1)
        if result[1] == "tool_calls":
            messages.append(result[4])
            limit -= 1
            tool_calls = result[4]["tool_calls"]
            for tool_call in tool_calls:
                if tool_call["function"]["name"] == "calculate_quote":
                    try:
                        arguments = json.loads(tool_call["function"]["arguments"])
                    except json.JSONDecodeError:
                        messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": "error: The LLM call did not return a valid json"})
                        continue
                    guest_count = arguments.get("guest_count")
                    food_preference = arguments.get("food_preference")
                    quote = calculate_quote(guest_count, food_preference)
                    messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": json.dumps(quote)})
                    print(f"{tool_call["function"]["name"]} tool was called. Arguments were {arguments}. The Quote generated was {quote}")
                else:
                    messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": "error: The LLM call did not return a valid function name"})
        else:
            limit = 5
            print(f"{result[0]} \nType \"quit\" to Quit")
            messages.append(result[4])
            user_message=input()
            if user_message.strip().lower() == "quit":
                break
            messages.append({"role": "user", "content": user_message})
    if limit <= 0:
        print("The number of calculation attempts exceeded the limits, Try Again later.")
    else:
        print("Thank you for using Our Quote Assistant")
            


if __name__ == "__main__":
    run_turn(message)
