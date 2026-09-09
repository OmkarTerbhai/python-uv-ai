WEATHER_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_weather_data",
        "description": "Get the weather for a particular city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City whose weather is to be fetched"}
            },
            "required": ["city"]
        }
    }
}