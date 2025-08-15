# from .LLMAgent.MyAgent.Agent.MyAgent import Agent
from .LLMAgent.MyAgent.Agent.MyAgent import Agent
from .LLMAgent.MyAgent.LLM.GeminiLLM import GeminiLLM
from .LLMAgent.MyAgent.Tools.ScraperTool import ScraperTool
from .LLMAgent.MyAgent.Tools.PdfHandlerTool import PdfHandlerTool
from .LLMAgent.MyAgent.Tools.SerperTool import SerperTool
from .LLMAgent.MyAgent.Tools.ExecutePythonTool import ExecutePythonTool
from .LLMAgent.MyAgent.utils.load_config import load_aget_config
from .. import schemas

from typing import List


CURRENT_NEW_MESSAGE = "[NEW_MESSAGE]"
PREVIOUS_CONVERSATION_MESSAGE = "[PREVIOUS_MESSAGES]"

def getResponse(messages, config: schemas.AgentConfig = None):

    llm = GeminiLLM(model_name="gemini-2.5-flash")
   

    for convo in messages[:-1]:
        convo["content"] = f"{PREVIOUS_CONVERSATION_MESSAGE} {convo['content']}"
    
    messages[-1]["content"] = f"{CURRENT_NEW_MESSAGE} {messages[-1]['content']}"

    if len(messages)>1:
        chat_history = messages[:-1]
    else:
        chat_history = []
    curr_user_message = messages[-1]["content"]
    
    if config:
        role = config.role
        goal = config.goal
        back_story=config.back_story
        name=config.name
    else:
        config = load_aget_config()
        role=config["agent"]["role"]
        goal=config["agent"]["goal"]
        back_story=config["agent"]["back_story"]
        name=config["agent"]["name"]

    model = Agent (
        name=name,
        role=role,
        goal=goal,
        back_story=back_story,
        llm=llm,
        tools=[SerperTool(show_tool_call=True), ScraperTool(show_tool_call=True), PdfHandlerTool(show_tool_call=True)],
        timeout=2,
        chat_history=chat_history,
        max_chat_history=10
    )

    response = model.chat(curr_user_message)

    return response
