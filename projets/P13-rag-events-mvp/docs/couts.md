# Estimation des coûts - RAG Events MVP

## Objectif

Ce document présente une estimation des coûts de développement et d’exploitation du MVP RAG Events.

L’objectif est :
- d’anticiper les dépenses cloud ;
- de justifier les choix techniques ;
- de démontrer une approche réaliste de gestion budgétaire ;
- de préparer une montée en charge future.

## Approche utilisée

Le projet étant un MVP pédagogique, l’approche retenue privilégie :
- la simplicité ;
- la maîtrise des coûts ;
- l’utilisation minimale des ressources cloud ;
- une architecture facilement démontrable.

Le projet distingue :
- les coûts de build ;
- les coûts d’exploitation (OPEX).

## Coûts de build

Les coûts de build correspondent :
- au temps de développement ;
- à la mise en place de l’infrastructure ;
- aux tests ;
- au déploiement initial.

## Estimation du développement

| Poste | Estimation |
|---|---|
| Analyse du besoin | 1 jour |
| Architecture technique | 1 jour |
| Développement API FastAPI | 2 jours |
| Développement RAG | 2 jours |
| Recherche vectorielle | 1 jour |
| Mémoire conversationnelle | 1 jour |
| Dockerisation | 1 jour |
| Déploiement AWS | 1 jour |
| Monitoring & logs | 1 jour |
| Documentation | 2 jours |

Estimation totale :
- environ 13 jours de travail.

## Infrastructure build

| Ressource | Coût estimé |
|---|---|
| AWS EC2 micro | faible |
| Docker | gratuit |
| GitHub | gratuit |
| VS Code | gratuit |
| FastAPI | open source |
| Python | open source |

## Stratégie de réduction des coûts

Plusieurs choix ont été réalisés afin de limiter les coûts :

- utilisation d’une seule instance EC2 ;
- absence de GPU ;
- absence de Kubernetes ;
- absence de services managés coûteux ;
- arrêt manuel des instances ;
- version cloud-light allégée ;
- pas de base de données payante ;
- architecture MVP simple.

## Coûts OPEX

Les coûts OPEX correspondent :
- à l’hébergement ;
- à l’exécution des services ;
- au stockage ;
- aux appels API ;
- à la maintenance.

## Estimation MVP faible trafic

Hypothèse :
- démonstration portfolio ;
- faible nombre d’utilisateurs ;
- trafic très faible.

| Ressource | Estimation mensuelle |
|---|---|
| EC2 t2.micro | faible |
| Stockage EBS | faible |
| Transfert réseau | faible |
| Appels API Mistral | faible à modéré |
| Logs | faible |

## Pourquoi limiter les coûts cloud

Le projet est un MVP pédagogique.

L’objectif principal n’est pas :
- la haute disponibilité ;
- le scaling massif ;
- la production entreprise.

L’objectif est :
- démontrer les compétences ;
- présenter une architecture crédible ;
- rester cohérent avec les contraintes financières.

## Problème rencontré

Lors du premier déploiement AWS :
- le build Docker a échoué ;
- manque de stockage ;
- dépendances ML trop lourdes.

Cause :
- Torch ;
- Sentence Transformers ;
- FAISS.

## Solution retenue

Une version cloud-light a été créée.

Cette version :
- réduit les dépendances ;
- réduit la taille Docker ;
- réduit la consommation mémoire ;
- facilite le déploiement EC2 micro.

## Arbitrage technique

Le projet illustre un arbitrage classique :
- performance ;
- simplicité ;
- coût ;
- ressources disponibles.

La version locale complète reste plus performante.

La version cloud-light privilégie :
- le coût ;
- la stabilité ;
- la démonstration cloud.

## Estimation future - montée en charge

En cas de montée en charge, plusieurs coûts augmenteraient :

| Composant | Évolution possible |
|---|---|
| EC2 | instance plus puissante |
| Base vectorielle | Pinecone ou OpenSearch |
| Monitoring | CloudWatch |
| Load balancing | ALB |
| Stockage | S3 |
| Mémoire conversationnelle | Redis |
| CI/CD | GitHub Actions |
| HTTPS | Route53 + ACM |

## Optimisations futures

Plusieurs optimisations sont possibles :

- mutualisation des ressources ;
- mise en veille automatique ;
- cache ;
- quantization modèles ;
- API batching ;
- vector DB optimisée ;
- ECS Fargate ;
- autoscaling.

## Conclusion

Le MVP a été conçu avec une logique de coût maîtrisé.

Les choix techniques réalisés permettent :
- une démonstration crédible ;
- un déploiement cloud réel ;
- une consommation cloud minimale ;
- une adaptation aux contraintes Free Tier AWS.

Le projet démontre également une capacité à adapter l’architecture en fonction :
- des contraintes budgétaires ;
- des limites techniques ;
- des besoins métier ;
- du niveau de maturité du produit.