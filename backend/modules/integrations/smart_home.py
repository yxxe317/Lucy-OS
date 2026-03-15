"""
Smart Home Integration - Control IoT devices
"""

from typing import Dict, List, Optional
import json
import os
import random

class SmartHome:
    """
    Smart home device control (simulated)
    """
    
    def __init__(self, hub_address: str = None):
        self.hub_address = hub_address
        self.devices_file = "smart_home_devices.json"
        self.devices = self._load_devices()
        self.states = {}
    
    def _load_devices(self) -> List[Dict]:
        """Load devices from file"""
        if os.path.exists(self.devices_file):
            try:
                with open(self.devices_file, 'r') as f:
                    return json.load(f)
            except:
                return self._generate_sample_devices()
        else:
            return self._generate_sample_devices()
    
    def _generate_sample_devices(self) -> List[Dict]:
        """Generate sample smart home devices"""
        return [
            {'id': 'light1', 'name': 'Living Room Light', 'type': 'light', 'room': 'living_room', 'state': 'off'},
            {'id': 'light2', 'name': 'Kitchen Light', 'type': 'light', 'room': 'kitchen', 'state': 'off'},
            {'id': 'light3', 'name': 'Bedroom Light', 'type': 'light', 'room': 'bedroom', 'state': 'off'},
            {'id': 'thermostat1', 'name': 'Main Thermostat', 'type': 'thermostat', 'room': 'hallway', 'temperature': 22, 'target': 22},
            {'id': 'lock1', 'name': 'Front Door Lock', 'type': 'lock', 'room': 'entrance', 'state': 'locked'},
            {'id': 'lock2', 'name': 'Back Door Lock', 'type': 'lock', 'room': 'backyard', 'state': 'locked'},
            {'id': 'camera1', 'name': 'Front Door Camera', 'type': 'camera', 'room': 'entrance', 'state': 'active'},
            {'id': 'plug1', 'name': 'Coffee Maker', 'type': 'plug', 'room': 'kitchen', 'state': 'off'},
            {'id': 'plug2', 'name': 'TV', 'type': 'plug', 'room': 'living_room', 'state': 'off'},
            {'id': 'sensor1', 'name': 'Motion Sensor', 'type': 'sensor', 'room': 'living_room', 'state': 'inactive'},
        ]
    
    def get_devices(self, room: str = None) -> List[Dict]:
        """
        Get all devices, optionally filtered by room
        """
        if room:
            return [d for d in self.devices if d['room'] == room]
        return self.devices.copy()
    
    def get_device(self, device_id: str) -> Optional[Dict]:
        """
        Get specific device
        """
        for device in self.devices:
            if device['id'] == device_id:
                return device.copy()
        return None
    
    def turn_on(self, device_id: str) -> bool:
        """
        Turn on a device
        """
        for device in self.devices:
            if device['id'] == device_id:
                if device['type'] in ['light', 'plug']:
                    device['state'] = 'on'
                    print(f"✅ Turned on {device['name']}")
                    return True
                elif device['type'] == 'camera':
                    device['state'] = 'active'
                    print(f"✅ Activated {device['name']}")
                    return True
        return False
    
    def turn_off(self, device_id: str) -> bool:
        """
        Turn off a device
        """
        for device in self.devices:
            if device['id'] == device_id:
                if device['type'] in ['light', 'plug']:
                    device['state'] = 'off'
                    print(f"✅ Turned off {device['name']}")
                    return True
                elif device['type'] == 'camera':
                    device['state'] = 'inactive'
                    print(f"✅ Deactivated {device['name']}")
                    return True
        return False
    
    def lock(self, device_id: str) -> bool:
        """
        Lock a device (for locks)
        """
        for device in self.devices:
            if device['id'] == device_id and device['type'] == 'lock':
                device['state'] = 'locked'
                print(f"✅ Locked {device['name']}")
                return True
        return False
    
    def unlock(self, device_id: str) -> bool:
        """
        Unlock a device (for locks)
        """
        for device in self.devices:
            if device['id'] == device_id and device['type'] == 'lock':
                device['state'] = 'unlocked'
                print(f"✅ Unlocked {device['name']}")
                return True
        return False
    
    def set_temperature(self, device_id: str, temperature: float) -> bool:
        """
        Set thermostat temperature
        """
        for device in self.devices:
            if device['id'] == device_id and device['type'] == 'thermostat':
                device['target'] = temperature
                print(f"✅ Set {device['name']} to {temperature}°C")
                return True
        return False
    
    def get_temperature(self, device_id: str) -> Optional[float]:
        """
        Get current temperature from thermostat
        """
        for device in self.devices:
            if device['id'] == device_id and device['type'] == 'thermostat':
                # Simulate small variation
                device['temperature'] += random.uniform(-0.5, 0.5)
                device['temperature'] = round(max(15, min(30, device['temperature'])), 1)
                return device['temperature']
        return None
    
    def get_rooms(self) -> List[str]:
        """
        Get all rooms with devices
        """
        return list(set(d['room'] for d in self.devices))
    
    def get_devices_by_type(self, device_type: str) -> List[Dict]:
        """
        Get devices by type
        """
        return [d for d in self.devices if d['type'] == device_type]
    
    def toggle(self, device_id: str) -> bool:
        """
        Toggle device state
        """
        device = self.get_device(device_id)
        if not device:
            return False
        
        if device['state'] in ['on', 'active', 'unlocked']:
            if device['type'] == 'lock':
                return self.lock(device_id)
            else:
                return self.turn_off(device_id)
        else:
            if device['type'] == 'lock':
                return self.unlock(device_id)
            else:
                return self.turn_on(device_id)