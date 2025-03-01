"""empty message

Revision ID: 2eb783852f7e
Revises: 
Create Date: 2025-02-15 18:05:29.665141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2eb783852f7e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_category_name'), 'categories', ['category_name'], unique=True)
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_table('user_profiles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=40), nullable=False),
    sa.Column('last_name', sa.String(length=40), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('profile_picture', sa.String(), nullable=True),
    sa.Column('role', sa.Enum('teacher', 'student', name='userrole'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('level', sa.Enum('level1', 'level2', 'level3', name='statuscourse'), nullable=False),
    sa.Column('price', sa.DECIMAL(precision=8, scale=2), nullable=False),
    sa.Column('type_course', sa.Enum('type1', 'type2', name='typecourse'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_course_name'), 'courses', ['course_name'], unique=False)
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    op.create_table('certificates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('issued_at', sa.DateTime(), nullable=False),
    sa.Column('certificate_url', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['user_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_certificates_id'), 'certificates', ['id'], unique=False)
    op.create_table('exams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('end_time', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exams_id'), 'exams', ['id'], unique=False)
    op.create_index(op.f('ix_exams_title'), 'exams', ['title'], unique=False)
    op.create_table('lessons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('video_url', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lessons_id'), 'lessons', ['id'], unique=False)
    op.create_index(op.f('ix_lessons_title'), 'lessons', ['title'], unique=False)
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exam_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exam_id'], ['exams.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)
    op.create_index(op.f('ix_questions_title'), 'questions', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_questions_title'), table_name='questions')
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_table('questions')
    op.drop_index(op.f('ix_lessons_title'), table_name='lessons')
    op.drop_index(op.f('ix_lessons_id'), table_name='lessons')
    op.drop_table('lessons')
    op.drop_index(op.f('ix_exams_title'), table_name='exams')
    op.drop_index(op.f('ix_exams_id'), table_name='exams')
    op.drop_table('exams')
    op.drop_index(op.f('ix_certificates_id'), table_name='certificates')
    op.drop_table('certificates')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_index(op.f('ix_courses_course_name'), table_name='courses')
    op.drop_table('courses')
    op.drop_table('user_profiles')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_index(op.f('ix_categories_category_name'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
