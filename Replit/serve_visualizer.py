import http.server
import socketserver
import webbrowser
import os

# Set the port
PORT = 8080

# Change to the directory containing the HTML file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a simple HTTP server
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print("Open your browser to view the Replit Assistant visualization")
    # Open the browser automatically
    webbrowser.open(f"http://localhost:{PORT}/system_prompt_visualizer.html")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")