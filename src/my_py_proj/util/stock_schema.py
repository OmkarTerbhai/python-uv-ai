STOCK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_stock_details",
        "description": "Get the stock details for a ticker symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "sym": {"type": "string", "description": "Ticker symbol of company"}
            },
            "required": ["sym"]
        }
    }
}