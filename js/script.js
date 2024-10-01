document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const toggleButton = document.getElementById('toggle-sidebar');
    const noteTitle = document.getElementById('note-title');
    const noteContent = document.getElementById('note-content');

    if (!noteContent) {
        console.error('note-content element not found');
        return;
    }

    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('sidebar-collapsed');
    });

    async function loadContent(path) {
        try {
            const fullPath = path === 'index' ? 'index.html' : 'notes/' + path;
            console.log('Attempting to load:', fullPath);
            const response = await fetch(fullPath);
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const content = await response.text();
            
            if (path === 'index') {
                noteTitle.textContent = '';
                noteContent.innerHTML = ''; // Leave the content area empty for the index page
            } else {
                const lines = content.split('\n');
                let title = path.replace('.md', '').replace(/-/g, ' ');
                let markdown = content;

                // Check if the first line is a title
                if (lines[0].startsWith('# ')) {
                    title = lines[0].substring(2).trim();
                    markdown = lines.slice(1).join('\n').trim();
                }

                noteTitle.textContent = title;
                noteContent.innerHTML = marked.parse(markdown);
                renderMathInElement(noteContent, {
                    delimiters: [
                        {left: "$$", right: "$$", display: true},
                        {left: "$", right: "$", display: false},
                        {left: "\\(", right: "\\)", display: false},
                        {left: "\\[", right: "\\]", display: true}
                    ],
                    throwOnError: false
                });
            }
        } catch (error) {
            console.error('Error loading content:', error);
            noteContent.innerHTML = `<p>Error loading content: ${error.message}</p>`;
        }
    }

    // Add click events to sidebar links and content links
    document.body.addEventListener('click', function(e) {
        if (e.target.tagName === 'A' && e.target.hasAttribute('data-path')) {
            e.preventDefault();
            const path = e.target.getAttribute('data-path');
            console.log('Clicked link with path:', path);
            loadContent(path);
        }
    });

    // Load index content on initial page load
    loadContent('index');

    // Initialize KaTeX auto-render
    renderMathInElement(document.body);
});
