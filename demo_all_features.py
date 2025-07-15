#!/usr/bin/env python3
"""
Network Engineering Toolkit - Comprehensive Demo Script
Showcasing 100+ networking use cases and advanced features
"""

import requests
import json
import time

# Base URL for the toolkit
BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n--- {title} ---")

def demo_core_features():
    """Demonstrate core networking tools"""
    print_section("CORE NETWORKING TOOLS DEMONSTRATION")
    
    # 1. Regex Pattern Testing
    print_subsection("1. Regex Pattern Testing")
    response = requests.post(f"{BASE_URL}/api/regex-test", json={
        "pattern": r"(\d{1,3}\.){3}\d{1,3}",
        "text": "Router configs: 192.168.1.1, 10.0.0.1, DNS: 8.8.8.8, Invalid: 999.999.999.999",
        "flags": ""
    })
    result = response.json()
    print(f"Pattern: IP Address Extraction")
    print(f"Found {result['total_matches']} IP addresses:")
    for i, match in enumerate(result['matches'], 1):
        print(f"  {i}. {match['match']} (position {match['start']}-{match['end']})")
    
    # 2. CIDR Network Analysis
    print_subsection("2. CIDR Network Analysis")
    response = requests.post(f"{BASE_URL}/api/cidr-calc", json={
        "cidr": "172.16.0.0/12",
        "operation": "info"
    })
    result = response.json()
    print(f"Network: 172.16.0.0/12")
    print(f"  Network Address: {result['network_address']}")
    print(f"  Broadcast Address: {result['broadcast_address']}")
    print(f"  Usable Hosts: {result['num_hosts']:,}")
    print(f"  Private Network: {result['is_private']}")

def demo_security_analysis():
    """Demonstrate security analysis capabilities"""
    print_section("SECURITY ANALYSIS TOOLS")
    
    # Password Security Assessment
    print_subsection("Password Security Assessment")
    weak_config = """username admin password cisco123
enable secret admin
snmp-server community public ro
crypto key generate rsa general-keys modulus 1024
username guest password guest123"""
    
    response = requests.post(f"{BASE_URL}/api/security-analyze", json={
        "config": weak_config,
        "type": "passwords"
    })
    result = response.json()
    print(f"Security Analysis - Found {result['total_findings']} password issues:")
    for i, finding in enumerate(result['findings'], 1):
        print(f"  {i}. Password '{finding['value']}' - Strength: {finding['strength']}")
        print(f"     Recommendation: {finding['recommendation']}")
    
    # ACL Security Analysis
    print_subsection("ACL Security Analysis")
    acl_config = """access-list 100 permit ip any any
access-list 101 deny tcp any host 192.168.1.1 eq 22
access-list 101 permit ip any any
access-list 102 deny ip any any"""
    
    response = requests.post(f"{BASE_URL}/api/security-analyze", json={
        "config": acl_config,
        "type": "acl"
    })
    result = response.json()
    print(f"ACL Analysis - Found {result['total_issues']} security issues:")
    for i, issue in enumerate(result['issues'], 1):
        print(f"  {i}. Line {issue['line']}: {issue['issue']} (Severity: {issue['severity']})")

def demo_protocol_analysis():
    """Demonstrate protocol analysis tools"""
    print_section("PROTOCOL ANALYSIS TOOLS")
    
    # OSPF Configuration Analysis
    print_subsection("OSPF Configuration Analysis")
    ospf_config = """router ospf 1
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
 network 192.168.2.0 0.0.0.255 area 1
 network 10.0.0.0 0.255.255.255 area 0
 area 1 nssa"""
    
    response = requests.post(f"{BASE_URL}/api/protocol-analyze", json={
        "config": ospf_config,
        "protocol": "ospf"
    })
    result = response.json()
    analysis = result['analysis']
    print(f"OSPF Areas Found: {', '.join(analysis['areas'])}")
    print(f"Network Statements: {len(analysis['interfaces'])}")
    for intf in analysis['interfaces']:
        print(f"  {intf['network']}/{intf['wildcard']} in area {intf['area']}")
    
    # BGP Configuration Analysis
    print_subsection("BGP Configuration Analysis")
    bgp_config = """router bgp 65001
 bgp router-id 1.1.1.1
 neighbor 192.168.1.2 remote-as 65002
 neighbor 192.168.1.3 remote-as 65003
 neighbor 10.0.0.1 remote-as 65001
 network 10.0.0.0 mask 255.0.0.0"""
    
    response = requests.post(f"{BASE_URL}/api/protocol-analyze", json={
        "config": bgp_config,
        "protocol": "bgp"
    })
    result = response.json()
    analysis = result['analysis']
    print(f"BGP AS Number: {analysis['asn']}")
    print(f"BGP Neighbors: {len(analysis['neighbors'])}")
    for neighbor in analysis['neighbors']:
        print(f"  {neighbor['ip']} (AS {neighbor['remote_as']})")

def demo_advanced_calculations():
    """Demonstrate advanced network calculations"""
    print_section("ADVANCED NETWORK CALCULATIONS")
    
    # VLSM Subnet Design
    print_subsection("VLSM Subnet Design")
    response = requests.post(f"{BASE_URL}/api/vlsm-calc", json={
        "network": "192.168.1.0/24",
        "requirements": [100, 50, 25, 10]
    })
    result = response.json()
    print(f"Base Network: {result['base_network']}")
    print(f"Optimized VLSM Subnets:")
    for i, subnet in enumerate(result['subnets'], 1):
        print(f"  {i}. {subnet['network']} - {subnet['hosts_needed']} hosts needed, {subnet['hosts_available']} available")
        print(f"     Range: {subnet['first_host']} - {subnet['last_host']}")
    
    # Supernet Aggregation
    print_subsection("Supernet Aggregation")
    networks = [
        "192.168.1.0/24",
        "192.168.2.0/24", 
        "192.168.3.0/24",
        "192.168.4.0/24"
    ]
    response = requests.post(f"{BASE_URL}/api/supernet-calc", json={
        "networks": networks
    })
    result = response.json()
    print(f"Input Networks: {', '.join(result['input_networks'])}")
    print(f"Aggregated Supernet: {', '.join(result['supernet'])}")

def demo_vlan_qos_analysis():
    """Demonstrate VLAN and QoS analysis"""
    print_section("VLAN & QoS ANALYSIS TOOLS")
    
    # VLAN Database Analysis
    print_subsection("VLAN Database Analysis")
    vlan_config = """vlan 10
 name DATA_VLAN
vlan 20
 name VOICE_VLAN
vlan 30
 name GUEST_VLAN
vlan 100
 name MGMT_VLAN
vlan 200
 name DMZ_VLAN"""
    
    response = requests.post(f"{BASE_URL}/api/vlan-analyze", json={
        "config": vlan_config
    })
    result = response.json()
    print(f"Total VLANs Found: {result['total_vlans']}")
    for vlan in result['vlans']:
        print(f"  VLAN {vlan['id']}: {vlan['name']}")
    
    # QoS Configuration Analysis
    print_subsection("QoS Configuration Analysis")
    qos_config = """class-map match-all VOICE
 match dscp ef
class-map match-all VIDEO
 match dscp af41
class-map match-all BUSINESS_CRITICAL
 match dscp af31
policy-map CORPORATE_QOS
 class VOICE
  priority percent 30
 class VIDEO
  bandwidth percent 25
 class BUSINESS_CRITICAL
  bandwidth percent 20
 class class-default
  fair-queue"""
    
    response = requests.post(f"{BASE_URL}/api/qos-analyze", json={
        "config": qos_config
    })
    result = response.json()
    analysis = result['analysis']
    print(f"Class Maps Found: {len(analysis['class_maps'])}")
    for cm in analysis['class_maps']:
        print(f"  - {cm}")
    print(f"Policy Maps Found: {len(analysis['policy_maps'])}")
    for pm in analysis['policy_maps']:
        print(f"  - {pm}")

def demo_ip_planning():
    """Demonstrate IP address planning"""
    print_section("IP ADDRESS PLANNING")
    
    networks = [
        "192.168.1.0/24",
        "10.0.0.0/8", 
        "172.16.0.0/12",
        "203.0.113.0/24",
        "8.8.8.0/24"
    ]
    
    response = requests.post(f"{BASE_URL}/api/ip-plan", json={
        "networks": networks
    })
    result = response.json()
    print(f"IP Address Plan for {result['total_networks']} networks:")
    print(f"{'Network':<18} {'Class':<12} {'Type':<8} {'Total IPs':<12} {'Usable':<12}")
    print("-" * 70)
    for plan in result['ip_plan']:
        print(f"{plan['network']:<18} {plan['network_class']:<12} {plan['type']:<8} {plan['size']:<12,} {plan['usable_hosts']:<12,}")

def demo_use_cases_overview():
    """Display comprehensive use cases overview"""
    print_section("100+ NETWORKING USE CASES OVERVIEW")
    
    response = requests.get(f"{BASE_URL}/api/use-cases")
    result = response.json()
    
    print(f"Total Categories: {result['total_categories']}")
    print(f"Total Use Cases: {result['total_use_cases']}")
    print("\nCategories and Tools:")
    
    for category, cases in result['use_cases'].items():
        category_name = category.replace('_', ' ').title()
        print(f"\n📂 {category_name} ({len(cases)} tools):")
        for i, case in enumerate(cases[:5], 1):  # Show first 5 of each category
            print(f"   {i}. {case}")
        if len(cases) > 5:
            print(f"   ... and {len(cases) - 5} more tools")

def demo_config_conversion():
    """Demonstrate configuration conversion"""
    print_section("CONFIGURATION CONVERSION")
    
    cisco_config = """interface GigabitEthernet0/1
 description Access port for workstation
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
!
interface GigabitEthernet0/24
 description Trunk to distribution switch
 switchport mode trunk
 switchport trunk allowed vlan 10,20"""
    
    response = requests.post(f"{BASE_URL}/api/config-convert", json={
        "source_config": cisco_config,
        "source_platform": "cisco_ios",
        "target_platform": "arista_eos"
    })
    result = response.json()
    
    print("Original Cisco IOS Configuration:")
    print(cisco_config)
    print("\nConverted to Arista EOS:")
    print(result['converted_config'])

def demo_ansible_examples():
    """Demonstrate Ansible Infrastructure as Code"""
    print_section("ANSIBLE INFRASTRUCTURE AS CODE")
    
    response = requests.get(f"{BASE_URL}/api/ansible-examples")
    examples = response.json()
    
    print("Available Ansible Examples:")
    for platform in examples.keys():
        platform_name = platform.replace('_', ' ').title()
        print(f"  📜 {platform_name}")
    
    print(f"\nSample Cisco IOS Playbook (excerpt):")
    playbook_lines = examples['cisco_ios']['playbook'].split('\n')[:15]
    for line in playbook_lines:
        print(f"  {line}")
    print("  ...")

def performance_test():
    """Test API performance with multiple requests"""
    print_section("PERFORMANCE TESTING")
    
    start_time = time.time()
    
    # Test multiple API calls
    apis = [
        ("Regex Test", f"{BASE_URL}/api/regex-test", {"pattern": r"\d+", "text": "test123", "flags": ""}),
        ("CIDR Calc", f"{BASE_URL}/api/cidr-calc", {"cidr": "192.168.1.0/24", "operation": "info"}),
        ("Security Analysis", f"{BASE_URL}/api/security-analyze", {"config": "password test", "type": "passwords"}),
        ("Protocol Analysis", f"{BASE_URL}/api/protocol-analyze", {"config": "router ospf 1", "protocol": "ospf"}),
        ("VLSM Calc", f"{BASE_URL}/api/vlsm-calc", {"network": "10.0.0.0/24", "requirements": [50, 25]})
    ]
    
    for name, url, data in apis:
        api_start = time.time()
        if data:
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        api_time = (time.time() - api_start) * 1000
        print(f"  {name:<20} - {api_time:.2f}ms - Status: {response.status_code}")
    
    total_time = time.time() - start_time
    print(f"\nTotal test time: {total_time:.3f} seconds")

def main():
    """Run comprehensive demo of all features"""
    print("🚀 NETWORK ENGINEERING TOOLKIT - COMPREHENSIVE DEMONSTRATION")
    print("This demo showcases 100+ networking use cases and advanced automation features")
    
    try:
        # Test basic connectivity
        response = requests.get(f"{BASE_URL}/api/use-cases")
        if response.status_code != 200:
            print("❌ ERROR: Could not connect to the toolkit.")
            print("Please ensure the application is running with: python app.py")
            return
        
        print("✅ Successfully connected to Network Engineering Toolkit")
        
        # Run all demonstrations
        demo_use_cases_overview()
        demo_core_features()
        demo_security_analysis() 
        demo_protocol_analysis()
        demo_advanced_calculations()
        demo_vlan_qos_analysis()
        demo_ip_planning()
        demo_config_conversion()
        demo_ansible_examples()
        performance_test()
        
        print_section("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("""
🌟 Key Highlights:
   • 100+ networking use cases across 10 categories
   • Advanced security analysis and compliance checking
   • Multi-vendor configuration conversion
   • Sophisticated network planning and optimization
   • Infrastructure as Code with Ansible examples
   • Real-time protocol analysis and diagnostics
   • Modern web interface with API access

🔗 Access the web interface at: http://localhost:5000
📚 API documentation available in README.md
💡 Ready for production network engineering workflows!
        """)
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the toolkit.")
        print("Please ensure the application is running with: python app.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()