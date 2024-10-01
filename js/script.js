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
            console.log('Attempting to load:', path);
            const response = await fetch(path);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const markdown = await response.text();
            console.log('Markdown content:', markdown);
            document.getElementById('note-content').innerHTML = marked.parse(markdown);
            renderMathInElement(document.getElementById('note-content'));
        } catch (error) {
            console.error('Error loading content:', error);
            document.getElementById('note-content').innerHTML = '<p>Error loading content. Please try again.</p>';
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
