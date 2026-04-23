"""Module de démonstration de chiffrement"""
import os
import sys
import time
import csv
import random
import datetime
from typing import Optional, Callable
from cryptography.fernet import Fernet, InvalidToken

COMPANIES = [
        'Alpha SARL', 'Beta SA', 'Gamma & Co', 'Delta Services', 'Epsilon Industries',
        'Zeta Consulting', 'Eta Logistics', 'Theta Foods'
    ]
EMPLOYEES = [
        'Alice Dupont', 'Bob Martin', 'Claire Leroy', 'David Moreau', 'Emma Petit',
        'Franck Dubois', 'Gilles Marchal', 'Hélène Laurent'
    ]
CATEGORIES = [
    'Fournitures', 'Repas', 'Transport', 'Hébergement', 'Matériel', 'Services'
    ]


def copy_folder(src: str, dst: str) -> None:
    """Copie un dossier et son contenu"""
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_folder(s, d)
        else:
            with open(s, 'rb') as f_src:
                data = f_src.read()
            with open(d, 'wb') as f_dst:
                f_dst.write(data)


def random_date(start_year: int =2023, end_year: int =2026) -> str:
    """
    Génère une date aléatoire entre le 1er janvier de start_year
    et le 31 décembre de end_year.
    """
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    delta = (end - start).days
    return (start + datetime.timedelta(days=random.randint(0, delta))).isoformat()


def generate_demo_files(
        target_dir: str,
        invoices: int = 400,
        bank_tx: int = 200,
        expenses: int = 100,
        payroll: int = 50
        ) -> None:
    """Génère des fichiers CSV de démonstration ressemblant à des fichiers comptables.

    Crée les fichiers: invoices.csv, bank_statement.csv, expenses.csv, payroll.csv
    dans `target_dir`.
    """
    os.makedirs(target_dir, exist_ok=True)

    # invoices.csv
    invoices_path = os.path.join(target_dir, 'invoices.csv')
    with open(invoices_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['invoice_id', 'date', 'client', 'amount', 'tax', 'total'])
        for i in range(1, invoices + 1):
            amount = round(random.uniform(50.0, 5000.0), 2)
            tax = round(amount * 0.2, 2)
            total = round(amount + tax, 2)
            writer.writerow([
                f'INV{1000+i}',
                random_date(),
                random.choice(COMPANIES),
                f'{amount:.2f}',
                f'{tax:.2f}',
                f'{total:.2f}'
                ])

    # bank_statement.csv
    bank_path = os.path.join(target_dir, 'bank_statement.csv')
    balance = 10000.0
    with open(bank_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'description', 'debit', 'credit', 'balance'])
        for i in range(bank_tx):
            amt = round(random.uniform(5.0, 3000.0), 2)
            if random.random() < 0.5:
                # debit
                balance -= amt
                writer.writerow([
                    random_date(),
                    random.choice(['Paiement', 'Retrait', 'Virement', 'Achat']),
                    f'{amt:.2f}',
                    '',
                    f'{balance:.2f}'
                    ])
            else:
                # credit
                balance += amt
                writer.writerow([
                    random_date(),
                    random.choice(['Virement reçu', 'Salaire', 'Remboursement']),
                    '',
                    f'{amt:.2f}',
                    f'{balance:.2f}'
                    ])

    # expenses.csv
    expenses_path = os.path.join(target_dir, 'expenses.csv')
    with open(expenses_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'category', 'employee', 'amount', 'description'])
        for i in range(expenses):
            amt = round(random.uniform(10.0, 800.0), 2)
            writer.writerow([
                random_date(),
                random.choice(CATEGORIES),
                random.choice(EMPLOYEES),
                f'{amt:.2f}',
                random.choice(['Déjeuner client', 'Taxi', 'Papeterie', 'Matériel'])
            ])

    # payroll.csv
    payroll_path = os.path.join(target_dir, 'payroll.csv')
    with open(payroll_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['employee_id', 'name', 'month', 'gross', 'tax', 'net'])
        for i in range(1, payroll + 1):
            gross = round(random.uniform(1500.0, 8000.0), 2)
            tax = round(gross * random.uniform(0.15, 0.30), 2)
            net = round(gross - tax, 2)
            writer.writerow([
                f'EMP{100+i}',
                random.choice(EMPLOYEES),
                f'{random.randint(1,12):02d}/{random.choice([2023,2024,2025,2026])}',
                f'{gross:.2f}',
                f'{tax:.2f}',
                f'{net:.2f}'
            ])

    print(f"Fichiers générés dans '{target_dir}'.")


def demo_ransomware(target_dir: str) -> None:
    """Démonstration de chiffrement d'un ensemble de fichiers"""
    # 1. Génération de la clé de chiffrement
    key = Fernet.generate_key()
    _ = Fernet(key)

    # 1bis. Confirmation de l'utilisateur avant de procéder au chiffrement
    print(f"Vous êtes sur le point de chiffrer tous les fichiers du dossier '{target_dir}'.")
    confirmation = input("Êtes-vous sûr de vouloir continuer ? (oui/non) : ")
    while confirmation.lower() not in ['oui', 'non']:
        confirmation = input("Veuillez répondre par 'oui' ou 'non' : ")
    if confirmation.lower() != 'oui':
        print("Opération annulée par l'utilisateur.")
        print("--- FIN DU SCRIPT ---")
        return

    # Utiliser la fonction de bas niveau pour effectuer le chiffrement
    key = encrypt_folder(target_dir)
    if key is None:
        print("Aucune clé générée (peut-être utilisé un chiffrement fourni).")
    else:
        print(f"--- Clé de chiffrement (gardez-la précieusement) : {key.decode()} ---")
        print("--- Essayez d'ouvrir maintenant les fichiers chiffrés pour voir le résultat ---")


def _create_backup_if_needed(target_dir: str) -> None:
    """Create a backup folder for target_dir."""
    src_abs = os.path.abspath(target_dir)
    normalized = src_abs.rstrip(os.sep)
    backup_dir = normalized + "_backup"
    try:
        if os.path.commonpath([backup_dir, src_abs]) == src_abs:
            parent = os.path.dirname(normalized)
            base = os.path.basename(normalized)
            backup_dir = os.path.join(parent, base + "_backup")
    except ValueError:
        pass
    if os.path.exists(backup_dir):
        print(f"Le dossier de sauvegarde '{backup_dir}' existe déjà. La création est ignorée.")
    else:
        copy_folder(target_dir, backup_dir)


def _encrypt_files(
        target_dir: str,
        files: list[str],
        cipher: Fernet,
        on_file_encrypted: Optional[Callable[[str], None]]
    ) -> None:
    """Encrypt all files in the list using the provided cipher."""
    for filename in files:
        file_path = os.path.join(target_dir, filename)
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = cipher.encrypt(data)
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
        if on_file_encrypted:
            try:
                on_file_encrypted(filename)
            except TypeError:
                pass


def encrypt_folder(
        target_dir: str,
        on_file_encrypted: Optional[Callable[[str], None]] = None,
        create_backup: bool = True,
        cipher: Optional[Fernet] = None) -> None | bytes:
    """
    Encrypt all files in `target_dir` and optionally call
    `on_file_encrypted(filename)` after each file.

    If `cipher` is None, a new Fernet key is generated and returned (bytes).
    If `cipher` is provided, the function returns None.
    """
    # validation
    if not os.path.exists(target_dir):
        raise FileNotFoundError(target_dir)

    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    if not files:
        return None

    # prepare cipher/key
    generated_key = None
    if cipher is None:
        generated_key = Fernet.generate_key()
        cipher = Fernet(generated_key)

    # backup
    if create_backup:
        _create_backup_if_needed(target_dir)

    # encrypt files (synchronous)
    _encrypt_files(target_dir, files, cipher, on_file_encrypted)

    # small sleep to make UI progress readable
    time.sleep(0.02)

    return generated_key


def decrypt_folder(
        target_dir: str,
        key: Optional[bytes | str],
        on_file_decrypted: Optional[Callable[[str], None]] = None
        ) -> None:
    """Decrypt all files in `target_dir` using the provided `key`.

    `key` may be bytes or a str. Calls `on_file_decrypted(filename)` after each file.
    Raises FileNotFoundError if target missing, InvalidToken on decryption errors.
    """
    if not os.path.exists(target_dir):
        raise FileNotFoundError(target_dir)

    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    if not files:
        return

    if isinstance(key, str):
        key_bytes = key.encode()
    else:
        key_bytes = key

    cipher = Fernet(key_bytes)  # type: ignore

    for filename in files:
        file_path = os.path.join(target_dir, filename)
        with open(file_path, 'rb') as f:
            data = f.read()
        try:
            decrypted = cipher.decrypt(data)
        except InvalidToken as e:
            raise InvalidToken('Clé invalide ou fichier corrompu') from e
        with open(file_path, 'wb') as f:
            f.write(decrypted)
        if on_file_decrypted:
            try:
                on_file_decrypted(filename)
            except (TypeError, AttributeError):
                pass
        time.sleep(0.02)



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Démonstration : génération de fichiers demo + chiffrement"
    )
    parser.add_argument('folder', help='dossier cible')
    parser.add_argument(
        '--generate',
        action='store_true',
        help='générer des fichiers de démonstration dans le dossier cible'
    )
    parser.add_argument(
        '--invoices',
        type=int,
        default=20,
        help='nombre de factures à générer'
    )
    parser.add_argument(
        '--transactions',
        type=int,
        default=200,
        help='nombre d opérations bancaires à générer'
    )
    parser.add_argument(
        '--expenses',
        type=int,
        default=50,
        help='nombre de notes de frais à générer'
    )
    parser.add_argument(
        '--payroll',
        type=int,
        default=10,
        help='nombre d entrées de paie à générer'
    )
    parser.add_argument(
        '--factor',
        type=int,
        default=1,
        help='facteur multiplicatif pour augmenter le volume (ex: 100)'
    )
    parser.add_argument(
        '--no-encrypt',
        action='store_true',
        help="ne pas chiffrer après génération"
    )
    args = parser.parse_args()

    # Appliquer le facteur sur les compteurs
    factor = max(1, int(args.factor))
    invoices_count = max(1, int(args.invoices) * factor)
    transactions_count = max(1, int(args.transactions) * factor)
    expenses_count = max(1, int(args.expenses) * factor)
    payroll_count = max(1, int(args.payroll) * factor)

    if args.generate:
        print(f"""
              Génération avec facteur x{factor}:\n
                    invoices={invoices_count},\n
                    transactions={transactions_count}, \n
                    expenses={expenses_count}, \n
                    payroll={payroll_count}
              """)
        generate_demo_files(
            args.folder,
            invoices=invoices_count,
            bank_tx=transactions_count,
            expenses=expenses_count,
            payroll=payroll_count
        )
        if args.no_encrypt:
            sys.exit(0)

    demo_ransomware(args.folder)
