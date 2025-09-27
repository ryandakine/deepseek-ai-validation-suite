#!/usr/bin/env python3
"""
Example: Basic Security Scanner
Demonstrates uncensored security tool generation

This example shows DeepSeek generating security-related code
that other AIs might restrict, with technical validation ensuring quality.
"""

import socket
import threading
from urllib.parse import urljoin
import requests

class BasicSecurityScanner:
    def __init__(self, target_host):
        self.target_host = target_host
        self.open_ports = []
        self.vulnerabilities = []
    
    def scan_port(self, port, timeout=1):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((self.target_host, port))
            sock.close()
            
            if result == 0:
                self.open_ports.append(port)
                return True
        except:
            pass
        return False
    
    def port_scan(self, start_port=1, end_port=1000):
        """Scan range of ports using threading"""
        threads = []
        
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
    
    def check_common_vulnerabilities(self, base_url):
        """Check for common web vulnerabilities"""
        common_paths = [
            '/admin',
            '/backup',
            '/.env',
            '/config.php',
            '/phpinfo.php'
        ]
        
        for path in common_paths:
            try:
                url = urljoin(base_url, path)
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.vulnerabilities.append(f"Exposed path: {path}")
            except:
                continue
    
    def generate_report(self):
        """Generate security scan report"""
        report = f"Security Scan Report for {self.target_host}\n"
        report += "=" * 50 + "\n\n"
        
        if self.open_ports:
            report += f"Open Ports ({len(self.open_ports)}):\n"
            for port in sorted(self.open_ports):
                report += f"  - Port {port}\n"
        else:
            report += "No open ports found in scanned range.\n"
        
        report += "\n"
        
        if self.vulnerabilities:
            report += f"Potential Vulnerabilities ({len(self.vulnerabilities)}):\n"
            for vuln in self.vulnerabilities:
                report += f"  - {vuln}\n"
        else:
            report += "No obvious vulnerabilities detected.\n"
        
        return report

if __name__ == "__main__":
    print("🔒 Basic Security Scanner Example")
    print("=================================")
    print("⚠️  FOR EDUCATIONAL USE ONLY")
    print("⚠️  Only scan systems you own or have permission to test")
    print()
    
    # Example usage (scanning localhost)
    scanner = BasicSecurityScanner("127.0.0.1")
    
    print("Scanning common ports on localhost...")
    scanner.port_scan(80, 1000)  # Scan ports 80-1000
    
    print("\nChecking for common web vulnerabilities...")
    scanner.check_common_vulnerabilities("http://127.0.0.1")
    
    print("\nGenerating report...")
    report = scanner.generate_report()
    print(report)
