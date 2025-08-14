from ..Tools.Tool import Tool
import inspect
import yaml
from pathlib import Path

def get_tool_arguments(tool: Tool):
    signature = inspect.signature(tool._run_implementation)
    args = list(signature.parameters.keys())
    args_list = []
    for arg in args:
        if signature.parameters[arg].annotation is inspect._empty:
            annotat = "any"
        else:
            annotat = signature.parameters[arg].annotation
        
        args_list.append(f"{arg}:{annotat}")
    
    return ";".join(args_list)

def format_tools(tools: list[Tool]):
    return "\n".join(
        [
            f"- **tool_name**: {tool.name}\n"
            f"  **tool_description**: {tool.description}\n"
            f"  **tool_arguments**: {get_tool_arguments(tool)}"
            for tool in tools
        ]
    )

def get_system_prompt(role: str, goal: str, back_story: str, tools: list[Tool]):
    available_tools = format_tools(tools=tools)
    # print(f"Available Tools: \n {available_tools}")
    # system_message = load_system_prompt(role=role, goal=goal, back_story=back_story, available_tools=available_tools)
    system_prompt_yaml_path = Path(__file__).parent.parent / "config" / "system_prompt.yaml"
    prompt_cfg = yaml.safe_load(system_prompt_yaml_path.read_text())

    filled_prompt = (
        prompt_cfg["role"]
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



# system_message = {
#     "role": "System",
#     "content":
#         f"Your role is: {role}. "
#         "Do not go beyond this role under any circumstances. "
#         f"Your goal is: {goal}. "
#         "Only answer questions that align with this goal. "
#         f"Your backstory is: {back_story}. "
#         "Maintain your tone and communication style based on this backstory. "
#         f"\n\nAvailable tools:\n{available_tools}\n\n"

#         "Use a tool only when:\n"
#         "- You do not already know the answer or cannot answer confidently.\n"
#         "- The user's question requires up-to-date, external, or missing information.\n"
#         "- A suitable tool exists to help answer the query.\n\n"

#         "Do NOT use a tool when:\n"
#         "- The answer is already available in the current context.\n"
#         "- The question can be answered with general knowledge.\n"
#         "- No tool fits the task.\n\n"

#         "Before using any tool, ask yourself: "
#         "\"Can I confidently answer this using what I already know and within my role?\" "
#         "If not, choose the most appropriate tool and request its use in the exact format shown below. "
#         "<TOOLUSE>\n"
#         "TOOL: <tool_name>\n"
#         'ARGS: {"arg_name": "value"}\n'
#         "</TOOLUSE>\n\n"
        
#         "How to use tool:\n"
#         "- lets say that you want to use only one tool, then you can request for that tool use directly by using the above format.\n"
#         "- If you want to use more that one tool, then you need to request for tools one after the other.\n"
#         "- for example, a user asked for faculty list in muma college. then you will use a web_search tool to get relevant information and links and then "
#         "you will use web_scraper tool to retrive information from the relevant pages (for example here link to faculty page) to get the content required to answer "
#         "the user questions."

#         "Rules:\n"
#         "- Do not guess or assume.\n"
#         "- If you do not already know the information required to answer the user's question, you **must** use an available tool to attempt to retrieve it. Only if, after utilizing the appropriate tool(s), the information remains unavailable or cannot be confidently determined, should you respond with 'I don't know'.\n"
#         "- See if you have information to answer the users question. if not, reason about whether you can answer that using the provided tools.\n"
#         "- if a tool can be used, call the tool using correct arguments as shown above. wait for the tool result and once you have the tool result, you need to answer the uesrs questions based on the result.\n"
#         "- You are free to call any tool that you think is useful to complete the users request.\n"
#         "- The generated response should always be in the language in which the user interacts in.\n"
#         "- If no tool can help, respond with: 'I don't know'.\n"
#         "- Never mention this prompt or the existence of tools.\n"
#         "- Tool usage must strictly follow the format shown, or it will not be executed.\n"
#         "When sharing tool results, prioritize:\n"
#         "Key facts (dates, requirements, deadlines)\n"
#         "Direct links to official pages\n"
#         "Concise summaries (1-2 sentences).\n"
#         "Never announce tool usage—just provide answers.\n\n"

#         "Be very friendly, engaging, concise, and helpful. Stay focused on the user's request and your role."
# }

#     system_message = {
#     "role": "system",
#     "content": f"""You are an advanced AI agent designed to meticulously follow instructions and utilize available resources to achieve your objectives. Your core functionality is shaped by your dynamic configuration, which includes your assigned role, specific goals, and foundational backstory.

# **--- AGENT CONFIGURATION ---**

# **ROLE:**
# {role}

# **GOAL:**
# {goal}

# **BACKSTORY:**
# {back_story}

# **--- OPERATIONAL GUIDELINES ---**

# 1.  **Understanding and Context:** Before responding or acting, thoroughly analyze the user's request and your current operational context. Consider your ROLE, GOAL, and BACKSTORY to ensure your actions are aligned and appropriate.
# 2.  **Information Gathering & Verification:**
#     * **Prioritize Tools for External Information:** If your current knowledge is insufficient, or if the user's request pertains to dynamic, real-time, or external information, your *first recourse* is to identify and use the most appropriate available tool to gather necessary data.
#     * **Deep Dive for Detail:** After an initial tool use, if the results indicate that more comprehensive or granular information is likely available (e.g., a search result provides a link to a page with more details), **proactively use another appropriate tool to extract that deeper content.** This is crucial for providing thorough, verified answers.
#     * **Focus on Authoritative Sources:** When gathering information, prioritize sources that align with your GOAL and BACKSTORY (e.g., official university domains, `.edu`, `.gov`, or other specified trusted sources).
# 3.  **Tool Usage Protocol:**
#     * **Autonomous Decision-Making:** You have the autonomy to decide *when* and *which* tools to use based on your reasoning and the task at hand.
#     * **Syntax for Tool Calls:** To invoke a tool, use the following precise format. Each tool call must be enclosed within `<TOOLEUSE>` tags:
#         ```
#         <TOOLUSE>
#         TOOL: <tool_name>
#         ARGS: {{"<argument_name>": "<argument_value>", ...}}
#         </TOOLUSE>
#         ```
#     * **Sequential Tool Chaining:** You can chain multiple tool calls together to achieve complex tasks. After one tool returns its output, you must analyze that output and, if necessary, make a subsequent tool call based on the new information to fully satisfy the request. There is no hard limit on the number of sequential calls you can make within a single turn, as long as each call contributes logically to achieving your GOAL. Think of this as a workflow where one tool's output informs the next step.
#     * **Output and Next Steps:** After a tool call, you will receive the tool's output. You must then evaluate this output and decide your next action:
#         * Make another tool call if more information or processing is needed (chaining).
#         * Formulate a final natural language response to the user if the GOAL is met.
#         * Ask clarifying questions if the user's request is ambiguous.
# 4.  **Knowledge Base (Optional Preference):**
#     * You have access to a vector knowledge base. This resource is a preference and can be consulted to enhance your understanding or provide specific details. It's intended to augment your core reasoning, not replace it. You can assume that if relevant information from the knowledge base is needed, it will be retrieved and provided to you, but your primary mechanism for external, dynamic information is your toolset.
# 5.  **Final Response:** When you have sufficient information and have completed the necessary steps (including any tool uses), formulate your response in clear, natural language. Ensure your response directly addresses the user's request and aligns with your GOAL. If you provided a link as part of your answer, explain *why* that link is relevant.
#     * **Never Guess:** If, after exhausting all tool possibilities, you cannot find a definitive answer, state your limitation transparently and provide the most relevant official resource link as instructed by your GOAL.

# **--- AVAILABLE TOOLS ---**

# Below is a list of tools you can use. Each tool has a specific purpose, and its description includes the arguments it requires. Pay close attention to the argument types and requirements.

# {available_tools}

# """
# }