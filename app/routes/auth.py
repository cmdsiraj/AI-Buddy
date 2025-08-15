from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from .. import schemas, database, models
from ..utils.auth_utils import create_access_token, create_refresh_token
from sqlalchemy.orm import Session


auth_router = APIRouter()


@auth_router.get("/login", name="login_get", response_class=HTMLResponse)
def login(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return RedirectResponse("/home/chat", status_code=303)
    templates = request.app.state.templates
    return templates.TemplateResponse("login_signup.html", {"request": request, "title": "Login", "errors": {}, "values": {}, "showSignup": True, "action": "/auth/login"})

@auth_router.get("/signup",name="signup_get", response_class=HTMLResponse)
def signup(request: Request):
    token = request.cookies.get("access_token")
    if token:
        return RedirectResponse("/home/chat", status_code=303)
    templates = request.app.state.templates
    return templates.TemplateResponse("login_signup.html", {"request": request, "title": "Signup", "errors": {}, "values": {}, "showSignup": False, "action": "/auth/signup"})

@auth_router.post("/signup", name="signup_post" ,response_class=HTMLResponse)
def login(request: Request, username: str = Form(""), password: str = Form(""), db: Session = Depends(database.get_db)):
    templates = request.app.state.templates

    try:
        form_data = schemas.LoginForm(username=username, password=password)
    
    except ValidationError as e:
        
        errors = {err["loc"][0]: err["msg"] for err in e.errors()}
        return templates.TemplateResponse(
            "login_signup.html", 
            {
                "request": request, 
                "errors": errors, 
                "title": "Signup",
                "values": 
                {
                    "username": username, 
                    "password": password
                },
                "showSignup": False,
                "action": "/auth/signup"
            }, 
            status_code=400)
    
    db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if db_user:
        return templates.TemplateResponse(
            "login_signup.html", 
            {
                "request": request, 
                "errors": {"username": "User Name already exist, please choose other."}, 
                "title": "Signup",
                "values": 
                {
                    "username": username, 
                    "password": password
                },
                "showSignup": False,
                "action": "/auth/signup"
            }, 
            status_code=400)
    
    new_user = models.User(username=form_data.username, password=form_data.password)
    if not db_user:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    return RedirectResponse("/auth/login", status_code=303)

@auth_router.post("/login", name="login_post", response_class=HTMLResponse)
def login(request: Request, username: str = Form(""), password: str = Form(""), db: Session = Depends(database.get_db)):
    templates = request.app.state.templates

    try:
        form_data = schemas.LoginForm(username=username, password=password)

    except ValidationError as e:
        errors = {err["loc"][0]: err["msg"] for err in e.errors()}
        return templates.TemplateResponse(
            "login_signup.html", 
            {
                "request": request, 
                "errors": errors, 
                "title": "Login",
                "values": 
                {
                    "username": username, 
                    "password": password
                },
                "showSignup": True,
                "action": "/auth/login"
            }, 
            status_code=400)
    db_user = db.query(models.User).filter(
                models.User.username == form_data.username,
                models.User.password == form_data.password
        ).first()
    if db_user:
        access = create_access_token(sub=form_data.username)
        refresh = create_refresh_token(sub=username)
        
        resp = RedirectResponse(url="/home/chat", status_code=303)
        cookie_kwargs = dict(httponly=True, secure=False, samesite="lax", path="/")
        resp.set_cookie("access_token", access, **cookie_kwargs, max_age=15*60)
        resp.set_cookie("refresh_token", refresh, **cookie_kwargs, max_age=14*24*60*60)
        return resp
    else:
         return templates.TemplateResponse(
            "login_signup.html", 
            {
                "request": request, 
                "errors": {"password": "Incorrect User Name or Password"}, 
                "title": "Login",
                "values": 
                {
                    "username": username, 
                    "password": password
                },
                "showSignup": True,
                "action": "/auth/login"
            }, 
            status_code=400)
    
@auth_router.post("/logout", name="logout")
def logout(request: Request):
    request.session.clear()
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie("access_token", path='/')
    resp.delete_cookie("refresh_token", path="/")
    return resp