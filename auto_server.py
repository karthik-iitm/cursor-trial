import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarkdownHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            generate_html()

def generate_html():
    with open('template.html', 'r') as template_file:
        template = template_file.read()
    
    sidebar_content = generate_sidebar_content('notes')
    html_content = template.replace('{sidebar_content}', sidebar_content)
    
    with open('index.html', 'w') as index_file:
        index_file.write(html_content)
    
    print("Generated index.html")

def generate_sidebar_content(directory):
    content = "<ul>"
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                content += f'<li><a href="#" data-path="{relative_path}">{os.path.splitext(file)[0]}</a></li>\n'
    content += "</ul>"
    return content

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return SimpleHTTPRequestHandler.do_GET(self)

def run_server(port=8000):
    handler = CustomHandler
    httpd = HTTPServer(("", port), handler)
    print(f"Serving on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    generate_html()
    
    event_handler = MarkdownHandler()
    observer = Observer()
    observer.schedule(event_handler, path='notes', recursive=False)
    observer.start()

    try:
        run_server()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()