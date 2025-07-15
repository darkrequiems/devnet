// Network Engineering Toolkit JavaScript

// Global variables
let ansibleExamples = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Load Ansible examples on page load
    fetchAnsibleExamples();
    
    // Set up navigation
    setupNavigation();
    
    // Add keyboard shortcuts
    setupKeyboardShortcuts();
});

// Navigation setup
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            if (target.startsWith('#')) {
                document.querySelector(target).scrollIntoView({
                    behavior: 'smooth'
                });
                
                // Update active nav link
                navLinks.forEach(nl => nl.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
}

// Keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case '1':
                    e.preventDefault();
                    document.querySelector('#regex-tool').scrollIntoView({ behavior: 'smooth' });
                    break;
                case '2':
                    e.preventDefault();
                    document.querySelector('#cidr-tool').scrollIntoView({ behavior: 'smooth' });
                    break;
                case '3':
                    e.preventDefault();
                    document.querySelector('#config-tool').scrollIntoView({ behavior: 'smooth' });
                    break;
                case '4':
                    e.preventDefault();
                    document.querySelector('#ansible-tool').scrollIntoView({ behavior: 'smooth' });
                    break;
            }
        }
    });
}

// Regex Tool Functions
function testRegex() {
    const pattern = document.getElementById('regex-pattern').value;
    const text = document.getElementById('regex-text').value;
    const flags = getRegexFlags();
    
    if (!pattern) {
        showMessage('regex-results', 'Please enter a regex pattern', 'error');
        return;
    }
    
    showLoadingSpinner('regex-results');
    
    fetch('/api/regex-test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            pattern: pattern,
            text: text,
            flags: flags
        })
    })
    .then(response => response.json())
    .then(data => {
        displayRegexResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('regex-results', 'An error occurred while testing regex', 'error');
    });
}

function getRegexFlags() {
    const flags = [];
    if (document.getElementById('flag-i').checked) flags.push('i');
    if (document.getElementById('flag-m').checked) flags.push('m');
    if (document.getElementById('flag-s').checked) flags.push('s');
    return flags.join('');
}

function displayRegexResults(data) {
    const resultsDiv = document.getElementById('regex-results');
    
    if (!data.success) {
        showMessage('regex-results', `Regex Error: ${data.error}`, 'error');
        return;
    }
    
    if (data.total_matches === 0) {
        showMessage('regex-results', 'No matches found', 'info');
        return;
    }
    
    let html = `
        <div class="success-message">
            <h5><i class="fas fa-check-circle me-2"></i>Found ${data.total_matches} match(es)</h5>
        </div>
        <div class="mt-3">
            <h6>Matches:</h6>
    `;
    
    data.matches.forEach((match, index) => {
        html += `
            <div class="match-highlight mb-2">
                <strong>Match ${index + 1}:</strong> "${match.match}"
                <br><small>Position: ${match.start}-${match.end}</small>
                ${match.groups.length > 0 ? `<br><small>Groups: [${match.groups.join(', ')}]</small>` : ''}
            </div>
        `;
    });
    
    html += '</div>';
    resultsDiv.innerHTML = html;
}

function loadRegexExamples() {
    const examples = [
        {
            name: 'IP Address',
            pattern: '(\\d{1,3}\\.){3}\\d{1,3}',
            text: 'Server IP: 192.168.1.1, Gateway: 10.0.0.1, DNS: 8.8.8.8'
        },
        {
            name: 'MAC Address',
            pattern: '([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})',
            text: 'Interface MAC addresses: 00:1B:44:11:3A:B7, aa-bb-cc-dd-ee-ff'
        },
        {
            name: 'VLAN Configuration',
            pattern: 'vlan\\s+(\\d+)',
            text: 'vlan 10\nvlan 20\nvlan 100\nswitchport access vlan 30'
        },
        {
            name: 'Interface Names',
            pattern: '(GigabitEthernet|FastEthernet|Ethernet)(\\d+/\\d+)',
            text: 'interface GigabitEthernet0/1\ninterface FastEthernet0/24\ninterface Ethernet1/1'
        }
    ];
    
    // Show examples in a modal or dropdown
    let html = '<div class="mt-3"><h6>Common Networking Regex Examples:</h6><div class="row">';
    
    examples.forEach(example => {
        html += `
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h6 class="card-title">${example.name}</h6>
                        <button class="btn btn-sm btn-outline-primary" onclick="loadRegexExample('${example.pattern}', '${example.text.replace(/'/g, "\\'")}')">
                            Use This Example
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div></div>';
    document.getElementById('regex-results').innerHTML = html;
}

function loadRegexExample(pattern, text) {
    document.getElementById('regex-pattern').value = pattern;
    document.getElementById('regex-text').value = text.replace(/\\n/g, '\n');
}

// CIDR Tool Functions
function calculateCIDR(operation) {
    const cidr = document.getElementById('cidr-input').value;
    
    if (!cidr) {
        showMessage('cidr-results', 'Please enter a CIDR network', 'error');
        return;
    }
    
    showLoadingSpinner('cidr-results');
    
    fetch('/api/cidr-calc', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            cidr: cidr,
            operation: operation
        })
    })
    .then(response => response.json())
    .then(data => {
        displayCIDRResults(data, operation);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('cidr-results', 'An error occurred while calculating CIDR', 'error');
    });
}

function displayCIDRResults(data, operation) {
    const resultsDiv = document.getElementById('cidr-results');
    
    if (!data.success) {
        showMessage('cidr-results', `CIDR Error: ${data.error}`, 'error');
        return;
    }
    
    if (operation === 'info') {
        let html = `
            <div class="success-message">
                <h5><i class="fas fa-info-circle me-2"></i>Network Information</h5>
            </div>
            <div class="network-info-grid">
        `;
        
        const infoItems = [
            { label: 'Network Address', value: data.network_address },
            { label: 'Broadcast Address', value: data.broadcast_address },
            { label: 'Subnet Mask', value: data.netmask },
            { label: 'Wildcard Mask', value: data.wildcard },
            { label: 'Prefix Length', value: `/${data.prefix_length}` },
            { label: 'Number of Hosts', value: data.num_hosts },
            { label: 'First Host', value: data.first_host },
            { label: 'Last Host', value: data.last_host },
            { label: 'Private Network', value: data.is_private ? 'Yes' : 'No' },
            { label: 'Multicast', value: data.is_multicast ? 'Yes' : 'No' }
        ];
        
        infoItems.forEach(item => {
            html += `
                <div class="info-item">
                    <div class="info-label">${item.label}</div>
                    <div class="info-value">${item.value}</div>
                </div>
            `;
        });
        
        html += '</div>';
        resultsDiv.innerHTML = html;
    } else if (operation === 'subnets') {
        let html = `
            <div class="success-message">
                <h5><i class="fas fa-sitemap me-2"></i>Subnet Information</h5>
                <p>Subnets with /${data.subnets[0].split('/')[1]} prefix length:</p>
            </div>
            <div class="subnet-list">
        `;
        
        data.subnets.forEach(subnet => {
            html += `<div class="subnet-item">${subnet}</div>`;
        });
        
        html += '</div>';
        resultsDiv.innerHTML = html;
    }
}

function setCIDR(cidr) {
    document.getElementById('cidr-input').value = cidr;
    calculateCIDR('info');
}

// Config Converter Functions
function convertConfig() {
    const sourceConfig = document.getElementById('source-config').value;
    const sourcePlatform = document.getElementById('source-platform').value;
    const targetPlatform = document.getElementById('target-platform').value;
    
    if (!sourceConfig.trim()) {
        showMessage('converted-config', 'Please enter source configuration', 'error');
        return;
    }
    
    if (sourcePlatform === targetPlatform) {
        showMessage('converted-config', 'Source and target platforms cannot be the same', 'error');
        return;
    }
    
    fetch('/api/config-convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            source_config: sourceConfig,
            source_platform: sourcePlatform,
            target_platform: targetPlatform
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('converted-config').value = data.converted_config;
            showMessage('converted-config', `Successfully converted from ${data.source_platform} to ${data.target_platform}`, 'success');
        } else {
            showMessage('converted-config', `Conversion Error: ${data.error}`, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('converted-config', 'An error occurred during conversion', 'error');
    });
}

function loadConfigExamples() {
    const examples = {
        cisco_ios: `! Sample Cisco IOS Configuration
hostname SW01
!
vlan 10
 name DATA_VLAN
vlan 20
 name VOICE_VLAN
!
interface GigabitEthernet0/1
 description Access port for workstation
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
!
interface GigabitEthernet0/24
 description Trunk to distribution switch
 switchport mode trunk
 switchport trunk allowed vlan 10,20`,
        
        cisco_nxos: `! Sample Cisco NX-OS Configuration
hostname NEXUS01
!
feature interface-vlan
feature vpc
!
vlan 10
  name WEB_SERVERS
vlan 20
  name DB_SERVERS
!
interface Ethernet1/1
  description Server connection
  switchport
  switchport mode access
  switchport access vlan 10`,
        
        arista_eos: `! Sample Arista EOS Configuration
hostname ARISTA01
!
vlan 10
   name DATA_VLAN
vlan 20
   name VOICE_VLAN
!
interface Ethernet1
   description Access port
   switchport access vlan 10
   spanning-tree portfast`
    };
    
    const sourcePlatform = document.getElementById('source-platform').value;
    if (examples[sourcePlatform]) {
        document.getElementById('source-config').value = examples[sourcePlatform];
    }
}

// Ansible Functions
function fetchAnsibleExamples() {
    fetch('/api/ansible-examples')
    .then(response => response.json())
    .then(data => {
        ansibleExamples = data;
    })
    .catch(error => {
        console.error('Error fetching Ansible examples:', error);
    });
}

function loadAnsibleExample() {
    const vendor = document.getElementById('vendor-select').value;
    const contentDiv = document.getElementById('ansible-content');
    
    if (!vendor || !ansibleExamples[vendor]) {
        contentDiv.style.display = 'none';
        return;
    }
    
    const example = ansibleExamples[vendor];
    
    // Update tab content
    document.getElementById('playbook-code').textContent = example.playbook;
    document.getElementById('inventory-code').textContent = example.inventory;
    document.getElementById('requirements-code').textContent = example.requirements;
    
    // Show content and trigger syntax highlighting
    contentDiv.style.display = 'block';
    
    // Re-run Prism highlighting
    if (window.Prism) {
        Prism.highlightAll();
    }
}

function downloadAnsibleFiles() {
    const vendor = document.getElementById('vendor-select').value;
    if (!vendor || !ansibleExamples[vendor]) {
        alert('Please select a vendor first');
        return;
    }
    
    const example = ansibleExamples[vendor];
    
    // Create and download files
    downloadFile(`${vendor}-playbook.yml`, example.playbook);
    downloadFile(`${vendor}-inventory.ini`, example.inventory);
    downloadFile(`${vendor}-requirements.yml`, example.requirements);
    
    showMessage('ansible-content', 'Files downloaded successfully!', 'success');
}

function downloadFile(filename, content) {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Utility Functions
function showMessage(containerId, message, type) {
    const container = document.getElementById(containerId);
    const className = type === 'error' ? 'error-message' : 
                     type === 'success' ? 'success-message' : 'info-message';
    
    container.innerHTML = `<div class="${className}">${message}</div>`;
}

function showLoadingSpinner(containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div class="text-center">
            <div class="loading-spinner me-2"></div>
            Loading...
        </div>
    `;
}

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Show success message
        const toast = document.createElement('div');
        toast.className = 'position-fixed top-0 end-0 p-3';
        toast.style.zIndex = '1050';
        toast.innerHTML = `
            <div class="toast show" role="alert">
                <div class="toast-body bg-success text-white">
                    <i class="fas fa-check me-2"></i>Copied to clipboard!
                </div>
            </div>
        `;
        document.body.appendChild(toast);
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 2000);
    });
}

// Add copy buttons to code blocks
document.addEventListener('DOMContentLoaded', function() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.innerHTML = '<i class="fas fa-copy"></i>';
        button.onclick = () => copyToClipboard(block.textContent);
        block.parentElement.style.position = 'relative';
        block.parentElement.appendChild(button);
    });
});