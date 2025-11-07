
# init_db.py
import os
import sys
import csv
from app import app, db

def init_database():
    with app.app_context():
        try:
            print("🔄 Initialisation de la base de données...")
            
            # Crée toutes les tables
            db.create_all()
            print("✅ Tables créées avec succès!")
            
            # Vérifie et initialise les données de base
            from models import User, Language, Sentence
            
            # Créer l'admin s'il n'existe pas
            admin = User.query.filter_by(is_admin=True).first()
            if not admin:
                admin = User(
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
                
                admin_password = os.environ.get('ADMIN_PASSWORD')
                
                if not admin_password:
                    raise ValueError("ADMIN_PASSWORD non défini dans les variables d'environnement. Ajoute-le dans ton fichier .env.")
                
                
                admin.set_password(admin_password)
                db.session.add(admin)
                print("✅ Compte admin créé")
            
            # Créer la langue Rund si elle n'existe pas
            rund = Language.query.filter_by(code='rund').first()
            if not rund:
                rund = Language(
                    name='Rund',
                    code='rund',
                    csv_file='languages/rund.csv'
                )
                db.session.add(rund)
                db.session.commit()
                print("✅ Langue Rund créée")
                
                # Créer le fichier CSV s'il n'existe pas
                if not os.path.exists(rund.csv_file):
                    os.makedirs(os.path.dirname(rund.csv_file), exist_ok=True)
                    with open(rund.csv_file, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['text', 'translation'])
                        writer.writerow(['Bonjour', 'Hello'])
                        writer.writerow(['Merci', 'Thank you'])
                    print("✅ Fichier CSV créé avec des exemples")
            
            # Charger les phrases depuis le CSV
            if os.path.exists(rund.csv_file):
                with open(rund.csv_file, 'r', encoding='utf-8') as f:
                    csv_reader = csv.DictReader(f)
                    sentences_added = 0
                    
                    for row in csv_reader:
                        text = row.get('text', '').strip()
                        translation = row.get('translation', '').strip()
                        
                        if text and translation:
                            # Vérifier si la phrase existe déjà
                            existing = Sentence.query.filter_by(
                                language_id=rund.id,
                                text=text
                            ).first()
                            
                            if not existing:
                                sentence = Sentence(
                                    language_id=rund.id,
                                    text=text,
                                    translation=translation
                                )
                                db.session.add(sentence)
                                sentences_added += 1
                
                if sentences_added > 0:
                    db.session.commit()
                    print(f"✅ {sentences_added} phrases chargées depuis {rund.csv_file}")
                else:
                    print("ℹ️  Toutes les phrases sont déjà en base")
            else:
                print(f"⚠️  Fichier CSV introuvable: {rund.csv_file}")
            
            db.session.commit()
            print("🎉 Base de données initialisée avec succès!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
