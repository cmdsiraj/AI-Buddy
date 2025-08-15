from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse,  RedirectResponse
from ..deps import current_user
from ..ai.Agent_main import getResponse
from copy import deepcopy
from ..utils.html_bleach import sanitize_html
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..utils.history_utils import _clear_history, _history, _save_chat

home_router = APIRouter()




@home_router.get("/chat", name="chat_get", response_class=HTMLResponse)
def chat_page(request: Request, username: str = Depends(current_user), db: Session = Depends(database.get_db)):
    template = request.app.state.templates
    history = _history(db, username)
    config = (
        db.query(models.Config.name)
        .filter(models.Config.username.in_([username, "system"]))
        .order_by(models.Config.username!=username)
        .first()
        )
    return template.TemplateResponse(
        "home.html", 
        {
            "request": request, 
            "title": "Chat",
            "history": history,
            "agent_name": config.name,
            "user_name": username
        })

@home_router.post("/chat", name="chat_post", response_class=HTMLResponse)
def chat_send(request: Request, message: str = Form(""), username:str = Depends(current_user), db: Session = Depends(database.get_db)):
    history = _history(db, username)
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
        
        reply = getResponse(messages=safe_histroy, config=config)
        reply = reply.replace("{{user_name}}", username)
        history.append({"role": "assistant", "content": sanitize_html(reply)})
      
        _save_chat(db,username, history)
        
    
    return RedirectResponse(url="/home/chat", status_code=303)

@home_router.post("/clear_chat", name="clear_chat", response_class=HTMLResponse)
def clear_chat(request: Request, username: str = Depends(current_user), db: Session = Depends(database.get_db)):
    
    _clear_history(db, username)
   
    return RedirectResponse("/home/chat", status_code=303)
