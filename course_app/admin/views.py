from pydantic_core.core_schema import model_field
from sqladmin import ModelView
from course_app.db.models import UserProfile, Category, Course, Lesson, Exam, Question, Certificate


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.role]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]


class CourseAdmin(ModelView, model=Course):
    column_list = [Course.id, Course.course_name]


class LessonAdmin(ModelView, model=Lesson):
    column_list = [column.name for column in Lesson.__table__.columns]


class ExamAdmin(ModelView, model=Exam):
    column_list = [column.name for column in Exam.__table__.columns]


class QuestionAdmin(ModelView, model=Question):
    column_list = [column.name for column in Question.__table__.columns]


class CertificateAdmin(ModelView, model=Certificate):
    column_list = [column.name for column in Certificate.__table__.columns]
