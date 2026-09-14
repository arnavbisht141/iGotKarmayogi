import json
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models.models import BehaviouralSessionResult


def save_behavioural_result(
    db: Session,
    *,
    session_id: str,
    session_type: str,
    user_id: Optional[int],
    case_or_course_id: Optional[str],
    score: float,
    result_payload: Dict[str, Any],
) -> None:
    row = db.query(BehaviouralSessionResult).filter_by(session_id=session_id).first()
    if row:
        row.score = score
        row.result_json = json.dumps(result_payload)
        row.user_id = user_id
        row.case_or_course_id = case_or_course_id
    else:
        row = BehaviouralSessionResult(
            session_id=session_id,
            session_type=session_type,
            user_id=user_id,
            case_or_course_id=case_or_course_id,
            score=score,
            result_json=json.dumps(result_payload),
        )
        db.add(row)
    db.commit()
