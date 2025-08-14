from abc import ABC, abstractmethod

class Knowledge(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass


    @abstractmethod
    def get_content(self) -> str:
        pass