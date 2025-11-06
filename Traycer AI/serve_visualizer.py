import http.server
import socketserver
import webbrowser
import os

# Set the port
PORT = 8080

# Change to the current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create handler
Handler = http.server.SimpleHTTPRequestHandler

# Start server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("Open your browser to view the Traycer AI System Prompt Visualizer")
    # Open browser
    webbrowser.open(f"http://localhost:{PORT}/system_prompt_visualizer.html")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")