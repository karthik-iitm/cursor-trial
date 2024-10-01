import os
import json
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class MyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        SimpleHTTPRequestHandler.end_headers(self)

def generate_sidebar_structure(root_dir):
    structure = {}
    for root, dirs, files in os.walk(root_dir):
        current = structure
        path = root.split(os.sep)[1:]  # Skip the root directory
        for folder in path:
            current = current.setdefault(folder, {})
        for file in files:
            if file.endswith('.md'):
                name = os.path.splitext(file)[0]
                file_path = os.path.join(root, file).replace('\\', '/')
                current[name] = file_path
    return structure

def generate_sidebar_html(structure, level=0):
    html = '<ul>' if level == 0 else ''
    for key, value in sorted(structure.items()):
        if isinstance(value, dict):
            html += f'<li>{key}{generate_sidebar_html(value, level + 1)}</li>'
        else:
            html += f'<li><a href="#" data-path="{value}">{key}</a></li>'
    html += '</ul>' if level == 0 else ''
    return html

def generate_html():
    notes_dir = 'notes'
    sidebar_structure = generate_sidebar_structure(notes_dir)
    sidebar_html = generate_sidebar_html(sidebar_structure)

    with open('template.html', 'r') as f:
        template = f.read()

    index_content = template.replace('{sidebar_content}', sidebar_html)
    index_content = index_content.replace('{sidebar_structure}', json.dumps(sidebar_structure))

    with open('index.html', 'w') as f:
        f.write(index_content)

    print("HTML generated")

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            print(f"Change detected in {event.src_path}")
            generate_html()

def watch_files():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='notes', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Server running on http://localhost:8000')
    httpd.serve_forever()

def generate_sidebar_content(directory):
    content = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                content += f'<li><a href="#" data-path="{relative_path}">{os.path.splitext(file)[0]}</a></li>\n'
    print("Generated sidebar content:", content)  # Debug print
    return content

if __name__ == '__main__':
    generate_html()
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    watch_files()
