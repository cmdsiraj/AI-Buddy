from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse,  RedirectResponse
from ..deps import current_user
from ..ai.Agent_main import getResponse
from copy import deepcopy
from ..utils.html_bleach import sanitize_html
from .. import schemas, models, database
from sqlalchemy.orm import Session

home_router = APIRouter()

def _history(request: Request) -> list[dict]:
    return request.session.setdefault("chat_history", [])

def _save_chat(request: Request, history):
     request.session["chat_history"] = history

def _clear_history(request: Request):
    request.session.pop("chat_history", None)


@home_router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request, username: str = Depends(current_user)):
    template = request.app.state.templates
    history = _history(request)
    return template.TemplateResponse(
        "home.html", 
        {
            "request": request, 
            "title": "Chat",
            "history": history
        })

@home_router.post("/chat", response_class=HTMLResponse)
def chat_send(request: Request, message: str = Form(""), username:str = Depends(current_user), db: Session = Depends(database.get_db)):
    history = _history(request)
    msg = message.strip()
    if msg:
        history.append({"role": "user", "content": msg})
        safe_histroy = deepcopy(history)
        config = (
            db.query(models.Config)
            .filter(models.Config.username.in_([username, "system"]))
            .order_by(models.Config.username!=username)
            .first()
            )
        
        reply = getResponse(messages=safe_histroy, config=config, user_name=username)
        history.append({"role": "assistant", "content": reply})
        for msg in history:
            msg["content"] = sanitize_html(msg["content"])
        _save_chat(request, history)
        
    
    return RedirectResponse(url="/home/chat", status_code=303)

@home_router.post("/clear_chat", response_class=HTMLResponse)
def clear_chat(request: Request, username: str = Depends(current_user)):
    _clear_history(request)
    return RedirectResponse("/home/chat", status_code=303)
