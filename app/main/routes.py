from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from app.extensions import db
from app.models import User, Question, Answer, Tag, Notification
import threading, re

bp = Blueprint('main', __name__)

# ✅ Async Gemini AI answer generator
def generate_and_save_ai_answer(app, question_id, title, description):
    from app.gemini import generate_ai_answer
    with app.app_context():
        question = Question.query.get(question_id)
        gemini_user = User.query.filter_by(username='GeminiAI').first()
        ai_content = generate_ai_answer(title, description)

        if ai_content and gemini_user and question:
            ai_answer = Answer(content=ai_content, author=gemini_user, question=question)
            db.session.add(ai_answer)
            db.session.commit()


@bp.route('/')
def index():
    query = request.args.get('q', '').strip().lower()
    questions = Question.query
    tags = Tag.query.order_by(Tag.name).all()

    if query:
        questions = questions.filter(
            db.or_(
                Question.title.ilike(f"%{query}%"),
                Question.description.ilike(f"%{query}%"),
                Question.tags.any(Tag.name.ilike(f"%{query}%"))
            )
        )

    questions = questions.order_by(Question.timestamp.desc()).all()
    return render_template('index.html', questions=questions, all_tags=tags, Answer=Answer)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('main.register'))

        hashed_pw = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid credentials.')
        return redirect(url_for('main.login'))

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

@bp.route('/ask', methods=['GET', 'POST'])
@login_required
def ask_question():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tags_input = request.form.get('tags', '')

        tags = []
        if tags_input:
            tag_names = [t.strip().lower() for t in tags_input.split(',')]
            for name in tag_names:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                tags.append(tag)

        question = Question(
            title=title,
            description=description,
            author=current_user,
            timestamp=datetime.utcnow(),
            tags=tags
        )

        db.session.add(question)
        db.session.commit()

        # ✅ Run AI generation in a background thread with app context
        threading.Thread(
            target=generate_and_save_ai_answer,
            args=(current_app._get_current_object(), question.id, title, description)
        ).start()

        flash('Your question has been posted! Gemini is generating an answer...')
        return redirect(url_for('main.view_question', question_id=question.id))

    return render_template('ask.html')

@bp.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def view_question(question_id):
    question = Question.query.get_or_404(question_id)
    answers = question.answers.order_by(Answer.timestamp.desc()).all()
    ai_pending = not any(ans.author.username == 'GeminiAI' for ans in answers)

    if request.method == 'POST':
        content = request.form['content']
        answer = Answer(content=content, author=current_user, question=question)
        db.session.add(answer)

        # Mention notifications
        mentioned_usernames = re.findall(r'@(\w+)', content)
        for uname in mentioned_usernames:
            mentioned_user = User.query.filter_by(username=uname).first()
            if mentioned_user and mentioned_user.id != current_user.id:
                db.session.add(Notification(
                    message=f"You were mentioned in an answer by @{current_user.username}",
                    recipient=mentioned_user
                ))

        # Notify question author
        if current_user.id != question.author.id:
            db.session.add(Notification(
                message=f"{current_user.username} answered your question: {question.title}",
                recipient=question.author
            ))

        db.session.commit()
        flash('Your answer has been posted!')
        return redirect(url_for('main.view_question', question_id=question.id))

    return render_template('view_question.html', question=question, answers=answers, ai_pending=ai_pending)

@bp.route('/answers/<int:answer_id>/accept', methods=['POST'])
@login_required
def accept_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question = answer.question

    if current_user.id != question.author.id:
        flash('Only the question author can accept an answer.')
        return redirect(url_for('main.view_question', question_id=question.id))

    for ans in question.answers:
        ans.is_accepted = False

    answer.is_accepted = True
    db.session.commit()
    flash('Answer accepted successfully.')
    return redirect(url_for('main.view_question', question_id=question.id))

def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'ADMIN':
            flash('Admin access required.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return wrapped

@bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html',
                           users=User.query.all(),
                           questions=Question.query.order_by(Question.timestamp.desc()).all(),
                           answers=Answer.query.order_by(Answer.timestamp.desc()).all())

@bp.route('/notifications')
@login_required
def notifications():
    notes = current_user.notifications.order_by(Notification.timestamp.desc()).all()
    for n in notes:
        n.is_read = True
    db.session.commit()
    return render_template('notifications.html', notifications=notes)

@bp.route('/questions/<int:question_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_question(question_id):
    q = Question.query.get_or_404(question_id)
    db.session.delete(q)
    db.session.commit()
    flash('Question deleted.')
    return redirect(url_for('main.admin_dashboard'))

@bp.route('/answers/<int:answer_id>/vote/<string:action>', methods=['POST'])
@login_required
def vote_answer(answer_id, action):
    answer = Answer.query.get_or_404(answer_id)
    if action == 'up':
        answer.upvotes += 1
    elif action == 'down':
        answer.downvotes += 1
    else:
        flash('Invalid action.')
        return redirect(url_for('main.view_question', question_id=answer.question.id))
    db.session.commit()
    return redirect(url_for('main.view_question', question_id=answer.question.id))

@bp.route('/home')
def home():
    questions = Question.query.order_by(Question.timestamp.desc()).all()
    return render_template('index.html', questions=questions, Answer=Answer)
