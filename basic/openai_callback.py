import os
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage
from langchain.schema import HumanMessage
from langchain.callbacks import get_openai_callback

load_dotenv()

BASE_URL = os.getenv('AZURE_OPENAI_BASE_URL')
DEPLOYMENT_NAME = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
API_KEY = os.getenv('AZURE_OPENAI_KEY')
AZURE_OPENAI_VERSION = os.getenv('AZURE_OPENAI_VERSION')

model = AzureChatOpenAI(
    openai_api_base=BASE_URL,
    openai_api_version=AZURE_OPENAI_VERSION,
    deployment_name=DEPLOYMENT_NAME,
    openai_api_key=API_KEY,
    openai_api_type="azure",
)

with get_openai_callback() as cb:
    model(
        [
            SystemMessage(
                content="You are a helpful assistant"
            ),
            HumanMessage(
                content="When was PTC founded ?"
            )
        ]
    )

print(f"Output: {cb}")
print(f"Total Cost (USD): ${format(cb.total_cost, '.6f')}")

