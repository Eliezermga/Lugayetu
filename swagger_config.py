from flasgger import Swagger

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api-docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Lugayetu API",
        "description": "API pour la plateforme de préservation et numérisation des langues en danger de la RDC",
        "version": "1.0.0",
        "contact": {
            "name": "Équipe Lugayetu",
            "url": "https://lugayetu.cd"
        }
    },
    "host": "",
    "basePath": "/",
    "schemes": ["https", "http"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Entrez votre token JWT dans le format: Bearer <token>"
        }
    },
    "tags": [
        {
            "name": "Authentification",
            "description": "Endpoints pour l'inscription et la connexion"
        },
        {
            "name": "Utilisateur",
            "description": "Gestion du profil utilisateur"
        },
        {
            "name": "Langues",
            "description": "Gestion des langues disponibles"
        },
        {
            "name": "Phrases",
            "description": "Récupération des phrases à enregistrer"
        },
        {
            "name": "Enregistrements",
            "description": "Gestion des enregistrements audio"
        },
        {
            "name": "Public",
            "description": "Endpoints publics sans authentification"
        }
    ]
}

def init_swagger(app):
    return Swagger(app, config=swagger_config, template=swagger_template)
