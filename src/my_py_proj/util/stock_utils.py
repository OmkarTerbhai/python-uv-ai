import yfinance as yf;
import json;
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def get_stock_details(sym: str) :
    """A simple tool to fetch JSON data of stock of single company"""
    stock = yf.Ticker(sym.upper().strip());

    price = (stock.fast_info['lastPrice']);
    currency = (stock.fast_info['currency']);
    exchange = (stock.fast_info['exchange']);

    return json.dumps({
        "price": price,
        "currency": currency,
        "exchange": exchange
    });