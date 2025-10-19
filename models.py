from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), unique=True, nullable=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    langue_parlee = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    ville_village = db.Column(db.String(100), nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    accepted_terms = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    recordings = db.relationship('Recording', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def generate_user_id():
        """Génère un ID utilisateur unique"""
        try:
            # Récupère le dernier utilisateur
            last_user = User.query.order_by(User.id.desc()).first()
            
            # Vérifie si last_user existe et a un user_id valide
            if last_user and last_user.user_id and last_user.user_id.startswith('user'):
                try:
                    last_num = int(last_user.user_id.replace('user', ''))
                    return f'user{last_num + 1}'
                except (ValueError, AttributeError):
                    # En cas d'erreur de conversion, on utilise l'ID max
                    pass
            
            # Si pas de dernier utilisateur ou format invalide, on utilise l'ID max
            max_id = db.session.query(db.func.max(User.id)).scalar() or 0
            return f'user{max_id + 1}'
            
        except Exception as e:
            # En cas d'erreur générale, on génère un ID basé sur le timestamp
            import time
            return f'user{int(time.time())}'
    
    def __repr__(self):
        return f'<User {self.email}>'

class Language(db.Model):
    __tablename__ = 'languages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    sentences_file = db.Column(db.String(255), nullable=False)
    translations_file = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sentences = db.relationship('Sentence', backref='language', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Language {self.name}>'

class Sentence(db.Model):
    __tablename__ = 'sentences'
    
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    translation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    recordings = db.relationship('Recording', backref='sentence', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Sentence {self.id}>'

class Recording(db.Model):
    __tablename__ = 'recordings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentences.id'), nullable=False)
    audio_path = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Recording {self.id}>'