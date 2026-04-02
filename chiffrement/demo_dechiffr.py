"""Module de démonstration de déchiffrement"""

import os
from cryptography.fernet import Fernet, InvalidToken

def demo_restore(key_input: str, folder: str):
    """Démonstration de déchiffrement d'un ensemble de fichiers
    avec une clé fournie par l'utilisateur.
    Si la clé est correcte, les fichiers sont restaurés.
    Sinon, un message d'erreur est affiché et les fichiers restent chiffrés.
    """
    try:
        cipher = Fernet(key_input)
        target_dir = folder
        files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]

        print("--- Restauration des fichiers avec la clé ---")

        for file_name in files:
            file_path = os.path.join(target_dir, file_name)

            with open(file_path, "rb") as f:
                encrypted_data = f.read()

            # Déchiffrement
            decrypted_data = cipher.decrypt(encrypted_data)

            with open(file_path, "wb") as f:
                f.write(decrypted_data)

            print(f"Restauré : {file_name}")

        print("\n--- SYSTÈME RÉTABLI ---")
    except (InvalidToken, ValueError) as e:
        print(f"Erreur : Clé invalide. Les données restent chiffrées. ({e})")

if __name__ == "__main__":
    print("=== DÉMONSTRATION DE DÉCHIFFREMENT ===")
    key = input("Entrez la clé de déchiffrement : ")
    fold = input("Entrez le chemin du dossier contenant les fichiers à restaurer : ")
    demo_restore(key, fold)
    print("--- FIN DU SCRIPT ---")
