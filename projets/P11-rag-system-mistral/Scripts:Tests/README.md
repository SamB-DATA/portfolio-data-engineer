# 🎯 Projet 11 – Système RAG de recommandation d’événements

## Présentation

Dans ce projet, j’ai développé un système de recommandation d’événements culturels et scientifiques basé sur une architecture RAG (Retrieval-Augmented Generation).

L’objectif est de permettre à un utilisateur de poser une question en langage naturel, par exemple « Je cherche une exposition artistique » ou « Je veux une conférence scientifique », et d’obtenir une réponse structurée, contextualisée et cohérente à partir de données réelles issues d’OpenAgenda.

Ce projet a été réalisé dans une logique de proof of concept. Il couvre l’ensemble de la chaîne de traitement :
- ingestion des données
- nettoyage et structuration
- préparation des documents
- vectorisation
- recherche sémantique
- génération de réponses
- évaluation simple du système

---

## Objectif métier

L’objectif métier est de démontrer la faisabilité d’un assistant capable de recommander des événements pertinents à partir d’une base de données vectorielle, en combinant :
- un moteur de recherche sémantique
- un modèle de langage
- un pipeline de données reproductible

Le système est conçu pour répondre à des questions utilisateur en langage naturel, sans avoir recours à une recherche manuelle par mots-clés.

---

## Architecture générale du système

Le système repose sur une architecture RAG, qui combine deux étapes :
- Retrieval : récupération des documents les plus pertinents
- Generation : génération d’une réponse à partir du contexte retrouvé

Schéma simplifié du RAG :

Utilisateur
   ↓
Question en langage naturel
   ↓
Embedding de la requête
   ↓
Recherche vectorielle dans FAISS
   ↓
Top-k documents les plus pertinents
   ↓
Construction du prompt
   ↓
Modèle Mistral
   ↓
Réponse générée

---

## Schéma complet du pipeline du projet

OpenAgenda API
   ↓
Ingestion des événements
   ↓
Stockage brut en JSON
   ↓
Préprocessing des données
   ↓
Nettoyage / filtrage / structuration
   ↓
Création d’un CSV propre
   ↓
Préparation des documents textuels
   ↓
Embeddings
   ↓
Index vectoriel FAISS
   ↓
Question utilisateur
   ↓
Recherche sémantique
   ↓
Récupération du contexte
   ↓
Prompt enrichi
   ↓
Mistral
   ↓
Réponse finale

---

## Sources de données

Les données proviennent de la source OpenAgenda, conformément au cahier des charges du projet.

J’ai utilisé l’API OpenAgenda pour récupérer des événements publics à partir d’un agenda sélectionné. Les données récupérées contiennent notamment :
- le titre
- la description
- la date de début et de fin
- le lieu
- la ville
- l’adresse
- certains mots-clés ou métadonnées

J’ai également exploré le dataset OpenDataSoft des événements publics OpenAgenda, mais les champs de dates y présentaient des anomalies importantes. J’ai donc retenu l’API OpenAgenda comme source principale du pipeline final.

---

## Périmètre du projet

Le système a été construit à partir d’un périmètre géographique restreint, centré sur les événements de l’agenda sélectionné autour de Paris-Saclay.

Les villes retrouvées dans le dataset final incluent notamment :
- Paris
- Gif-sur-Yvette
- Palaiseau
- Saclay
- Orsay
- Évry
- Évry-Courcouronnes
- Saint-Aubin
- Versailles
- Bures-sur-Yvette
- Pantin
- Le Kremlin-Bicêtre
- Guyancourt

Ce choix de périmètre permet de garder un dataset cohérent et exploitable pour un proof of concept.

---

## Stack technique

J’ai utilisé les outils suivants :

- Python 3.13
- Pandas pour la manipulation et le nettoyage des données
- Requests pour les appels API
- LangChain pour orchestrer le pipeline RAG
- Mistral AI pour les embeddings et la génération de réponses
- FAISS pour la recherche vectorielle
- Pytest pour les tests unitaires

---

## Structure du projet

Le projet est organisé de la manière suivante :

projet_11_rag_events/
│
├── data/
│   ├── raw/                  données brutes JSON
│   ├── processed/            données nettoyées et documents préparés
│   ├── vectorstore/          index FAISS
│   └── test/                 jeu de test et résultats d’évaluation
│
├── src/
│   ├── ingestion_openagenda_api.py
│   ├── preprocessing.py
│   ├── prepare_documents.py
│   ├── vectorstore.py
│   ├── rag.py
│   ├── chatbot.py
│   ├── evaluate_rag.py
│   ├── retrieval_demo.py
│   ├── check_env.py
│   ├── check_mistral_key.py
│   ├── inspect_raw.py
│   └── test_data_quality.py
│
├── tests/
│   └── test_qa.json
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore

---

## Fichiers principaux

- ingestion_openagenda_api.py  
  Récupère les événements via l’API OpenAgenda et les sauvegarde dans `data/raw/events_raw.json`

- preprocessing.py  
  Nettoie les données, filtre les lignes incohérentes et produit `data/processed/events_clean.csv`

- prepare_documents.py  
  Transforme chaque événement en document textuel structuré pour le RAG

- vectorstore.py  
  Génère les embeddings et construit l’index vectoriel FAISS

- rag.py  
  Exécute un pipeline RAG simple avec retrieval + génération

- chatbot.py  
  Lance une interface CLI permettant de dialoguer avec le système

- evaluate_rag.py  
  Exécute le système sur un jeu de test et produit un fichier de résultats

- test_data_quality.py  
  Vérifie la qualité des données intégrées dans le pipeline

---

## Reproductibilité du projet

Le projet a été conçu pour être reproductible.

Les scripts permettent de reconstruire le pipeline à partir de zéro :
1. ingestion des données
2. nettoyage
3. préparation des documents
4. vectorisation
5. lancement du chatbot

Pour des raisons de sécurité et de volume :
- le fichier `.env` n’est pas versionné
- le vector store FAISS n’est pas versionné
- les données brutes ne sont pas destinées à être versionnées systématiquement

Un échantillon de données propres peut être conservé pour faciliter la démonstration et la reproductibilité du projet.

---

## Installation

### 1. Créer l’environnement virtuel

python3 -m venv .venv
source .venv/bin/activate

### 2. Installer les dépendances

pip install -r requirements.txt

### 3. Configurer les variables d’environnement

Créer un fichier `.env` à partir de `.env.example` et renseigner les clés :

OPENAGENDA_API_KEY=...
MISTRAL_API_KEY=...

---

## Exécution du pipeline

### 1. Ingestion des données

python src/ingestion_openagenda_api.py

### 2. Préprocessing

python src/preprocessing.py

### 3. Préparation des documents

python src/prepare_documents.py

### 4. Création de la base vectorielle

python src/vectorstore.py

### 5. Test du pipeline RAG

python src/rag.py

### 6. Lancement du chatbot

python src/chatbot.py

### 7. Évaluation du système

python src/evaluate_rag.py

---

## Tests unitaires

Les tests sont exécutés avec pytest :

pytest

Les tests permettent de vérifier notamment :
- l’existence du fichier nettoyé
- la présence des colonnes obligatoires
- la validité des dates
- la cohérence du périmètre géographique
- la qualité minimale des données intégrées

---

## Jeu de test d’évaluation

J’ai créé un jeu de test composé de 12 questions/réponses attendues dans :

data/test/test_qa.json

Le script `evaluate_rag.py` produit ensuite :

data/test/test_results.json

Ce mécanisme permet d’évaluer qualitativement la cohérence du système sur des requêtes représentatives :
- exposition artistique
- conférence scientifique
- événement lié à l’intelligence artificielle
- événement culturel par ville
- concert ou soirée musicale
- etc.

---

## Exemple de fonctionnement

Question :
Je cherche une conférence scientifique

Réponse attendue :
Le système doit proposer au moins une conférence pertinente avec son titre, sa date et son lieu.

Exemple de réponse générée :
Le système recommande une conférence scientifique à Gif-sur-Yvette avec le titre, la date, le lieu et une description concise.

---

## Résultats obtenus

Le système est capable :
- de retrouver des événements cohérents avec la requête
- de produire des réponses structurées
- de s’appuyer sur le contexte retrouvé
- de recommander des événements par thématique ou par ville

Les tests unitaires passent et l’évaluation sur le jeu de test montre des réponses globalement pertinentes.

---

## Limites du projet

Ce projet reste un proof of concept et présente plusieurs limites :

- le volume de données reste limité
- le système dépend fortement de la qualité des données sources
- l’évaluation est surtout qualitative
- les documents n’ont pas été découpés en chunks, car ils étaient déjà relativement courts
- certaines métadonnées restent brutes, comme certains codes ou mots-clés
- l’interface est uniquement en ligne de commande

---

## Axes d’amélioration

Plusieurs pistes d’amélioration sont possibles :

- enrichir le dataset
- améliorer le filtrage par date et par localisation
- ajouter une interface web
- mettre en place des métriques d’évaluation plus avancées
- améliorer le traitement des métadonnées
- industrialiser le pipeline avec une API de déploiement

---

## Choix techniques principaux

J’ai choisi :
- FAISS pour construire une base vectorielle locale, simple et efficace
- LangChain pour orchestrer le retrieval et la génération
- Mistral pour les embeddings et la génération de texte
- un périmètre de données restreint pour garantir la cohérence du POC

J’ai également fait le choix de ne pas mettre en place de chunking avancé, car les documents issus des événements étaient relativement courts et compréhensibles tels quels.

---

## Auteur

Samir Belasri

Projet réalisé dans le cadre d’un projet de data engineering autour de la mise en place d’un système RAG de recommandation d’événements.

---

