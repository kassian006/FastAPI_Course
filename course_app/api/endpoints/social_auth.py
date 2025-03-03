from sqlalchemy.orm import Session
from course_app.db.database import SessionLocal
from fastapi import APIRouter, Depends
from starlette.requests import Request
from course_app.config import setting
from authlib.integrations.starlette_client import OAuth

social_router = APIRouter(prefix="/oauth", tags=["Social_Auth"])

oauth = OAuth()
oauth.register(
    name="github",
    client_id=setting.GITHUB_CLIENT_ID,
    client_secret=setting.GITHUB_SECRET_KEY,
    authorize_url="https://github.com/login/oauth/authorize",
)

oauth.register(
    name="google",
    client_id=setting.GOOGLE_CLIENT_ID,
    client_secret=setting.GOOGLE_SECRET_KEY,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid email profile"},
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@social_router.get("/github/")
async def github_login(request: Request):
    return await oauth.github.authorize_redirect(request, setting.GITHUB_URL)


@social_router.get("/google/")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(request, setting.GOOGLE_URL)
