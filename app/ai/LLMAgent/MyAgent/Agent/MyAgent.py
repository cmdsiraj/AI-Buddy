import re
import json
import time

from ..VectorDB.VectorDB import VectorDB
from ..Tools.Tool import Tool
from ..utils.load_config import load_system_config
from ..LLM.LLMBase import LLM
from ..LLM.OllamaLLM import OllamaLLM
from ..utils.tool_utils import extract_tools_needed
from ..Exceptions.CustomExceptions import ToolUseExtractionError

from ..utils.print_utils import log_message


class Agent:

    
    
    def __init__(self, 
                 name: str,
                 role: str, 
                 goal: str, 
                 back_story: str, 
                 llm:LLM, 
                 chat_history=[], 
                 tools:list[Tool]=[], 
                 knowledge: list = None, 
                 top_k: int = 3, 
                 max_chat_history:int=20,
                 timeout: int = None):
        self.llm = llm if llm else OllamaLLM(model_name="llama3")
            
        self.chat_history=chat_history
        self.system_prompt=load_system_config(name=name, role=role, goal=goal, back_story=back_story, tools=tools)
        self.tools={tool.name: tool for tool in tools}
        self.__vectorDb = None

        if knowledge:
            self._db = VectorDB(knowledgeFiles=knowledge)
        else:
            self._db = None
        
        self.top_k = top_k

        self.__max_chat_history = max_chat_history
        self.timeout = timeout
        self.MAX_TOOL_ITER = 7

    
    def _run_tool(self, tool_name: str, args: dict):
        try:
            tool = self.tools.get(tool_name)
            if tool:
                # print(f"\nArgs: {args}\n its type {type(args)}")
                return tool.run(**args)
            else:
                return f"{tool_name} not found"
        except Exception as e:
            # print(f"Got exception while running tools (tool_name: {tool_name}): {e}" )
            return f"Got exception while running tools (tool_name: {tool_name}): {e}"

    def _run_tools(self, tools_needed: list[Tool]):
        # print(f"From _run_tools func ******{tools_needed}******", "\n\n")
        try:
            tools_results = []
            for tool in tools_needed:
                # print(f"Running tool: {tool}")
                tool_result = self._run_tool(**tool) # type: ignore
                tools_results.append(f'TOOL RESULT FOR {tool["tool_name"]} : {tool_result}') # type: ignore
            
            return '\n'.join(tools_results)
        except Exception as e:
            print(f"Got exception in _run_tools func: {e}")
            print(f"argument passed: {tool}") # type: ignore
            return f"Got exception in _run_tools func: {e}"
        
    def _sleep(self):
        # print(f"Sending Message to {self.llm.model_name()}:", end=' ') # type: ignore
        for i in range(0, self.timeout):
            # print(f"{i+1}...", end=' ', flush=True)
            time.sleep(1)
        # print()
    

    def __chat__(self, messages):
        prompt = [self.system_prompt] + messages
        self._sleep()
        result = self.llm.chat(messages=prompt) # type: ignore
        return result
        
    def chat(self, user_input):

        reply = ''
        # Retriving required knowledge (if knowledge is setup)
        if self._db:
            context = self._db.get_context(user_input, self.top_k)
            user_input = (
                    "you can use the context to answer the question:\n"
                    f"{context}"
                    f"\nQuestion: {user_input}"
            )
        
        self.chat_history.append({"role": "user", "content":"[Current New Message]" + user_input})

        tool_iter = 0

        while True:
            if tool_iter >= self.MAX_TOOL_ITER:
                log_message(f"Ending the model conversation because it reached maximum tool use in this iteration ({tool_iter})")
                self.chat_history.append({"role": "System", "content": "Use have reached max tool uses in a turn. if you have called a tool repeatedly because of some error, let the user know about it, about why you are unable to use the tool. if you reached this limit without tool repeated calls and just want to use more tools, tell the user about this to, in next iteration you will have your tool calls freed again."})
                reply = self.__chat__(self.chat_history)
                return reply

            reply = self.__chat__(self.chat_history)

            if self.chat_history[-1]["role"] == "user":
                self.chat_history[-1]["content"] = self.chat_history[-1]["content"].replace("[Current New Message]", "[Previous Conversation]")

            try:
                tools_needed = extract_tools_needed(reply)
            except Exception as e:
                tool_iter+=1
                reply = {"role": "system", "content": f"Encountered an error while try to parse the tools information from your previous response (from a tool use request). please check and try again. here is the error message to give you more insight: {e}"}
                log_message(f"Error while Extracting tools needed: {e}")
                continue

            if tools_needed:
                tool_iter += 1
                tools_content = self._run_tools(tools_needed)

                prompt_with_tool_result = (
                    "Use the following content from tools to answer the user's question:\n"
                    f"\n{tools_content}"
                    f"\nuser question (repeating question again along with the tool result.): {user_input}"
                )

                if tool_iter == self.MAX_TOOL_ITER:
                    prompt_with_tool_result += "\nTool usage limit reached for this turn. Please review the current results or errors and provide further instructions. Tools will be available again after your next prompt."

                self.chat_history.append({"role": "assistant", "content": prompt_with_tool_result})

            else:
                self.chat_history.append({"role": "assistant", "content": reply})
                self.chat_history = self.chat_history[-self.__max_chat_history:]
                return reply