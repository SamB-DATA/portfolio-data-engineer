# Architecture technique du MVP RAG Events

## Objectif

Ce document décrit l’architecture technique du MVP RAG Events.

L’objectif du MVP est de transformer un POC RAG en application backend plus structurée, conteneurisée et préparée pour un déploiement cloud.

Le système permet de recommander des événements culturels à partir d’une recherche utilisateur, d’un moteur de recherche sémantique et d’un modèle LLM.

## Vue d’ensemble

Le MVP est organisé autour de plusieurs composants :

- une API FastAPI ;
- un service d’ingestion de données ;
- un service d’embedding ;
- un service de recherche ;
- un service RAG ;
- un service LLM ;
- un service de mémoire conversationnelle ;
- un système de logs applicatifs ;
- une configuration Docker ;
- une version cloud-light pour AWS EC2.

## Architecture logique

Utilisateur
   |
   v
API FastAPI
   |
   +-- Endpoint /documents
   |      +-- Lecture des événements JSON
   |
   +-- Endpoint /rag/build-index
   |      +-- Création des embeddings
   |      +-- Construction de l’index
   |
   +-- Endpoint /rag/search
   |      +-- Recherche sémantique
   |      +-- Retour des événements pertinents
   |
   +-- Endpoint /rag/ask
   |      +-- Recherche des documents
   |      +-- Construction du prompt RAG
   |      +-- Appel API Mistral
   |      +-- Réponse avec sources
   |
   +-- Endpoint /chat/ask
          +-- Gestion session_id
          +-- Récupération historique
          +-- Enrichissement de la question
          +-- Réponse RAG contextualisée

## Architecture locale complète

La version locale complète utilise :

- FastAPI pour exposer les endpoints ;
- Sentence Transformers pour créer les embeddings ;
- FAISS pour l’index vectoriel ;
- Mistral pour générer les réponses ;
- Docker Compose pour lancer l’application ;
- un fichier .env pour les variables sensibles ;
- un fichier logging.yaml pour les logs.

Cette version est plus proche de la logique RAG complète, mais elle nécessite davantage de ressources à cause des dépendances ML.

## Architecture cloud-light

Une branche cloud-light a été créée pour le déploiement AWS EC2.

Cette version remplace les dépendances ML lourdes par une approche plus légère basée sur NumPy.

Objectif :

- réduire la taille de l’image Docker ;
- éviter les erreurs de stockage sur une instance EC2 micro ;
- respecter la contrainte de coût zéro ou quasi zéro ;
- démontrer le déploiement cloud sans surdimensionner l’infrastructure.

Cette version garde l’architecture globale :

- API FastAPI ;
- ingestion JSON ;
- index léger ;
- recherche sémantique simplifiée ;
- service RAG ;
- mémoire conversationnelle ;
- Docker ;
- déploiement EC2.

## Endpoints principaux

GET /health

Vérifie que l’API fonctionne.

GET /documents

Retourne les événements chargés depuis le fichier JSON.

POST /rag/build-index

Construit l’index de recherche.

GET /rag/status

Vérifie l’existence de l’index.

POST /rag/search

Recherche les événements les plus pertinents.

POST /rag/ask

Génère une réponse RAG avec les sources.

POST /chat/ask

Pose une question avec mémoire conversationnelle.

GET /chat/history/{session_id}

Retourne l’historique d’une session.

DELETE /chat/history/{session_id}

Supprime l’historique d’une session.

## Choix techniques

### FastAPI

J’ai choisi FastAPI car c’est un framework Python moderne, léger et adapté aux APIs de données et d’IA.

Il permet aussi de générer automatiquement une documentation Swagger, utile pour tester et présenter le MVP.

### Docker

Docker permet de rendre le projet reproductible.

L’objectif est de pouvoir lancer l’application localement ou sur un serveur cloud avec la même base technique.

### Mistral

Mistral est utilisé pour générer des réponses naturelles à partir du contexte retrouvé par le moteur de recherche.

Le prompt limite les hallucinations en demandant au modèle de répondre uniquement à partir du contexte fourni.

### FAISS en local

FAISS est utilisé dans la version locale complète pour simuler une base vectorielle performante.

C’est un bon choix pour un POC ou un MVP local car il est rapide et simple à intégrer.

### Version cloud-light

La version cloud-light a été créée à cause des contraintes d’une petite instance EC2.

Les dépendances comme Torch, Sentence Transformers et FAISS peuvent être trop lourdes pour une instance micro.

La version allégée permet donc de démontrer le déploiement cloud sans générer de coûts inutiles.

## Sécurité

Le projet applique plusieurs principes de sécurité :

- variables sensibles dans un fichier .env non versionné ;
- fichier .env.example pour documenter les variables attendues ;
- clés API exclues du dépôt GitHub ;
- accès AWS via utilisateur IAM dédié ;
- séparation entre utilisateur root AWS et utilisateur IAM ;
- budget AWS configuré ;
- règle entrante EC2 limitée pour les tests ;
- instance EC2 arrêtée après démonstration.

## Scalabilité

La version actuelle est un MVP.

Pour passer à une architecture scalable, les évolutions possibles sont :

- remplacer l’index local par une base vectorielle managée ;
- déployer l’API sur ECS Fargate ;
- ajouter un load balancer ;
- externaliser la mémoire conversationnelle dans Redis ou DynamoDB ;
- stocker les données dans S3 ;
- ajouter CloudWatch pour l’observabilité ;
- ajouter un pipeline CI/CD avec GitHub Actions.

## Limites

Les limites actuelles sont :

- index local ;
- mémoire conversationnelle non persistée ;
- absence de base de données ;
- absence de CI/CD ;
- absence de monitoring CloudWatch avancé ;
- version cloud simplifiée ;
- pas de haute disponibilité.

## Conclusion

L’architecture actuelle permet de démontrer le passage d’un POC RAG à un MVP backend structuré.

Le projet montre une capacité à arbitrer entre qualité technique, coût cloud, sécurité et contraintes matérielles.

La version locale démontre la logique RAG complète.

La version cloud-light démontre la capacité à adapter le système pour un déploiement AWS à coût maîtrisé.