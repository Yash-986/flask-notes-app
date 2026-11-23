from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_wtf.csrf import CSRFProtect

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from sqlalchemy import or_

from config import Config
from models import db, User, Note
from forms import RegisterForm, LoginForm, NoteForm, DeleteForm


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

csrf = CSRFProtect(app)

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Create database and instance directory
import os

os.makedirs(app.instance_path, exist_ok=True)

with app.app_context():
    db.create_all()


# HOME
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    return render_template("index.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()

        existing_user = User.query.filter(
            or_(
                User.username.ilike(username),
                User.email.ilike(email)
            )
        ).first()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return render_template("register.html", form=form)

        user = User(
            username=username,
            email=email
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)

            flash("Welcome back!", "success")

            next_page = request.args.get("next")

            # Only allow local relative redirect paths
            if next_page and next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


# LOGOUT
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    query = Note.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(
            or_(
                Note.title.ilike(f"%{search}%"),
                Note.content.ilike(f"%{search}%")
            )
        )

    if category:
        query = query.filter_by(category=category)

    notes = query.order_by(Note.updated_at.desc()).all()

    categories = [
        row[0]
        for row in db.session.query(Note.category)
        .filter_by(user_id=current_user.id)
        .distinct()
        .all()
        if row[0]
    ]

    total_notes = Note.query.filter_by(
        user_id=current_user.id
    ).count()

    return render_template(
        "dashboard.html",
        notes=notes,
        categories=categories,
        total_notes=total_notes,
        search=search,
        selected_category=category,
        delete_form=DeleteForm()
    )


# CREATE NOTE
@app.route("/notes/create", methods=["GET", "POST"])
@login_required
def create_note():
    form = NoteForm()

    if form.validate_on_submit():
        note = Note(
            title=form.title.data.strip(),
            content=form.content.data,
            category=form.category.data.strip() or "General",
            user_id=current_user.id
        )

        db.session.add(note)
        db.session.commit()

        flash("Note created successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("create_note.html", form=form)


# EDIT NOTE
@app.route("/notes/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data.strip()
        note.content = form.content.data
        note.category = form.category.data.strip() or "General"

        db.session.commit()

        flash("Note updated successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "edit_note.html",
        form=form,
        note=note
    )


# DELETE NOTE
@app.route("/notes/delete/<int:note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    form = DeleteForm()

    if not form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("dashboard"))

    note = Note.query.filter_by(
        id=note_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(note)
    db.session.commit()

    flash("Note deleted successfully.", "success")

    return redirect(url_for("dashboard"))


# PROFILE
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=os.environ.get('FLASK_DEBUG') == "1")
