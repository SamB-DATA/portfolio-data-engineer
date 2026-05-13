Projet BottleNeck - Livrable 2 - Workflow Kestra

Contenu :
- workflow/main_tutorial_bottleneck_pipeline.yaml
- outputs/rapport_chiffre_affaires.xlsx
- outputs/vins_premium.csv
- outputs/vins_ordinaires.csv

Fonction du workflow :
- ingestion des données ERP, liaison et web
- nettoyage des données
- fusion des jeux de données
- calcul du chiffre d’affaires
- classification des vins via z-score
- génération des exports

Tests intégrés :
- volumétrie finale = 714
- chiffre d’affaires global = 70568.6
- vins premium = 30
- vins ordinaires = 684
