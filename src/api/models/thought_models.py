"""API models for thought-related endpoints."""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.entities.semantic_entry import SemanticEntry
from src.domain.entities.thought import GeoLocation, Thought, ThoughtMetadata, WeatherData


class GeoLocationRequest(BaseModel):
    """Request model for geographic location."""

    latitude: float
    longitude: float
    name: Optional[str] = None


class WeatherDataRequest(BaseModel):
    """Request model for weather information."""

    temperature: Optional[float] = None
    condition: Optional[str] = None
    humidity: Optional[float] = None


class ThoughtMetadataRequest(BaseModel):
    """Request model for thought metadata."""

    location: Optional[GeoLocationRequest] = None
    weather: Optional[WeatherDataRequest] = None
    mood: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    custom: Dict[str, str] = Field(default_factory=dict)

    def to_domain(self) -> ThoughtMetadata:
        """Convert to domain ThoughtMetadata.

        Returns:
            Domain ThoughtMetadata object
        """
        location = None
        if self.location:
            location = GeoLocation(
                latitude=self.location.latitude,
                longitude=self.location.longitude,
                name=self.location.name,
            )

        weather = None
        if self.weather:
            weather = WeatherData(
                temperature=self.weather.temperature,
                condition=self.weather.condition,
                humidity=self.weather.humidity,
            )

        return ThoughtMetadata(
            location=location,
            weather=weather,
            mood=self.mood,
            tags=self.tags,
            custom=self.custom,
        )


class CreateThoughtRequest(BaseModel):
    """Request model for creating a thought."""

    content: str = Field(..., min_length=1, description="The thought content")
    metadata: Optional[ThoughtMetadataRequest] = None
    timestamp: Optional[datetime] = None


class UpdateThoughtRequest(BaseModel):
    """Request model for updating a thought."""

    content: Optional[str] = Field(None, min_length=1, description="The updated thought content")
    metadata: Optional[ThoughtMetadataRequest] = None


class GeoLocationResponse(BaseModel):
    """Response model for geographic location."""

    latitude: float
    longitude: float
    name: Optional[str] = None

    @classmethod
    def from_domain(cls, location: GeoLocation) -> "GeoLocationResponse":
        """Create from domain GeoLocation.

        Args:
            location: Domain GeoLocation object

        Returns:
            GeoLocationResponse object
        """
        return cls(
            latitude=location.latitude,
            longitude=location.longitude,
            name=location.name,
        )


class WeatherDataResponse(BaseModel):
    """Response model for weather information."""

    temperature: Optional[float] = None
    condition: Optional[str] = None
    humidity: Optional[float] = None

    @classmethod
    def from_domain(cls, weather: WeatherData) -> "WeatherDataResponse":
        """Create from domain WeatherData.

        Args:
            weather: Domain WeatherData object

        Returns:
            WeatherDataResponse object
        """
        return cls(
            temperature=weather.temperature,
            condition=weather.condition,
            humidity=weather.humidity,
        )


class ThoughtMetadataResponse(BaseModel):
    """Response model for thought metadata."""

    location: Optional[GeoLocationResponse] = None
    weather: Optional[WeatherDataResponse] = None
    mood: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    custom: Dict[str, str] = Field(default_factory=dict)

    @classmethod
    def from_domain(cls, metadata: ThoughtMetadata) -> "ThoughtMetadataResponse":
        """Create from domain ThoughtMetadata.

        Args:
            metadata: Domain ThoughtMetadata object

        Returns:
            ThoughtMetadataResponse object
        """
        location = None
        if metadata.location:
            location = GeoLocationResponse.from_domain(metadata.location)

        weather = None
        if metadata.weather:
            weather = WeatherDataResponse.from_domain(metadata.weather)

        return cls(
            location=location,
            weather=weather,
            mood=metadata.mood,
            tags=metadata.tags,
            custom=metadata.custom,
        )


class SemanticEntryResponse(BaseModel):
    """Response model for semantic entries."""

    id: UUID
    entity_type: str
    entity_value: str
    confidence: float
    context: str
    extracted_at: datetime

    @classmethod
    def from_domain(cls, entry: SemanticEntry) -> "SemanticEntryResponse":
        """Create from domain SemanticEntry.

        Args:
            entry: Domain SemanticEntry object

        Returns:
            SemanticEntryResponse object
        """
        return cls(
            id=entry.id,
            entity_type=entry.entity_type.value,
            entity_value=entry.entity_value,
            confidence=entry.confidence,
            context=entry.context,
            extracted_at=entry.extracted_at,
        )


class ThoughtResponse(BaseModel):
    """Response model for thoughts."""

    id: UUID
    content: str
    timestamp: datetime
    metadata: ThoughtMetadataResponse
    semantic_entries: List[SemanticEntryResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, thought: Thought) -> "ThoughtResponse":
        """Create from domain Thought.

        Args:
            thought: Domain Thought object

        Returns:
            ThoughtResponse object
        """
        return cls(
            id=thought.id,
            content=thought.content,
            timestamp=thought.timestamp,
            metadata=ThoughtMetadataResponse.from_domain(thought.metadata),
            semantic_entries=[
                SemanticEntryResponse.from_domain(entry)
                for entry in thought.semantic_entries
            ],
            created_at=thought.created_at,
            updated_at=thought.updated_at,
        )


class ThoughtListResponse(BaseModel):
    """Response model for paginated thought lists."""

    thoughts: List[ThoughtResponse]
    total: int
    skip: int
    limit: int

    @classmethod
    def from_domain_list(
        cls, thoughts: List[Thought], total: int, skip: int, limit: int
    ) -> "ThoughtListResponse":
        """Create from list of domain Thoughts.

        Args:
            thoughts: List of domain Thought objects
            total: Total number of thoughts available
            skip: Number of thoughts skipped
            limit: Maximum number of thoughts returned

        Returns:
            ThoughtListResponse object
        """
        return cls(
            thoughts=[ThoughtResponse.from_domain(thought) for thought in thoughts],
            total=total,
            skip=skip,
            limit=limit,
        )


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)