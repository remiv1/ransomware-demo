"""
Module de l'interface graphique pour la démonstration de chiffrement.
"""
import threading
import time
import os
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    # Prefer package-relative import when run as a module
    from . import demo_chiffr
except ImportError:
    # Fallback when executed as a script (python chiffrement/gui.py)
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    import demo_chiffr


class DemoGUI(tk.Tk):
    """
    classe graphique de démonstration
    """

    def __init__(self) -> None:
        super().__init__()
        self.title('Demo Chiffrement')
        self.geometry('500x400')

        self.folder_var = tk.StringVar()

        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, fill='x')

        tk.Label(frame, text='Dossier cible:').pack(anchor='w')
        entry = tk.Entry(frame, textvariable=self.folder_var)
        entry.pack(fill='x')

        # Clé pour déchiffrement
        tk.Label(
            frame,
            text='Clé de chiffrement (coller ici pour déchiffrer):'
            ).pack(anchor='w', pady=(6, 0))
        self.key_var = tk.StringVar()
        key_entry = tk.Entry(frame, textvariable=self.key_var)
        key_entry.pack(fill='x')

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill='x', pady=(6, 0))
        tk.Button(
            btn_frame,
            text='Parcourir',
            command=self.browse
            ).pack(side='left')
        tk.Button(
            btn_frame,
            text='Générer demo',
            command=self.generate
        ).pack(
            side='left',
            padx=6
        )
        tk.Button(
            btn_frame,
            text='Coller la clé',
            command=self.paste_key
        ).pack(
            side='left',
            padx=6
        )
        self.decrypt_btn = tk.Button(
            btn_frame,
            text='Déchiffrer',
            command=self.decrypt
        )
        self.decrypt_btn.pack(side='right')
        self.start_btn = tk.Button(btn_frame, text='Démarrer', command=self.start)
        self.start_btn.pack(side='right', padx=6)

        self.timer_label = tk.Label(self, text='Temps: 0.00 s', font=('Consolas', 12))
        self.timer_label.pack(pady=(6, 0))

        self.listbox: tk.Listbox = tk.Listbox(self, font=('Consolas', 11))
        self.listbox.pack(fill='both', expand=True, padx=10, pady=8)

        self._start_time = None
        self._running = False
        self._update_after_id = None

    def browse(self) -> None:
        """Méthode pour parcourir et sélectionner un dossier cible."""
        path = filedialog.askdirectory()
        if path:
            self.folder_var.set(path)
            self.refresh_file_list()

    def generate(self) -> None:
        """Méthode pour générer des fichiers de démonstration."""
        folder = self.folder_var.get()
        if not folder:
            messagebox.showwarning('Avertissement', 'Choisissez d abord un dossier.')
            return
        demo_chiffr.generate_demo_files(folder, invoices=5, bank_tx=10, expenses=3, payroll=2)
        self.refresh_file_list()

    def refresh_file_list(self) -> None:
        """Méthode pour actualiser la liste des fichiers dans le dossier cible."""
        folder = self.folder_var.get()
        self.listbox.delete(0, tk.END)
        if not folder or not os.path.exists(folder):
            return
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        for f in files:
            self.listbox.insert(tk.END, f' [ ] {f}')

    def start(self) -> None:
        """Méthode pour démarrer le processus de chiffrement."""
        folder = self.folder_var.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror('Erreur', 'Dossier invalide.')
            return
        # disable controls
        self.start_btn.config(state='disabled')
        self._start_time = time.perf_counter()
        self._running = True
        self._update_timer()

        # prepare files in listbox
        _: list[str] = [
            self.listbox.get(i).strip()[4:] for i in range(self.listbox.size())    # type: ignore
            ]

        def on_file(fn: str) -> None:
            # called from worker thread; schedule UI update (mark as encrypted)
            self.after(0, self.mark_file, fn, 'X')

        def worker() -> None:
            try:
                key = demo_chiffr.encrypt_folder(
                    folder, on_file_encrypted=on_file, create_backup=True
                )
                self.after(0, self.finish, key) # type: ignore
            except FileExistsError as e:
                self.after(0, messagebox.showerror, 'Erreur',
                           f"Le dossier de sauvegarde existe: {e}")
                self.after(0, self.reset_ui)
            except (OSError, IOError, ValueError) as e:
                self.after(0, messagebox.showerror, 'Erreur', str(e))
                self.after(0, self.reset_ui)

        threading.Thread(target=worker, daemon=True).start()

    def _update_timer(self) -> None:
        if not self._running:
            return
        elapsed = time.perf_counter() - self._start_time    # type: ignore
        self.timer_label.config(text=f'Temps: {elapsed:.2f} s')
        self._update_after_id = self.after(100, self._update_timer)

    def mark_file(self, filename: str, mark: str = 'X') -> None:
        """Find filename in listbox and mark it with given mark."""
        for i in range(self.listbox.size()):
            text = self.listbox.get(i)  # type: ignore
            if text.endswith(filename): # type: ignore
                self.listbox.delete(i)
                self.listbox.insert(i, f' [{mark}] {filename}')
                return

    def paste_key(self) -> None:
        """Ajouter la clé du presse-papier dans le champ de saisie."""
        try:
            val = self.clipboard_get()
            if val:
                self.key_var.set(val)
        except tk.TclError:
            messagebox.showwarning('Clipboard', 'Impossible de lire le presse-papier.')

    def decrypt(self) -> None:
        """Méthode pour démarrer le processus de déchiffrement."""
        folder = self.folder_var.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror('Erreur', 'Dossier invalide.')
            return
        key_text = self.key_var.get().strip()
        if not key_text:
            # try clipboard
            try:
                key_text = self.clipboard_get().strip()
            except tk.TclError:
                key_text = ''
        if not key_text:
            messagebox.showerror('Erreur', 'Aucune clé fournie.')
            return

        # disable controls
        self.decrypt_btn.config(state='disabled')
        self._start_time = time.perf_counter()
        self._running = True
        self._update_timer()

        def on_file_dec(fn: str) -> None:
            # mark as decrypted with 'D'
            self.after(0, self.mark_file, fn, 'D')

        def worker_dec() -> None:
            try:
                demo_chiffr.decrypt_folder(folder, key_text, on_file_decrypted=on_file_dec)
                self.after(0, messagebox.showinfo, 'Succès', 'Déchiffrement terminé')
            except (OSError, IOError, ValueError) as e:
                self.after(0, messagebox.showerror, 'Erreur', str(e))
            finally:
                self.after(0, self.reset_ui)

        threading.Thread(target=worker_dec, daemon=True).start()

    def finish(self, key: bytes) -> None:
        """
        Terminer le processus de chiffrement, afficher la clé et réinitialiser l'interface.
        """
        self._running = False
        if self._update_after_id:
            self.after_cancel(self._update_after_id)
        self.timer_label.config(text=self.timer_label.cget('text') + ' — Terminé')
        if key:
            try:
                # copier la clé dans le presse-papier
                self.clipboard_clear()
                self.clipboard_append(key.decode())
                messagebox.showinfo('Clé de chiffrement',
                                    f"Clé copiée dans le presse-papier:\n\n{key.decode()}")
            except tk.TclError:
                # fallback si clipboard non disponible
                messagebox.showinfo('Clé de chiffrement', key.decode())
        self.reset_ui()

    def reset_ui(self) -> None:
        """Réinitialiser l'interface après chiffrement/déchiffrement."""
        # réactiver les boutons
        self.start_btn.config(state='normal')
        try:
            self.decrypt_btn.config(state='normal')
        except Exception:
            pass

        # arrêter le chronomètre si en cours
        self._running = False
        if self._update_after_id:
            try:
                self.after_cancel(self._update_after_id)
            except Exception:
                pass
            self._update_after_id = None


def run() -> None:
    """Lancer l'application de démonstration."""
    app = DemoGUI()
    app.mainloop()


if __name__ == '__main__':
    run()
