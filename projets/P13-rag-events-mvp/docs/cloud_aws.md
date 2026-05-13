# Déploiement AWS - RAG Events MVP

## Objectif

Ce document décrit le déploiement cloud du projet RAG Events MVP sur AWS.

L’objectif du déploiement était :
- démontrer la capacité à déployer une API IA sur le cloud ;
- conteneuriser l’application avec Docker ;
- gérer les contraintes de coûts AWS ;
- préparer une architecture scalable ;
- sécuriser un minimum l’infrastructure.

## Choix du cloud provider

Le cloud provider choisi est AWS.

AWS a été choisi car :
- c’est le leader du marché cloud ;
- il est largement utilisé dans les projets data ;
- il propose une forte intégration avec les architectures IA et data ;
- il permet de préparer une architecture scalable ;
- il possède de nombreux services compatibles avec les architectures RAG.

## Contraintes du projet

Le projet devait respecter plusieurs contraintes :

- coût très faible ;
- environnement pédagogique ;
- MVP et non architecture production complète ;
- déploiement simple ;
- infrastructure reproductible ;
- démonstration cloud fonctionnelle.

## Architecture AWS utilisée

Le déploiement cloud utilise :

- une instance EC2 Linux ;
- Docker ;
- une API FastAPI ;
- un Security Group AWS ;
- un accès SSH sécurisé ;
- une stratégie IAM dédiée ;
- des alertes Budgets AWS.

## Architecture simplifiée

Utilisateur
   |
   v
Internet
   |
   v
EC2 AWS
   |
   +-- Docker
          |
          +-- API FastAPI
                 |
                 +-- RAG Service
                 +-- Recherche sémantique
                 +-- Mémoire conversationnelle

## Compte AWS

Un compte AWS dédié au portfolio Data Engineer a été créé.

Objectifs :
- isoler les projets ;
- contrôler les coûts ;
- centraliser les projets cloud ;
- construire un environnement professionnel.

## IAM et sécurité

### Compte root

Le compte root AWS n’est utilisé que pour :
- la configuration initiale ;
- les opérations critiques.

### Utilisateur IAM

Un utilisateur IAM administrateur dédié a été créé.

Objectif :
- éviter l’utilisation quotidienne du compte root ;
- appliquer les bonnes pratiques AWS.

### MFA

Le MFA a été activé afin de :
- réduire les risques de compromission ;
- sécuriser l’accès au compte cloud.

## Gestion des coûts

### Budgets AWS

Des alertes Budgets AWS ont été configurées.

Objectifs :
- surveiller les dépenses ;
- détecter rapidement les coûts ;
- éviter toute facturation imprévue.

### Stratégie zéro coût

Le projet applique une stratégie de coût minimal :
- arrêt des instances après démonstration ;
- pas de services managés coûteux ;
- pas de GPU ;
- pas de base de données managée ;
- pas de cluster Kubernetes ;
- pas de NAT Gateway ;
- pas de Load Balancer.

## Pourquoi EC2 et non ECS

Plusieurs architectures cloud ont été étudiées :

- ECS Fargate ;
- Kubernetes ;
- App Runner ;
- EC2.

Le choix final a été EC2 pour :
- limiter les coûts ;
- garder une architecture simple ;
- réduire la complexité ;
- rester compatible avec le niveau MVP ;
- faciliter la démonstration.

## Pourquoi une version cloud-light

La version locale complète utilise :
- Torch ;
- Sentence Transformers ;
- FAISS.

Ces dépendances deviennent rapidement lourdes pour une petite instance EC2.

Lors des premiers tests, le build Docker a échoué à cause :
- du stockage limité ;
- des dépendances ML lourdes ;
- des contraintes Free Tier.

Une branche cloud-light a donc été créée.

Cette version :
- réduit les dépendances ;
- simplifie les embeddings ;
- réduit la taille Docker ;
- facilite le déploiement AWS.

## Docker

Le projet est déployé avec Docker.

Avantages :
- reproductibilité ;
- isolation ;
- déploiement simplifié ;
- cohérence local/cloud.

## Réseau AWS

Le Security Group AWS limite les accès réseau.

Seuls les ports nécessaires sont ouverts :
- SSH ;
- port 8000 pour la démonstration.

Les règles réseau sont limitées à l’IP utilisateur.

## Déploiement de l’API

L’API FastAPI est exposée via :

```text
http://IP_EC2:8000/docs

Swagger permet :

tester les endpoints ;
démontrer le MVP ;
faciliter la validation technique.
Monitoring

Le projet intègre :

des logs applicatifs ;
un middleware de monitoring ;
des traces API ;
un endpoint healthcheck.
Scalabilité future

L’architecture actuelle reste un MVP.

Les évolutions possibles sont :

ECS Fargate ;
Load Balancer ;
CloudWatch ;
S3 ;
base vectorielle managée ;
CI/CD ;
Redis ;
HTTPS ;
domaine personnalisé.
Limites actuelles

Le projet reste volontairement simple :

une seule instance EC2 ;
pas de haute disponibilité ;
pas d’auto scaling ;
pas de monitoring avancé ;
pas de base vectorielle distribuée.

Ces choix ont été faits afin de :

maîtriser les coûts ;
rester cohérent avec le MVP ;
privilégier la simplicité et la démonstration.
Conclusion

Le déploiement AWS démontre :

la capacité à conteneuriser une application IA ;
la capacité à déployer un backend cloud ;
la gestion des contraintes budgétaires ;
l’adaptation de l’architecture aux ressources disponibles ;
la mise en place de bonnes pratiques AWS de base.

Le projet montre une approche réaliste d’un MVP Data/IA déployé sur le cloud avec une stratégie de coût maîtrisée.