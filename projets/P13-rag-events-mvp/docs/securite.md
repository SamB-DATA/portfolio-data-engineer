# Sécurité du projet RAG Events MVP

## Objectif

Ce document présente les mesures de sécurité mises en place dans le projet RAG Events MVP.

Même si le projet reste un MVP pédagogique, plusieurs bonnes pratiques de sécurité ont été appliquées afin de :
- protéger les données sensibles ;
- limiter les risques cloud ;
- éviter les erreurs classiques ;
- préparer une architecture plus robuste.

## Gestion des secrets

### Fichier .env

Les variables sensibles sont stockées dans un fichier `.env`.

Exemples :
- clés API ;
- variables de configuration ;
- paramètres cloud.

Le fichier `.env` n’est jamais versionné sur GitHub.

## Fichier .gitignore

Le projet contient un `.gitignore` afin d’exclure :
- `.env`
- fichiers temporaires ;
- caches Python ;
- logs ;
- artefacts Docker.

Objectif :
éviter l’exposition accidentelle de secrets ou de données inutiles.

## Fichier .env.example

Un fichier `.env.example` est fourni afin de :
- documenter les variables nécessaires ;
- faciliter le déploiement ;
- éviter de partager un vrai fichier `.env`.

Aucune clé réelle n’est stockée dans ce fichier.

## Sécurité AWS

### Séparation root / IAM

Le compte AWS applique une séparation entre :
- le compte root ;
- un utilisateur IAM administrateur dédié.

Le compte root n’est utilisé que pour :
- la configuration initiale ;
- les opérations critiques.

Toutes les opérations courantes sont réalisées avec un utilisateur IAM.

### MFA

L’authentification multifacteur a été activée sur le compte AWS.

Objectif :
réduire les risques de compromission du compte cloud.

### Budget AWS

Des alertes budgétaires AWS ont été configurées.

Objectif :
- éviter les coûts imprévus ;
- contrôler la consommation cloud ;
- respecter une stratégie de coût proche de zéro.

## Sécurité réseau

### Security Group AWS

Le Security Group EC2 limite les accès réseau.

Seuls les ports nécessaires sont ouverts :
- SSH ;
- port applicatif temporaire pour la démonstration.

Le port 8000 n’est pas laissé ouvert publiquement en permanence.

### Restriction IP

Les règles réseau utilisent le mode :
- "Mon IP"

Objectif :
limiter l’exposition du serveur EC2.

## Docker

### Isolation du conteneur

L’application est exécutée dans un conteneur Docker isolé.

Avantages :
- environnement reproductible ;
- limitation des dépendances système ;
- séparation application / machine hôte.

### Réduction de surface d’attaque

La version cloud-light réduit :
- le nombre de dépendances ;
- la taille de l’image Docker ;
- les risques liés aux bibliothèques lourdes.

## Logs applicatifs

Le projet génère des logs applicatifs :
- démarrage API ;
- requêtes ;
- erreurs ;
- monitoring minimal.

Les logs sont stockés dans :
```text
logs/app.log

Sécurité API
Validation des entrées

FastAPI et Pydantic permettent :

la validation automatique des requêtes ;
le contrôle des types ;
la réduction des erreurs de format.
Prompt contrôlé

Le service RAG construit un prompt limitant les hallucinations du modèle.

Le LLM est encouragé à répondre uniquement à partir du contexte fourni.

Limites actuelles

Le projet reste un MVP pédagogique.

Certaines protections avancées ne sont pas encore implémentées :

HTTPS ;
WAF ;
gestion avancée des rôles IAM ;
chiffrement avancé ;
audit logs centralisés ;
rate limiting ;
authentification utilisateur ;
secrets manager AWS ;
monitoring sécurité avancé.
Améliorations possibles

Les évolutions futures possibles sont :

intégration AWS Secrets Manager ;
HTTPS avec Nginx ;
ajout d’un reverse proxy ;
ajout d’authentification JWT ;
ajout d’un système RBAC ;
centralisation des logs ;
intégration CloudWatch ;
scans de vulnérabilités Docker ;
CI/CD sécurisé.
Conclusion

Même si ce projet reste un MVP, plusieurs bonnes pratiques de sécurité ont été appliquées :

gestion correcte des secrets ;
séparation IAM ;
contrôle budgétaire ;
isolation Docker ;
sécurisation réseau ;
validation des données ;
limitation de l’exposition cloud.

Ces éléments permettent de construire une base plus propre et plus crédible pour un projet Data Engineer orienté cloud et IA.