import os
import markdown
from http.server import SimpleHTTPRequestHandler, HTTPServer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

def get_markdown_title(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
    return first_line.lstrip('# ')

def generate_sidebar_content(directory):
    notes = [f for f in os.listdir(directory) if f.endswith('.md')]
    sidebar_items = []
    for note in notes:
        title = get_markdown_title(os.path.join(directory, note))
        link = note.replace('.md', '.html')
        sidebar_items.append(f'<li><a href="{link}">{title}</a></li>')
    return '<ul>' + '\n'.join(sidebar_items) + '</ul>'

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '/index' or self.path == '/index.html':
            self.path = '/index.html'
        elif self.path.startswith('/notes/'):
            # Serve files directly from the 'notes' directory
            self.path = self.path[1:]  # Remove leading slash
        elif self.path.endswith('.html'):
            # Convert .html request to .md and serve the content
            md_path = os.path.join('notes', self.path[1:].replace('.html', '.md'))
            if os.path.exists(md_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('template.html', 'r') as template_file:
                    template = template_file.read()
                with open(md_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()
                title = get_markdown_title(md_path)
                html_content = markdown.markdown(content)
                sidebar_content = generate_sidebar_content('notes')
                note_html = template.replace('{sidebar_content}', sidebar_content)
                note_html = note_html.replace('{note_title}', title)
                note_html = note_html.replace('{note_content}', html_content)
                self.wfile.write(note_html.encode())
                return
        return SimpleHTTPRequestHandler.do_GET(self)

def generate_html():
    with open('template.html', 'r') as template_file:
        template = template_file.read()
    
    sidebar_content = generate_sidebar_content('notes')
    index_content, index_title = generate_index_content('index.md')
    
    # Generate index.html
    index_html = template.replace('{sidebar_content}', sidebar_content)
    index_html = index_html.replace('{note_title}', index_title)
    index_html = index_html.replace('{note_content}', index_content)
    
    with open('index.html', 'w') as index_file:
        index_file.write(index_html)
    
    print("Generated index.html")

    # Generate HTML for each note
    for root, dirs, files in os.walk('notes'):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                generate_note_html(file_path)

def generate_index_content(index_file):
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
            title = 'Index'
            if lines and lines[0].startswith('# '):
                title = lines[0][2:].strip()
                content = '\n'.join(lines[1:])
            html_content = markdown.markdown(content)
            return html_content, title
    else:
        return "<p>Welcome to your notes!</p>", "Index"

def generate_note_html(file_path):
    with open('template.html', 'r') as template_file:
        template = template_file.read()
    
    sidebar_content = generate_sidebar_content('notes')
    with open(file_path, 'r', encoding='utf-8') as note_file:
        content = note_file.read()
        title = get_markdown_title(file_path)
    
    html_content = markdown.markdown(content)
    note_html = template.replace('{sidebar_content}', sidebar_content)
    note_html = note_html.replace('{note_title}', title)
    note_html = note_html.replace('{note_content}', html_content)
    
    output_path = file_path.replace('.md', '.html')
    with open(output_path, 'w') as output_file:
        output_file.write(note_html)
    
    print(f"Generated {output_path}")

def run_server(port=8000):
    handler = CustomHandler
    httpd = HTTPServer(("", port), handler)
    print(f"Serving on port {port}")
    httpd.serve_forever()

class MarkdownHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.md'):
            print(f"Markdown file modified: {event.src_path}")
            generate_html()

if __name__ == "__main__":
    generate_html()
    
    event_handler = MarkdownHandler()
    observer = Observer()
    observer.schedule(event_handler, path='notes', recursive=True)
    observer.schedule(event_handler, path='.', recursive=False)  # Watch for changes to index.md
    observer.start()

    try:
        run_server()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()