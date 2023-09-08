import json
import requests
import yfinance as yf
from tenacity import retry, wait_random_exponential, stop_after_attempt

GPT_MODEL = "gpt-3.5-turbo"

def get_stock_price(tickerSymbol):
    ticker = yf.Ticker(tickerSymbol).info
    market_price = ticker['regularMarketOpen']
    print("function get_stock_price is invoked with %s using Yahoo Finance %s" % (tickerSymbol, market_price) )
    return market_price

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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",
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        print("HTTP Request = %s" % json.dumps(json_data, indent=1))
        print("HTTP Response = %s %s" % (response, json.dumps(response.json(), indent=1)))
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

functions = [
    {
      "name": "get_stock_price",
      "description": "Get current stock price",
      "parameters": {
        "type": "object",
        "properties": {
          "ticker_symbol": {
            "type": "string",
            "description": "Ticker symbol of the stock"
          }
        }
      }
    }
]

user_message = "What's the current price of Apple stocks?"
messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. "
                                              "Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": user_message})
chat_response = chat_completion_request(
    messages, functions=functions
)
assistant_message = chat_response.json()["choices"][0]["message"]
print("User = %s" %user_message)
print("Assistant = %s" %assistant_message)

if assistant_message['function_call'] and assistant_message['function_call']['name'] == 'get_stock_price':
    market_price = get_stock_price((json.loads(assistant_message['function_call']['arguments'])['ticker_symbol']))

messages.append({"role": "function", "name": "get_stock_price", "content": "{\"market_price\": \"110.23\"}"})
chat_response = chat_completion_request(
    messages, functions=functions
)
assistant_message = chat_response.json()["choices"][0]["message"]
print("Assistant = %s" %assistant_message)