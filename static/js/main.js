// Initialize AOS (Animate on Scroll)
AOS.init({ duration: 800, once: true });

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Set active nav link
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
});

// Live Announcements Ticker
async function loadNotices() {
    try {
        const response = await fetch('/api/noticeboard');
        const notices = await response.json();
        const ticker = document.getElementById('liveTicker');
        if (ticker && notices.length) {
            ticker.innerHTML = notices.map(n => `📢 ${n.title}: ${n.content}`).join(' • ');
        }
    } catch(error) {
        console.log('Error loading notices:', error);
    }
}

// Course Search
function initCourseSearch() {
    const searchInput = document.getElementById('courseSearch');
    if (searchInput) {
        let debounceTimer;
        searchInput.addEventListener('input', function(e) {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(async () => {
                const query = e.target.value;
                const resultsDiv = document.getElementById('searchResults');
                const allCoursesDiv = document.getElementById('allCourses');
                
                if (query.length > 1) {
                    try {
                        const response = await fetch(`/api/search-courses?q=${encodeURIComponent(query)}`);
                        const courses = await response.json();
                        
                        if (resultsDiv) {
                            if (courses.length > 0) {
                                resultsDiv.innerHTML = `
                                    <h3>Search Results (${courses.length})</h3>
                                    <div class="grid">
                                        ${courses.map(course => `
                                            <div class="card">
                                                <div class="card-content">
                                                    <span class="badge">${course.category}</span>
                                                    <h3>${course.name}</h3>
                                                    <p>${course.duration} | KES ${course.fee.toLocaleString()}</p>
                                                    <a href="/course/${course.id}" class="btn btn-primary">View Details →</a>
                                                </div>
                                            </div>
                                        `).join('')}
                                    </div>
                                `;
                                if (allCoursesDiv) allCoursesDiv.style.display = 'none';
                            } else {
                                resultsDiv.innerHTML = '<p>No courses found.</p>';
                            }
                        }
                    } catch(error) {
                        console.log('Search error:', error);
                    }
                } else if (query.length === 0) {
                    if (resultsDiv) resultsDiv.innerHTML = '';
                    if (allCoursesDiv) allCoursesDiv.style.display = 'block';
                }
            }, 300);
        });
    }
}

// M-Pesa Payment
function initMpesaPayment() {
    const mpesaBtn = document.getElementById('mpesaPayBtn');
    if (mpesaBtn) {
        mpesaBtn.addEventListener('click', function() {
            const studentId = this.getAttribute('data-student-id') || 'E2024001';
            alert(`M-Pesa Payment:\nPaybill: 123456\nAccount: ${studentId}\nComplete payment on your phone.`);
        });
    }
}

// Load all functions
document.addEventListener('DOMContentLoaded', function() {
    loadNotices();
    setInterval(loadNotices, 60000);
    initCourseSearch();
    initMpesaPayment();
});