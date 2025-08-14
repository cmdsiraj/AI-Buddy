from abc import ABC, abstractmethod

class LLM(ABC):

    @property
    @abstractmethod
    def model_name() -> str:
        pass

    @abstractmethod
    def chat(messages):
        pass