from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserOut(BaseModel):
    id: str
    email: EmailStr
    display_name: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    display_name: str = Field(default="", max_length=120)
class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)
class ProjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=5000)
    tags: list[str] = Field(default_factory=list, max_length=20)
class ProjectPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=5000)
    tags: list[str] | None = Field(default=None, max_length=20)
class ProjectOut(BaseModel):
    id: str
    name: str
    description: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime
    archived_at: datetime | None
    model_config = ConfigDict(from_attributes=True)
class DocumentIn(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    content_markdown: str = Field(default="", max_length=1_000_000)
class DocumentPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=240)
    content_markdown: str | None = Field(default=None, max_length=1_000_000)
    change_summary: str = Field(default="Saved changes", max_length=500)
class DocumentOut(BaseModel):
    id: str
    project_id: str
    title: str
    content_markdown: str
    version_number: int
    created_at: datetime
    updated_at: datetime
    archived_at: datetime | None
    model_config = ConfigDict(from_attributes=True)
class SourceOut(BaseModel):
    id: str
    project_id: str
    filename: str
    content_type: str
    size_bytes: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class GenerationIn(BaseModel):
    source_id: str | None = None
    title: str = Field(default="API Documentation", max_length=240)
    audience: str = Field(default="Developers", max_length=120)
    instructions: str = Field(default="", max_length=5000)
class ShareIn(BaseModel):
    expires_in_days: int | None = Field(default=None, ge=1, le=365)
    allow_download: bool = True
class ShareOut(BaseModel):
    id: str
    url: str
    is_active: bool
    allow_download: bool
    expires_at: datetime | None
    created_at: datetime

class GeminiSettingsIn(BaseModel):
    api_key: str = Field(min_length=10, max_length=500)
    model: str = Field(default="gemini-3.5-flash-lite", min_length=1, max_length=120)

class GeminiModelIn(BaseModel):
    model: str = Field(min_length=1, max_length=120)
