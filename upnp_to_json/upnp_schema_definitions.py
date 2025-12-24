from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class UPnPNamespace(Enum):
    """Standard UPnP XML namespaces"""
    DEVICE = "urn:schemas-upnp-org:device-1-0"
    SERVICE = "urn:schemas-upnp-org:service-1-0"
    CONTROL = "urn:schemas-upnp-org:control-1-0"
    EVENT = "urn:schemas-upnp-org:event-1-0"


@dataclass
class UPnPIcon:
    """Represents a device icon"""
    mimetype: str
    width: int
    height: int
    depth: int
    url: str


@dataclass
class UPnPService:
    """Represents a UPnP service"""
    service_type: str
    service_id: str
    scpd_url: str  # Service Control Protocol Description URL
    control_url: str
    event_sub_url: str


@dataclass
class UPnPDevice:
    """Represents a UPnP device description"""
    device_type: str
    friendly_name: str
    manufacturer: str
    manufacturer_url: Optional[str] = None
    model_description: Optional[str] = None
    model_name: Optional[str] = None
    model_number: Optional[str] = None
    model_url: Optional[str] = None
    serial_number: Optional[str] = None
    udn: Optional[str] = None  # Unique Device Name (UUID)
    upc: Optional[str] = None  # Universal Product Code
    icons: List[UPnPIcon] = field(default_factory=list)
    services: List[UPnPService] = field(default_factory=list)
    devices: List['UPnPDevice'] = field(default_factory=list)  # Embedded devices
    presentation_url: Optional[str] = None


@dataclass
class UPnPAction:
    """Represents a service action"""
    name: str
    arguments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class UPnPStateVariable:
    """Represents a state variable"""
    name: str
    data_type: str
    send_events: bool = False
    default_value: Optional[str] = None
    allowed_values: List[str] = field(default_factory=list)
    allowed_value_range: Optional[Dict[str, Any]] = None


@dataclass
class UPnPServiceDescription:
    """Service Control Protocol Description (SCPD)"""
    spec_version: Dict[str, int]
    actions: List[UPnPAction] = field(default_factory=list)
    state_variables: List[UPnPStateVariable] = field(default_factory=list)