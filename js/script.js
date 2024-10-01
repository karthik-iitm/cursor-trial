document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const toggleButton = document.getElementById('toggle-sidebar');
    const noteTitle = document.getElementById('note-title');
    const noteContent = document.getElementById('note-content');
    const homeButton = document.getElementById('home-button');

    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('sidebar-collapsed');
    });

    // Load content based on the current URL
    loadContent(window.location.pathname);

    async function loadContent(path) {
        try {
            let fullPath = path;
            if (path === '/' || path === '/index' || path === '/index.html') {
                fullPath = '/index.html';
            } else if (!path.startsWith('/notes/') && !path.startsWith('/index')) {
                fullPath = '/notes/' + path;
            }
            if (!fullPath.endsWith('.html')) {
                fullPath += '.html';
            }
            console.log('Attempting to load:', fullPath);
            const response = await fetch(fullPath);
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const content = await response.text();
            
            const parser = new DOMParser();
            const doc = parser.parseFromString(content, 'text/html');
            const title = doc.getElementById('note-title').textContent;
            const noteContentElement = doc.getElementById('note-content').innerHTML;
            
            noteTitle.textContent = title;
            noteContent.innerHTML = noteContentElement;

            // Update sidebar links
            const sidebarContent = doc.getElementById('sidebar-content');
            if (sidebarContent) {
                document.getElementById('sidebar-content').innerHTML = sidebarContent.innerHTML;
            }

            // Fix image paths
            noteContent.querySelectorAll('img').forEach(img => {
                if (!img.src.startsWith('http')) {
                    img.src = `/notes/${img.getAttribute('src')}`;
                }
            });

            // Render math
            renderMathInElement(noteContent, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false},
                    {left: "\\(", right: "\\)", display: false},
                    {left: "\\[", right: "\\]", display: true}
                ],
                throwOnError: false
            });

            // Update URL without reloading the page
            history.pushState(null, '', path);
        } catch (error) {
            console.error('Error loading content:', error);
            noteContent.innerHTML = `<p>Error loading content: ${error.message}</p>`;
        }
    }

    // Add click events to sidebar links and prevent default behavior
    document.body.addEventListener('click', function(e) {
        if (e.target.tagName === 'A' && !e.target.id.includes('home-button')) {
            e.preventDefault();
            const path = e.target.getAttribute('href');
            loadContent(path);
        }
    });

    // Handle home button click
    homeButton.addEventListener('click', function(e) {
        e.preventDefault();
        loadContent('/index.html');
    });

    // Handle browser back/forward navigation
    window.addEventListener('popstate', function() {
        loadContent(window.location.pathname);
    });
});
