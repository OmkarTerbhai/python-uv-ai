from util.llm_utils import *;
from util.weather_schema import WEATHER_SCHEMA;
import json
from util.weather_data import WEATHER_DATA;

def get_weather_data(city: str) -> str :
    """Get the weather for a particular city"""
    rec = WEATHER_DATA.get(city.lower());

    if rec is None :
        print("City not found");
        return None;

    return (f"The temperature in {city} is {rec['celcius']} and the sky is {rec['sky']}");

TOOLS = {
    "get_weather_data": get_weather_data
}

def get_llm_reply(prompt: str) :
    client = get_client(get_llm_provider());

    messages : list[dict[str, str]] = [];
    messages.append({
        "role": "user",
        "content": prompt
    });

    return agent_loop(client, messages);


def agent_loop(client, messages: list[dict[str, str]]) :
    while True :

        res = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=[WEATHER_SCHEMA]
        );
        raw = res.choices[0].message;

        if not raw.tool_calls :
            return raw.content;

        messages.append({
            "role": "assistant",
            "content": raw.content,
            "tool_calls": raw.tool_calls
        });

        append_tool_call_result(raw, messages);


def append_tool_call_result(raw, messages: list[dict[str, str]]):
    for tool_call in raw.tool_calls:
        tool_id = tool_call.id;
        tool_func_name = tool_call.function.name;
        tool_func_args = json.loads(tool_call.function.arguments);

        if tool_func_name not in TOOLS:
            raise ValueError("Func not found");

        tool_func = TOOLS[tool_func_name];
        result = tool_func(**tool_func_args);

        messages.append({
            "role": "tool",
            "tool_call_id": tool_id,
            "content": result
        })

print(get_llm_reply(input()));
