# Network Engineering Toolkit

A comprehensive web-based tool for network engineers to handle common networking tasks, configuration conversions, and Infrastructure as Code examples with Ansible.

## Features

### 🔍 Regex Pattern Tester
- Test regex patterns against network configuration text
- Support for common regex flags (ignore case, multiline, dotall)
- Pre-built examples for common networking patterns:
  - IP addresses
  - MAC addresses
  - VLAN configurations
  - Interface names
- Visual highlighting of matches with position information

### 🌐 CIDR Calculator
- Calculate network information from CIDR notation
- Display network address, broadcast address, subnet mask, wildcard mask
- Show number of hosts, first/last host addresses
- Generate subnets with next prefix length
- Quick examples for common private networks

### 🔄 Configuration Converter
- Convert network configurations between different platforms:
  - Cisco IOS ↔ Arista EOS
  - Cisco NX-OS → Arista EOS
  - Cisco IOS → Juniper JunOS
- Pre-loaded example configurations for each platform
- Real-time conversion with error handling

### 📜 Ansible Infrastructure as Code Examples
- Complete Ansible playbooks for different network vendors:
  - Cisco IOS
  - Cisco NX-OS
  - Arista EOS
- Includes inventory files and requirements
- Ready-to-use examples for VLAN management, interface configuration
- Download functionality for all files

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd network-engineering-toolkit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the toolkit**
   Open your web browser and navigate to `http://localhost:5000`

### Docker Installation (Optional)

```bash
# Build the Docker image
docker build -t network-toolkit .

# Run the container
docker run -p 5000:5000 network-toolkit
```

## Usage Examples

### Regex Pattern Testing
1. Navigate to the Regex tool
2. Enter a pattern like `(\d{1,3}\.){3}\d{1,3}` for IP addresses
3. Paste network configuration text
4. Click "Test Regex" to see matches

### CIDR Calculations
1. Go to the CIDR Calculator
2. Enter a network like `192.168.1.0/24`
3. Click "Get Network Info" for detailed information
4. Use "Show Subnets" to see subnet breakdown

### Configuration Conversion
1. Select source and target platforms
2. Paste or load example configuration
3. Click "Convert Configuration"
4. Review the converted output

### Ansible Examples
1. Select a vendor from the dropdown
2. Browse through Playbook, Inventory, and Requirements tabs
3. Download the files for your infrastructure

## API Endpoints

### `/api/regex-test` (POST)
Test regex patterns against text.

**Request Body:**
```json
{
  "pattern": "regex_pattern",
  "text": "text_to_test",
  "flags": "regex_flags"
}
```

### `/api/cidr-calc` (POST)
Calculate CIDR network information.

**Request Body:**
```json
{
  "cidr": "192.168.1.0/24",
  "operation": "info|subnets"
}
```

### `/api/config-convert` (POST)
Convert network configurations between platforms.

**Request Body:**
```json
{
  "source_config": "configuration_text",
  "source_platform": "cisco_ios",
  "target_platform": "arista_eos"
}
```

### `/api/ansible-examples` (GET)
Retrieve Ansible examples for all supported platforms.

## Supported Platforms

### Configuration Conversion
- **Cisco IOS** - Traditional Cisco router/switch OS
- **Cisco NX-OS** - Cisco Nexus data center switches
- **Arista EOS** - Arista switches and routers
- **Juniper JunOS** - Juniper network devices (basic support)

### Ansible Support
- **Cisco IOS** - Full playbook examples with VLANs and interfaces
- **Cisco NX-OS** - NX-OS specific features like VPC
- **Arista EOS** - EOS configuration management

## Common Use Cases

### Network Documentation
- Extract IP addresses from configuration files
- Parse VLAN information with regex
- Calculate subnet ranges for documentation

### Migration Projects
- Convert configurations when migrating between vendors
- Validate configuration syntax across platforms
- Generate Ansible playbooks for automated deployment

### Infrastructure as Code
- Use provided Ansible examples as templates
- Automate network configuration management
- Implement GitOps workflows for network changes

## Advanced Features

### Keyboard Shortcuts
- `Ctrl+1` - Jump to Regex tool
- `Ctrl+2` - Jump to CIDR calculator
- `Ctrl+3` - Jump to Config converter
- `Ctrl+4` - Jump to Ansible examples

### Copy Functionality
- Click copy buttons on code blocks
- Automatic clipboard integration
- Success notifications

## Extending the Toolkit

### Adding New Platform Converters
1. Extend the `NetworkingTools` class in `app.py`
2. Add conversion methods following the pattern `_source_to_target`
3. Update the `converter_map` dictionary
4. Add example configurations in the frontend

### Adding Ansible Examples
1. Add new platform data to the `ansible_examples` endpoint
2. Include playbook, inventory, and requirements files
3. Update the frontend dropdown options

## Troubleshooting

### Common Issues

**Flask app won't start:**
- Ensure Python 3.8+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`

**Regex patterns not working:**
- Use double backslashes for escape characters in the web interface
- Test with simple patterns first

**Configuration conversion errors:**
- Ensure source and target platforms are different
- Check that the conversion path is supported

**Ansible examples not loading:**
- Check browser console for JavaScript errors
- Ensure the Flask backend is running properly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Include tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, feature requests, or questions:
- Create an issue in the repository
- Check existing documentation
- Review the API endpoints for integration needs

---

**Built for Network Engineers, by Network Engineers** 🚀