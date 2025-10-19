import os
import random
import zipfile
import io
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from models import db, User, Language, Sentence, Recording
import pandas as pd
from sqlalchemy import func
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'lugayetu-secret-key-2024')
app.config['JWT_SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'lugayetu-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 10,
    'max_overflow': 20
}
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads/audio')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 50 * 1024 * 1024))

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from api import api_bp
app.register_blueprint(api_bp)

PROVINCES = [
    'Kinshasa', 'Kongo-Central', 'Kwango', 'Kwilu', 'Mai-Ndombe',
    'Kasaï', 'Kasaï-Central', 'Kasaï-Oriental', 'Lomami', 'Sankuru',
    'Maniema', 'Sud-Kivu', 'Nord-Kivu', 'Ituri', 'Haut-Uélé', 'Bas-Uélé',
    'Tshopo', 'Tshuapa', 'Mongala', 'Nord-Ubangi', 'Sud-Ubangi', 'Équateur',
    'Haut-Lomami', 'Lualaba', 'Haut-Katanga', 'Tanganyika'
]

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def init_db():
    with app.app_context():
        db.create_all()
        
        users_without_id = User.query.filter_by(user_id=None).all()
        for user in users_without_id:
            user.user_id = f'user{user.id}'
        if users_without_id:
            db.session.commit()
        
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            admin = User(
                user_id='user1',
                nom='Admin',
                prenom='Lugayetu',
                age=30,
                langue_parlee='Français',
                province='Kinshasa',
                ville_village='Kinshasa',
                sexe='Autre',
                email='admin@lugayetu.cd',
                is_admin=True,
                is_approved=True,
                accepted_terms=True
            )
            admin.set_password('31082003')
            db.session.add(admin)
        
        rund = Language.query.filter_by(code='rund').first()
        if not rund:
            rund = Language(
                name='Rund',
                code='rund',
                sentences_file='languages/rund.txt',
                translations_file='languages/translate_rund.txt'
            )
            db.session.add(rund)
            db.session.commit()
            
            load_sentences_from_files(rund)
        
        db.session.commit()

def load_sentences_from_files(language):
    try:
        with open(language.sentences_file, 'r', encoding='utf-8') as f:
            sentences = [line.strip() for line in f if line.strip()]
        
        with open(language.translations_file, 'r', encoding='utf-8') as f:
            translations = [line.strip() for line in f if line.strip()]
        
        for sentence_text, translation_text in zip(sentences, translations):
            existing = Sentence.query.filter_by(
                language_id=language.id,
                text=sentence_text
            ).first()
            
            if not existing:
                sentence = Sentence(
                    language_id=language.id,
                    text=sentence_text,
                    translation=translation_text
                )
                db.session.add(sentence)
        
        db.session.commit()
    except Exception as e:
        print(f"Error loading sentences: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    languages = Language.query.all()
    form_data = {}
    
    if request.method == 'POST':
        form_data = {
            'nom': request.form.get('nom', ''),
            'prenom': request.form.get('prenom', ''),
            'age': request.form.get('age', ''),
            'sexe': request.form.get('sexe', ''),
            'langue_parlee': request.form.get('langue_parlee', ''),
            'province': request.form.get('province', ''),
            'ville_village': request.form.get('ville_village', ''),
            'email': request.form.get('email', '')
        }
        
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if User.query.filter_by(email=email).first():
            flash('Cette adresse email est déjà utilisée.', 'error')
            return render_template('register.html', provinces=PROVINCES, languages=languages, form_data=form_data)
        
        if not request.form.get('terms'):
            flash('Vous devez accepter les conditions d\'utilisation et la politique de confidentialité.', 'error')
            return render_template('register.html', provinces=PROVINCES, languages=languages, form_data=form_data)
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return render_template('register.html', provinces=PROVINCES, languages=languages, form_data=form_data)
        
        user = User(
            user_id=User.generate_user_id(),
            nom=request.form.get('nom'),
            prenom=request.form.get('prenom'),
            age=int(request.form.get('age')),
            langue_parlee=request.form.get('langue_parlee'),
            province=request.form.get('province'),
            ville_village=request.form.get('ville_village'),
            sexe=request.form.get('sexe'),
            email=email,
            accepted_terms=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Votre inscription a été soumise. Veuillez attendre l\'approbation de l\'administrateur.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', provinces=PROVINCES, languages=languages, form_data=form_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    email = ''
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if user.is_admin or user.is_approved:
                login_user(user, remember=bool(remember))
                return redirect(url_for('admin_dashboard') if user.is_admin else url_for('record'))
            else:
                flash('Votre compte n\'a pas encore été approuvé par l\'administrateur.', 'warning')
        else:
            flash('Email ou mot de passe incorrect.', 'error')
    
    return render_template('login.html', email=email)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/record')
@login_required
def record():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    languages = Language.query.all()
    
    recorded_sentence_ids = [r.sentence_id for r in current_user.recordings]
    
    available_sentences = Sentence.query.filter(
        ~Sentence.id.in_(recorded_sentence_ids) if recorded_sentence_ids else True
    ).all()
    
    if not available_sentences:
        flash('Vous avez enregistré toutes les phrases disponibles. Merci pour votre contribution!', 'info')
        return render_template('record.html', sentence=None, total_recorded=len(current_user.recordings))
    
    sentence = random.choice(available_sentences)
    
    return render_template('record.html', 
                         sentence=sentence, 
                         total_recorded=len(current_user.recordings),
                         language=sentence.language)

@app.route('/save_recording', methods=['POST'])
@login_required
def save_recording():
    if 'audio' not in request.files:
        return jsonify({'success': False, 'message': 'Aucun fichier audio trouvé'})
    
    audio_file = request.files['audio']
    sentence_id = request.form.get('sentence_id')
    duration = float(request.form.get('duration', 0))
    
    if not sentence_id:
        return jsonify({'success': False, 'message': 'ID de phrase manquant'})
    
    existing = Recording.query.filter_by(
        user_id=current_user.id,
        sentence_id=sentence_id
    ).first()
    
    if existing:
        return jsonify({'success': False, 'message': 'Vous avez déjà enregistré cette phrase'})
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"user{current_user.id}_sentence{sentence_id}_{timestamp}.wav"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    audio_file.save(filepath)
    
    recording = Recording(
        user_id=current_user.id,
        sentence_id=sentence_id,
        audio_path=filepath,
        duration=duration
    )
    
    db.session.add(recording)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Enregistrement sauvegardé avec succès!'})

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('record'))
    
    total_users = User.query.filter_by(is_approved=True, is_admin=False).count()
    pending_users = User.query.filter_by(is_approved=False, is_admin=False).count()
    total_recordings = Recording.query.count()
    
    total_duration = db.session.query(func.sum(Recording.duration)).scalar() or 0
    total_hours = total_duration / 3600
    
    today = datetime.utcnow().date()
    today_recordings = Recording.query.filter(
        func.date(Recording.created_at) == today
    ).count()
    
    recent_recordings = Recording.query.order_by(
        Recording.created_at.desc()
    ).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         pending_users=pending_users,
                         total_recordings=total_recordings,
                         total_hours=total_hours,
                         today_recordings=today_recordings,
                         recent_recordings=recent_recordings)

@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/approve_user/<int:user_id>')
@login_required
def approve_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    
    flash(f'Utilisateur {user.prenom} {user.nom} approuvé avec succès.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/reject_user/<int:user_id>')
@login_required
def reject_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    user = User.query.get_or_404(user_id)
    user.is_approved = False
    db.session.commit()
    
    flash(f'Utilisateur {user.prenom} {user.nom} rejeté.', 'warning')
    return redirect(url_for('admin_users'))

@app.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    user = User.query.get_or_404(user_id)
    
    for recording in user.recordings:
        if os.path.exists(recording.audio_path):
            os.remove(recording.audio_path)
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Utilisateur supprimé avec succès.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/delete_recording/<int:recording_id>')
@login_required
def delete_recording(recording_id):
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    recording = Recording.query.get_or_404(recording_id)
    
    if os.path.exists(recording.audio_path):
        os.remove(recording.audio_path)
    
    db.session.delete(recording)
    db.session.commit()
    
    flash('Enregistrement supprimé avec succès.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/export_csv')
@login_required
def export_csv():
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    recordings = Recording.query.all()
    
    data = []
    for rec in recordings:
        data.append({
            'ID Enregistrement': rec.id,
            'Nom Utilisateur': f"{rec.user.prenom} {rec.user.nom}",
            'Sexe': rec.user.sexe,
            'Âge': rec.user.age,
            'Provenance': f"{rec.user.ville_village}, {rec.user.province}",
            'Email': rec.user.email,
            'Langue': rec.sentence.language.name,
            'Phrase': rec.sentence.text,
            'Traduction': rec.sentence.translation,
            'Chemin Fichier Audio': rec.audio_path,
            'Durée (secondes)': rec.duration,
            'Date Enregistrement': rec.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'lugayetu_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/admin/export_zip')
@login_required
def export_zip():
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    recordings = Recording.query.all()
    
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        data = []
        for rec in recordings:
            data.append({
                'ID Enregistrement': rec.id,
                'Nom Utilisateur': f"{rec.user.prenom} {rec.user.nom}",
                'Sexe': rec.user.sexe,
                'Âge': rec.user.age,
                'Provenance': f"{rec.user.ville_village}, {rec.user.province}",
                'Email': rec.user.email,
                'Langue': rec.sentence.language.name,
                'Phrase': rec.sentence.text,
                'Traduction': rec.sentence.translation,
                'Chemin Fichier Audio': rec.audio_path,
                'Durée (secondes)': rec.duration,
                'Date Enregistrement': rec.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
            
            if os.path.exists(rec.audio_path):
                zf.write(rec.audio_path, rec.audio_path)
        
        df = pd.DataFrame(data)
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
        zf.writestr('metadata.csv', csv_data)
    
    memory_file.seek(0)
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'lugayetu_complete_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
    )

@app.route('/admin/languages')
@login_required
def admin_languages():
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    languages = Language.query.all()
    return render_template('admin_languages.html', languages=languages)

@app.route('/admin/add_language', methods=['POST'])
@login_required
def add_language():
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    name = request.form.get('name')
    code = request.form.get('code')
    
    existing = Language.query.filter_by(code=code).first()
    if existing:
        flash('Cette langue existe déjà.', 'error')
        return redirect(url_for('admin_languages'))
    
    sentences_file = f'languages/{code}.txt'
    translations_file = f'languages/translate_{code}.txt'
    
    language = Language(
        name=name,
        code=code,
        sentences_file=sentences_file,
        translations_file=translations_file
    )
    
    db.session.add(language)
    db.session.commit()
    
    os.makedirs('languages', exist_ok=True)
    
    if not os.path.exists(sentences_file):
        with open(sentences_file, 'w', encoding='utf-8') as f:
            f.write('')
    
    if not os.path.exists(translations_file):
        with open(translations_file, 'w', encoding='utf-8') as f:
            f.write('')
    
    flash(f'Langue {name} ajoutée avec succès. Veuillez ajouter les phrases dans les fichiers {sentences_file} et {translations_file}.', 'success')
    return redirect(url_for('admin_languages'))

@app.route('/admin/delete_language/<int:language_id>')
@login_required
def delete_language(language_id):
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    language = Language.query.get_or_404(language_id)
    
    db.session.delete(language)
    db.session.commit()
    
    flash(f'Langue {language.name} supprimée avec succès.', 'success')
    return redirect(url_for('admin_languages'))

@app.route('/admin/recordings')
@login_required
def admin_recordings():
    if not current_user.is_admin:
        return redirect(url_for('record'))
    
    user_filter = request.args.get('user', '')
    language_filter = request.args.get('language', '')
    date_filter = request.args.get('date', '')
    search_query = request.args.get('search', '')
    
    query = Recording.query
    
    if user_filter:
        query = query.filter(Recording.user_id == int(user_filter))
    
    if language_filter:
        query = query.join(Sentence).join(Language).filter(Language.id == int(language_filter))
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(func.date(Recording.created_at) == filter_date)
        except:
            pass
    
    if search_query:
        query = query.join(Sentence).filter(
            db.or_(
                Sentence.text.ilike(f'%{search_query}%'),
                Sentence.translation.ilike(f'%{search_query}%')
            )
        )
    
    recordings = query.order_by(Recording.created_at.desc()).all()
    users = User.query.filter_by(is_admin=False).order_by(User.prenom).all()
    languages = Language.query.order_by(Language.name).all()
    
    return render_template('admin_recordings.html',
                         recordings=recordings,
                         users=users,
                         languages=languages,
                         user_filter=user_filter,
                         language_filter=language_filter,
                         date_filter=date_filter,
                         search_query=search_query)

@app.route('/audio/<path:filename>')
@login_required
def serve_audio(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        flash('Fichier audio introuvable.', 'error')
        return redirect(url_for('my_recordings'))
    
    recording = Recording.query.filter_by(audio_path=filepath).first()
    
    if not recording:
        flash('Enregistrement non trouvé.', 'error')
        return redirect(url_for('my_recordings'))
    
    if recording.user_id != current_user.id and not current_user.is_admin:
        flash('Accès non autorisé à cet enregistrement.', 'error')
        return redirect(url_for('my_recordings'))
    
    return send_file(filepath)

@app.route('/api/pending_users_count')
@login_required
def pending_users_count():
    if not current_user.is_admin:
        return jsonify({'count': 0})
    
    count = User.query.filter_by(is_approved=False, is_admin=False).count()
    return jsonify({'count': count})

@app.route('/api/dashboard_stats')
@login_required
def dashboard_stats():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    total_users = User.query.filter_by(is_approved=True, is_admin=False).count()
    pending_users = User.query.filter_by(is_approved=False, is_admin=False).count()
    total_recordings = Recording.query.count()
    
    total_duration = db.session.query(func.sum(Recording.duration)).scalar() or 0
    total_hours = total_duration / 3600
    
    today = datetime.utcnow().date()
    today_recordings = Recording.query.filter(
        func.date(Recording.created_at) == today
    ).count()
    
    recent_recordings = Recording.query.order_by(
        Recording.created_at.desc()
    ).limit(10).all()
    
    recent_data = []
    for rec in recent_recordings:
        recent_data.append({
            'id': rec.id,
            'user': f"{rec.user.prenom} {rec.user.nom}",
            'language': rec.sentence.language.name,
            'sentence': rec.sentence.text[:50] + '...',
            'duration': rec.duration,
            'audio_filename': rec.audio_path.split('/')[-1],
            'created_at': rec.created_at.strftime('%d/%m/%Y %H:%M')
        })
    
    return jsonify({
        'total_users': total_users,
        'pending_users': pending_users,
        'total_recordings': total_recordings,
        'total_hours': round(total_hours, 2),
        'today_recordings': today_recordings,
        'recent_recordings': recent_data
    })

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    languages = Language.query.all()
    
    if request.method == 'POST':
        try:
            nom = request.form.get('nom')
            prenom = request.form.get('prenom')
            age = request.form.get('age')
            sexe = request.form.get('sexe')
            langue_parlee = request.form.get('langue_parlee')
            province = request.form.get('province')
            ville_village = request.form.get('ville_village')
            
            if not all([nom, prenom, age, sexe, langue_parlee, province, ville_village]):
                flash('Tous les champs sont requis.', 'error')
                return render_template('profile.html', provinces=PROVINCES, languages=languages)
            
            try:
                age = int(age)
                if age < 13 or age > 120:
                    flash('L\'âge doit être entre 13 et 120 ans.', 'error')
                    return render_template('profile.html', provinces=PROVINCES, languages=languages)
            except ValueError:
                flash('L\'âge doit être un nombre valide.', 'error')
                return render_template('profile.html', provinces=PROVINCES, languages=languages)
            
            if sexe not in ['Homme', 'Femme', 'Autre']:
                flash('Sexe invalide.', 'error')
                return render_template('profile.html', provinces=PROVINCES, languages=languages)
            
            if province not in PROVINCES:
                flash('Province invalide.', 'error')
                return render_template('profile.html', provinces=PROVINCES, languages=languages)
            
            current_user.nom = nom
            current_user.prenom = prenom
            current_user.age = age
            current_user.sexe = sexe
            current_user.langue_parlee = langue_parlee
            current_user.province = province
            current_user.ville_village = ville_village
            
            new_password = request.form.get('new_password')
            confirm_new_password = request.form.get('confirm_new_password')
            
            if new_password:
                if len(new_password) < 6:
                    flash('Le mot de passe doit contenir au moins 6 caractères.', 'error')
                    return render_template('profile.html', provinces=PROVINCES, languages=languages)
                if new_password != confirm_new_password:
                    flash('Les mots de passe ne correspondent pas.', 'error')
                    return render_template('profile.html', provinces=PROVINCES, languages=languages)
                current_user.set_password(new_password)
            
            db.session.commit()
            flash('Profil mis à jour avec succès!', 'success')
            return redirect(url_for('profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('Une erreur est survenue. Veuillez réessayer.', 'error')
            return render_template('profile.html', provinces=PROVINCES, languages=languages)
    
    return render_template('profile.html', provinces=PROVINCES, languages=languages)

@app.route('/my-recordings')
@login_required
def my_recordings():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    recordings = Recording.query.filter_by(user_id=current_user.id).order_by(Recording.created_at.desc()).all()
    total_duration = db.session.query(func.sum(Recording.duration)).filter(Recording.user_id == current_user.id).scalar() or 0
    
    return render_template('my_recordings.html', recordings=recordings, total_duration=total_duration)

@app.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    if current_user.is_admin:
        flash('Impossible de supprimer un compte administrateur.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    password = request.form.get('password')
    if not password or not current_user.check_password(password):
        flash('Mot de passe incorrect. Suppression annulée.', 'error')
        return redirect(url_for('profile'))
    
    user_id = current_user.id
    
    try:
        for recording in current_user.recordings:
            if os.path.exists(recording.audio_path):
                os.remove(recording.audio_path)
        
        logout_user()
        
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        
        flash('Votre compte a été supprimé avec succès.', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        flash('Une erreur est survenue lors de la suppression du compte.', 'error')
        return redirect(url_for('profile'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
