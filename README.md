# Outil pédagogique sur le ransomware

Cet outil vise à démontrer auprès d'un public décideur qu'un chiffrement/déchiffrement est rapide et silencieux, et que les données sont irrécupérables sans la clé de chiffrement.

## Fonctionnement

L'outil est composé de deux scripts Python : `demo_chiffr.py` et `demo_dechiffr.py`.

### Installation de l'environnement

1. Cloner le dépôt GitHub de l'outil pédagogique sur le ransomware.

    ```bash
    git clone https://github.com/remiv1/ransomware-demo.git
    cd ransomware-demo
    ```

2. Installer les dépendances nécessaires.

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate
    pip install -r requirements.txt
    ```

### Génération d'une donnée

Le script `demo_chiffr.py` permet de générer de la donnée aléatoire à chiffrer.

Factor 20 000 genère 250Mo de données réparties dans 4 fichiers CSV :
    - 4 millions de lignes dans `bank_statement.csv`,
    - 1 million de lignes dans `expenses.csv`,
    - 400 000 lignes dans `invoices.csv`.
    - 200 000 lignes dans `payroll.csv`.

```bash
python ./chiffrement/demo_chiffr.py --generate --factor 20000 --no-encrypt demo_folder
```

### Chiffrement des données

Le même script `demo_chiffr.py` peut être utilisé pour chiffrer les données générées.

```bash
python ./chiffrement/demo_chiffr.py demo_folder
```

```console
Vous êtes sur le point de chiffrer tous les fichiers du dossier 'demo_folder'.
Êtes-vous sûr de vouloir continuer ? (oui/non) : oui
Les fichiers originaux ont été copiés dans 'demo_folder_backup'.
--- DEBUT D'OPERATION DE CHIFFREMENT ---
--- Début de chiffrement de 4 fichiers dans 'demo_folder'... ---
Fichier 'invoices.csv' chiffré.
Fichier 'bank_statement.csv' chiffré.
Fichier 'expenses.csv' chiffré.
Fichier 'payroll.csv' chiffré.
--- OPERATION DE CHIFFREMENT TERMINÉE ---
--- Chiffrement terminé en 1.55 secondes ---
--- Clé de chiffrement (gardez-la précieusement) : BnsBCgDz0uBD8M7J_2S18fvFjYyObWdRFv1JpKpEN2Y= ---
--- Essayez d'ouvrir maintenant les fichiers chiffrés pour voir le résultat ---
```

### Déchiffrement des données

```bash
python ./chiffrement/demo_dechiffr.py demo_folder
```

```console
=== DÉMONSTRATION DE DÉCHIFFREMENT ===
Entrez la clé de déchiffrement : BnsBCgDz0uBD8M7J_2S18fvFjYyObWdRFv1JpKpEN2Y=
Entrez le chemin du dossier contenant les fichiers à restaurer : demo_folder
--- Restauration des fichiers avec la clé ---
Restauré : invoices.csv
Restauré : bank_statement.csv
Restauré : expenses.csv
Restauré : payroll.csv

--- SYSTÈME RÉTABLI ---
--- FIN DU SCRIPT ---
```

## Conclusion

Cet outil pédagogique permet de démontrer de manière concrète et visuelle les effets d'un ransomware sur des données sensibles. En montrant la rapidité du chiffrement et l'irréversibilité sans la clé, il sensibilise les décideurs à l'importance de la cybersécurité et de la protection des données.

## Avertissement

Cet outil est destiné à des fins éducatives uniquement. Il ne doit pas être utilisé à des fins malveillantes ou pour causer des dommages. Assurez-vous de l'utiliser dans un environnement contrôlé et de respecter les lois en vigueur concernant la cybersécurité.
