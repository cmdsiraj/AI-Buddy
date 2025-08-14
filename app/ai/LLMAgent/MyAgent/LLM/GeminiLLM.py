from ..LLM.LLMBase import LLM
from google import genai
import os
from dotenv import load_dotenv

class GeminiLLM(LLM):

    def __init__(self, model_name: str="gemini-2.0-flash", api_key: str=None):
        self.__model_name = model_name
        try:
            if api_key is None:
                load_dotenv()
                api_key = os.getenv("GEMINI_API_KEY")
            
            self.__client = genai.Client(api_key=api_key)
        except Exception as e:
            print("Error while connecting to google client\n")
            print(e)
    

    def model_name(self) -> str:
        return self.__model_name
    
    def __make_prompt(self, messages):
        prompt=""
        for item in messages:
            prompt += f"{item['role'].capitalize()}: {item['content']}\n"
        
        return prompt
    
    def chat(self, messages):
        prompt = self.__make_prompt(messages)
        response = self.__client.models.generate_content(model=self.__model_name, contents=prompt)

        return response.text
