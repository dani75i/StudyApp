from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=2, max_length=80)
    password: str = Field(min_length=8, max_length=128)
    level: str


class LoginIn(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    first_name: str
    level: str
    role: str


class AnswerIn(BaseModel):
    answer: str


class ProfileIn(BaseModel):
    first_name: str = Field(min_length=2, max_length=80)
    level: str


class WeeklyGoalIn(BaseModel):
    weekly_goal: int = Field(ge=5, le=100)


class AdminChapterIn(BaseModel):
    subject_id: int
    level: str
    title: str = Field(min_length=2, max_length=180)
    summary: str = Field(default='', max_length=2000)
    order_index: int = Field(default=0, ge=0, le=10000)


class AdminLessonIn(BaseModel):
    chapter_id: int
    title: str = Field(min_length=2, max_length=180)
    body: str = Field(min_length=1, max_length=20000)
    order_index: int = Field(default=0, ge=0, le=10000)


class AdminExerciseIn(BaseModel):
    chapter_id: int
    title: str = Field(min_length=2, max_length=180)
    statement: str = Field(min_length=1, max_length=10000)
    exercise_type: str = Field(pattern='^(mcq|text)$')
    options: list[str] = Field(default_factory=list, max_length=12)
    hints: list[str] = Field(default_factory=list, max_length=2)
    steps: list[str] = Field(default_factory=list, max_length=12)
    method: str = Field(default='', max_length=1500)
    correct_answer: str = Field(min_length=1, max_length=3000)
    correction: str = Field(min_length=1, max_length=12000)
    difficulty: int = Field(default=1, ge=1, le=3)
    points: int = Field(default=10, ge=1, le=1000)
    order_index: int = Field(default=0, ge=0, le=10000)
