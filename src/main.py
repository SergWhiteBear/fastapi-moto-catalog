from fastapi import FastAPI, Request, Depends, HTTPExceptionfrom fastapi.responses import HTMLResponsefrom fastapi.staticfiles import StaticFilesfrom fastapi.templating import Jinja2Templatesfrom fastapi.middleware.cors import CORSMiddlewarefrom sqlalchemy.ext.asyncio import AsyncSessionfrom src.database import get_async_sessionfrom src.moto.router import get_motofrom src.moto.router import router as moto_routerfrom src.user.base_config import fastapi_users, auth_backendfrom src.user.schemas import UserRead, UserCreatefrom .exceptions import (    db_connection_exception_handler,    sqlalchemy_exception_handler, http_exception_handler)from sqlalchemy.exc import SQLAlchemyErrorapp = FastAPI(    title="BuyMoto",)app.add_middleware(    CORSMiddleware,    allow_origins=["*"],  # Разрешить все источники, можно заменить на конкретный домен    allow_credentials=True,    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)    allow_headers=["*"],  # Разрешить любые заголовки)# Подключение статических файловapp.mount("/static", StaticFiles(directory="static"), name="static")app.mount('/js', StaticFiles(directory='js'), name='js')# Шаблоны (HTML файлы)templates = Jinja2Templates(directory="templates")app.include_router(    fastapi_users.get_auth_router(auth_backend),    prefix="/user",    tags=["Auth"],)app.include_router(    fastapi_users.get_register_router(UserRead, UserCreate),    prefix="/user",    tags=["Auth"],)@app.get("/", response_class=HTMLResponse)async def read_root(request: Request):    return templates.TemplateResponse("catalog.html", {"request": request})@app.get("/profile", response_class=HTMLResponse)async def read_profile(request: Request):    return templates.TemplateResponse("profile.html", {"request": request})@app.get("/about/{name_moto}", response_class=HTMLResponse)async def read_moto(request: Request, name_moto: str, session: AsyncSession = Depends(get_async_session)):    moto_data = await get_moto(name_moto, session)    return templates.TemplateResponse("about.html", {"request": request, "moto": moto_data["moto"]})app.add_exception_handler(OSError, db_connection_exception_handler)app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)app.add_exception_handler(HTTPException, http_exception_handler)app.include_router(moto_router)