from rich import print

def log_tool_action(label, detail, emoji="🔧", color="yellow"):
    print(f"[bold {color}]{emoji} {label}[/] [dim]{detail}[/]")


def log_agent_response(model_name, response, color="green", emoji="🤖"):
    print(f"\n[bold {color}]{emoji} Agent ({model_name}):[/] {response}\n")

def log_message(message, emoji="memo", color="cyan"):
    print(f":{emoji}: [{color}]{message}[/{color}]")
