from typing import Optional
import xml.etree.ElementTree as ET

from .upnp_schema_definitions import (
    UPnPAction, 
    UPnPDevice, 
    UPnPIcon, 
    UPnPService, 
    UPnPServiceDescription, 
    UPnPStateVariable)


class UPnPXMLParser:
    """Parses standard UPnP XML documents"""
    
    @staticmethod
    def parse_device_description(xml_content: str) -> UPnPDevice:
        """Parse a UPnP device description XML"""
        root = ET.fromstring(xml_content)
        
        # Remove namespace prefix for easier parsing
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        
        device_elem = root.find('.//device')
        if not device_elem:
            raise ValueError("No device element found in XML")
        
        return UPnPXMLParser._parse_device_element(device_elem)
    
    @staticmethod
    def _parse_device_element(device_elem: ET.Element) -> UPnPDevice:
        """Parse a device XML element"""
        
        def get_text(tag: str, default=None) -> Optional[str]:
            elem = device_elem.find(tag)
            return elem.text if elem is not None and elem.text else default
        
        # Parse icons
        icons = []
        icon_list = device_elem.find('iconList')
        if icon_list:
            for icon_elem in icon_list.findall('icon'):
                icons.append(UPnPIcon(
                    mimetype=icon_elem.findtext('mimetype', ''),
                    width=int(icon_elem.findtext('width', '0')),
                    height=int(icon_elem.findtext('height', '0')),
                    depth=int(icon_elem.findtext('depth', '0')),
                    url=icon_elem.findtext('url', '')
                ))
        
        # Parse services
        services = []
        service_list = device_elem.find('serviceList')
        if service_list:
            for service_elem in service_list.findall('service'):
                services.append(UPnPService(
                    service_type=service_elem.findtext('serviceType', ''),
                    service_id=service_elem.findtext('serviceId', ''),
                    scpd_url=service_elem.findtext('SCPDURL', ''),
                    control_url=service_elem.findtext('controlURL', ''),
                    event_sub_url=service_elem.findtext('eventSubURL', '')
                ))
        
        # Parse embedded devices
        embedded_devices = []
        device_list = device_elem.find('deviceList')
        if device_list:
            for embedded_elem in device_list.findall('device'):
                embedded_devices.append(UPnPXMLParser._parse_device_element(embedded_elem))
        
        return UPnPDevice(
            device_type=get_text('deviceType', ''),
            friendly_name=get_text('friendlyName', ''),
            manufacturer=get_text('manufacturer', ''),
            manufacturer_url=get_text('manufacturerURL'),
            model_description=get_text('modelDescription'),
            model_name=get_text('modelName'),
            model_number=get_text('modelNumber'),
            model_url=get_text('modelURL'),
            serial_number=get_text('serialNumber'),
            udn=get_text('UDN'),
            upc=get_text('UPC'),
            icons=icons,
            services=services,
            devices=embedded_devices,
            presentation_url=get_text('presentationURL')
        )
    
    @staticmethod
    def parse_service_description(xml_content: str) -> UPnPServiceDescription:
        """Parse a Service Control Protocol Description (SCPD) XML"""
        root = ET.fromstring(xml_content)
        
        # Remove namespace prefix
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        
        # Parse spec version
        spec_version = {}
        spec_elem = root.find('specVersion')
        if spec_elem:
            spec_version = {
                'major': int(spec_elem.findtext('major', '1')),
                'minor': int(spec_elem.findtext('minor', '0'))
            }
        
        # Parse actions
        actions = []
        action_list = root.find('actionList')
        if action_list:
            for action_elem in action_list.findall('action'):
                arguments = []
                arg_list = action_elem.find('argumentList')
                if arg_list:
                    for arg_elem in arg_list.findall('argument'):
                        arguments.append({
                            'name': arg_elem.findtext('name', ''),
                            'direction': arg_elem.findtext('direction', ''),
                            'relatedStateVariable': arg_elem.findtext('relatedStateVariable', '')
                        })
                
                actions.append(UPnPAction(
                    name=action_elem.findtext('name', ''),
                    arguments=arguments
                ))
        
        # Parse state variables
        state_variables = []
        var_list = root.find('serviceStateTable')
        if var_list:
            for var_elem in var_list.findall('stateVariable'):
                send_events = var_elem.get('sendEvents', 'no').lower() == 'yes'
                
                allowed_values = []
                allowed_list = var_elem.find('allowedValueList')
                if allowed_list:
                    allowed_values = [v.text for v in allowed_list.findall('allowedValue') if v.text]
                
                allowed_range = None
                range_elem = var_elem.find('allowedValueRange')
                if range_elem:
                    allowed_range = {
                        'minimum': range_elem.findtext('minimum'),
                        'maximum': range_elem.findtext('maximum'),
                        'step': range_elem.findtext('step')
                    }
                
                state_variables.append(UPnPStateVariable(
                    name=var_elem.findtext('name', ''),
                    data_type=var_elem.findtext('dataType', ''),
                    send_events=send_events,
                    default_value=var_elem.findtext('defaultValue'),
                    allowed_values=allowed_values,
                    allowed_value_range=allowed_range
                ))
        
        return UPnPServiceDescription(
            spec_version=spec_version,
            actions=actions,
            state_variables=state_variables
        )
