from pydantic import BaseModel, EmailStr, Field


class LibrarianCreate(BaseModel):
    email: EmailStr = Field(..., description="Librarian email")
    password: str = Field(
        ...,
        min_length=8,
        description="Librarian password",
    )
