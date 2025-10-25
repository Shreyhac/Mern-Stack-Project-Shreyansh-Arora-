#!/usr/bin/env python3
"""
Simple demo server for Web to MCP extension
This replaces the complex Django backend for demo purposes
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import uuid
import base64
from urllib.parse import urlparse, parse_qs
import os
import time

# In-memory storage for captures
captures_storage = {}

class DemoHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/captures/create/':
            self.handle_create_capture()
        else:
            self.send_error(404, "Not Found")
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Web to MCP Demo Server - Running!')
        elif self.path.startswith('/mcp/capture/'):
            self.handle_mcp_capture()
        else:
            self.send_error(404, "Not Found")

    def handle_create_capture(self):
        """Handle capture creation"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Generate a proper capture ID with timestamp
            import time
            timestamp = int(time.time())
            capture_id = f"capture-{timestamp}-{uuid.uuid4().hex[:6]}"
            
            # Extract domain from website URL for better naming
            website_url = data.get('website_url', '')
            domain = urlparse(website_url).netloc.replace('www.', '') if website_url else 'unknown'
            domain_short = domain.split('.')[0] if '.' in domain else domain
            
            # Create a more meaningful reference ID
            reference_id = f"{domain_short}-{timestamp}-{uuid.uuid4().hex[:4]}"
            
            # Store capture data for MCP access
            capture_data = {
                "id": reference_id,
                "website_url": website_url,
                "token_count": data.get('token_count', 0),
                "html": data.get('html', ''),
                "screenshot": data.get('png_screenshot', ''),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "domain": domain
            }
            captures_storage[reference_id] = capture_data
            
            # Create response
            response = {
                "slug": reference_id,
                "id": reference_id,
                "website_url": website_url,
                "token_count": data.get('token_count', 0),
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "status": "success",
                "mcp_reference": reference_id,
                "agent_instruction": f"Use the web-to-mcp tool with reference {reference_id} to analyze the captured component from {domain}"
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
            print(f"✅ Demo capture created: {reference_id}")
            print(f"   Website: {website_url}")
            print(f"   Tokens: {data.get('token_count', 0)}")
            print(f"   MCP URL: http://localhost:8000/mcp/capture/{reference_id}")
            
        except Exception as e:
            print(f"❌ Error creating capture: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def handle_mcp_capture(self):
        """Handle MCP capture requests"""
        try:
            # Extract capture ID from path
            capture_id = self.path.split('/mcp/capture/')[-1]
            
            if capture_id in captures_storage:
                capture_data = captures_storage[capture_id]
                
                # Create MCP response
                mcp_response = {
                    "id": capture_data["id"],
                    "website_url": capture_data["website_url"],
                    "domain": capture_data["domain"],
                    "token_count": capture_data["token_count"],
                    "html": capture_data["html"],
                    "screenshot": capture_data["screenshot"],
                    "created_at": capture_data["created_at"],
                    "mcp_tool": "web-to-mcp",
                    "instruction": f"Analyze this captured component from {capture_data['domain']}",
                    "usage": f"Use this data to understand the component structure and styling"
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(mcp_response, indent=2).encode('utf-8'))
                
                print(f"🔗 MCP capture accessed: {capture_id}")
            else:
                self.send_error(404, f"Capture {capture_id} not found")
                
        except Exception as e:
            print(f"❌ Error accessing MCP capture: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Web to MCP Demo Server - Running!')
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        """Override to reduce log noise"""
        pass

def run_server(port=8000):
    """Start the demo server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DemoHandler)
    print(f"🚀 Starting Web to MCP Demo Server on port {port}")
    print(f"   Frontend: http://localhost:5174")
    print(f"   Backend API: http://localhost:{port}")
    print(f"   Extension will work with API calls!")
    print("   Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
