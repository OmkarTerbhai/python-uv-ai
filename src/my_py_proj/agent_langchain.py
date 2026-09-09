from langchain.agents import create_agent
from langchain_groq import ChatGroq
from util.stock_utils import get_stock_details;
from dotenv import load_dotenv;
import os;


load_dotenv();

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY", "")  # or rely on GROQ_API_KEY env var
)

agent = create_agent(
    model=llm,
    tools=[get_stock_details],
    system_prompt="You are expert at stock analysis. You take company name and find its stock symbol first and then call the tool with that symbol"
);

res = agent.invoke({
        "messages" : [
            {"role": "user", "content": "Compare stock price of RELIANCE and ADANIPORTS"}
        ]
});

print(res["messages"][-1].content);

#
# for msg in res["messages"] :
#     print(msg)