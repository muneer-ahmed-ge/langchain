import yfinance as yf
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")

def get_stock_price(tickerSymbol):
    ticker = yf.Ticker(tickerSymbol).info
    market_price = ticker['regularMarketOpen']
    print("function get_stock_price is invoked with %s using Yahoo Finance %s" % (tickerSymbol, market_price) )
    return market_price

tools = [
    Tool(
        name = "get_stock_price",
        func=get_stock_price,
        description="Useful to get stock price given Ticker symbol"
    )
]

chain = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
chain.run("What's the current price of Apple stocks?")

