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
            } else if (!path.startsWith('/notes/') && !path.startsWith('/')) {
                fullPath = '/notes/' + path;
            }
            if (!fullPath.endsWith('.html')) {
                fullPath += '.html';
            }

            // Prevent loading /notes/index.html
            if (fullPath === '/notes/index.html') {
                fullPath = '/index.html';
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
            const sidebarContentElement = doc.getElementById('sidebar-content');
            
            document.getElementById('note-title').textContent = title;
            document.getElementById('note-content').innerHTML = noteContentElement;

            // Update sidebar links
            if (sidebarContentElement) {
                document.getElementById('sidebar-content').innerHTML = sidebarContentElement.innerHTML;
            }

            // Update URL without reloading the page
            history.pushState(null, '', path);

            // Render math after content is loaded
            renderMath();
        } catch (error) {
            console.error('Error loading content:', error);
            document.getElementById('note-content').innerHTML = `<p>Error loading content: ${error.message}</p>`;
        }
    }

    function renderMath() {
        renderMathInElement(document.body, {
            delimiters: [
                {left: "$$", right: "$$", display: true},
                {left: "$", right: "$", display: false},
                {left: "\\(", right: "\\)", display: false},
                {left: "\\[", right: "\\]", display: true}
            ],
            throwOnError : false
        });
    }

    // Add click events to links and prevent default behavior for internal links
    document.body.addEventListener('click', function(e) {
        if (e.target.tagName === 'A') {
            const href = e.target.getAttribute('href');
            if (href.startsWith('http') || href.startsWith('https')) {
                // External link: allow default behavior
                return;
            }
            e.preventDefault();
            if (e.target.id === 'home-button') {
                loadContent('index.html');
            } else {
                loadContent(href);
            }
        }
    });

    // Handle home button click
    homeButton.addEventListener('click', function(e) {
        e.preventDefault();
        loadContent('/');
    });

    // Handle browser back/forward navigation
    window.addEventListener('popstate', function() {
        loadContent(window.location.pathname);
    });
});
