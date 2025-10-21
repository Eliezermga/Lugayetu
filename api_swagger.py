import os
import random
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flasgger import swag_from
from werkzeug.utils import secure_filename
from models import db, User, Language, Sentence, Recording
from sqlalchemy import func

api_swagger_bp = Blueprint('api_swagger', __name__, url_prefix='/api/v2')

PROVINCES = [
    'Kinshasa', 'Kongo-Central', 'Kwango', 'Kwilu', 'Mai-Ndombe',
    'Kasaï', 'Kasaï-Central', 'Kasaï-Oriental', 'Lomami', 'Sankuru',
    'Maniema', 'Sud-Kivu', 'Nord-Kivu', 'Ituri', 'Haut-Uélé', 'Bas-Uélé',
    'Tshopo', 'Tshuapa', 'Mongala', 'Nord-Ubangi', 'Sud-Ubangi', 'Équateur',
    'Haut-Lomami', 'Lualaba', 'Haut-Katanga', 'Tanganyika'
]

@api_swagger_bp.route('/register', methods=['POST'])
def api_register():
    """
    Inscription d'un nouvel utilisateur
    ---
    tags:
      - Authentification
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nom
            - prenom
            - age
            - sexe
            - langue_parlee
            - province
            - ville_village
            - email
            - password
          properties:
            nom:
              type: string
              example: "Kasongo"
            prenom:
              type: string
              example: "Jean"
            age:
              type: integer
              example: 25
            sexe:
              type: string
              enum: ["Homme", "Femme", "Autre"]
              example: "Homme"
            langue_parlee:
              type: string
              example: "Rund"
            province:
              type: string
              example: "Kinshasa"
            ville_village:
              type: string
              example: "Kinshasa"
            email:
              type: string
              example: "jean.kasongo@example.com"
            password:
              type: string
              example: "motdepasse123"
    responses:
      201:
        description: Inscription réussie
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              type: object
      400:
        description: Champ manquant ou invalide
      409:
        description: Email déjà utilisé
      500:
        description: Erreur serveur
    """
    try:
        data = request.get_json()
        
        required_fields = ['nom', 'prenom', 'age', 'sexe', 'langue_parlee', 
                          'province', 'ville_village', 'email', 'password']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'Le champ {field} est requis'
                }), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'message': 'Cette adresse email est déjà utilisée'
            }), 409
        
        if data.get('province') not in PROVINCES:
            return jsonify({
                'success': False,
                'message': 'Province invalide'
            }), 400
        
        user = User(
            user_id=User.generate_user_id(),
            nom=data['nom'],
            prenom=data['prenom'],
            age=int(data['age']),
            langue_parlee=data['langue_parlee'],
            province=data['province'],
            ville_village=data['ville_village'],
            sexe=data['sexe'],
            email=data['email'],
            accepted_terms=True
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Inscription réussie. Veuillez attendre l\'approbation de l\'administrateur.',
            'data': {
                'user_id': user.user_id,
                'email': user.email,
                'is_approved': user.is_approved
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de l\'inscription: {str(e)}'
        }), 500

@api_swagger_bp.route('/login', methods=['POST'])
def api_login():
    """
    Connexion utilisateur
    ---
    tags:
      - Authentification
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "utilisateur@example.com"
            password:
              type: string
              example: "votre_mot_de_passe"
    responses:
      200:
        description: Connexion réussie
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              type: object
              properties:
                access_token:
                  type: string
                user:
                  type: object
      400:
        description: Email ou mot de passe manquant
      401:
        description: Identifiants incorrects
      403:
        description: Compte non approuvé
      500:
        description: Erreur serveur
    """
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Email et mot de passe requis'
            }), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'message': 'Email ou mot de passe incorrect'
            }), 401
        
        if not user.is_approved and not user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Votre compte n\'a pas encore été approuvé par l\'administrateur'
            }), 403
        
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'success': True,
            'message': 'Connexion réussie',
            'data': {
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'user_id': user.user_id,
                    'nom': user.nom,
                    'prenom': user.prenom,
                    'email': user.email,
                    'is_admin': user.is_admin,
                    'is_approved': user.is_approved
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la connexion: {str(e)}'
        }), 500

@api_swagger_bp.route('/user/profile', methods=['GET'])
@jwt_required()
def api_get_profile():
    """
    Obtenir le profil utilisateur
    ---
    tags:
      - Utilisateur
    security:
      - Bearer: []
    responses:
      200:
        description: Profil récupéré avec succès
      401:
        description: Token invalide ou expiré
      404:
        description: Utilisateur non trouvé
    """
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Utilisateur non trouvé'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': user.id,
                'user_id': user.user_id,
                'nom': user.nom,
                'prenom': user.prenom,
                'age': user.age,
                'sexe': user.sexe,
                'langue_parlee': user.langue_parlee,
                'province': user.province,
                'ville_village': user.ville_village,
                'email': user.email,
                'is_approved': user.is_approved,
                'created_at': user.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500

@api_swagger_bp.route('/user/stats', methods=['GET'])
@jwt_required()
def api_user_stats():
    """
    Statistiques de l'utilisateur
    ---
    tags:
      - Utilisateur
    security:
      - Bearer: []
    responses:
      200:
        description: Statistiques récupérées
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                total_recordings:
                  type: integer
                total_duration_seconds:
                  type: number
                total_duration_minutes:
                  type: number
                today_recordings:
                  type: integer
    """
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Utilisateur non trouvé'
            }), 404
        
        total_recordings = Recording.query.filter_by(user_id=user.id).count()
        total_duration = db.session.query(func.sum(Recording.duration)).filter_by(user_id=user.id).scalar() or 0
        
        today = datetime.utcnow().date()
        today_recordings = Recording.query.filter(
            Recording.user_id == user.id,
            func.date(Recording.created_at) == today
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_recordings': total_recordings,
                'total_duration_seconds': round(total_duration, 2),
                'total_duration_minutes': round(total_duration / 60, 2),
                'today_recordings': today_recordings
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500

@api_swagger_bp.route('/languages', methods=['GET'])
@jwt_required()
def api_get_languages():
    """
    Liste des langues disponibles
    ---
    tags:
      - Langues
    security:
      - Bearer: []
    responses:
      200:
        description: Liste des langues récupérée
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                languages:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
                      code:
                        type: string
                      total_sentences:
                        type: integer
    """
    try:
        languages = Language.query.all()
        
        return jsonify({
            'success': True,
            'data': {
                'languages': [
                    {
                        'id': lang.id,
                        'name': lang.name,
                        'code': lang.code,
                        'total_sentences': len(lang.sentences)
                    } for lang in languages
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500

@api_swagger_bp.route('/sentences/next', methods=['GET'])
@jwt_required()
def api_get_next_sentence():
    """
    Prochaine phrase à enregistrer
    ---
    tags:
      - Phrases
    security:
      - Bearer: []
    parameters:
      - in: query
        name: language_id
        type: integer
        required: false
        description: ID de la langue (optionnel)
    responses:
      200:
        description: Phrase récupérée
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                sentence:
                  type: object
                  properties:
                    id:
                      type: integer
                    text:
                      type: string
                    translation:
                      type: string
                    language:
                      type: object
    """
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Utilisateur non trouvé'
            }), 404
        
        language_id = request.args.get('language_id')
        
        recorded_sentence_ids = [r.sentence_id for r in user.recordings]
        
        query = Sentence.query
        
        if language_id:
            query = query.filter_by(language_id=int(language_id))
        
        query = query.filter(
            ~Sentence.id.in_(recorded_sentence_ids) if recorded_sentence_ids else True
        )
        
        available_sentences = query.all()
        
        if not available_sentences:
            return jsonify({
                'success': True,
                'message': 'Vous avez enregistré toutes les phrases disponibles',
                'data': {
                    'sentence': None
                }
            }), 200
        
        sentence = random.choice(available_sentences)
        
        return jsonify({
            'success': True,
            'data': {
                'sentence': {
                    'id': sentence.id,
                    'text': sentence.text,
                    'translation': sentence.translation,
                    'language': {
                        'id': sentence.language.id,
                        'name': sentence.language.name,
                        'code': sentence.language.code
                    }
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500

@api_swagger_bp.route('/recordings', methods=['POST'])
@jwt_required()
def api_save_recording():
    """
    Sauvegarder un enregistrement audio
    ---
    tags:
      - Enregistrements
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: audio
        type: file
        required: true
        description: Fichier audio (WAV, WebM, MP3, OGG, M4A, AAC)
      - in: formData
        name: sentence_id
        type: integer
        required: true
        description: ID de la phrase
      - in: formData
        name: duration
        type: number
        required: true
        description: Durée en secondes
    responses:
      201:
        description: Enregistrement sauvegardé
      400:
        description: Fichier ou sentence_id manquant
      409:
        description: Phrase déjà enregistrée
    """
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Utilisateur non trouvé'
            }), 404
        
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'message': 'Fichier audio manquant'
            }), 400
        
        audio_file = request.files['audio']
        sentence_id = request.form.get('sentence_id')
        duration = float(request.form.get('duration', 0))
        
        if not sentence_id:
            return jsonify({
                'success': False,
                'message': 'ID de phrase manquant'
            }), 400
        
        sentence = Sentence.query.get(sentence_id)
        if not sentence:
            return jsonify({
                'success': False,
                'message': 'Phrase non trouvée'
            }), 404
        
        existing = Recording.query.filter_by(
            user_id=user.id,
            sentence_id=sentence_id
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'message': 'Vous avez déjà enregistré cette phrase'
            }), 409
        
        file_ext = 'wav'
        if audio_file.filename and '.' in audio_file.filename:
            original_ext = audio_file.filename.rsplit('.', 1)[1].lower()
            if original_ext in ['wav', 'webm', 'mp3', 'ogg', 'm4a', 'aac']:
                file_ext = original_ext
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"user{user.id}_sentence{sentence_id}_{timestamp}.{file_ext}"
        
        upload_folder = 'uploads/audio'
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        audio_file.save(filepath)
        
        recording = Recording(
            user_id=user.id,
            sentence_id=sentence_id,
            audio_path=filepath,
            duration=duration
        )
        
        db.session.add(recording)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Enregistrement sauvegardé avec succès',
            'data': {
                'recording': {
                    'id': recording.id,
                    'duration': recording.duration,
                    'created_at': recording.created_at.isoformat()
                }
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la sauvegarde: {str(e)}'
        }), 500

@api_swagger_bp.route('/recordings', methods=['GET'])
@jwt_required()
def api_get_recordings():
    """
    Liste des enregistrements utilisateur
    ---
    tags:
      - Enregistrements
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
        description: Numéro de page
      - in: query
        name: per_page
        type: integer
        default: 20
        description: Éléments par page
    responses:
      200:
        description: Liste des enregistrements
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                recordings:
                  type: array
                pagination:
                  type: object
    """
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Utilisateur non trouvé'
            }), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        recordings_query = Recording.query.filter_by(user_id=user.id).order_by(Recording.created_at.desc())
        
        total = recordings_query.count()
        recordings = recordings_query.limit(per_page).offset((page - 1) * per_page).all()
        
        return jsonify({
            'success': True,
            'data': {
                'recordings': [
                    {
                        'id': rec.id,
                        'duration': rec.duration,
                        'created_at': rec.created_at.isoformat(),
                        'sentence': {
                            'id': rec.sentence.id,
                            'text': rec.sentence.text,
                            'translation': rec.sentence.translation,
                            'language': {
                                'id': rec.sentence.language.id,
                                'name': rec.sentence.language.name,
                                'code': rec.sentence.language.code
                            }
                        }
                    } for rec in recordings
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur: {str(e)}'
        }), 500

@api_swagger_bp.route('/provinces', methods=['GET'])
def api_get_provinces():
    """
    Liste des provinces de la RDC
    ---
    tags:
      - Public
    responses:
      200:
        description: Liste des provinces
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                provinces:
                  type: array
                  items:
                    type: string
    """
    return jsonify({
        'success': True,
        'data': {
            'provinces': PROVINCES
        }
    }), 200
