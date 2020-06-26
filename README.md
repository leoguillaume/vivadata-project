# vivadata_project
Projet final pour le batch10 du bootcamp VIVADATA.

## VIVADATA PROJECT

Ce repo retrace mon projet final dans le cadre du batch 10 du bootcamp Data science de VIVADATA. Ce projet exploite la base de données CAPP fournie par la Direction de l'Information Légale et Administratives (DILA) placée sous l'autorité du Premier ministre et rattachée au secrétaire général du gouvernement.

### La base de données

La base de données est disponible sur [ici](https://www.data.gouv.fr/fr/datasets/capp/#_). Il s'agit d'un fonds documentaire de jurisprudence des cours d’appel et des juridictions de premier degré est composé d’une sélection de décisions en matière civile et pénale.

Les données sont téléchargeables [ici](https://echanges.dila.gouv.fr/OPENDATA/CAPP/). La base de donnée est mise à jour plusieurs fois par mois.

### Le projet

Le projet de classer les décisions de justice à l'aide des labels indiqués sous certaines décisions.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/schema_projet.png)

-------
### Récuparation des données

#### `CAPP_retrivial.py`

La base de donnée est composée de fichiers gunzip contenant chacun une arborescence de dossiers où se trouve des les décisions de justice sous format XML. Ce script permet de python CAPP comprend deux fonctions permettant à partir des fichiers gunzip téléchargés de récupérer l'ensemble des fichiers XML distincts et de les stockers dans un dossier unique facilitant leur utilisation.

`CAPP_retrievial(path_in: str, path_out: str)`<br>
Permet de récupérer les décisions des fichiers gunzip périodiques. Alexis Eidelman fournis sur son Gitub un script python pour télécharger de manière automatique tous ces fichiers et les décompresser ([TarDilaData](https://github.com/AlexisEidelman/TarDilaData)).

`CAPP_freemium_retrievial(path_in: str, path_out: str)`<br>
Permet de récupérer les décisions du fichier Freemium_capp_global_20180315-170000.tar.gz. Ce fichier est bien plus lourd puisqu'il contient les décisions postérieures à mars 2018. Il doit être télécharger et décompresser à la main.

#### `xml_to_sql.py`

Ce script contient une fonction `data(path_in: str, path_out: str)` permettant de scrapper les données suivantes des décisions :
* l'identifiant de la décision `ID`
* le numéro `NUMERO_AFFAIRE`
* la date `DATE_DEC`
* la nature de la décision `NATURE`
* la juridiction `SIEGE_APPEL`
* les labels `SCT`
* la décision `CONTENU`

Ces données sont stockées dans une table 'Data' d'une base de donnée SQL qu'il faut définir.

------------
### I- Nettoyage des données

*Notebook: [CLEANING](https://github.com/leoguillaume/vivadata_project/blob/master/jupyter_notebooks/CLEANING.ipynb)*

Les données ont été téléchargées le 04/05/2020, la base de donnée à ce jour contient 67210 décisions. Le nettoyage des données à consisté à trouver et formater les valeurs nulles ainsi que les dates, ainsi que de supprimer les décisions en double. Afin de faciliter le traitement de la base de donnée, les modifications de celles-ci sont stockées dans un DataFrame Pandas contenu dans un fichier pickle.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/null_values.png)

On remarque que seulement 26,44 % ont un label.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/df_null_values.png)

### II- Analyse exploratoire des données
*Notebook: [EDA](https://github.com/leoguillaume/vivadata_project/blob/master/jupyter_notebooks/EDA.ipynb)*

Les décisions ne sont pas réparties de manière homogènes dans le temps, une majorité ont été rendu entre 2006 et de 2008.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/time_distribution.png)

La répartition spatiale des décisions semble être liée logiquement à la taille de la population du ressort.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/spatial_distribution.png)

Si la base contient des décisions des premières instants, elle reste largement composée de décisions d'appel.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/nature_of_decisions.png)

### III- Pré-traitement
*Notebook: [PREPROCESSING](https://github.com/leoguillaume/vivadata_project/blob/master/notebooks/PREPROCESSING.ipynb)*

## Labels

Une première analyse des labels permet d'avoir un premier aperçu des principales thématiques juridiques dans la base de données.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/wordcloud_label_1.png)

Les labels sont composés comme suit:
`'CONTRAT DE TRAVAIL, EXECUTION - Salaire - Paiement - Redressement et liquidation judiciaires\n\n'``
Par soucis de simplification je conserve uniquement le premier label. On se retrouve avec 514 labels. Il s'avère nécessaire de réduire ce nombre, pour cela je conserve uniquement les labels présents dans plus de 2 décisions et je regroupe certains labels. J'obtiens alors 253 labels uniques.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/distribution_labels.png)

## Textes

L'étape de pré-traitement consiste à appliquer la fonction `preprocessing(text)` sur les textes qui applique les opérations suivantes :

1. Retire la ponctuation
2. Tokenise les mots
3. Retire les espaces inutiles
4. Retire les tokens dont la longueur est inférieure à 2 caractères
5. Retire les accents
6. Passe en minuscule
7. Retire les mots qui font partie des mots les plus fréquents (présents dans plus de 50% des décisions) et les moins fréquents du corpus (présents dans une seule décision)
8. Retire les stop words
9. Retire les nombres sauf si le token précédent est 'article'

### IV- Préparation des données
*Notebook: [DATA_PREPARATION](https://github.com/leoguillaume/vivadata_project/blob/master/jupyter_notebooks/DATA_PREPARATION.ipynb)*

La préparation des données a consisté à encoder les tokens et les labels et ajouter un token `[<START>]` au début des textes.

### V- Graph de similarité et génération des données d'entrainement
*Notebook: [DOC2VEC](https://github.com/leoguillaume/vivadata_project/blob/master/jupyter_notebooks/DOC2VEC.ipynb)*

Le graph de similarity ou graph synthétique est construit à partir des embeddings résultants d'un model Doc2Vec entrainé sur l'ensemble de la base pendant 10 époques.
A l'issue de cet entrainement j'ai pu analyser la similarité entre des décisions du même label.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/distribution_cosine_similarity.png)

J'ai opté pour un graph tenant compte de similarité de plus 0.6.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/synthetized_graph.png)

A partir de ce graph et des textes sont générés les données d'entrainement. Je tiens compte uniquement des 2 plus proches voisins.

![alt text](https://github.com/leoguillaume/vivadata_project/blob/master/data_visualisations/feat-prop-clean.png)
