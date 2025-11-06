import http.server
import socketserver
import webbrowser
import os

# Set the directory to serve files from
directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(directory)

# Define the port
PORT = 8000

# Create handler
Handler = http.server.SimpleHTTPRequestHandler

# Start server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    # Open the browser
    webbrowser.open(f"http://localhost:{PORT}/system_prompt_visualizer.html")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")