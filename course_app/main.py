import fastapi
from fastapi import FastAPI
from api.endpoints import auth, categories, courses, users, lessons, exams, questions, certificates, social_auth
import redis
import uvicorn
from admin.setup import setup_admin
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from contextlib import asynccontextmanager
import redis.asyncio as redis
from starlette.middleware.sessions import SessionMiddleware
from course_app.config import SECRET_KEY


async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding="utf-8", decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()

course_app = fastapi.FastAPI(title='Course site', lifespan=lifespan)
course_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
setup_admin(course_app)

course_app.include_router(auth.auth_router, tags=["Auth"])
course_app.include_router(categories.category_router, tags=["Categories"])
course_app.include_router(courses.course_router, tags=["Courses"])
course_app.include_router(users.user_router, tags=["Users"])
course_app.include_router(lessons.lesson_router, tags=["Lessons"])
course_app.include_router(exams.exam_router, tags=["Exams"])
course_app.include_router(questions.question_router, tags=["Questions"])
course_app.include_router(certificates.certificate_router, tags=["Certificates"])
course_app.include_router(social_auth.social_router)



# def verify_password(plain_password, hashed_password):
#     return password_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return password_context.hash(password)


if __name__ == "__main__":
    uvicorn.run(course_app, host="127.0.0.1", port=8001)