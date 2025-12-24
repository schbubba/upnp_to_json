import json
from typing import Any, Dict

from .upnp_schema_definitions import (
    UPnPAction, 
    UPnPDevice, 
    UPnPIcon, 
    UPnPService, 
    UPnPServiceDescription, 
    UPnPStateVariable)


class UPnPJSONConverter:
    """Converts UPnP objects to JSON format"""
    
    @staticmethod
    def device_to_json(device: UPnPDevice, indent: int = 2) -> str:
        """Convert UPnPDevice to JSON string"""
        return json.dumps(UPnPJSONConverter.device_to_dict(device), indent=indent)
    
    @staticmethod
    def device_to_dict(device: UPnPDevice) -> Dict[str, Any]:
        """Convert UPnPDevice to dictionary"""
        return {
            'deviceType': device.device_type,
            'friendlyName': device.friendly_name,
            'manufacturer': device.manufacturer,
            'manufacturerURL': device.manufacturer_url,
            'modelDescription': device.model_description,
            'modelName': device.model_name,
            'modelNumber': device.model_number,
            'modelURL': device.model_url,
            'serialNumber': device.serial_number,
            'UDN': device.udn,
            'UPC': device.upc,
            'icons': [UPnPJSONConverter._icon_to_dict(icon) for icon in device.icons],
            'services': [UPnPJSONConverter._service_to_dict(svc) for svc in device.services],
            'devices': [UPnPJSONConverter.device_to_dict(dev) for dev in device.devices],
            'presentationURL': device.presentation_url
        }
    
    @staticmethod
    def _icon_to_dict(icon: UPnPIcon) -> Dict[str, Any]:
        """Convert UPnPIcon to dictionary"""
        return {
            'mimetype': icon.mimetype,
            'width': icon.width,
            'height': icon.height,
            'depth': icon.depth,
            'url': icon.url
        }
    
    @staticmethod
    def _service_to_dict(service: UPnPService) -> Dict[str, Any]:
        """Convert UPnPService to dictionary"""
        return {
            'serviceType': service.service_type,
            'serviceId': service.service_id,
            'SCPDURL': service.scpd_url,
            'controlURL': service.control_url,
            'eventSubURL': service.event_sub_url
        }
    
    @staticmethod
    def service_description_to_json(scpd: UPnPServiceDescription, indent: int = 2) -> str:
        """Convert UPnPServiceDescription to JSON string"""
        return json.dumps(UPnPJSONConverter.service_description_to_dict(scpd), indent=indent)
    
    @staticmethod
    def service_description_to_dict(scpd: UPnPServiceDescription) -> Dict[str, Any]:
        """Convert UPnPServiceDescription to dictionary"""
        return {
            'specVersion': scpd.spec_version,
            'actions': [UPnPJSONConverter._action_to_dict(action) for action in scpd.actions],
            'serviceStateTable': [UPnPJSONConverter._state_var_to_dict(var) for var in scpd.state_variables]
        }
    
    @staticmethod
    def _action_to_dict(action: UPnPAction) -> Dict[str, Any]:
        """Convert UPnPAction to dictionary"""
        return {
            'name': action.name,
            'arguments': action.arguments
        }
    
    @staticmethod
    def _state_var_to_dict(var: UPnPStateVariable) -> Dict[str, Any]:
        """Convert UPnPStateVariable to dictionary"""
        result = {
            'name': var.name,
            'dataType': var.data_type,
            'sendEvents': var.send_events
        }
        
        if var.default_value:
            result['defaultValue'] = var.default_value
        
        if var.allowed_values:
            result['allowedValueList'] = var.allowed_values
        
        if var.allowed_value_range:
            result['allowedValueRange'] = var.allowed_value_range
        
        return result