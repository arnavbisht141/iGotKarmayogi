import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="learner")  # "learner" or "admin"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    assessment_attempts = relationship("AssessmentAttempt", back_populates="user", cascade="all, delete-orphan")
    planned_courses = relationship("PlannedCourse", back_populates="user", cascade="all, delete-orphan")
    learning_history = relationship("LearningHistory", back_populates="user", cascade="all, delete-orphan")
    search_history = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    phone = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Onboarding step 3: Education / Work Experience / Previous Training
    education = Column(String(255), nullable=True)
    work_experience_years = Column(Integer, default=0)
    prior_training = Column(Text, nullable=True)
    
    # Onboarding step 4: Designation / Department / Job Role
    designation = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    job_role = Column(String(255), nullable=True)
    
    # Onboarding step 5: Current Assignment / Areas of Interest
    current_assignment = Column(Text, nullable=True)
    areas_of_interest = Column(Text, nullable=True)  # Comma-separated or JSON string
    
    language_pref = Column(String(20), default="en")  # "en" or "hi"
    appearance_pref = Column(String(20), default="light")  # "light" or "dark"
    profile_pic_url = Column(String(500), nullable=True)
    onboarding_completed = Column(Boolean, default=False)
    
    daily_goal_minutes = Column(Integer, default=30)
    current_streak_days = Column(Integer, default=1)
    last_active_date = Column(DateTime, default=datetime.datetime.utcnow)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    overview = Column(Text, nullable=False)
    instructor = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=False)  # e.g., MoSPI, CSO, ISTM
    duration_hours = Column(Float, default=4.0)
    difficulty = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    source = Column(String(50), default="internal")  # internal, external
    category = Column(String(100), default="General", index=True)
    thumbnail_url = Column(String(500), nullable=True)
    rating = Column(Float, default=4.8)
    enrolled_count = Column(Integer, default=0)
    is_popular = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan", order_by="Module.order")
    course_skills = relationship("CourseSkill", back_populates="course", cascade="all, delete-orphan")
    assessment = relationship("Assessment", back_populates="course", uselist=False, cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=1)

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content_type = Column(String(50), default="reading")  # video, reading, lab
    duration_minutes = Column(Integer, default=15)
    content = Column(Text, nullable=False)  # Markdown text or video transcript
    video_url = Column(String(500), nullable=True)
    
    # In-lesson Practice Activity (per Section 4.3 conflict #4)
    activity_question = Column(Text, nullable=True)
    activity_options_json = Column(Text, nullable=True)  # JSON array of strings
    activity_correct_option = Column(Integer, nullable=True)  # 0-indexed
    activity_explanation = Column(Text, nullable=True)
    
    order = Column(Integer, default=1)

    module = relationship("Module", back_populates="lessons")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    category = Column(String(100), default="Technical")

    course_skills = relationship("CourseSkill", back_populates="skill")
    user_skills = relationship("UserSkill", back_populates="skill")


class CourseSkill(Base):
    __tablename__ = "course_skills"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)

    course = relationship("Course", back_populates="course_skills")
    skill = relationship("Skill", back_populates="course_skills")


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    source_course_id = Column(Integer, ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    acquired_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")
    source_course = relationship("Course")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="in_progress")  # in_progress, completed
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    progress_percent = Column(Float, default=0.0)
    last_lesson_id = Column(Integer, nullable=True)

    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    progress_records = relationship("Progress", back_populates="enrollment", cascade="all, delete-orphan")


class Progress(Base):
    __tablename__ = "progress_records"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False)
    module_id = Column(Integer, nullable=False)
    lesson_id = Column(Integer, nullable=False)
    completed = Column(Boolean, default=True)
    activity_completed = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    enrollment = relationship("Enrollment", back_populates="progress_records")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    time_limit_minutes = Column(Integer, default=30)
    pass_threshold_percent = Column(Float, default=70.0)

    course = relationship("Course", back_populates="assessment")
    questions = relationship("Question", back_populates="assessment", cascade="all, delete-orphan", order_by="Question.order")
    attempts = relationship("AssessmentAttempt", back_populates="assessment", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)  # JSON array of strings
    correct_option_index = Column(Integer, nullable=False)  # 0, 1, 2, 3
    explanation = Column(Text, nullable=True)
    order = Column(Integer, default=1)

    assessment = relationship("Assessment", back_populates="questions")


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    score_percent = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)
    answers_json = Column(Text, nullable=False)  # JSON object {question_id: selected_index}
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="assessment_attempts")
    assessment = relationship("Assessment", back_populates="attempts")


class PlannedCourse(Base):
    __tablename__ = "planned_courses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    planned_for = Column(String(100), nullable=True)  # e.g., "Next Month" or date
    source = Column(String(50), default="self")  # "self" or "admin"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="planned_courses")
    course = relationship("Course")


class LearningHistory(Base):
    __tablename__ = "learning_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    viewed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="learning_history")
    course = relationship("Course")


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    query = Column(String(255), nullable=False)
    searched_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="search_history")
