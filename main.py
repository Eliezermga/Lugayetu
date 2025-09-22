import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import csv
from io import StringIO
from flask import make_response
import random
import secrets
import os
import zipfile
import tempfile
from datetime import datetime


class Base(DeclarativeBase):
    pass


# Create the app
app = Flask(__name__)

# Setup a secret key, required by sessions - MUST be set in production
if not os.environ.get("SESSION_SECRET"):
    raise ValueError("SESSION_SECRET environment variable must be set for security")
app.secret_key = os.environ.get("SESSION_SECRET")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure upload settings
app.config['UPLOAD_FOLDER'] = 'static/recordings'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db = SQLAlchemy(app, model_class=Base)
csrf = CSRFProtect(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define Models
class User(UserMixin, db.Model):
    """User model with all required fields."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)  # 'Homme', 'Femme', 'Autre'
    age = db.Column(db.Integer, nullable=False)
    provenance = db.Column(db.String(200), nullable=False)  # Place of origin
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    consent = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to recordings
    recordings = db.relationship('Recording', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'


class Phrase(db.Model):
    """Phrase model for Rund language phrases."""
    __tablename__ = 'phrases'
    
    id = db.Column(db.Integer, primary_key=True)
    text_rund = db.Column(db.Text, nullable=False)
    translate = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to recordings
    recordings = db.relationship('Recording', backref='phrase', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Phrase {self.id}: {self.text_rund[:50]}...>'


class Recording(db.Model):
    """Recording model to store audio recording metadata."""
    __tablename__ = 'recordings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phrase_id = db.Column(db.Integer, db.ForeignKey('phrases.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)  # Path to audio file
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Recording {self.id}: User {self.user_id}, Phrase {self.phrase_id}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Utility functions
def load_phrases_from_file():
    """Load phrases from phrases.txt file into database with translations."""
    phrases_file = 'phrases.txt'
    translate_file = 'translate.txt'
    
    if not os.path.exists(phrases_file):
        return  # File doesn't exist yet
    
    try:
        # Read phrases
        with open(phrases_file, 'r', encoding='utf-8') as f:
            phrases_lines = [line.strip() for line in f.readlines() if line.strip()]
        
        # Read translations if file exists
        translations = []
        if os.path.exists(translate_file):
            with open(translate_file, 'r', encoding='utf-8') as f:
                translations = [line.strip() for line in f.readlines() if line.strip()]
        
        # Ensure we have same number of phrases and translations
        if len(translations) != len(phrases_lines) and translations:
            print(f"Warning: {len(phrases_lines)} phrases but {len(translations)} translations")
        
        for i, phrase_text in enumerate(phrases_lines):
            # Check if phrase already exists
            existing = Phrase.query.filter_by(text_rund=phrase_text).first()
            if not existing:
                # Get translation if available
                translation = translations[i] if i < len(translations) else None
                phrase = Phrase(text_rund=phrase_text, translate=translation)
                db.session.add(phrase)
            else:
                # Update translation if not set and we have one
                if i < len(translations) and not existing.translate:
                    existing.translate = translations[i]
        
        db.session.commit()
        print(f"Loaded {len(phrases_lines)} phrases with translations")
        
    except Exception as e:
        print(f"Error loading phrases: {e}")
        db.session.rollback()


def get_random_phrase():
    """Get a random phrase for recording."""
    phrases = Phrase.query.all()
    if phrases:
        return random.choice(phrases)
    return None


def create_admin_user():
    """Create a default admin user if none exists, or update existing admin password."""
    admin = User.query.filter_by(is_admin=True).first()
    admin_password = "31082003"
    hashed_password = generate_password_hash(admin_password)
    
    if not admin:
        # Create admin user with predefined password
        admin_user = User(
            nom='Administrateur',
            sexe='Autre',
            age=30,
            provenance='Système',
            email='admin@rund.local',
            password_hash=hashed_password,
            consent=True,
            is_admin=True
        )
        
        db.session.add(admin_user)
        try:
            db.session.commit()
            print(f"Admin user created: {admin_user.email}")
        except Exception as e:
            print(f"Error creating admin user: {e}")
            db.session.rollback()
    else:
        # Update existing admin password
        admin.password_hash = hashed_password
        try:
            db.session.commit()
            print(f"Admin password updated for: {admin.email}")
        except Exception as e:
            print(f"Error updating admin password: {e}")
            db.session.rollback()


# Routes
@app.route('/')
def index():
    """Homepage explaining the Rund language preservation project."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with consent requirement."""
    if request.method == 'POST':
        # Get form data
        nom = request.form['nom']
        sexe = request.form['sexe']
        age = int(request.form['age'])
        provenance = request.form['provenance']
        email = request.form['email']
        password = request.form['password']
        consent = request.form.get('consent') == 'on'
        
        # Validate consent
        if not consent:
            flash('Vous devez accepter la politique de confidentialité pour vous inscrire.', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Un utilisateur avec cette adresse email existe déjà.', 'error')
            return render_template('register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        user = User(
            nom=nom,
            sexe=sexe,
            age=age,
            provenance=provenance,
            email=email,
            password_hash=hashed_password,
            consent=consent
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de l\'inscription. Veuillez réessayer.', 'error')
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Connexion réussie!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('record'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('index'))

@app.route('/privacy')
def privacy():
    """Privacy policy page."""
    return render_template('privacy.html')

@app.route('/record')
@login_required
def record():
    """Audio recording page."""
    # Get a random phrase
    phrase = get_random_phrase()
    if not phrase:
        flash('Aucune phrase disponible. Veuillez contacter l\'administrateur.', 'error')
        return redirect(url_for('index'))
    
    return render_template('record.html', phrase=phrase)

@app.route('/save_recording', methods=['POST'])
@login_required
def save_recording():
    """Save audio recording to server and database."""
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'message': 'Aucun fichier audio trouvé'})
        
        file = request.files['audio']
        phrase_id = request.form.get('phrase_id')
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Aucun fichier sélectionné'})
        
        if file and phrase_id:
            # Enhanced file validation
            allowed_types = ['audio/wav', 'audio/webm', 'audio/ogg', 'audio/mp3', 'audio/mp4']
            if not file.content_type or file.content_type not in allowed_types:
                return jsonify({'success': False, 'message': 'Seuls les fichiers audio WAV, WebM, OGG, MP3 sont autorisés'})
            
            # Validate file size (max 10MB for audio)
            if len(file.read()) > 10 * 1024 * 1024:
                return jsonify({'success': False, 'message': 'Fichier trop volumineux (max 10MB)'})
            file.seek(0)  # Reset file pointer after reading
            
            # Generate secure, unique filename
            import uuid
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            secure_name = secure_filename(f"rec_{current_user.id}_{phrase_id}_{timestamp}_{unique_id}.wav")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_name)
            
            # Ensure the filepath is within the upload directory (prevent path traversal)
            if not os.path.abspath(filepath).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
                return jsonify({'success': False, 'message': 'Chemin de fichier non autorisé'})
            
            # Save file
            file.save(filepath)
            
            # Save to database
            recording = Recording(
                user_id=current_user.id,
                phrase_id=int(phrase_id),
                file_path=filepath,
                date_recorded=datetime.now()
            )
            
            db.session.add(recording)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Enregistrement sauvegardé avec succès!'})
        
        return jsonify({'success': False, 'message': 'Erreur lors de la sauvegarde'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Erreur: {str(e)}'})

@app.route('/admin')
@login_required
def admin():
    """Admin dashboard."""
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('index'))
    
    # Get all recordings with user and phrase info
    recordings = db.session.query(Recording, User, Phrase).join(
        User, Recording.user_id == User.id
    ).join(
        Phrase, Recording.phrase_id == Phrase.id
    ).order_by(Recording.date_recorded.desc()).all()
    
    # Calculate today's recordings count
    from datetime import date
    today = date.today()
    today_count = sum(1 for recording, _, _ in recordings 
                      if recording.date_recorded.date() == today)
    
    return render_template('admin.html', recordings=recordings, today_count=today_count)

@app.route('/admin/export')
@login_required
def admin_export():
    """Export recordings data to CSV."""
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('index'))
    
    # Query all recordings with user and phrase data
    recordings = db.session.query(Recording, User, Phrase).join(
        User, Recording.user_id == User.id
    ).join(
        Phrase, Recording.phrase_id == Phrase.id
    ).order_by(Recording.date_recorded.desc()).all()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID Enregistrement', 'Nom Utilisateur', 'Sexe', 'Âge', 'Provenance', 
        'Email', 'Phrase (Rund)', 'Traduction', 'Chemin Fichier Audio', 'Date Enregistrement'
    ])
    
    # Write data
    for recording, user, phrase in recordings:
        writer.writerow([
            recording.id, user.nom, user.sexe, user.age, user.provenance,
            user.email, phrase.text_rund, phrase.translate or '', recording.file_path, 
            recording.date_recorded.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=enregistrements_rund.csv'
    response.headers['Content-type'] = 'text/csv'
    
    return response

@app.route('/admin/export_zip')
@login_required
def admin_export_zip():
    """Export all recordings data and audio files to ZIP."""
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Query all recordings with user and phrase data
        recordings = db.session.query(Recording, User, Phrase).join(
            User, Recording.user_id == User.id
        ).join(
            Phrase, Recording.phrase_id == Phrase.id
        ).order_by(Recording.date_recorded.desc()).all()
        
        # Create temporary ZIP file
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Create CSV data in memory
            csv_output = StringIO()
            writer = csv.writer(csv_output)
            
            # Write CSV header
            writer.writerow([
                'ID Enregistrement', 'Nom Utilisateur', 'Sexe', 'Âge', 'Provenance', 
                'Email', 'Phrase (Rund)', 'Traduction', 'Chemin Fichier Audio', 'Date Enregistrement'
            ])
            
            # Write CSV data and collect audio files
            for recording, user, phrase in recordings:
                writer.writerow([
                    recording.id, user.nom, user.sexe, user.age, user.provenance,
                    user.email, phrase.text_rund, phrase.translate or '', recording.file_path, 
                    recording.date_recorded.strftime('%Y-%m-%d %H:%M:%S')
                ])
                
                # Add audio file to ZIP if it exists
                if os.path.exists(recording.file_path):
                    # Create a clean filename for the ZIP
                    audio_filename = f"audio_{recording.id}_{os.path.basename(recording.file_path)}"
                    zipf.write(recording.file_path, audio_filename)
            
            # Add CSV to ZIP
            csv_content = csv_output.getvalue()
            zipf.writestr('enregistrements_rund.csv', csv_content)
        
        # Read the ZIP file content
        with open(temp_zip.name, 'rb') as f:
            zip_data = f.read()
        
        # Clean up temporary file
        os.unlink(temp_zip.name)
        
        # Create response
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        response = make_response(zip_data)
        response.headers['Content-Disposition'] = f'attachment; filename=enregistrements_rund_{timestamp}.zip'
        response.headers['Content-Type'] = 'application/zip'
        
        return response
        
    except Exception as e:
        flash(f'Erreur lors de la création du fichier ZIP: {str(e)}', 'error')
        return redirect(url_for('admin'))

@app.route('/admin/delete_recording/<int:recording_id>', methods=['POST'])
@login_required
def delete_recording(recording_id):
    """Delete a recording."""
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('index'))
    
    recording = Recording.query.get_or_404(recording_id)
    
    try:
        # Delete file if it exists
        if os.path.exists(recording.file_path):
            os.remove(recording.file_path)
        
        # Delete from database
        db.session.delete(recording)
        db.session.commit()
        
        flash('Enregistrement supprimé avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user and all their recordings."""
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting current admin user
    if user.id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'error')
        return redirect(url_for('admin'))
    
    try:
        # Delete all user's recordings and files
        recordings = Recording.query.filter_by(user_id=user_id).all()
        for recording in recordings:
            if os.path.exists(recording.file_path):
                os.remove(recording.file_path)
            db.session.delete(recording)
        
        # Delete user
        db.session.delete(user)
        db.session.commit()
        
        flash('Utilisateur et ses enregistrements supprimés avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
    
    return redirect(url_for('admin'))


# Initialize database and data
def init_database():
    with app.app_context():
        db.create_all()
        
        # Add translate column if it doesn't exist
        try:
            # Try to add the column if it doesn't exist
            from sqlalchemy import text
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE phrases ADD COLUMN IF NOT EXISTS translate TEXT"))
                conn.commit()
        except Exception as e:
            print(f"Column translate may already exist: {e}")
        
        load_phrases_from_file()
        create_admin_user()


if __name__ == '__main__':
    # Initialize database when running directly
    init_database()
    app.run(host='0.0.0.0', port=5000, debug=True)