from flask import Flask, render_template, request, jsonify
import re
import ipaddress
import json
from typing import Dict, List, Any

app = Flask(__name__)

class NetworkingTools:
    @staticmethod
    def test_regex(pattern: str, text: str, flags: str = '') -> Dict[str, Any]:
        """Test regex pattern against text"""
        try:
            regex_flags = 0
            if 'i' in flags.lower():
                regex_flags |= re.IGNORECASE
            if 'm' in flags.lower():
                regex_flags |= re.MULTILINE
            if 's' in flags.lower():
                regex_flags |= re.DOTALL
            
            compiled_pattern = re.compile(pattern, regex_flags)
            matches = compiled_pattern.finditer(text)
            
            results = []
            for match in matches:
                results.append({
                    'match': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'groups': match.groups()
                })
            
            return {
                'success': True,
                'matches': results,
                'total_matches': len(results)
            }
        except re.error as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def cidr_operations(cidr: str, operation: str) -> Dict[str, Any]:
        """Perform CIDR calculations and conversions"""
        try:
            network = ipaddress.IPv4Network(cidr, strict=False)
            
            if operation == 'info':
                return {
                    'success': True,
                    'network_address': str(network.network_address),
                    'broadcast_address': str(network.broadcast_address),
                    'netmask': str(network.netmask),
                    'wildcard': str(network.hostmask),
                    'prefix_length': network.prefixlen,
                    'num_hosts': network.num_addresses - 2 if network.prefixlen < 31 else network.num_addresses,
                    'first_host': str(list(network.hosts())[0]) if network.num_addresses > 2 else 'N/A',
                    'last_host': str(list(network.hosts())[-1]) if network.num_addresses > 2 else 'N/A',
                    'is_private': network.is_private,
                    'is_multicast': network.is_multicast,
                    'is_loopback': network.is_loopback
                }
            elif operation == 'subnets':
                # Return subnets for next prefix length
                if network.prefixlen < 30:
                    subnets = list(network.subnets(new_prefix=network.prefixlen + 1))
                    return {
                        'success': True,
                        'subnets': [str(subnet) for subnet in subnets[:10]]  # Limit to first 10
                    }
                else:
                    return {'success': False, 'error': 'Network too small to subnet'}
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def convert_config(source_config: str, source_platform: str, target_platform: str) -> Dict[str, Any]:
        """Convert configuration between different network platforms"""
        try:
            converter_map = {
                ('cisco_ios', 'arista_eos'): NetworkingTools._ios_to_eos,
                ('cisco_nxos', 'arista_eos'): NetworkingTools._nxos_to_eos,
                ('arista_eos', 'cisco_ios'): NetworkingTools._eos_to_ios,
                ('cisco_ios', 'juniper_junos'): NetworkingTools._ios_to_junos,
            }
            
            converter = converter_map.get((source_platform, target_platform))
            if converter:
                converted_config = converter(source_config)
                return {
                    'success': True,
                    'converted_config': converted_config,
                    'source_platform': source_platform,
                    'target_platform': target_platform
                }
            else:
                return {
                    'success': False,
                    'error': f'Conversion from {source_platform} to {target_platform} not supported yet'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def _ios_to_eos(config: str) -> str:
        """Convert Cisco IOS config to Arista EOS"""
        lines = config.split('\n')
        converted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('!'):
                converted_lines.append(line)
                continue
            
            # Convert interface commands
            if line.startswith('interface'):
                # Convert FastEthernet/GigabitEthernet to Ethernet
                line = re.sub(r'interface (FastEthernet|GigabitEthernet)(\d+/\d+)', r'interface Ethernet\2', line)
                converted_lines.append(line)
            elif 'switchport mode access' in line:
                converted_lines.append(line.replace('switchport mode access', 'switchport access'))
            elif 'switchport access vlan' in line:
                converted_lines.append(line)
            elif 'spanning-tree portfast' in line:
                converted_lines.append('   spanning-tree portfast')
            else:
                converted_lines.append(line)
        
        return '\n'.join(converted_lines)
    
    @staticmethod
    def _nxos_to_eos(config: str) -> str:
        """Convert Cisco NX-OS config to Arista EOS"""
        lines = config.split('\n')
        converted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('!'):
                converted_lines.append(line)
                continue
            
            # Convert NX-OS specific commands
            if 'feature' in line and any(x in line for x in ['ospf', 'bgp', 'eigrp']):
                converted_lines.append(f'! {line} (feature enabled by default in EOS)')
            elif line.startswith('interface Ethernet'):
                converted_lines.append(line)
            elif 'switchport' in line:
                converted_lines.append(line)
            else:
                converted_lines.append(line)
        
        return '\n'.join(converted_lines)
    
    @staticmethod
    def _eos_to_ios(config: str) -> str:
        """Convert Arista EOS config to Cisco IOS"""
        lines = config.split('\n')
        converted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('!'):
                converted_lines.append(line)
                continue
            
            # Convert EOS to IOS
            if 'switchport access' in line and 'vlan' not in line:
                converted_lines.append(line.replace('switchport access', 'switchport mode access'))
            else:
                converted_lines.append(line)
        
        return '\n'.join(converted_lines)
    
    @staticmethod
    def _ios_to_junos(config: str) -> str:
        """Convert Cisco IOS config to Juniper JunOS"""
        lines = config.split('\n')
        converted_lines = ['# Converted from Cisco IOS to Juniper JunOS', 'set groups basic-config']
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('!'):
                continue
            
            # Basic conversion examples
            if line.startswith('hostname'):
                hostname = line.split()[1]
                converted_lines.append(f'set system host-name {hostname}')
            elif line.startswith('interface'):
                interface = line.split()[1]
                converted_lines.append(f'# Interface {interface} configuration')
        
        return '\n'.join(converted_lines)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/regex-test', methods=['POST'])
def regex_test():
    data = request.json
    pattern = data.get('pattern', '')
    text = data.get('text', '')
    flags = data.get('flags', '')
    
    result = NetworkingTools.test_regex(pattern, text, flags)
    return jsonify(result)

@app.route('/api/cidr-calc', methods=['POST'])
def cidr_calc():
    data = request.json
    cidr = data.get('cidr', '')
    operation = data.get('operation', 'info')
    
    result = NetworkingTools.cidr_operations(cidr, operation)
    return jsonify(result)

@app.route('/api/config-convert', methods=['POST'])
def config_convert():
    data = request.json
    source_config = data.get('source_config', '')
    source_platform = data.get('source_platform', '')
    target_platform = data.get('target_platform', '')
    
    result = NetworkingTools.convert_config(source_config, source_platform, target_platform)
    return jsonify(result)

@app.route('/api/ansible-examples')
def ansible_examples():
    examples = {
        'cisco_ios': {
            'playbook': '''---
- name: Configure Cisco IOS devices
  hosts: cisco_devices
  gather_facts: no
  connection: network_cli
  
  tasks:
    - name: Configure VLANs
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 10
            name: "DATA_VLAN"
          - vlan_id: 20
            name: "VOICE_VLAN"
        state: merged
    
    - name: Configure interfaces
      cisco.ios.ios_interfaces:
        config:
          - name: GigabitEthernet0/1
            description: "Access port for DATA"
            enabled: true
        state: merged
    
    - name: Configure switchport
      cisco.ios.ios_l2_interfaces:
        config:
          - name: GigabitEthernet0/1
            access:
              vlan: 10
        state: merged''',
            'inventory': '''[cisco_devices]
router1 ansible_host=192.168.1.1
switch1 ansible_host=192.168.1.2

[cisco_devices:vars]
ansible_network_os=ios
ansible_user=admin
ansible_password=cisco123
ansible_connection=network_cli''',
            'requirements': '''collections:
  - cisco.ios
  - community.general'''
        },
        'arista_eos': {
            'playbook': '''---
- name: Configure Arista EOS devices
  hosts: arista_devices
  gather_facts: no
  connection: network_cli
  
  tasks:
    - name: Configure VLANs
      arista.eos.eos_vlans:
        config:
          - vlan_id: 10
            name: "DATA_VLAN"
          - vlan_id: 20
            name: "VOICE_VLAN"
        state: merged
    
    - name: Configure interfaces
      arista.eos.eos_interfaces:
        config:
          - name: Ethernet1
            description: "Access port for DATA"
            enabled: true
        state: merged
    
    - name: Configure switchport
      arista.eos.eos_l2_interfaces:
        config:
          - name: Ethernet1
            access:
              vlan: 10
        state: merged''',
            'inventory': '''[arista_devices]
switch1 ansible_host=192.168.1.10
switch2 ansible_host=192.168.1.11

[arista_devices:vars]
ansible_network_os=eos
ansible_user=admin
ansible_password=arista123
ansible_connection=network_cli''',
            'requirements': '''collections:
  - arista.eos
  - community.general'''
        },
        'cisco_nxos': {
            'playbook': '''---
- name: Configure Cisco NX-OS devices
  hosts: nxos_devices
  gather_facts: no
  connection: network_cli
  
  tasks:
    - name: Enable features
      cisco.nxos.nxos_feature:
        feature: "{{ item }}"
        state: enabled
      loop:
        - interface-vlan
        - hsrp
        - vpc
    
    - name: Configure VLANs
      cisco.nxos.nxos_vlans:
        config:
          - vlan_id: 10
            name: "WEB_SERVERS"
          - vlan_id: 20
            name: "DB_SERVERS"
        state: merged
    
    - name: Configure VPC domain
      cisco.nxos.nxos_vpc:
        domain: 100
        pkl_src: 192.168.100.1
        pkl_dest: 192.168.100.2
        pkl_vrf: management''',
            'inventory': '''[nxos_devices]
nexus1 ansible_host=192.168.1.20
nexus2 ansible_host=192.168.1.21

[nxos_devices:vars]
ansible_network_os=nxos
ansible_user=admin
ansible_password=nexus123
ansible_connection=network_cli''',
            'requirements': '''collections:
  - cisco.nxos
  - community.general'''
        }
    }
    return jsonify(examples)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)