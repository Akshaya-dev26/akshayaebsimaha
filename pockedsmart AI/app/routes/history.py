import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..dependencies import get_current_user

from ..models import (
    User,
    Recommendation,
)


router = APIRouter(
    tags=["History"]
)


@router.get("/history")
def history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    rows = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == user.id
        )
        .order_by(
            Recommendation.created_at.desc()
        )
        .all()
    )

    return [

        {
            "id": row.id,

            "planner_type":
                row.planner_type,

            "budget":
                row.budget,

            "request":
                json.loads(
                    row.request_json
                ),

            "response":
                json.loads(
                    row.response_json
                ),

            "created_at":
                row.created_at.isoformat(),
        }

        for row in rows
    ]


@router.get(
    "/recommendations-details/{recommendation_id}"
)
def recommendation_details(
    recommendation_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    row = (
        db.query(Recommendation)
        .filter(
            Recommendation.id
            == recommendation_id,

            Recommendation.user_id
            == user.id,
        )
        .first()
    )

    if not row:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return {

        "id": row.id,

        "planner_type":
            row.planner_type,

        "budget":
            row.budget,

        "request":
            json.loads(
                row.request_json
            ),

        "response":
            json.loads(
                row.response_json
            ),

        "created_at":
            row.created_at.isoformat(),
    }