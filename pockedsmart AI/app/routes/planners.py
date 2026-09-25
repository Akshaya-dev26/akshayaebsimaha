import json

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    HTTPException,
)

from sqlalchemy.orm import Session

from ..database import (
    get_db,
    settings,
)

from ..dependencies import get_current_user

from ..models import (
    User,
    Recommendation,
)

from ..schemas import (
    HomeRequest,
    PartyRequest,
    RecommendationResponse,
)

from ..services.recommendation_service import (
    get_recommendations,
)


router = APIRouter(
    tags=["Planners"]
)


def save_history(
    db,
    user,
    planner_type,
    payload,
    result,
):

    row = Recommendation(

        user_id=user.id,

        planner_type=planner_type,

        budget=float(
            payload["budget"]
        ),

        request_json=json.dumps(
            payload
        ),

        response_json=json.dumps(
            result
        ),
    )

    db.add(row)

    db.commit()


@router.post(
    "/generate-home",
    response_model=RecommendationResponse,
)
async def generate_home(
    payload: HomeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    data = payload.model_dump()

    result, source = await get_recommendations(
        "home",
        data,
    )

    save_history(
        db,
        user,
        "home",
        data,
        result,
    )

    return {
        "planner_type": "home",
        "budget": payload.budget,
        **result,
        "source": source,
    }


@router.post(
    "/generate-party",
    response_model=RecommendationResponse,
)
async def generate_party(
    payload: PartyRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    data = payload.model_dump()

    result, source = await get_recommendations(
        "party",
        data,
    )

    save_history(
        db,
        user,
        "party",
        data,
        result,
    )

    return {
        "planner_type": "party",
        "budget": payload.budget,
        **result,
        "source": source,
    }


@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_description: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail="Budget must be greater than zero",
        )

    image_bytes = None

    mime_type = None

    if (
        outfit_image
        and outfit_image.filename
    ):

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if outfit_image.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail="Only JPG, PNG and WEBP images are supported",
            )

        image_bytes = (
            await outfit_image.read()
        )

        max_bytes = (
            settings.max_upload_mb
            * 1024
            * 1024
        )

        if len(image_bytes) > max_bytes:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Image must be smaller "
                    f"than {settings.max_upload_mb} MB"
                ),
            )

        mime_type = outfit_image.content_type

    data = {

        "budget": budget,

        "occasion": occasion,

        "style": style,

        "outfit_description":
            outfit_description,
    }

    result, source = await get_recommendations(
        "jewelry",
        data,
        image_bytes,
        mime_type,
    )

    save_history(
        db,
        user,
        "jewelry",
        data,
        result,
    )

    return {

        "planner_type": "jewelry",

        "budget": budget,

        **result,

        "source": source,
    }