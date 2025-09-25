# remove_password_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import pikepdf
from pathlib import Path


def escolher_pdf():
    caminho = filedialog.askopenfilename(
        title="Selecione o PDF protegido",
        filetypes=[("Arquivos PDF", "*.pdf")],
    )
    if caminho:
        entrada_var.set(caminho)


def escolher_saida():
    caminho = filedialog.asksaveasfilename(
        title="Salvar PDF sem senha como...",
        defaultextension=".pdf",
        filetypes=[("Arquivos PDF", "*.pdf")],
    )
    if caminho:
        saida_var.set(caminho)


def remover_senha():
    entrada = Path(entrada_var.get().strip())
    saida = Path(saida_var.get().strip())
    senha = senha_var.get().strip()

    if not entrada.exists():
        messagebox.showerror("Erro", f"Arquivo não encontrado:\n{entrada}")
        return

    if not senha:
        messagebox.showwarning("Aviso", "Digite a senha do PDF.")
        return

    try:
        with pikepdf.open(entrada, password=senha) as pdf:
            pdf.save(saida)
        messagebox.showinfo("Sucesso", f"PDF salvo sem senha em:\n{saida}")
    except pikepdf._qpdf.PasswordError:
        messagebox.showerror("Erro", "Senha incorreta.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))


# --- GUI ---
root = tk.Tk()
root.title("Remover Senha de PDF")
root.geometry("500x200")

entrada_var = tk.StringVar()
saida_var = tk.StringVar()
senha_var = tk.StringVar()

# Linha 1 - PDF de entrada
tk.Label(root, text="PDF protegido:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
tk.Entry(root, textvariable=entrada_var, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Procurar", command=escolher_pdf).grid(row=0, column=2, padx=5, pady=5)

# Linha 2 - PDF de saída
tk.Label(root, text="PDF de saída:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
tk.Entry(root, textvariable=saida_var, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Salvar como", command=escolher_saida).grid(row=1, column=2, padx=5, pady=5)

# Linha 3 - Senha
tk.Label(root, text="Senha:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
tk.Entry(root, textvariable=senha_var, show="*", width=20).grid(row=2, column=1, sticky="w", padx=5, pady=5)

# Linha 4 - Botão principal
tk.Button(root, text="Remover Senha", command=remover_senha, bg="#4CAF50", fg="white").grid(
    row=3, column=1, pady=15
)

root.mainloop()
