#!/usr/bin/env python3
"""
Network Engineering Toolkit - Demo Script
This script demonstrates how to use the networking toolkit programmatically.
"""

import requests
import json

# Base URL for the toolkit
BASE_URL = "http://localhost:5000"

def demo_regex_testing():
    """Demonstrate regex pattern testing functionality"""
    print("=" * 60)
    print("REGEX PATTERN TESTING DEMO")
    print("=" * 60)
    
    # Test IP address extraction
    response = requests.post(f"{BASE_URL}/api/regex-test", json={
        "pattern": r"(\d{1,3}\.){3}\d{1,3}",
        "text": "Router 1: 192.168.1.1, Router 2: 10.0.0.1, DNS: 8.8.8.8",
        "flags": ""
    })
    
    result = response.json()
    print(f"Pattern: IP Address Regex")
    print(f"Text: Router 1: 192.168.1.1, Router 2: 10.0.0.1, DNS: 8.8.8.8")
    print(f"Matches Found: {result['total_matches']}")
    for i, match in enumerate(result['matches'], 1):
        print(f"  Match {i}: {match['match']} (position {match['start']}-{match['end']})")
    print()

def demo_cidr_calculations():
    """Demonstrate CIDR network calculations"""
    print("=" * 60)
    print("CIDR NETWORK CALCULATIONS DEMO")
    print("=" * 60)
    
    # Test network information
    response = requests.post(f"{BASE_URL}/api/cidr-calc", json={
        "cidr": "172.16.0.0/12",
        "operation": "info"
    })
    
    result = response.json()
    print(f"Network: 172.16.0.0/12")
    print(f"Network Address: {result['network_address']}")
    print(f"Broadcast Address: {result['broadcast_address']}")
    print(f"Subnet Mask: {result['netmask']}")
    print(f"Wildcard Mask: {result['wildcard']}")
    print(f"Number of Hosts: {result['num_hosts']}")
    print(f"First Host: {result['first_host']}")
    print(f"Last Host: {result['last_host']}")
    print(f"Private Network: {result['is_private']}")
    print()

def demo_config_conversion():
    """Demonstrate configuration conversion"""
    print("=" * 60)
    print("CONFIGURATION CONVERSION DEMO")
    print("=" * 60)
    
    cisco_config = """interface GigabitEthernet0/1
 description Access port for workstation
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast"""
    
    response = requests.post(f"{BASE_URL}/api/config-convert", json={
        "source_config": cisco_config,
        "source_platform": "cisco_ios",
        "target_platform": "arista_eos"
    })
    
    result = response.json()
    print("Source Configuration (Cisco IOS):")
    print(cisco_config)
    print("\nConverted Configuration (Arista EOS):")
    print(result['converted_config'])
    print()

def demo_ansible_examples():
    """Demonstrate Ansible examples retrieval"""
    print("=" * 60)
    print("ANSIBLE INFRASTRUCTURE AS CODE DEMO")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/ansible-examples")
    examples = response.json()
    
    print("Available Ansible Examples:")
    for platform in examples.keys():
        print(f"  - {platform.replace('_', ' ').title()}")
    
    print(f"\nSample Cisco IOS Playbook (first 10 lines):")
    playbook_lines = examples['cisco_ios']['playbook'].split('\n')[:10]
    for line in playbook_lines:
        print(f"  {line}")
    print("  ...")
    print()

def main():
    """Run all demos"""
    print("NETWORK ENGINEERING TOOLKIT - DEMONSTRATION")
    print("This demo showcases the key features of the toolkit\n")
    
    try:
        demo_regex_testing()
        demo_cidr_calculations()
        demo_config_conversion()
        demo_ansible_examples()
        
        print("=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Access the web interface at: http://localhost:5000")
        print("API Documentation available in README.md")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the toolkit.")
        print("Please ensure the application is running with: python app.py")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()