import os
import json
import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'embu_college_secret_key_2024')
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')

# Data files (simple JSON storage for demo)
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize sample data
def init_data():
    if not os.path.exists(os.path.join(DATA_DIR, 'courses.json')):
        courses = [
            {'id': 1, 'name': 'Diploma in ICT', 'category': 'ICT', 'duration': '2 years', 'fee': 45000, 'description': 'Software development, networking, database management'},
            {'id': 2, 'name': 'Certificate in Business Management', 'category': 'Business', 'duration': '1 year', 'fee': 35000, 'description': 'Accounting, marketing, entrepreneurship'},
            {'id': 3, 'name': 'Diploma in Engineering (Civil)', 'category': 'Engineering', 'duration': '3 years', 'fee': 55000, 'description': 'Structural design, construction management'},
            {'id': 4, 'name': 'Certificate in Hospitality', 'category': 'Hospitality', 'duration': '1 year', 'fee': 38000, 'description': 'Food production, front office, housekeeping'},
            {'id': 5, 'name': 'Diploma in Automotive Engineering', 'category': 'Automotive', 'duration': '3 years', 'fee': 52000, 'description': 'Vehicle diagnostics, repair, maintenance'},
            {'id': 6, 'name': 'Certificate in Beauty Therapy', 'category': 'Beauty', 'duration': '1 year', 'fee': 32000, 'description': 'Makeup, skincare, salon management'},
        ]
        save_data('courses.json', courses)
    
    if not os.path.exists(os.path.join(DATA_DIR, 'news.json')):
        news = [
            {'id': 1, 'title': 'Applications Open for May 2024 Intake', 'date': '2024-03-15', 'content': 'Admissions for May intake now open. Apply by April 30th.'},
            {'id': 2, 'title': 'Embu College Wins Innovation Award', 'date': '2024-02-10', 'content': 'Recognized for best technical training institution in Eastern Kenya.'},
        ]
        save_data('news.json', news)
    
    if not os.path.exists(os.path.join(DATA_DIR, 'notices.json')):
        notices = [
            {'id': 1, 'title': 'Mid-Semester Exams', 'date': '2024-03-20', 'content': 'Exams start April 10th. Check your timetables.'},
            {'id': 2, 'title': 'Library Hours Extended', 'date': '2024-03-18', 'content': 'Library now open until 8 PM during exam period.'},
        ]
        save_data('notices.json', notices)
    
    if not os.path.exists(os.path.join(DATA_DIR, 'gallery.json')):
        gallery = [
            {'id': 1, 'title': 'Computer Lab Session'},
            {'id': 2, 'title': 'Engineering Workshop'},
            {'id': 3, 'title': 'Business Class'},
        ]
        save_data('gallery.json', gallery)
    
    if not os.path.exists(os.path.join(DATA_DIR, 'applications.json')):
        save_data('applications.json', [])
    
    if not os.path.exists(os.path.join(DATA_DIR, 'students.json')):
        students = [
            {'id': 1, 'fullname': 'John Mwangi', 'email': 'john@example.com', 'course': 'Diploma in ICT', 'student_id': 'E2024001', 'password': generate_password_hash('student123')},
        ]
        save_data('students.json', students)
    
    if not os.path.exists(os.path.join(DATA_DIR, 'events.json')):
        events = [
            {'id': 1, 'title': 'Career Fair 2024', 'date': '2024-04-25', 'description': 'Meet top employers and find internships.'},
            {'id': 2, 'title': 'Open Day', 'date': '2024-05-10', 'description': 'Campus tours and course counseling.'},
        ]
        save_data('events.json', events)
    
    if not os.path.exists(os.path.join(DATA_DIR, 'success_stories.json')):
        stories = [
            {'id': 1, 'name': 'Mary Wanjiku', 'course': 'ICT Diploma', 'story': 'Now a software engineer at Safaricom'},
            {'id': 2, 'name': 'Peter Kamau', 'course': 'Automotive', 'story': 'Opened own garage employing 5 people'},
        ]
        save_data('success_stories.json', stories)

init_data()

# Authentication decorator for admin
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    courses = load_data('courses.json')[:4]
    news = load_data('news.json')[:3]
    notices = load_data('notices.json')[:3]
    events = load_data('events.json')[:3]
    stories = load_data('success_stories.json')[:2]
    gallery = load_data('gallery.json')[:4]
    return render_template('home.html', courses=courses, news=news, notices=notices, events=events, stories=stories, gallery=gallery)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/courses')
def courses():
    all_courses = load_data('courses.json')
    category = request.args.get('category', '')
    if category:
        all_courses = [c for c in all_courses if c['category'].lower() == category.lower()]
    return render_template('courses.html', courses=all_courses)

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    courses = load_data('courses.json')
    course = next((c for c in courses if c['id'] == course_id), None)
    return render_template('course_detail.html', course=course)

@app.route('/admissions')
def admissions():
    return render_template('admissions.html')

@app.route('/apply', methods=['POST'])
def apply():
    data = request.form
    application = {
        'id': int(datetime.datetime.now().timestamp()),
        'fullname': data.get('fullname'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'course': data.get('course'),
        'qualification': data.get('qualification'),
        'message': data.get('message'),
        'status': 'pending',
        'date': datetime.datetime.now().strftime('%Y-%m-%d')
    }
    applications = load_data('applications.json')
    applications.append(application)
    save_data('applications.json', applications)
    flash('Application submitted successfully! We will contact you soon.', 'success')
    return redirect(url_for('admissions'))

@app.route('/student-portal')
def student_portal():
    if session.get('student_logged_in'):
        student = session.get('student_data')
        return render_template('student_dashboard.html', student=student)
    return render_template('student_login.html')

@app.route('/student-login', methods=['POST'])
def student_login():
    email = request.form.get('email')
    password = request.form.get('password')
    students = load_data('students.json')
    student = next((s for s in students if s['email'] == email), None)
    if student and check_password_hash(student['password'], password):
        session['student_logged_in'] = True
        session['student_data'] = student
        return redirect(url_for('student_portal'))
    flash('Invalid credentials', 'error')
    return redirect(url_for('student_portal'))

@app.route('/student-logout')
def student_logout():
    session.pop('student_logged_in', None)
    session.pop('student_data', None)
    return redirect(url_for('student_portal'))

@app.route('/news')
def news():
    all_news = load_data('news.json')
    return render_template('news.html', news_list=all_news)

@app.route('/departments')
def departments():
    departments_data = [
        {'name': 'ICT', 'hod': 'Dr. Jane Muthoni', 'staff': 12, 'courses': 4, 'icon': 'fas fa-laptop-code'},
        {'name': 'Business', 'hod': 'Prof. James Kariuki', 'staff': 10, 'courses': 5, 'icon': 'fas fa-chart-line'},
        {'name': 'Engineering', 'hod': 'Eng. Susan Wambui', 'staff': 15, 'courses': 6, 'icon': 'fas fa-hard-hat'},
        {'name': 'Hospitality', 'hod': 'Chef Michael Otieno', 'staff': 8, 'courses': 3, 'icon': 'fas fa-utensils'},
        {'name': 'Automotive', 'hod': 'Mr. David Kimathi', 'staff': 7, 'courses': 3, 'icon': 'fas fa-car'},
        {'name': 'Beauty & Therapy', 'hod': 'Ms. Lucy Njeri', 'staff': 5, 'courses': 2, 'icon': 'fas fa-spa'},
    ]
    return render_template('departments.html', departments=departments_data)

@app.route('/gallery')
def gallery():
    images = load_data('gallery.json')
    return render_template('gallery.html', images=images)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/career-services')
def career_services():
    return render_template('career_services.html')

@app.route('/downloads')
def downloads():
    files = [
        {'name': 'Admission Form 2024', 'size': '1.2 MB', 'type': 'pdf'},
        {'name': 'College Prospectus', 'size': '3.5 MB', 'type': 'pdf'},
        {'name': 'Fee Structure', 'size': '0.8 MB', 'type': 'pdf'},
        {'name': 'Scholarship Application', 'size': '0.5 MB', 'type': 'pdf'},
        {'name': 'Student Handbook', 'size': '2.1 MB', 'type': 'pdf'},
    ]
    return render_template('downloads.html', files=files)

@app.route('/alumni')
def alumni():
    return render_template('alumni.html')

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == app.config['ADMIN_USERNAME'] and request.form.get('password') == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_login_required
def admin_dashboard():
    students = load_data('students.json')
    applications = load_data('applications.json')
    courses = load_data('courses.json')
    news_items = load_data('news.json')
    return render_template('admin_dashboard.html', students=students, applications=applications, courses=courses, news_items=news_items)

@app.route('/admin/news', methods=['GET', 'POST'])
@admin_login_required
def admin_news():
    if request.method == 'POST':
        news_items = load_data('news.json')
        new_id = max([n['id'] for n in news_items] + [0]) + 1
        news_items.append({
            'id': new_id,
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'date': datetime.datetime.now().strftime('%Y-%m-%d')
        })
        save_data('news.json', news_items)
        flash('News added successfully', 'success')
        return redirect(url_for('admin_news'))
    news_items = load_data('news.json')
    return render_template('admin_news.html', news_items=news_items)

@app.route('/admin/news/delete/<int:news_id>')
@admin_login_required
def admin_news_delete(news_id):
    news_items = load_data('news.json')
    news_items = [n for n in news_items if n['id'] != news_id]
    save_data('news.json', news_items)
    flash('News deleted', 'success')
    return redirect(url_for('admin_news'))

@app.route('/admin/courses', methods=['GET', 'POST'])
@admin_login_required
def admin_courses():
    if request.method == 'POST':
        courses = load_data('courses.json')
        new_id = max([c['id'] for c in courses] + [0]) + 1
        courses.append({
            'id': new_id,
            'name': request.form.get('name'),
            'category': request.form.get('category'),
            'duration': request.form.get('duration'),
            'fee': int(request.form.get('fee')),
            'description': request.form.get('description')
        })
        save_data('courses.json', courses)
        flash('Course added successfully', 'success')
        return redirect(url_for('admin_courses'))
    courses = load_data('courses.json')
    return render_template('admin_courses.html', courses=courses)

@app.route('/admin/courses/delete/<int:course_id>')
@admin_login_required
def admin_courses_delete(course_id):
    courses = load_data('courses.json')
    courses = [c for c in courses if c['id'] != course_id]
    save_data('courses.json', courses)
    flash('Course deleted', 'success')
    return redirect(url_for('admin_courses'))

@app.route('/admin/applications')
@admin_login_required
def admin_applications():
    applications = load_data('applications.json')
    return render_template('admin_applications.html', applications=applications)

@app.route('/admin/notices', methods=['GET', 'POST'])
@admin_login_required
def admin_notices():
    if request.method == 'POST':
        notices = load_data('notices.json')
        new_id = max([n['id'] for n in notices] + [0]) + 1
        notices.append({
            'id': new_id,
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'date': datetime.datetime.now().strftime('%Y-%m-%d')
        })
        save_data('notices.json', notices)
        flash('Notice added', 'success')
        return redirect(url_for('admin_notices'))
    notices = load_data('notices.json')
    return render_template('admin_notices.html', notices=notices)

@app.route('/admin/gallery', methods=['GET', 'POST'])
@admin_login_required
def admin_gallery():
    if request.method == 'POST':
        gallery_items = load_data('gallery.json')
        new_id = max([g['id'] for g in gallery_items] + [0]) + 1
        gallery_items.append({
            'id': new_id,
            'title': request.form.get('title'),
            'image': request.form.get('image')
        })
        save_data('gallery.json', gallery_items)
        flash('Image added', 'success')
        return redirect(url_for('admin_gallery'))
    gallery_items = load_data('gallery.json')
    return render_template('admin_gallery.html', gallery_items=gallery_items)

@app.route('/api/noticeboard')
def api_noticeboard():
    notices = load_data('notices.json')
    return jsonify(notices)

@app.route('/api/search-courses')
def search_courses():
    query = request.args.get('q', '').lower()
    courses = load_data('courses.json')
    results = [c for c in courses if query in c['name'].lower() or query in c['category'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)