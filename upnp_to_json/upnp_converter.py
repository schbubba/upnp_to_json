from typing import Any, Dict

from .upnp_json_converter import UPnPJSONConverter
from .upnp_xml_parser import UPnPXMLParser

class UPnPConverter:
    """High-level converter API"""
    
    @staticmethod
    def xml_to_json(xml_content: str, doc_type: str = 'device') -> str:
        """
        Convert UPnP XML to JSON
        
        Args:
            xml_content: XML string content
            doc_type: 'device' or 'service'
            
        Returns:
            JSON string
        """
        if doc_type == 'device':
            device = UPnPXMLParser.parse_device_description(xml_content)
            return UPnPJSONConverter.device_to_json(device)
        elif doc_type == 'service':
            scpd = UPnPXMLParser.parse_service_description(xml_content)
            return UPnPJSONConverter.service_description_to_json(scpd)
        else:
            raise ValueError(f"Unknown doc_type: {doc_type}. Use 'device' or 'service'")
    
    @staticmethod
    def xml_to_dict(xml_content: str, doc_type: str = 'device') -> Dict[str, Any]:
        """
        Convert UPnP XML to dictionary
        
        Args:
            xml_content: XML string content
            doc_type: 'device' or 'service'
            
        Returns:
            Dictionary representation
        """
        if doc_type == 'device':
            device = UPnPXMLParser.parse_device_description(xml_content)
            return UPnPJSONConverter.device_to_dict(device)
        elif doc_type == 'service':
            scpd = UPnPXMLParser.parse_service_description(xml_content)
            return UPnPJSONConverter.service_description_to_dict(scpd)
        else:
            raise ValueError(f"Unknown doc_type: {doc_type}. Use 'device' or 'service'")
