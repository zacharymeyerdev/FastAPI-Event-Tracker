from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    """Input model for creating an event (no id)"""
    ts: datetime = Field(..., description="ISO datetime string")
    label: str = Field(..., min_length=1, max_length=32, description="Short tag like 'crack' or 'rust' or 'note'")
    description: Optional[str] = Field(None, max_length=500, description="Optional longer text")
    x: Optional[float] = Field(None, description="Optional X coordinate")
    y: Optional[float] = Field(None, description="Optional Y coordinate")
    source: Optional[str] = Field(None, description="Optional source like 'manual' or 'video' or 'sensor'")

class EventOut(BaseModel):
    """Output model for an event (with id)"""
    id: int
    ts: datetime
    label: str
    description: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    source: Optional[str] = None

    class Config:
        from_attributes = True

class EventListResponse(BaseModel):
    """Output model for a list of events"""
    total: int = Field(..., description="Total number of events for the filters")
    limit: int = Field(..., ge=1, le=200, description="Items per page")
    offset: int = Field(..., description="Offset of the returned events")
    items: list[EventOut] = Field(..., description="List of event items")