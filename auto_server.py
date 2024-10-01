import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarkdownHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            generate_html()

def get_markdown_title(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()
        if first_line.startswith('# '):
            return first_line[2:]
        else:
            return os.path.splitext(os.path.basename(file_path))[0].replace('-', ' ')

def generate_html():
    with open('template.html', 'r') as template_file:
        template = template_file.read()
    
    sidebar_content = generate_sidebar_content('notes')
    index_content = generate_index_content('notes')
    
    # Generate index.html
    index_html = template.replace('{sidebar_content}', sidebar_content)
    index_html = index_html.replace('{note_title}', 'Notes')
    index_html = index_html.replace('{note_content}', index_content)
    
    with open('index.html', 'w') as index_file:
        index_file.write(index_html)
    
    print("Generated index.html")

def generate_sidebar_content(directory):
    content = "<ul>"
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                title = get_markdown_title(file_path)
                content += f'<li><a href="#" data-path="{relative_path}">{title}</a></li>\n'
    content += "</ul>"
    return content

def generate_index_content(directory):
    return ""  # Return an empty string instead of generating links

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