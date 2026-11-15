# Quotation Assistant
This is a simple program that gives a quotation for a fictional catering business using terminal chat.
The file needs to be run inside a venv
```bash
# Create and activate
python3 -m venv .venv
source .venv/bin/activate
```
requirements.txt has the required things to run it. 
```bash
python -m pip install -r requirements.txt
```

we need a .env file with your openrouter API key. use .env.example to create one.
Copy that file and save it as .env 
```bash
cp .env.example .env
```
You should be able to see OPENROUTER_API_KEY=your_api_key which takes your Openrouter API Key.
replace 'your_api_key' with your Key


The program has various guardrails and you can run it by simply running
```bash
python quote_chat.py
```
Ensure venv is turned on. It also has a function that allows it to hand off conversations to humans. it will be in handoffs.jsonl. 

## How it works
The is an Agent loop that runs and it has two branches one for Model replies and one for tool calls. 
There are guardrails for:
- Grounding Check so Model doesnt make up number.
- Handoffs for when Model cant reliably answer due to lack of tools.
- No Reply checks so customers dont get empty replies. 


## Known Limits
Guardrials arent perfect:
- Prices without a Rupee sign or Rs prefix get through. 
- A real number attached to a wrong item can get through.
- False positives such as when agent telling the customer the Order price is not what the customer expected gets denied by the grounding check as making up numbers
- No way to flag for big numbers on guest_count such as 200000
- A Discount promise in it without a price wont get stopped 

