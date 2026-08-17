from pydantic import BaseModel;
from llm_utils import *
from step_cot_sys_prompt import sys_prompt;
from StepDto import StepDto;

class StepRunner :


    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": sys_prompt
        }
    ];
    client = get_client(get_llm_provider());

    def get_coverted_llm_reply(self, role: str, prompt: str) -> StepDto :

        self.messages.append({
            "role": role,
            "content": prompt
        })
        res = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            max_tokens=4096,
            messages=self.messages,
            response_format={"type": "json_object"}
        );
        raw = res.choices[0].message.content.strip()
        self.messages.append({"role": "assistant", "content": raw})
        step_dto: StepDto = StepDto.model_validate_json(res.choices[0].message.content.strip());
        return step_dto;

    def isAssistant(self, data: StepDto):
        return "THINKING" == data.step;

    def isFinalOutput(self, data: StepDto):
        return "FINAL_OUTPUT" == data.step;

    def run(self) :

        print(f"Please enter a GSM8k problem as prompt: ....");
        user_prompt = input();
        res_step_dto : StepDto = self.get_coverted_llm_reply("user", user_prompt);
        for _ in range(15) :
            if self.isAssistant(res_step_dto) :
                print(res_step_dto)
            if self.isFinalOutput(res_step_dto) :
                print(res_step_dto)
                break;

            parsed_res: StepDto = self.get_coverted_llm_reply("user", res_step_dto.data);
            res_step_dto = parsed_res;

runner : StepRunner = StepRunner();
runner.run();