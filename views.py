from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from app.configs import Config
from app.utilities.session import Session
from app.utilities.check_login import check_login
from app.models.test import TestModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="/app/templates")
config = Config()
session = Session(config)

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def index(request: Request):
    """
    トップページを返す
    :param request: Request object
    :return:
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signup")
def signup(request: Request, username: str = Form(...), password: str = Form(...)):  
    test_model = TestModel(config)
    existed_sameuser = test_model.fetch_user_by_name(username)
    if existed_sameuser:
        return templates.TemplateResponse("index.html", {"request": request, "error": "すでに同じ名前の利用者がいます"})
    test_model.signup(username, password)
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    ログイン処理
    :param request:
    :param username:
    :param password:
    :return:
    """
    test_model = TestModel(config)
    [result, user] = test_model.login(username, password)
    if not result:
        # ユーザが存在しなければトップページへ戻す
        return templates.TemplateResponse("index.html", {"request": request, "error": "ユーザ名またはパスワードが間違っています"})
    response = RedirectResponse(url="/nextpage", status_code=HTTP_302_FOUND)
    session_id = session.set("user", user)
    response.set_cookie("session_id", session_id)
    return response

@app.get("/nextpage")
# check_loginデコレータをつけるとログインしていないユーザをリダイレクトできる
@check_login
def netxtpage(request: Request, session_id=Cookie(default=None)):
    user = session.get(session_id).get("user")
    return templates.TemplateResponse("nextpage.html", {
        "request": request,
        "user": user
    })

# @app.get("/profile")


@app.get("/nextnextpage")
# check_loginデコレータをつけるとログインしていないユーザをリダイレクトできる
@check_login
def nextnextpage(request: Request, session_id=Cookie(default=None)):
    user = session.get(session_id).get("user")
    return templates.TemplateResponse("nextnextpage.html", {
        "request": request,
        "user": user
    })


@app.get("/logout")
@check_login
def logout(session_id=Cookie(default=None)):
    session.destroy(session_id)
    response = RedirectResponse(url="/")
    response.delete_cookie("session_id")
    return response

#  @app.post("/profile")
# def signup(request: Request, username: str = Form(...), nation: str = Form(...), favClub: str = Form(...), favLeague: str = Form(...), favPlayer: str = Form(...)):  
#     test_model = TestModel(config)
#     test_model.signup(username, password)
#     return templates.TemplateResponse("nextpage.html", {
#         "request": request,
#         "userdata": userdata
#     })
