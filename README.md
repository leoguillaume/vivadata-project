# vivadata_project
Projet final pour le batch10 du bootcamp VIVADATA. 

## VIVADATA PROJECT

Ce repo retrace mon projet final dans le cadre du batch 10 du bootcamp Data science de VIVADATA. Ce projet exploite la base de données CAPP fournie par la Direction de l'Information Légale et Administratives (DILA) placée sous l'autorité du Premier ministre et rattachée au secrétaire général du gouvernement.

### La base de données

La base de données est disponible sur [ici](https://www.data.gouv.fr/fr/datasets/capp/#_). Il s'agit d'un fonds documentaire de jurisprudence des cours d’appel et des juridictions de premier degré est composé d’une sélection de décisions en matière civile et pénale.

Les données sont téléchargeables [ici](https://echanges.dila.gouv.fr/OPENDATA/CAPP/). La base de donnée est mise à jour plusieurs fois par mois.

### Le projet

Le projet est de mettre en place une application permettant pour une requête données de fournir les décisions les plus pertinentes.
-------
### Récuparation des données

#### `CAPP_retrivial.py`

La base de donnée est composée de fichiers gunzip contenant chacun une arboresence de dossiers où se trouve des les décisions de justice sous format XML. Ce script permet de python CAPP comprend deux fonctions permettant à partir des fichiers gunzip téléchargés de récupérer l'ensemble des fichiers XML distincts et de les stockers dans un dossier unique facilitant leur utilisation. 

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
### Nettoyage des données

Les données ont été téléchargées le 04/05/2020, la base de donnée à ce jour contient 67210 décisions. Le nettoyage des données
se trouve dans le notebook pre_cleaning et consiste à remplacer les valeurs 'null' en NaN, transformer les dates en format datetime. Afin de faciliter le traitement de la base de donnée, les modifications de celles-ci sont stockers dans un DataFrame Pandas contenu dans un fichier pickle.
------------
### Partie 1: EDA
Notebook : [part_1_EDA.ipynb]()

