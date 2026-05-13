# Macro backlog - RAG Events MVP

## Objectif

Ce document présente le macro backlog du MVP RAG Events.

Le backlog permet :
- de prioriser les fonctionnalités ;
- d’organiser le développement ;
- d’identifier les fonctionnalités critiques ;
- de préparer les futurs sprints.

## Méthodologie

Les fonctionnalités sont classées selon :
- Must-Have ;
- Nice-to-Have.

Le backlog tient compte :
- des contraintes MVP ;
- des contraintes cloud ;
- des contraintes budgétaires ;
- du temps de développement.

## Backlog MVP

| Fonctionnalité | Priorité | Complexité | Estimation |
|---|---|---|---|
| API FastAPI | Must-Have | Moyenne | 1 jour |
| Endpoint healthcheck | Must-Have | Faible | 0.5 jour |
| Ingestion JSON | Must-Have | Faible | 1 jour |
| Génération embeddings | Must-Have | Moyenne | 1 jour |
| Recherche sémantique | Must-Have | Moyenne | 1 jour |
| Pipeline RAG | Must-Have | Élevée | 2 jours |
| Intégration Mistral | Must-Have | Moyenne | 1 jour |
| Prompt engineering | Must-Have | Moyenne | 1 jour |
| Mémoire conversationnelle | Must-Have | Moyenne | 1 jour |
| Logs applicatifs | Must-Have | Faible | 0.5 jour |
| Middleware monitoring | Must-Have | Faible | 0.5 jour |
| Dockerisation | Must-Have | Moyenne | 1 jour |
| Déploiement AWS | Must-Have | Moyenne | 1 jour |
| Version cloud-light | Must-Have | Moyenne | 1 jour |
| Documentation technique | Must-Have | Moyenne | 2 jours |

## Fonctionnalités Nice-to-Have

| Fonctionnalité | Priorité | Complexité | Estimation |
|---|---|---|---|
| Authentification JWT | Nice-to-Have | Moyenne | 2 jours |
| Interface frontend | Nice-to-Have | Élevée | 4 jours |
| Dashboard monitoring | Nice-to-Have | Moyenne | 2 jours |
| Redis mémoire persistante | Nice-to-Have | Moyenne | 2 jours |
| Base vectorielle cloud | Nice-to-Have | Élevée | 3 jours |
| CI/CD GitHub Actions | Nice-to-Have | Moyenne | 2 jours |
| HTTPS + domaine | Nice-to-Have | Moyenne | 1 jour |
| Monitoring CloudWatch | Nice-to-Have | Moyenne | 2 jours |
| Kubernetes | Nice-to-Have | Élevée | 5 jours |
| Autoscaling | Nice-to-Have | Élevée | 3 jours |

## Priorisation

Les fonctionnalités Must-Have ont été choisies afin de :
- démontrer le fonctionnement complet du MVP ;
- valider la logique RAG ;
- permettre le déploiement cloud ;
- produire une démonstration cohérente.

Les fonctionnalités Nice-to-Have correspondent :
- aux améliorations futures ;
- à la montée en charge ;
- à une architecture plus proche de la production.

## Risques identifiés

| Risque | Impact | Mitigation |
|---|---|---|
| Dépendances ML lourdes | Élevé | Version cloud-light |
| Coûts AWS | Moyen | Budget + arrêt EC2 |
| Hallucinations LLM | Moyen | Prompt contrôlé |
| Limites EC2 micro | Élevé | Architecture simplifiée |
| Temps de développement | Moyen | Priorisation MVP |
| Absence de CI/CD | Faible | Documentation manuelle |

## Stratégie MVP

Le MVP privilégie :
- la démonstration fonctionnelle ;
- la simplicité ;
- la maîtrise des coûts ;
- la rapidité de développement ;
- la cohérence technique.

## Conclusion

Le backlog montre une approche progressive du développement.

La priorité a été donnée :
- aux fonctionnalités critiques ;
- à la démonstration cloud ;
- à la stabilité ;
- à la capacité de présentation devant un client ou un jury.