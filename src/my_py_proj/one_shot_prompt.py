from  util.llm_utils import *;
from util.one_shot_sys_prompt import *;
from util.one_shot_input import *;


client = get_client(get_llm_provider());
my_messages : list[dict[str, str]] = [];

my_messages.append({
    "role": "system",
    "content": sys_prompt
});
my_messages.append({
    "role": "user",
    "content": input_prp
});

res = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
         max_tokens=200,
        messages = my_messages
);

llm_res = res.choices[0].message.content;
print(llm_res);