from abc import ABC, abstractmethod
from ..utils.print_utils import log_tool_action
import json

class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def _run_implementation(self, **kwargs):
        pass

    
    def run(self, **kwargs):
        result = self._run_implementation(**kwargs)
        # log_message = f"Tool '{self.name}' - Description: '{self.description}' - called with args:\n{kwargs}\n\n"
        # with open("logs/tool_calls.txt", "+a") as f:
        #     f.write(f"-"*20+"\n",)
        #     f.write(log_message)
        return result