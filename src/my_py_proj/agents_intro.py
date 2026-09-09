from util.llm_utils import *;
from util.weather_schema import WEATHER_SCHEMA;
import json

WEATHER_DATA = {
    "london": {"celcius": 22, "sky": "cloudy"},
    "paris": {"celcius": 24, "sky": "sunny"},
    "tallinn": {"celcius": 28, "sky": "sunny"},
    "moscow": {"celcius": 18, "sky": "rainy"},
    "tokyo": {"celcius": 30, "sky": "sunny"},
    "beijing": {"celcius": 26, "sky": "cloudy"},
    "new york": {"celcius": 28, "sky": "sunny"},
    "mumbai": {"celcius": 32, "sky": "sunny"},
    "cape town": {"celcius": 16, "sky": "cloudy"},
    "sydney": {"celcius": 20, "sky": "sunny"},
    "rio de janeiro": {"celcius": 22, "sky": "cloudy"},
    "cairo": {"celcius": 24, "sky": "sunny"},
    "mexico city": {"celcius": 20, "sky": "cloudy"},
}

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

print(get_tools_llm_reply("What is the weather right now in Tokyo"));
