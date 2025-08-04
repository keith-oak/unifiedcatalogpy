"""
Response models for UnifiedCatalogPy API responses.
Provides type-safe dataclasses for better developer experience.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class EntityStatus(Enum):
    """Common status values for entities."""
    DRAFT = "Draft"
    PUBLISHED = "Published"
    EXPIRED = "Expired"
    CLOSED = "Closed"


class GovernanceDomainType(Enum):
    """Types of governance domains."""
    FUNCTIONAL_UNIT = "FunctionalUnit"
    LINE_OF_BUSINESS = "LineOfBusiness"
    DATA_DOMAIN = "DataDomain"
    REGULATORY = "Regulatory"
    PROJECT = "Project"


class DataProductType(Enum):
    """Types of data products."""
    DATASET = "Dataset"
    MASTER_DATA_AND_REFERENCE_DATA = "MasterDataAndReferenceData"
    BUSINESS_SYSTEM_OR_APPLICATION = "BusinessSystemOrApplication"
    MODEL_TYPES = "ModelTypes"
    DASHBOARDS_OR_REPORTS = "DashboardsOrReports"
    OPERATIONAL = "Operational"


class UpdateFrequency(Enum):
    """Update frequency options."""
    HOURLY = "Hourly"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    YEARLY = "Yearly"


class KeyResultStatus(Enum):
    """Key result status options."""
    BEHIND = "Behind"
    ON_TRACK = "OnTrack"
    AT_RISK = "AtRisk"


@dataclass
class Contact:
    """Represents a contact (owner, steward, etc.)."""
    id: str
    description: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Contact':
        return cls(
            id=data["id"],
            description=data.get("description")
        )


@dataclass
class Resource:
    """Represents a resource link."""
    name: str
    url: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Resource':
        return cls(
            name=data["name"],
            url=data["url"]
        )


@dataclass
class GovernanceDomain:
    """Represents a governance domain."""
    id: str
    name: str
    description: str
    type: GovernanceDomainType
    status: EntityStatus
    parent_id: Optional[str] = None
    owners: List[Contact] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GovernanceDomain':
        contacts = data.get("contacts", {})
        owners = [Contact.from_dict(owner) for owner in contacts.get("owner", [])]
        
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            type=GovernanceDomainType(data["type"]),
            status=EntityStatus(data["status"]),
            parent_id=data.get("parent_id"),
            owners=owners,
            created_at=cls._parse_datetime(data.get("createdAt")),
            updated_at=cls._parse_datetime(data.get("updatedAt")),
            raw_data=data
        )
    
    @staticmethod
    def _parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object."""
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None


@dataclass
class Term:
    """Represents a glossary term."""
    id: str
    name: str
    description: str
    status: EntityStatus
    domain_id: str
    parent_id: Optional[str] = None
    owners: List[Contact] = field(default_factory=list)
    acronyms: List[str] = field(default_factory=list)
    resources: List[Resource] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Term':
        contacts = data.get("contacts", {})
        owners = [Contact.from_dict(owner) for owner in contacts.get("owner", [])]
        resources = [Resource.from_dict(res) for res in data.get("resources", [])]
        
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            status=EntityStatus(data["status"]),
            domain_id=data["domain"],
            parent_id=data.get("parent_id"),
            owners=owners,
            acronyms=data.get("acronyms", []),
            resources=resources,
            created_at=GovernanceDomain._parse_datetime(data.get("createdAt")),
            updated_at=GovernanceDomain._parse_datetime(data.get("updatedAt")),
            raw_data=data
        )


@dataclass
class DataProduct:
    """Represents a data product."""
    id: str
    name: str
    description: str
    type: DataProductType
    status: EntityStatus
    domain_id: str
    business_use: str
    owners: List[Contact] = field(default_factory=list)
    audience: List[str] = field(default_factory=list)
    terms_of_use: List[str] = field(default_factory=list)
    documentation: List[str] = field(default_factory=list)
    update_frequency: Optional[UpdateFrequency] = None
    endorsed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DataProduct':
        contacts = data.get("contacts", {})
        owners = [Contact.from_dict(owner) for owner in contacts.get("owner", [])]
        
        update_freq = None
        if data.get("updateFrequency"):
            try:
                update_freq = UpdateFrequency(data["updateFrequency"])
            except ValueError:
                pass
        
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            type=DataProductType(data["type"]),
            status=EntityStatus(data["status"]),
            domain_id=data["domain"],
            business_use=data["businessUse"],
            owners=owners,
            audience=data.get("audience", []),
            terms_of_use=data.get("termsOfUse", []),
            documentation=data.get("documentation", []),
            update_frequency=update_freq,
            endorsed=data.get("endorsed", False),
            created_at=GovernanceDomain._parse_datetime(data.get("createdAt")),
            updated_at=GovernanceDomain._parse_datetime(data.get("updatedAt")),
            raw_data=data
        )


@dataclass
class Objective:
    """Represents an objective."""
    id: str
    definition: str
    status: EntityStatus
    domain_id: str
    owners: List[Contact] = field(default_factory=list)
    target_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Objective':
        contacts = data.get("contacts", {})
        owners = [Contact.from_dict(owner) for owner in contacts.get("owner", [])]
        
        return cls(
            id=data["id"],
            definition=data["definition"],
            status=EntityStatus(data["status"]),
            domain_id=data["domain"],
            owners=owners,
            target_date=GovernanceDomain._parse_datetime(data.get("targetDate")),
            created_at=GovernanceDomain._parse_datetime(data.get("createdAt")),
            updated_at=GovernanceDomain._parse_datetime(data.get("updatedAt")),
            raw_data=data
        )


@dataclass
class KeyResult:
    """Represents a key result."""
    id: str
    definition: str
    progress: int
    goal: int
    max_value: int
    status: KeyResultStatus
    domain_id: str
    objective_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress as percentage."""
        return (self.progress / self.max_value) * 100 if self.max_value > 0 else 0
    
    @property
    def goal_percentage(self) -> float:
        """Calculate goal as percentage."""
        return (self.goal / self.max_value) * 100 if self.max_value > 0 else 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KeyResult':
        return cls(
            id=data["id"],
            definition=data["definition"],
            progress=data["progress"],
            goal=data["goal"],
            max_value=data["max"],
            status=KeyResultStatus(data["status"]),
            domain_id=data["domainId"],
            objective_id=data.get("objectiveId", ""),
            created_at=GovernanceDomain._parse_datetime(data.get("createdAt")),
            updated_at=GovernanceDomain._parse_datetime(data.get("updatedAt")),
            raw_data=data
        )


@dataclass
class CriticalDataElement:
    """Represents a critical data element."""
    id: str
    name: str
    description: str
    status: EntityStatus
    domain_id: str
    data_type: str
    owners: List[Contact] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CriticalDataElement':
        contacts = data.get("contacts", {})
        owners = [Contact.from_dict(owner) for owner in contacts.get("owner", [])]
        
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            status=EntityStatus(data["status"]),
            domain_id=data["domain"],
            data_type=data["dataType"],
            owners=owners,
            created_at=GovernanceDomain._parse_datetime(data.get("createdAt")),
            updated_at=GovernanceDomain._parse_datetime(data.get("updatedAt")),
            raw_data=data
        )


@dataclass
class Relationship:
    """Represents a relationship between entities."""
    id: str
    description: str
    entity_id: str
    target_entity_id: str
    relationship_type: str
    entity_type: str
    created_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Relationship':
        return cls(
            id=data.get("id", ""),
            description=data.get("description", ""),
            entity_id=data.get("entityId", ""),
            target_entity_id=data.get("targetEntityId", ""),
            relationship_type=data.get("relationshipType", ""),
            entity_type=data.get("entityType", ""),
            created_at=GovernanceDomain._parse_datetime(data.get("createdAt")),
            raw_data=data
        )