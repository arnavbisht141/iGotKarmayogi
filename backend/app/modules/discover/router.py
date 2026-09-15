import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Course, SearchHistory, Module, Assessment

router = APIRouter(prefix="/discover", tags=["discover"])

RECENT_SEARCH_LIMIT = 5


@router.get("/courses")
def search_and_discover_courses(
    q: Optional[str] = Query(None, description="Search keyword"),
    category: Optional[str] = Query(None, description="Category filter"),
    difficulty: Optional[str] = Query(None, description="beginner, intermediate, advanced"),
    source: Optional[str] = Query(None, description="internal or external"),
    sort: Optional[str] = Query("popular", description="popular, new, rating, duration"),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Course)

    # 1. Keyword search
    if q and q.strip():
        search_str = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Course.title.ilike(search_str),
                Course.overview.ilike(search_str),
                Course.instructor.ilike(search_str),
                Course.organization.ilike(search_str),
                Course.category.ilike(search_str)
            )
        )
        # Record search history if user is logged in
        if current_user:
            sh = SearchHistory(user_id=current_user.id, query=q.strip())
            db.add(sh)
            db.commit()

    # 2. Filters
    if category and category.lower() != "all":
        if category.lower() == "popular":
            query = query.filter(Course.is_popular == True)
        elif category.lower() == "new":
            query = query.filter(Course.is_new == True)
        else:
            query = query.filter(Course.category.ilike(f"%{category}%"))

    if difficulty and difficulty.lower() != "all":
        query = query.filter(Course.difficulty == difficulty.lower())

    if source and source.lower() != "all":
        query = query.filter(Course.source == source.lower())

    # 3. Sorting
    if sort == "new":
        query = query.order_by(Course.created_at.desc())
    elif sort == "rating":
        query = query.order_by(Course.rating.desc())
    elif sort == "duration":
        query = query.order_by(Course.duration_hours.asc())
    else:  # popular
        query = query.order_by(Course.enrolled_count.desc())

    courses = query.all()

    # Counted in two grouped queries rather than lazy-loading per course (a round trip each on hosted Postgres)
    modules_per_course = dict(db.query(Module.course_id, func.count(Module.id)).group_by(Module.course_id).all())
    courses_with_assessment = {row[0] for row in db.query(Assessment.course_id).all()}

    # Get categories list
    all_categories = [c[0] for c in db.query(Course.category).distinct().all() if c[0]]

    # Trending search keywords
    trending_searches = [
        "National Sample Survey", "Consumer Price Index", "CAPI Field Validation",
        "UN-NQAF Data Quality", "Treasury Single Account PFMS", "Python Microdata Analysis"
    ]

    # User's recent distinct searches, newest first. Deduplicated in Python: Postgres rejects
    # SELECT DISTINCT combined with ORDER BY on a column that is not selected.
    user_recent_searches = []
    if current_user:
        history = (
            db.query(SearchHistory.query)
            .filter(SearchHistory.user_id == current_user.id)
            .order_by(SearchHistory.searched_at.desc())
            .limit(50)
            .all()
        )
        for (search_query,) in history:
            if search_query not in user_recent_searches:
                user_recent_searches.append(search_query)
            if len(user_recent_searches) == RECENT_SEARCH_LIMIT:
                break

    return {
        "total_results": len(courses),
        "courses": [
            {
                "id": c.id,
                "title": c.title,
                "overview": c.overview,
                "instructor": c.instructor,
                "organization": c.organization,
                "duration_hours": c.duration_hours,
                "difficulty": c.difficulty,
                "source": c.source,
                "category": c.category,
                "rating": c.rating,
                "enrolled_count": c.enrolled_count,
                "is_popular": c.is_popular,
                "is_new": c.is_new,
                "modules_count": modules_per_course.get(c.id, 0),
                "has_assessment": c.id in courses_with_assessment
            }
            for c in courses
        ],
        "categories": all_categories,
        "trending_searches": trending_searches,
        "user_recent_searches": user_recent_searches
    }
