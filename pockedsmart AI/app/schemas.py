from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=72,
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


class HomeRequest(BaseModel):

    budget: float = Field(gt=0)

    rooms: list[str] = Field(
        min_length=1
    )

    style: str = Field(
        min_length=2,
        max_length=100,
    )

    requirements: str = Field(
        default="",
        max_length=1000,
    )


class PartyRequest(BaseModel):

    budget: float = Field(gt=0)

    guests: int = Field(
        gt=0,
        le=10000,
    )

    event_type: str = Field(
        min_length=2,
        max_length=100,
    )

    venue: str = Field(
        default="",
        max_length=200,
    )

    requirements: str = Field(
        default="",
        max_length=1000,
    )


class RecommendationResponse(BaseModel):

    planner_type: str

    budget: float

    summary: str

    allocations: list[dict]

    recommendations: list[dict]

    tips: list[str]

    source: str