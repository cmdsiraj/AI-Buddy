from ..LLM.LLMBase import LLM
import ollama


class OllamaLLM(LLM):

    def __init__(self, model_name):
        self.__model_name = model_name
    
    def model_name(self) -> str :
        return self.__model_name
    
    def chat(self, messages):
        try:
            result = ollama.chat(model=self.__model_name, messages=messages)
        except Exception as e:
            print("Error from the model:")
            print(e)
        return result['message']['content']