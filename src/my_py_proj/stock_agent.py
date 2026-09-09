from util.llm_utils import *;
from util.stock_schema import STOCK_SCHEMA;
import json
from util.stock_utils import get_stock_details;

TOOLS = {
    "get_stock_details": get_stock_details
}

def get_tools_llm_reply(prompt: str) :
    client = get_client(get_llm_provider());

    messages : list[dict[str, str]] = [];
    messages.append({
        "role": "user",
        "content": prompt
    });

    while True :

        res = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=[STOCK_SCHEMA]
        );
        raw = res.choices[0].message;

        if not raw.tool_calls :
            return raw.content;

        messages.append({
            "role": "assistant",
            "content": raw.content,
            "tool_calls": raw.tool_calls
        });



        for tool_call in raw.tool_calls :
            tool_id = tool_call.id;
            tool_func_name = tool_call.function.name;
            tool_func_args = json.loads(tool_call.function.arguments);

            if tool_func_name not in TOOLS :
                raise ValueError("Func not found");

            tool_func = TOOLS[tool_func_name];
            result = tool_func(**tool_func_args);

            messages.append({
                "role": "tool",
                "tool_call_id": tool_id,
                "content": result
            })

print(get_tools_llm_reply(input()));