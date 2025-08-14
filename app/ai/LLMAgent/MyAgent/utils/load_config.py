import yaml
from pathlib import Path
import os
from .tool_utils import format_tools
from ..Tools.Tool import Tool


def load_aget_config() -> dict:
    path = Path(__file__).parent.parent / "config" / "agents.yaml"

    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

def load_system_config(name: str, role: str, goal: str, back_story: str, tools: list[Tool]):
    available_tools = format_tools(tools=tools)
    # print(f"Available Tools: \n {available_tools}")
    # system_message = load_system_prompt(role=role, goal=goal, back_story=back_story, available_tools=available_tools)
    system_prompt_yaml_path = Path(__file__).parent.parent / "config" / "system_prompt.yaml"
    prompt_cfg = yaml.safe_load(system_prompt_yaml_path.read_text())

    filled_prompt = (
        prompt_cfg["role"]
        .replace("{{name}}", name)
        .replace("{{role}}", role)
        .replace("{{goal}}", goal)
        .replace("{{back_story}}", back_story)
        + "\n"
        + prompt_cfg["goal"]
        + "\n"
        + prompt_cfg["available_tools_block"]
        .replace("{{available_tools}}", available_tools)
    )

    system_message = {"role": "system", "content": filled_prompt}

    return system_message



