import os
from dotenv import load_dotenv
from ..LLM.LLMBase import LLM
from groq import Groq


class GroqLLM(LLM):

    def __init__(self, model_name: str = "allam-2-7b", api_key:str=None):
        self.__model_name = model_name
        try:
            if api_key is None:
                load_dotenv()
                api_key = os.getenv("GROQ_API_KEY")
            
            self.__client = Groq(api_key=api_key)
        except Exception as e:
            print("Error while connecting to google client\n")
            print(e)
        
    def model_name(self):
        return self.__model_name
    
    def __reformate_prompt(self, messages):
        for message in messages:
            if message["role"] == "tool assistant":
                message["role"] = "assistant"
        
        return messages

    
    def chat(self, messages):
        prompt = self.__reformate_prompt(messages=messages)
        # print(f"\n\n{prompt}\n\n")
        response = self.__client.chat.completions.create(messages=prompt, model=self.__model_name)

        return response.choices[0].message.content