# Application de Préservation de la Langue Rund

Cette application Flask permet de préserver la langue Rund, une langue parlée rare, en créant une archive numérique d'enregistrements vocaux pour la recherche linguistique.

## Comment utiliser l'application

### Démarrage de l'application

#### Configuration préalable

1. **Installer les dépendances** :
   ```bash
   pip install -r requirement.txt
   ```

2. **Variables d'environnement obligatoires** :
   - `SESSION_SECRET` : Clé secrète pour sécuriser les sessions (exemple: "votre-cle-secrete-tres-longue")
   - `DATABASE_URL` : URL de connexion à la base de données PostgreSQL (exemple: "postgresql://user:password@localhost/rund_db")

   Exemple de configuration :
   ```bash
   export SESSION_SECRET="votre-cle-secrete-tres-longue"
   export DATABASE_URL="postgresql://user:password@localhost/rund_db"
   ```

#### Lancement

1. Configurez les variables d'environnement ci-dessus
2. Lancez l'application avec : `python main.py`
3. Ouvrez votre navigateur et allez à l'adresse indiquée (généralement http://localhost:5000)

### Pour les utilisateurs

#### 1. Inscription
- Cliquez sur "S'inscrire" sur la page d'accueil
- Remplissez tous les champs obligatoires :
  - Nom complet
  - Sexe
  - Âge
  - Provenance (lieu d'origine)
  - Adresse email
  - Mot de passe
- **Important :** Vous devez accepter la politique de confidentialité pour vous inscrire
- Cliquez sur "S'inscrire"

#### 2. Connexion
- Cliquez sur "Se connecter"
- Entrez votre email et mot de passe
- Cliquez sur "Se connecter"

#### 3. Enregistrement de phrases
- Une fois connecté, vous serez automatiquement dirigé vers la page d'enregistrement
- Une phrase en langue Rund vous sera présentée aléatoirement
- Cliquez sur le bouton pour commencer l'enregistrement audio
- Lisez la phrase à voix haute
- Arrêtez l'enregistrement et sauvegardez-le
- Répétez le processus avec de nouvelles phrases

### Pour l'administrateur

#### Connexion admin
- Email : `admin@rund.local`
- Mot de passe : `31082003`

#### Fonctionnalités admin
1. **Tableau de bord** : Accédez à `/admin` pour voir tous les enregistrements
2. **Statistiques** : Visualisez le nombre d'enregistrements du jour
3. **Export des données** : Téléchargez toutes les données en format CSV
4. **Gestion des enregistrements** : Supprimez des enregistrements individuels si nécessaire
5. **Gestion des utilisateurs** : Supprimez des utilisateurs et tous leurs enregistrements

### Structure des données

L'application stocke :
- **Utilisateurs** : Informations personnelles et consentement
- **Phrases** : Textes en langue Rund à enregistrer
- **Enregistrements** : Fichiers audio liés aux utilisateurs et phrases

### Politique de confidentialité

- Tous les utilisateurs doivent donner leur consentement explicite
- Les données sont utilisées uniquement pour la recherche linguistique
- L'accès aux données est restreint aux administrateurs autorisés

### Fonctionnalités techniques

- **Sécurité** : Authentification sécurisée avec hashage des mots de passe
- **Validation** : Vérification des fichiers audio (max 10MB, formats WAV/WebM/OGG/MP3)
- **Base de données** : PostgreSQL pour un stockage fiable
- **Interface** : Design responsive avec Bootstrap 5

### Support

Si vous rencontrez des problèmes ou avez des questions, contactez l'administrateur système.