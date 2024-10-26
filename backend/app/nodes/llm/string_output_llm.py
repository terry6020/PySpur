from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel
from .llm_utils import create_messages, generate_text
from ..base import BaseNode
from pydantic import BaseModel
from enum import Enum


class ModelName(str, Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"
    O1_PREVIEW = "o1-preview"
    O1_MINI = "o1-mini"
    GPT_4_TURBO = "gpt-4-turbo"


class StringOutputLLMNodeConfig(BaseModel):
    llm_name: ModelName
    max_tokens: int
    temperature: float
    system_prompt: str
    json_mode: bool = False
    few_shot_examples: Optional[List[Dict[str, str]]] = None


class StringOutputLLMNodeInput(BaseModel):
    user_message: str


class StringOutputLLMNodeOutput(BaseModel):
    assistant_message: str


class StringOutputLLMNode(BaseNode):
    """
    Basic node type for calling an LLM.
    """

    name = "string_output_llm_node"
    config_model = StringOutputLLMNodeConfig
    input_model = StringOutputLLMNodeInput
    output_model = StringOutputLLMNodeOutput

    def setup(self) -> None:
        pass

    async def run(self, input_data: StringOutputLLMNodeInput) -> StringOutputLLMNodeOutput:
        system_message = self.config.system_prompt
        messages = create_messages(
            system_message=system_message,
            user_message=input_data.user_message,
            few_shot_examples=self.config.few_shot_examples,  # Pass examples here
        )
        assistant_message = await generate_text(
            messages=messages,
            model_name=self.config.llm_name,
            temperature=self.config.temperature,
            json_mode=self.config.json_mode,
        )
        return StringOutputLLMNodeOutput(assistant_message=assistant_message)


if __name__ == "__main__":
    async def test_llm_nodes():
        string_output_llm_node = StringOutputLLMNode(
            config=StringOutputLLMNodeConfig(
                llm_name=ModelName.GPT_4O_MINI,
                max_tokens=32,
                temperature=0.1,
                json_mode=False,
                system_prompt="This is a test prompt.",
            )
        )
        basic_input = StringOutputLLMNodeInput(user_message="This is a test message.")
        basic_output = await string_output_llm_node(basic_input)
        print(basic_output)
        print("-" * 50)

    import asyncio

    asyncio.run(test_llm_nodes())