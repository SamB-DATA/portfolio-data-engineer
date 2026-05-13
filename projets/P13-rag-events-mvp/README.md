# RAG Events MVP - Projet 13 Data Engineer

## Présentation du projet

Ce projet correspond au MVP d’un système RAG dédié à la recommandation d’événements culturels.

Je suis parti d’un premier POC développé dans le projet 11 puis j’ai transformé cette première version en application backend plus structurée, conteneurisée et préparée pour le cloud.

L’objectif du projet est de démontrer ma capacité à faire évoluer une architecture IA locale vers un MVP plus proche d’un contexte réel de production.

Le projet inclut :
- une API FastAPI ;
- une recherche sémantique ;
- un moteur RAG ;
- une intégration LLM avec Mistral ;
- une mémoire conversationnelle ;
- une architecture Docker ;
- un déploiement AWS EC2 ;
- une gestion des logs et du monitoring ;
- une gestion sécurisée de la configuration.

## Objectifs du projet

Avec ce projet, je démontre ma capacité à :

- développer une API backend avec FastAPI ;
- manipuler des embeddings ;
- utiliser une recherche vectorielle ;
- intégrer un modèle LLM ;
- construire un pipeline RAG ;
- gérer des conversations multi-tours ;
- conteneuriser une application avec Docker ;
- déployer une application sur AWS ;
- sécuriser la configuration avec des variables d’environnement ;
- mettre en place une stratégie de monitoring ;
- gérer les contraintes de coûts cloud.

## Fonctionnalités principales

- API REST FastAPI
- Documentation Swagger
- Ingestion de données JSON
- Génération d’embeddings
- Recherche sémantique
- Réponses RAG avec Mistral
- Mémoire conversationnelle locale
- Logs applicatifs
- Docker Compose
- Déploiement AWS EC2
- Version cloud optimisée pour Free Tier AWS

## Architecture simplifiée

Utilisateur
   |
   v
FastAPI
   |
   +-- Ingestion JSON
   +-- Embeddings
   +-- Recherche vectorielle
   +-- Construction du prompt RAG
   +-- API Mistral
   +-- Mémoire conversationnelle
   +-- Réponse utilisateur

## Structure du projet

.
├── app
│   ├── core
│   ├── models
│   ├── services
│   └── main.py
├── config
│   ├── app.yaml
│   └── logging.yaml
├── data
│   └── raw
├── docker
│   └── Dockerfile
├── docs
├── logs
├── monitoring
├── notebooks
├── reports
├── tests
├── vector_store
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt

## Technologies utilisées

- Python
- FastAPI
- Uvicorn
- Docker
- Docker Compose
- NumPy
- Mistral API
- YAML
- Git
- GitHub
- AWS EC2

## Développement local

### Cloner le projet

git clone https://github.com/SamB-DATA/rag-events-mvp.git

cd rag-events-mvp

### Créer le fichier .env

cp .env.example .env

### Lancer le projet

docker compose up --build

### Ouvrir Swagger

http://localhost:8000/docs

## Déploiement cloud AWS

Le projet a été déployé sur une instance AWS EC2 Linux avec Docker.

Une version allégée appelée `cloud-light` a été créée pour le cloud afin de respecter les contraintes du Free Tier AWS.

Cette version retire les dépendances ML lourdes afin de :
- réduire la taille Docker ;
- limiter la consommation mémoire ;
- éviter les coûts inutiles ;
- rendre le déploiement compatible avec une instance EC2 micro.

## Pourquoi une version cloud-light

La version locale complète utilise :
- Sentence Transformers ;
- Torch ;
- FAISS.

Ces bibliothèques deviennent rapidement lourdes pour une petite instance EC2 gratuite.

J’ai donc créé une version cloud optimisée afin de :
- démontrer le déploiement cloud ;
- conserver l’architecture RAG ;
- respecter une contrainte de coût proche de zéro ;
- adapter le projet à un environnement AWS Free Tier.

Cette décision correspond à un arbitrage technique entre :
- performance ;
- coût ;
- ressources disponibles ;
- simplicité d’exploitation.

## Endpoints principaux

GET /health
GET /documents
POST /rag/build-index
GET /rag/status
POST /rag/search
POST /rag/ask
POST /chat/ask
GET /chat/history/{session_id}
DELETE /chat/history/{session_id}

## Exemple de requête

{
  "session_id": "samir-test",
  "query": "Je cherche un concert de musique",
  "top_k": 2
}

## Exemple de réponse

{
  "session_id": "samir-test",
  "query": "Je cherche un concert de musique",
  "answer": "Voici les concerts qui correspondent à votre recherche.",
  "sources": [
    {
      "title": "Concert classique en plein air",
      "location": "Bordeaux"
    }
  ]
}

## Sécurité

Le projet utilise :
- un fichier .env non versionné ;
- un .gitignore ;
- un utilisateur IAM AWS dédié ;
- une séparation entre root AWS et IAM ;
- des alertes budget AWS ;
- un contrôle des accès réseau.

## Monitoring

Le projet inclut :
- des logs applicatifs ;
- un middleware de monitoring ;
- des traces de requêtes API ;
- un fichier logs/app.log.

## Limites actuelles du MVP

Cette version reste un MVP.

Limites actuelles :
- mémoire conversationnelle stockée localement ;
- pas de base de données ;
- pas de CI/CD ;
- pas de Kubernetes ;
- pas de monitoring CloudWatch avancé ;
- pas de stockage distribué ;
- version cloud simplifiée pour Free Tier.

## Prochaines améliorations

- ajouter des tests automatisés ;
- mettre en place GitHub Actions ;
- ajouter CloudWatch ;
- ajouter HTTPS ;
- ajouter un nom de domaine ;
- ajouter une vraie base vectorielle ;
- améliorer l’évaluation RAG ;
- améliorer la sécurité cloud.

## Compétences démontrées

Avec ce projet, je démontre des compétences en :
- développement backend Python ;
- API REST ;
- architecture RAG ;
- intégration LLM ;
- recherche vectorielle ;
- Docker ;
- Git/GitHub ;
- cloud AWS ;
- sécurité cloud ;
- monitoring ;
- gestion des coûts cloud.

## Auteur

Samir Belasri

Projet 13 - Parcours Data Engineer OpenClassrooms