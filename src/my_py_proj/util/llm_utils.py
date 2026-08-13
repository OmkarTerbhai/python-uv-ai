from dataclasses import dataclass;
import os;
from groq import Groq;
from dotenv import load_dotenv;

load_dotenv();

messages : list[dict[str, str]] = [];


@dataclass(frozen=True)
class Provider :
    name: str;
    api_key: str;
    is_free: bool;
    model: str;

PROVIDERS : list[Provider] = [
    Provider(
        name="Groq",
        api_key=os.getenv("GROQ_API_KEY", ""),
        is_free=True,
        model=os.getenv("GROQ_MODEL", ""),
    )
];

def get_llm_provider() -> Provider :

    for p in PROVIDERS :
        if p.api_key and p.model :
            return p;
    return None

def get_client(provider: Provider) -> Groq :

    if provider.api_key and provider.model :
        print(f"Found API key and model for {provider.name}")
    return Groq(
        api_key = provider.api_key
    );

def llm_msg(prompt: str) -> str :
    curr_provider = get_llm_provider();
    client = get_client(curr_provider);
    messages.append({
            "role": "user",
            "content": prompt
    });
    res = client.chat.completions.create(
        model = curr_provider.model,
         max_tokens=200,
        messages = messages
    );

    llm_res = res.choices[0].message.content;
    messages.append

    messages.append({
        "role": "assistant",
        "content": llm_res
    })
    return llm_res;