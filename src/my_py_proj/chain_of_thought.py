from  util.llm_utils import *;
from util.cot_prompt import *;


client = get_client(get_llm_provider());
my_messages : list[dict[str, str]] = [];


my_messages.append({
    "role": "user",
    "content": cot_prompt
});

res = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
         max_tokens=2048,
        messages = my_messages
);

llm_res = res.choices[0].message.content;
print(llm_res);