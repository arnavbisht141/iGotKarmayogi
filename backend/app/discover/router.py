import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Course, SearchHistory

router = APIRouter(prefix="/discover", tags=["discover"])

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

    # Get categories list
    all_categories = [c[0] for c in db.query(Course.category).distinct().all() if c[0]]

    # Trending search keywords
    trending_searches = [
        "National Sample Survey", "Consumer Price Index", "CAPI Field Validation",
        "UN-NQAF Data Quality", "Treasury Single Account PFMS", "Python Microdata Analysis"
    ]

    # User's recent searches
    user_recent_searches = []
    if current_user:
        history = (
            db.query(SearchHistory.query)
            .filter(SearchHistory.user_id == current_user.id)
            .order_by(SearchHistory.searched_at.desc())
            .distinct()
            .limit(5)
            .all()
        )
        user_recent_searches = [h[0] for h in history]

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
                "modules_count": len(c.modules),
                "has_assessment": c.assessment is not None
            }
            for c in courses
        ],
        "categories": all_categories,
        "trending_searches": trending_searches,
        "user_recent_searches": user_recent_searches
    }
