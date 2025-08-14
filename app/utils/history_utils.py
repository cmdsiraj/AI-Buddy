from fastapi import Request

def _history(request: Request) -> list[dict]:
    return request.session.setdefault("chat_history", [])

def _save_chat(request: Request, history):
     request.session["chat_history"] = history

def _clear_history(request: Request):
    request.session["chat_history"] = []