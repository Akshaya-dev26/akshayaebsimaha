from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import User

from ..schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)

from ..auth import (
    hash_password,
    verify_password,
    create_access_token,
)

from ..dependencies import get_current_user


router = APIRouter(
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=TokenResponse,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):

    email = str(payload.email).lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user = User(
        name=payload.name.strip(),
        email=email,
        password_hash=hash_password(
            payload.password
        ),
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    token = create_access_token(
        user.id
    )

    return TokenResponse(
        access_token=token
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):

    email = str(payload.email).lower()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        payload.password,
        user.password_hash,
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return TokenResponse(
        access_token=create_access_token(
            user.id
        )
    )


@router.post("/logout")
def logout():

    return {
        "message":
            "Logged out. Remove the JWT from the client."
    }


@router.get("/session-info")
def session_info(
    user: User = Depends(get_current_user),
):

    return {
        "logged_in": True,
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
    }


@router.get("/session-data")
def session_data(
    user: User = Depends(get_current_user),
):

    return {
        "user_id": user.id,
        "name": user.name,
        "planner_access": [
            "home",
            "party",
            "jewelry",
        ],
    }