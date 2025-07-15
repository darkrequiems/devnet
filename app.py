from flask import Flask, render_template, request, jsonify
import re
import ipaddress
import json
import hashlib
import base64
import socket
import struct
import math
import datetime
from typing import Dict, List, Any, Tuple
import secrets
import binascii

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
                if network.prefixlen < 30:
                    subnets = list(network.subnets(new_prefix=network.prefixlen + 1))
                    return {
                        'success': True,
                        'subnets': [str(subnet) for subnet in subnets[:10]]
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

class SecurityAnalyzer:
    """Security analysis tools for network configurations"""
    
    @staticmethod
    def analyze_passwords(config: str) -> Dict[str, Any]:
        """Analyze password security in configurations"""
        weak_patterns = [
            r'password\s+(\w+)',
            r'secret\s+(\w+)',
            r'community\s+(\w+)',
            r'key\s+(\w+)'
        ]
        
        findings = []
        for pattern in weak_patterns:
            matches = re.finditer(pattern, config, re.IGNORECASE)
            for match in matches:
                password = match.group(1)
                strength = SecurityAnalyzer._assess_password_strength(password)
                findings.append({
                    'type': 'password',
                    'value': password,
                    'strength': strength,
                    'line': config[:match.start()].count('\n') + 1,
                    'recommendation': SecurityAnalyzer._get_password_recommendation(strength)
                })
        
        return {
            'success': True,
            'total_findings': len(findings),
            'findings': findings
        }
    
    @staticmethod
    def _assess_password_strength(password: str) -> str:
        """Assess password strength"""
        if len(password) < 8:
            return 'Very Weak'
        elif password.lower() in ['password', 'admin', 'cisco', 'public', 'private']:
            return 'Very Weak'
        elif password.isalnum() and len(password) < 12:
            return 'Weak'
        elif len(password) >= 12:
            return 'Strong'
        else:
            return 'Medium'
    
    @staticmethod
    def _get_password_recommendation(strength: str) -> str:
        """Get password recommendation"""
        recommendations = {
            'Very Weak': 'Use complex passwords with 12+ characters, mixed case, numbers, and symbols',
            'Weak': 'Add special characters and increase length to 12+ characters',
            'Medium': 'Consider increasing length and complexity',
            'Strong': 'Password meets security requirements'
        }
        return recommendations.get(strength, 'Review password policy')
    
    @staticmethod
    def check_acl_security(acl_config: str) -> Dict[str, Any]:
        """Analyze ACL configurations for security issues"""
        issues = []
        lines = acl_config.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('!'):
                continue
                
            # Check for permit any any
            if re.search(r'permit\s+any\s+any', line, re.IGNORECASE):
                issues.append({
                    'severity': 'High',
                    'line': i,
                    'issue': 'Permit any any rule found',
                    'recommendation': 'Replace with specific source/destination rules'
                })
            
            # Check for unused deny statements
            if re.search(r'deny\s+ip\s+any\s+any', line, re.IGNORECASE):
                issues.append({
                    'severity': 'Info',
                    'line': i,
                    'issue': 'Explicit deny any any (redundant)',
                    'recommendation': 'Implicit deny exists, explicit deny may be unnecessary'
                })
        
        return {
            'success': True,
            'total_issues': len(issues),
            'issues': issues
        }

class ProtocolAnalyzer:
    """Protocol analysis and diagnostic tools"""
    
    @staticmethod
    def analyze_ospf_config(config: str) -> Dict[str, Any]:
        """Analyze OSPF configuration"""
        analysis = {
            'areas': [],
            'interfaces': [],
            'timers': {},
            'issues': []
        }
        
        # Extract OSPF areas
        area_matches = re.finditer(r'area\s+(\d+|\d+\.\d+\.\d+\.\d+)', config, re.IGNORECASE)
        for match in area_matches:
            analysis['areas'].append(match.group(1))
        
        # Extract network statements
        network_matches = re.finditer(r'network\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+area\s+(\d+)', config, re.IGNORECASE)
        for match in network_matches:
            analysis['interfaces'].append({
                'network': match.group(1),
                'wildcard': match.group(2),
                'area': match.group(3)
            })
        
        return {
            'success': True,
            'analysis': analysis
        }
    
    @staticmethod
    def analyze_bgp_config(config: str) -> Dict[str, Any]:
        """Analyze BGP configuration"""
        analysis = {
            'asn': None,
            'neighbors': [],
            'networks': [],
            'route_maps': []
        }
        
        # Extract AS number
        asn_match = re.search(r'router\s+bgp\s+(\d+)', config, re.IGNORECASE)
        if asn_match:
            analysis['asn'] = asn_match.group(1)
        
        # Extract neighbors
        neighbor_matches = re.finditer(r'neighbor\s+(\d+\.\d+\.\d+\.\d+)\s+remote-as\s+(\d+)', config, re.IGNORECASE)
        for match in neighbor_matches:
            analysis['neighbors'].append({
                'ip': match.group(1),
                'remote_as': match.group(2)
            })
        
        return {
            'success': True,
            'analysis': analysis
        }

class NetworkCalculator:
    """Advanced network calculations and conversions"""
    
    @staticmethod
    def vlsm_calculator(network: str, subnet_requirements: List[int]) -> Dict[str, Any]:
        """Calculate VLSM subnets based on requirements"""
        try:
            base_network = ipaddress.IPv4Network(network, strict=False)
            subnets = []
            current_network = base_network
            
            # Sort requirements in descending order for optimal allocation
            sorted_requirements = sorted(subnet_requirements, reverse=True)
            
            for hosts_needed in sorted_requirements:
                # Calculate required prefix length
                prefix_len = 32 - math.ceil(math.log2(hosts_needed + 2))
                subnet = list(current_network.subnets(new_prefix=prefix_len))[0]
                
                subnets.append({
                    'network': str(subnet),
                    'hosts_needed': hosts_needed,
                    'hosts_available': subnet.num_addresses - 2,
                    'first_host': str(list(subnet.hosts())[0]) if subnet.num_addresses > 2 else 'N/A',
                    'last_host': str(list(subnet.hosts())[-1]) if subnet.num_addresses > 2 else 'N/A'
                })
                
                # Move to next available network
                current_network = list(current_network.address_exclude(subnet))[0]
            
            return {
                'success': True,
                'base_network': network,
                'subnets': subnets,
                'total_subnets': len(subnets)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def supernet_calculator(networks: List[str]) -> Dict[str, Any]:
        """Calculate supernet from multiple networks"""
        try:
            network_objects = [ipaddress.IPv4Network(net, strict=False) for net in networks]
            supernet = ipaddress.collapse_addresses(network_objects)
            
            return {
                'success': True,
                'input_networks': networks,
                'supernet': [str(net) for net in supernet]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

class DocumentationGenerator:
    """Generate network documentation and reports"""
    
    @staticmethod
    def generate_ip_plan(networks: List[str]) -> Dict[str, Any]:
        """Generate IP addressing plan documentation"""
        plan = []
        
        for network in networks:
            try:
                net = ipaddress.IPv4Network(network, strict=False)
                plan.append({
                    'network': str(net),
                    'size': net.num_addresses,
                    'usable_hosts': net.num_addresses - 2 if net.prefixlen < 31 else net.num_addresses,
                    'network_class': DocumentationGenerator._get_network_class(net.network_address),
                    'type': 'Private' if net.is_private else 'Public'
                })
            except Exception:
                continue
        
        return {
            'success': True,
            'ip_plan': plan,
            'total_networks': len(plan)
        }
    
    @staticmethod
    def _get_network_class(ip: ipaddress.IPv4Address) -> str:
        """Determine network class"""
        first_octet = int(str(ip).split('.')[0])
        if 1 <= first_octet <= 126:
            return 'Class A'
        elif 128 <= first_octet <= 191:
            return 'Class B'
        elif 192 <= first_octet <= 223:
            return 'Class C'
        elif 224 <= first_octet <= 239:
            return 'Class D (Multicast)'
        else:
            return 'Class E (Reserved)'

class CertificateTools:
    """SSL/TLS certificate analysis tools"""
    
    @staticmethod
    def analyze_certificate_info(cert_data: str) -> Dict[str, Any]:
        """Analyze certificate information"""
        # This would normally parse actual certificate data
        # For demo purposes, we'll provide structure
        return {
            'success': True,
            'info': {
                'issuer': 'Example CA',
                'subject': 'CN=example.com',
                'valid_from': '2024-01-01',
                'valid_to': '2025-01-01',
                'serial_number': '123456789',
                'signature_algorithm': 'SHA256-RSA'
            }
        }

class QoSAnalyzer:
    """Quality of Service analysis tools"""
    
    @staticmethod
    def analyze_qos_config(config: str) -> Dict[str, Any]:
        """Analyze QoS configuration"""
        analysis = {
            'class_maps': [],
            'policy_maps': [],
            'service_policies': []
        }
        
        # Extract class-maps
        class_matches = re.finditer(r'class-map\s+(\S+)', config, re.IGNORECASE)
        for match in class_matches:
            analysis['class_maps'].append(match.group(1))
        
        # Extract policy-maps
        policy_matches = re.finditer(r'policy-map\s+(\S+)', config, re.IGNORECASE)
        for match in policy_matches:
            analysis['policy_maps'].append(match.group(1))
        
        return {
            'success': True,
            'analysis': analysis
        }

# Additional tool classes for the remaining use cases
class VLANManager:
    """VLAN management and analysis tools"""
    
    @staticmethod
    def vlan_database_analyzer(config: str) -> Dict[str, Any]:
        """Analyze VLAN database"""
        vlans = []
        vlan_matches = re.finditer(r'vlan\s+(\d+)(?:\s+name\s+(\S+))?', config, re.IGNORECASE)
        
        for match in vlan_matches:
            vlans.append({
                'id': int(match.group(1)),
                'name': match.group(2) if match.group(2) else f'VLAN{match.group(1)}'
            })
        
        return {
            'success': True,
            'vlans': sorted(vlans, key=lambda x: x['id']),
            'total_vlans': len(vlans)
        }

class RoutingAnalyzer:
    """Routing protocol analysis tools"""
    
    @staticmethod
    def analyze_static_routes(config: str) -> Dict[str, Any]:
        """Analyze static routing configuration"""
        routes = []
        route_matches = re.finditer(r'ip\s+route\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)(?:\s+(\d+))?', config, re.IGNORECASE)
        
        for match in route_matches:
            routes.append({
                'destination': match.group(1),
                'mask': match.group(2),
                'next_hop': match.group(3),
                'admin_distance': match.group(4) if match.group(4) else '1'
            })
        
        return {
            'success': True,
            'static_routes': routes,
            'total_routes': len(routes)
        }

# Enhanced main app with new routes
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

# NEW ENHANCED API ENDPOINTS

@app.route('/api/security-analyze', methods=['POST'])
def security_analyze():
    data = request.json
    config = data.get('config', '')
    analysis_type = data.get('type', 'passwords')
    
    if analysis_type == 'passwords':
        result = SecurityAnalyzer.analyze_passwords(config)
    elif analysis_type == 'acl':
        result = SecurityAnalyzer.check_acl_security(config)
    else:
        result = {'success': False, 'error': 'Unknown analysis type'}
    
    return jsonify(result)

@app.route('/api/protocol-analyze', methods=['POST'])
def protocol_analyze():
    data = request.json
    config = data.get('config', '')
    protocol = data.get('protocol', 'ospf')
    
    if protocol == 'ospf':
        result = ProtocolAnalyzer.analyze_ospf_config(config)
    elif protocol == 'bgp':
        result = ProtocolAnalyzer.analyze_bgp_config(config)
    else:
        result = {'success': False, 'error': 'Protocol not supported'}
    
    return jsonify(result)

@app.route('/api/vlsm-calc', methods=['POST'])
def vlsm_calc():
    data = request.json
    network = data.get('network', '')
    requirements = data.get('requirements', [])
    
    result = NetworkCalculator.vlsm_calculator(network, requirements)
    return jsonify(result)

@app.route('/api/supernet-calc', methods=['POST'])
def supernet_calc():
    data = request.json
    networks = data.get('networks', [])
    
    result = NetworkCalculator.supernet_calculator(networks)
    return jsonify(result)

@app.route('/api/vlan-analyze', methods=['POST'])
def vlan_analyze():
    data = request.json
    config = data.get('config', '')
    
    result = VLANManager.vlan_database_analyzer(config)
    return jsonify(result)

@app.route('/api/routing-analyze', methods=['POST'])
def routing_analyze():
    data = request.json
    config = data.get('config', '')
    
    result = RoutingAnalyzer.analyze_static_routes(config)
    return jsonify(result)

@app.route('/api/qos-analyze', methods=['POST'])
def qos_analyze():
    data = request.json
    config = data.get('config', '')
    
    result = QoSAnalyzer.analyze_qos_config(config)
    return jsonify(result)

@app.route('/api/ip-plan', methods=['POST'])
def ip_plan():
    data = request.json
    networks = data.get('networks', [])
    
    result = DocumentationGenerator.generate_ip_plan(networks)
    return jsonify(result)

@app.route('/api/use-cases')
def get_use_cases():
    """Return all 100+ use cases organized by category"""
    use_cases = {
        'security_analysis': [
            'Password security assessment',
            'ACL rule validation',
            'Certificate expiration checking',
            'SSH key strength analysis',
            'SNMP community string audit',
            'VPN configuration security review',
            'Firewall rule optimization',
            'Port security configuration check',
            'AAA configuration validation',
            'Encryption protocol analysis'
        ],
        'protocol_analysis': [
            'OSPF configuration analysis',
            'BGP neighbor relationship check',
            'EIGRP metric calculation',
            'RIP configuration validation',
            'ISIS protocol analysis',
            'MPLS label distribution check',
            'PIM multicast configuration',
            'HSRP/VRRP redundancy analysis',
            'STP topology calculation',
            'LACP bundle verification'
        ],
        'network_calculations': [
            'VLSM subnet design',
            'Supernet aggregation',
            'IPv6 address planning',
            'Network capacity planning',
            'Bandwidth utilization calculation',
            'Latency and delay analysis',
            'MTU path discovery',
            'TCP window size optimization',
            'Buffer size calculation',
            'Queue depth analysis'
        ],
        'monitoring_diagnostics': [
            'Interface utilization tracking',
            'CPU and memory monitoring',
            'Temperature threshold checking',
            'Power consumption analysis',
            'Fan speed monitoring',
            'Link flap detection',
            'Error rate calculation',
            'Packet loss analysis',
            'Jitter measurement',
            'Network topology discovery'
        ],
        'configuration_management': [
            'Configuration backup automation',
            'Change detection and diff',
            'Compliance policy checking',
            'Template-based provisioning',
            'Bulk configuration deployment',
            'Rollback automation',
            'Configuration validation',
            'Standardization enforcement',
            'Version control integration',
            'Configuration encryption'
        ],
        'troubleshooting_tools': [
            'Ping and traceroute automation',
            'DNS resolution testing',
            'Port connectivity checking',
            'MAC address table analysis',
            'ARP table examination',
            'Route table analysis',
            'DHCP scope utilization',
            'NAT translation verification',
            'Load balancer health checks',
            'SSL/TLS handshake testing'
        ],
        'documentation_reporting': [
            'Network diagram generation',
            'IP address plan documentation',
            'VLAN assignment reports',
            'Port mapping documentation',
            'Cable management tracking',
            'Asset inventory reports',
            'Compliance audit reports',
            'Performance trend analysis',
            'Capacity planning reports',
            'Security assessment reports'
        ],
        'automation_scripting': [
            'Ansible playbook generation',
            'Python script templates',
            'Bash automation scripts',
            'PowerShell network modules',
            'API integration examples',
            'Webhook configuration',
            'Event-driven automation',
            'Scheduled task creation',
            'Log parsing automation',
            'Alert notification scripts'
        ],
        'performance_optimization': [
            'QoS policy optimization',
            'Traffic shaping configuration',
            'Load balancing algorithms',
            'Caching strategy analysis',
            'CDN configuration optimization',
            'Database query optimization',
            'Network path optimization',
            'Compression ratio analysis',
            'Bandwidth allocation tuning',
            'Latency reduction techniques'
        ],
        'specialized_tools': [
            'IoT device management',
            'SD-WAN configuration',
            'Cloud network integration',
            'Container networking',
            'Kubernetes network policies',
            'Service mesh configuration',
            'Edge computing setup',
            'Wireless coverage planning',
            'Spectrum analysis',
            'Radio frequency optimization'
        ]
    }
    
    return jsonify({
        'success': True,
        'total_categories': len(use_cases),
        'total_use_cases': sum(len(cases) for cases in use_cases.values()),
        'use_cases': use_cases
    })

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