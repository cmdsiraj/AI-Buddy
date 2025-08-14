from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from .. import schemas, database, deps, models
from sqlalchemy.orm import Session
from ..utils.history_utils import _clear_history

config_router = APIRouter()

# name: str = Form(""), role: str = Form(""), goal: str = Form(""), backstory: str = Form("")

@config_router.get("", response_class=HTMLResponse)
def config(request: Request, username: str = Depends(deps.current_user), db: Session = Depends(database.get_db)):
    templates = request.app.state.templates
    config = (
            db.query(models.Config)
            .filter(models.Config.username.in_([username, "system"]))
            .order_by(models.Config.username!=username)
            .first()
            )
    if config:
        values = {
            "name": config.name, 
            "role": config.role, 
            "goal": config.goal, 
            "backstory": config.back_story
            }
    else:
        values = {}
    return templates.TemplateResponse("config.html", {"request": request, "title": "AgentConfig", "values": values, "errors": {}})


@config_router.post("/save", response_class=HTMLResponse)
def config(request: Request, 
           name: str = Form(""), 
           role: str = Form(""), 
           goal: str = Form(""), 
           backstory: str = Form(""),
           username: str = Depends(deps.current_user),
           db: Session = Depends(database.get_db)
           ):
    templates = request.app.state.templates
    try:
        form_data = schemas.AgentConfig(name=name, role=role, goal=goal, back_story=backstory)
    except ValidationError as e:
        errors = {err["loc"][0]:err["msg"] for err in e.errors() }
        return templates.TemplateResponse(
            "config.html", 
            {
                "request": request, 
                "title": 'AgentConfig', 
                "errors": errors, 
                "values": {
                    "name": name, 
                    "role": role,
                    "goal": goal,
                    "backstory": backstory
                }
            })

    config = db.query(models.Config).filter(models.Config.username == username).first()
    if config:
        config.name = form_data.name
        config.role = form_data.role
        config.goal = form_data.goal
        config.back_story = form_data.back_story
    else:
        config = models.Config(
            username=username,
            name=form_data.name,
            role=form_data.role,
            goal=form_data.goal,
            back_story=form_data.back_story
        )
        db.add(config)
    db.commit()
    db.refresh(config)

    _clear_history(request)

    return RedirectResponse("/config", status_code=303)
