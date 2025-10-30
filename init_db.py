# init_db.py
import os
import sys
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
                admin.set_password('31082003')
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
            
            db.session.commit()
            print("🎉 Base de données initialisée avec succès!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)