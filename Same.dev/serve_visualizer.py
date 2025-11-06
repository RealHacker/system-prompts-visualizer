import http.server
import socketserver
import webbrowser
import os

# Set the port for the server
PORT = 8000

# Change to the Same.dev directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a simple HTTP server
Handler = http.server.SimpleHTTPRequestHandler

# Start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("Open your browser to view the Same.dev System Prompt Visualizer")
    print("Press Ctrl+C to stop the server")
    
    # Try to automatically open the browser
    try:
        webbrowser.open(f"http://localhost:{PORT}/system_prompt_visualizer.html")
    except:
        pass
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")