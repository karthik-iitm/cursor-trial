document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const toggleButton = document.getElementById('toggle-sidebar');

    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('sidebar-collapsed');
    });

    // Function to load content
    async function loadContent(path) {
        try {
            const fullPath = 'notes/' + path;
            console.log('Attempting to load:', fullPath);
            const response = await fetch(fullPath);
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const markdown = await response.text();
            console.log('Markdown content:', markdown.substring(0, 100) + '...'); // Log the first 100 characters
            
            if (typeof marked === 'undefined') {
                throw new Error('Marked library is not loaded');
            }
            
            document.getElementById('note-content').innerHTML = marked.parse(markdown);
            renderMathInElement(document.getElementById('note-content'), {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ],
                throwOnError: false
            });
        } catch (error) {
            console.error('Error loading content:', error);
            document.getElementById('note-content').innerHTML = `<p>Error loading content: ${error.message}</p>`;
        }
    }

    // Add click events to sidebar links
    document.querySelectorAll('#sidebar-content a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const path = link.getAttribute('data-path');
            console.log('Clicked link with path:', path);
            loadContent(path);
        });
    });

    // Initialize KaTeX auto-render
    renderMathInElement(document.body);
});
