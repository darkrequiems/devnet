// Network Engineering Toolkit JavaScript - Enhanced with 100+ Use Cases

// Global variables
let ansibleExamples = {};
let allUseCases = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Load data on page load
    fetchAnsibleExamples();
    loadAllUseCases();
    
    // Set up navigation
    setupNavigation();
    
    // Add keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Initialize VLSM requirements
    initializeVLSMRequirements();
});

// Navigation setup
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link, .dropdown-item');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const target = this.getAttribute('href');
            if (target && target.startsWith('#')) {
                e.preventDefault();
                document.querySelector(target).scrollIntoView({
                    behavior: 'smooth'
                });
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
                    document.querySelector('#security-analyzer').scrollIntoView({ behavior: 'smooth' });
                    break;
                case '4':
                    e.preventDefault();
                    document.querySelector('#protocol-analyzer').scrollIntoView({ behavior: 'smooth' });
                    break;
            }
        }
    });
}

// ============================================================================
// ORIGINAL CORE FUNCTIONS
// ============================================================================

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

// ============================================================================
// NEW ENHANCED FUNCTIONS FOR 100+ USE CASES
// ============================================================================

// Security Analysis Functions
function analyzeSecurityConfig() {
    const config = document.getElementById('security-config').value;
    const analysisType = document.getElementById('security-type').value;
    
    if (!config.trim()) {
        showMessage('security-results', 'Please enter configuration to analyze', 'error');
        return;
    }
    
    showLoadingSpinner('security-results');
    
    fetch('/api/security-analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            config: config,
            type: analysisType
        })
    })
    .then(response => response.json())
    .then(data => {
        displaySecurityResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('security-results', 'An error occurred during security analysis', 'error');
    });
}

function displaySecurityResults(data) {
    const resultsDiv = document.getElementById('security-results');
    
    if (!data.success) {
        showMessage('security-results', `Security Analysis Error: ${data.error}`, 'error');
        return;
    }
    
    let html = `
        <div class="success-message">
            <h5><i class="fas fa-shield-alt me-2"></i>Security Analysis Complete</h5>
            <p>Found ${data.total_findings || data.total_issues || 0} security findings</p>
        </div>
    `;
    
    const findings = data.findings || data.issues || [];
    if (findings.length > 0) {
        html += '<div class="mt-3"><h6>Security Findings:</h6>';
        findings.forEach((finding, index) => {
            const severity = finding.severity || 'Info';
            const severityClass = severity === 'High' ? 'danger' : severity === 'Medium' ? 'warning' : 'info';
            
            html += `
                <div class="alert alert-${severityClass} mb-2">
                    <strong>Finding ${index + 1}:</strong> ${finding.issue || finding.type}<br>
                    <small><strong>Line:</strong> ${finding.line || 'N/A'}</small><br>
                    <small><strong>Recommendation:</strong> ${finding.recommendation}</small>
                </div>
            `;
        });
        html += '</div>';
    } else {
        html += '<div class="alert alert-success mt-3">No security issues found!</div>';
    }
    
    resultsDiv.innerHTML = html;
}

function loadSecurityExamples() {
    const examples = {
        passwords: `username admin password cisco123
enable secret admin
snmp-server community public ro
crypto key generate rsa general-keys modulus 1024`,
        acl: `access-list 100 permit ip any any
access-list 101 deny tcp any host 192.168.1.1 eq 22
access-list 101 permit ip any any
access-list 102 deny ip any any`
    };
    
    const analysisType = document.getElementById('security-type').value;
    if (examples[analysisType]) {
        document.getElementById('security-config').value = examples[analysisType];
    }
}

// Protocol Analysis Functions
function analyzeProtocolConfig() {
    const config = document.getElementById('protocol-config').value;
    const protocol = document.getElementById('protocol-type').value;
    
    if (!config.trim()) {
        showMessage('protocol-results', 'Please enter protocol configuration', 'error');
        return;
    }
    
    showLoadingSpinner('protocol-results');
    
    fetch('/api/protocol-analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            config: config,
            protocol: protocol
        })
    })
    .then(response => response.json())
    .then(data => {
        displayProtocolResults(data, protocol);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('protocol-results', 'An error occurred during protocol analysis', 'error');
    });
}

function displayProtocolResults(data, protocol) {
    const resultsDiv = document.getElementById('protocol-results');
    
    if (!data.success) {
        showMessage('protocol-results', `Protocol Analysis Error: ${data.error}`, 'error');
        return;
    }
    
    const analysis = data.analysis;
    let html = `
        <div class="success-message">
            <h5><i class="fas fa-sitemap me-2"></i>${protocol.toUpperCase()} Analysis Complete</h5>
        </div>
        <div class="mt-3">
    `;
    
    if (protocol === 'ospf') {
        html += `
            <div class="row">
                <div class="col-md-6">
                    <h6>OSPF Areas</h6>
                    <ul class="list-group">
                        ${analysis.areas.map(area => `<li class="list-group-item">Area ${area}</li>`).join('')}
                    </ul>
                </div>
                <div class="col-md-6">
                    <h6>Network Statements</h6>
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr><th>Network</th><th>Wildcard</th><th>Area</th></tr>
                            </thead>
                            <tbody>
                                ${analysis.interfaces.map(intf => 
                                    `<tr><td>${intf.network}</td><td>${intf.wildcard}</td><td>${intf.area}</td></tr>`
                                ).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    } else if (protocol === 'bgp') {
        html += `
            <div class="row">
                <div class="col-md-6">
                    <h6>BGP Configuration</h6>
                    <p><strong>AS Number:</strong> ${analysis.asn || 'Not found'}</p>
                </div>
                <div class="col-md-6">
                    <h6>BGP Neighbors</h6>
                    <div class="table-responsive">
                        <table class="table table-sm">
                            <thead>
                                <tr><th>Neighbor IP</th><th>Remote AS</th></tr>
                            </thead>
                            <tbody>
                                ${analysis.neighbors.map(neighbor => 
                                    `<tr><td>${neighbor.ip}</td><td>${neighbor.remote_as}</td></tr>`
                                ).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
    }
    
    html += '</div>';
    resultsDiv.innerHTML = html;
}

function loadProtocolExamples() {
    const examples = {
        ospf: `router ospf 1
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
 network 192.168.2.0 0.0.0.255 area 1
 area 1 nssa`,
        bgp: `router bgp 65001
 bgp router-id 1.1.1.1
 neighbor 192.168.1.2 remote-as 65002
 neighbor 192.168.1.3 remote-as 65003
 network 10.0.0.0 mask 255.0.0.0`
    };
    
    const protocolType = document.getElementById('protocol-type').value;
    if (examples[protocolType]) {
        document.getElementById('protocol-config').value = examples[protocolType];
    }
}

// VLSM Calculator Functions
function initializeVLSMRequirements() {
    // Add initial requirement field if none exist
    const container = document.getElementById('vlsm-requirements');
    if (!container.children.length) {
        addVLSMRequirement();
    }
}

function addVLSMRequirement() {
    const container = document.getElementById('vlsm-requirements');
    const div = document.createElement('div');
    div.className = 'input-group mb-2';
    div.innerHTML = `
        <input type="number" class="form-control" placeholder="Number of hosts needed">
        <button class="btn btn-outline-danger" type="button" onclick="removeVLSMRequirement(this)">
            <i class="fas fa-trash"></i>
        </button>
    `;
    container.appendChild(div);
}

function removeVLSMRequirement(button) {
    const container = document.getElementById('vlsm-requirements');
    if (container.children.length > 1) {
        button.parentElement.remove();
    }
}

function setVLSMExample(requirements) {
    const container = document.getElementById('vlsm-requirements');
    container.innerHTML = '';
    
    requirements.forEach(req => {
        const div = document.createElement('div');
        div.className = 'input-group mb-2';
        div.innerHTML = `
            <input type="number" class="form-control" value="${req}">
            <button class="btn btn-outline-danger" type="button" onclick="removeVLSMRequirement(this)">
                <i class="fas fa-trash"></i>
            </button>
        `;
        container.appendChild(div);
    });
    
    document.getElementById('vlsm-network').value = '192.168.1.0/24';
}

function calculateVLSM() {
    const network = document.getElementById('vlsm-network').value;
    const requirementInputs = document.querySelectorAll('#vlsm-requirements input[type="number"]');
    const requirements = Array.from(requirementInputs).map(input => parseInt(input.value)).filter(val => !isNaN(val) && val > 0);
    
    if (!network) {
        showMessage('vlsm-results', 'Please enter a base network', 'error');
        return;
    }
    
    if (requirements.length === 0) {
        showMessage('vlsm-results', 'Please enter at least one subnet requirement', 'error');
        return;
    }
    
    showLoadingSpinner('vlsm-results');
    
    fetch('/api/vlsm-calc', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            network: network,
            requirements: requirements
        })
    })
    .then(response => response.json())
    .then(data => {
        displayVLSMResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('vlsm-results', 'An error occurred during VLSM calculation', 'error');
    });
}

function displayVLSMResults(data) {
    const resultsDiv = document.getElementById('vlsm-results');
    
    if (!data.success) {
        showMessage('vlsm-results', `VLSM Error: ${data.error}`, 'error');
        return;
    }
    
    let html = `
        <div class="success-message">
            <h5><i class="fas fa-calculator me-2"></i>VLSM Calculation Complete</h5>
            <p>Base Network: ${data.base_network} | Subnets Generated: ${data.total_subnets}</p>
        </div>
        <div class="mt-3">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Subnet</th>
                            <th>Hosts Needed</th>
                            <th>Hosts Available</th>
                            <th>First Host</th>
                            <th>Last Host</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    data.subnets.forEach((subnet, index) => {
        html += `
            <tr>
                <td><code>${subnet.network}</code></td>
                <td>${subnet.hosts_needed}</td>
                <td>${subnet.hosts_available}</td>
                <td><code>${subnet.first_host}</code></td>
                <td><code>${subnet.last_host}</code></td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = html;
}

// Supernet Calculator Functions
function calculateSupernet() {
    const networksText = document.getElementById('supernet-networks').value;
    const networks = networksText.split('\n').map(line => line.trim()).filter(line => line);
    
    if (networks.length < 2) {
        showMessage('supernet-results', 'Please enter at least 2 networks to aggregate', 'error');
        return;
    }
    
    showLoadingSpinner('supernet-results');
    
    fetch('/api/supernet-calc', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            networks: networks
        })
    })
    .then(response => response.json())
    .then(data => {
        displaySupernetResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('supernet-results', 'An error occurred during supernet calculation', 'error');
    });
}

function displaySupernetResults(data) {
    const resultsDiv = document.getElementById('supernet-results');
    
    if (!data.success) {
        showMessage('supernet-results', `Supernet Error: ${data.error}`, 'error');
        return;
    }
    
    let html = `
        <div class="success-message">
            <h5><i class="fas fa-compress me-2"></i>Supernet Calculation Complete</h5>
        </div>
        <div class="mt-3">
            <div class="row">
                <div class="col-md-6">
                    <h6>Input Networks</h6>
                    <ul class="list-group">
                        ${data.input_networks.map(net => `<li class="list-group-item"><code>${net}</code></li>`).join('')}
                    </ul>
                </div>
                <div class="col-md-6">
                    <h6>Aggregated Supernet(s)</h6>
                    <ul class="list-group">
                        ${data.supernet.map(net => `<li class="list-group-item"><code class="text-success">${net}</code></li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = html;
}

// VLAN Analyzer Functions
function analyzeVLANConfig() {
    const config = document.getElementById('vlan-config').value;
    
    if (!config.trim()) {
        showMessage('vlan-results', 'Please enter VLAN configuration', 'error');
        return;
    }
    
    showLoadingSpinner('vlan-results');
    
    fetch('/api/vlan-analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            config: config
        })
    })
    .then(response => response.json())
    .then(data => {
        displayVLANResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('vlan-results', 'An error occurred during VLAN analysis', 'error');
    });
}

function displayVLANResults(data) {
    const resultsDiv = document.getElementById('vlan-results');
    
    if (!data.success) {
        showMessage('vlan-results', `VLAN Analysis Error: ${data.error}`, 'error');
        return;
    }
    
    let html = `
        <div class="success-message">
            <h5><i class="fas fa-layer-group me-2"></i>VLAN Analysis Complete</h5>
            <p>Total VLANs Found: ${data.total_vlans}</p>
        </div>
    `;
    
    if (data.vlans.length > 0) {
        html += `
            <div class="mt-3">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>VLAN ID</th>
                                <th>VLAN Name</th>
                            </tr>
                        </thead>
                        <tbody>
        `;
        
        data.vlans.forEach(vlan => {
            html += `
                <tr>
                    <td><span class="badge bg-primary">${vlan.id}</span></td>
                    <td>${vlan.name}</td>
                </tr>
            `;
        });
        
        html += `
                        </tbody>
                    </table>
                </div>
            </div>
        `;
    }
    
    resultsDiv.innerHTML = html;
}

function loadVLANExamples() {
    const example = `vlan 10
 name DATA_VLAN
vlan 20
 name VOICE_VLAN
vlan 30
 name GUEST_VLAN
vlan 100
 name MGMT_VLAN
vlan 200
 name DMZ_VLAN`;
    
    document.getElementById('vlan-config').value = example;
}

// QoS Analyzer Functions
function analyzeQoSConfig() {
    const config = document.getElementById('qos-config').value;
    
    if (!config.trim()) {
        showMessage('qos-results', 'Please enter QoS configuration', 'error');
        return;
    }
    
    showLoadingSpinner('qos-results');
    
    fetch('/api/qos-analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            config: config
        })
    })
    .then(response => response.json())
    .then(data => {
        displayQoSResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('qos-results', 'An error occurred during QoS analysis', 'error');
    });
}

function displayQoSResults(data) {
    const resultsDiv = document.getElementById('qos-results');
    
    if (!data.success) {
        showMessage('qos-results', `QoS Analysis Error: ${data.error}`, 'error');
        return;
    }
    
    const analysis = data.analysis;
    let html = `
        <div class="success-message">
            <h5><i class="fas fa-tachometer-alt me-2"></i>QoS Analysis Complete</h5>
        </div>
        <div class="mt-3">
            <div class="row">
                <div class="col-md-6">
                    <h6>Class Maps</h6>
                    <ul class="list-group">
                        ${analysis.class_maps.map(cm => `<li class="list-group-item">${cm}</li>`).join('') || '<li class="list-group-item text-muted">No class maps found</li>'}
                    </ul>
                </div>
                <div class="col-md-6">
                    <h6>Policy Maps</h6>
                    <ul class="list-group">
                        ${analysis.policy_maps.map(pm => `<li class="list-group-item">${pm}</li>`).join('') || '<li class="list-group-item text-muted">No policy maps found</li>'}
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = html;
}

function loadQoSExamples() {
    const example = `class-map match-all VOICE
 match dscp ef
class-map match-all VIDEO
 match dscp af41
policy-map QOS_POLICY
 class VOICE
  priority percent 30
 class VIDEO
  bandwidth percent 25
 class class-default
  fair-queue`;
    
    document.getElementById('qos-config').value = example;
}

// IP Planning Functions
function generateIPPlan() {
    const networksText = document.getElementById('ip-networks').value;
    const networks = networksText.split('\n').map(line => line.trim()).filter(line => line);
    
    if (networks.length === 0) {
        showMessage('ip-plan-results', 'Please enter at least one network', 'error');
        return;
    }
    
    showLoadingSpinner('ip-plan-results');
    
    fetch('/api/ip-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            networks: networks
        })
    })
    .then(response => response.json())
    .then(data => {
        displayIPPlanResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('ip-plan-results', 'An error occurred during IP plan generation', 'error');
    });
}

function displayIPPlanResults(data) {
    const resultsDiv = document.getElementById('ip-plan-results');
    
    if (!data.success) {
        showMessage('ip-plan-results', `IP Plan Error: ${data.error}`, 'error');
        return;
    }
    
    let html = `
        <div class="success-message">
            <h5><i class="fas fa-map me-2"></i>IP Address Plan Generated</h5>
            <p>Total Networks: ${data.total_networks}</p>
        </div>
        <div class="mt-3">
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Network</th>
                            <th>Class</th>
                            <th>Type</th>
                            <th>Total IPs</th>
                            <th>Usable Hosts</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    data.ip_plan.forEach(plan => {
        html += `
            <tr>
                <td><code>${plan.network}</code></td>
                <td><span class="badge bg-info">${plan.network_class}</span></td>
                <td><span class="badge bg-${plan.type === 'Private' ? 'success' : 'warning'}">${plan.type}</span></td>
                <td>${plan.size.toLocaleString()}</td>
                <td>${plan.usable_hosts.toLocaleString()}</td>
            </tr>
        `;
    });
    
    html += `
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    resultsDiv.innerHTML = html;
}

// Use Cases Functions
function loadAllUseCases() {
    fetch('/api/use-cases')
    .then(response => response.json())
    .then(data => {
        allUseCases = data;
        displayUseCasesOverview(data);
    })
    .catch(error => {
        console.error('Error loading use cases:', error);
    });
}

function displayUseCasesOverview(data) {
    const contentDiv = document.getElementById('use-cases-content');
    
    if (!data.success) {
        contentDiv.innerHTML = '<div class="alert alert-danger">Failed to load use cases</div>';
        return;
    }
    
    let html = `
        <div class="alert alert-info">
            <h5><i class="fas fa-info-circle me-2"></i>Comprehensive Networking Toolkit</h5>
            <p>This toolkit includes <strong>${data.total_use_cases}</strong> networking use cases across <strong>${data.total_categories}</strong> categories.</p>
        </div>
        <div class="accordion" id="useCasesAccordion">
    `;
    
    Object.entries(data.use_cases).forEach(([category, cases], index) => {
        const categoryName = category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        const collapseId = `collapse${index}`;
        
        html += `
            <div class="accordion-item">
                <h2 class="accordion-header" id="heading${index}">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#${collapseId}">
                        <i class="fas fa-layer-group me-2"></i>
                        ${categoryName} (${cases.length} tools)
                    </button>
                </h2>
                <div id="${collapseId}" class="accordion-collapse collapse" data-bs-parent="#useCasesAccordion">
                    <div class="accordion-body">
                        <div class="row">
        `;
        
        cases.forEach(useCase => {
            html += `
                <div class="col-md-6 mb-2">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-check-circle text-success me-2"></i>
                        <span>${useCase}</span>
                    </div>
                </div>
            `;
        });
        
        html += `
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    contentDiv.innerHTML = html;
}

// ============================================================================
// ORIGINAL FUNCTIONS (Config Converter, Ansible, etc.)
// ============================================================================

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

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

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