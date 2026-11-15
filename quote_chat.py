import json
import re
from llm import ask
from pricing import calculate_quote
from handoff import handoff


system = {"role": "system", "content": """You are a catering quote assistant. 
Use calculate_quote to find the price and dont invent it yourself. 
Discounts are given to orders which have guest_count of 500 or more only.
we give 10% discount for those customers only. 
You cant offer discounts for any other reason.

When you cant handle the situation, use handoff.
when the customer wants to talk to a human use handoff."""}


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
},
{
    "type": "function",
    "function": {
        "name": "handoff",
        "description": "Use this to hand the issue to a human when you dont have any tools to handle it.",
        "parameters": {
            "type": "object",
            "properties": {
                "handoff_reason": {"type": "string", "description": "The reason that we are handing off, Give all the relavent data for the human to understand the sitaution and also mention any data you got from the customer."}
            },
            "required": ["handoff_reason"]
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
                elif tool_call["function"]["name"] == "handoff":
                    try:
                        arguments = json.loads(tool_call["function"]["arguments"])
                    except json.JSONDecodeError:
                        messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": "error: The LLM call did not return a valid json"})
                        continue
                    reason = arguments.get("handoff_reason")
                    handoff(reason)
                    print("This request has been forwarded to a Human agent. They will get back to you about this")
                    exit(1)
                else:
                    messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": "error: The LLM call did not return a valid function name"})

        else:
            messages.append(result[4])
            allowed=set()
            for item in messages:
                if item["role"] != "tool":
                    continue
                try:
                    arguments=json.loads(item["content"])
                except json.JSONDecodeError:
                    continue
                if "error" in arguments:
                    continue
                allowed.add(float(arguments.get("total")))
                allowed.add(float(arguments.get("sub_total")))
                allowed.add(float(arguments.get("price_per_plate")))
            claimed=set()

            if result[0] is None or not result[0].strip():
                messages.append({"role": "system", "content": "The content was empty on a reply"})
                print(f"The LLM call had an empty reply {result}")
                limit -= 1
                continue
            elif result[1] == "length":
                print("Session limit exceeded. Sorry!")
                exit(1)
            else:
                captured = re.findall(r"(?:Rs|₹)\.?\s?(\d[\d,]*)", result[0])
                for item in captured:
                    item_f=float(item.replace(",", ""))
                    claimed.add(item_f)
                unbacked = claimed - allowed
                if unbacked:
                    messages.append({"role": "system", "content": f"I think you used made up values instead of using the tool output. here is the numbers found {unbacked}"})
                    limit -= 1
                    print(f"The LLM call made up some numbers {unbacked}")
                    continue
                else:
                    print(f"{result[0]} \nType \"quit\" to Quit")
            limit = 5
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