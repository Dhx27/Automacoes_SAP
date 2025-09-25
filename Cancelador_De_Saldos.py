import sys
import tkinter as tk
from tkinter import ttk
import win32com.client
import time
from tkinter import ttk, messagebox

session = None

def fechar_sistema(session=None):
    try:
        if session:  
            session.findById("wnd[0]").close()
    except:
        pass

    root.destroy()
    sys.exit()
    
    
#Função definida para obter a janela logada, iniciar uma nova e dar a trativa prevista nela
def sap_logon():
    
    # Conectar ao SAP GUI via COM
    sap_gui = win32com.client.GetObject("SAPGUI")
    app = sap_gui.GetScriptingEngine
    connection = app.Children(0)
    session = connection.Children(0)

    session.createSession()
    
    time.sleep(10)

    # pegar a última sessão (a nova aba criada)
    new_session = connection.Children(connection.Children.Count - 1)

    return new_session


#Função definida para aguardar elementos 
def aguardar_elemento(session, element_id, timeout=10, poll=0.2):
    
    t0 = time.time()
    
    while time.time() - t0 < timeout:
        try:
            
            obj = session.findById(element_id)
            return obj
        except:
            
            time.sleep(poll)
    
    raise TimeoutError(f"Fornecimento  não encontrado (ou já excluído")



def cancelar_fornecimentos():
    
    global session
    
    conteudo = texto.get("1.0", tk.END).strip()
    
    lista_fornecimentos = conteudo.split("\n")
    
    lista_fornecimentos = list(dict.fromkeys(x.strip() for x in lista_fornecimentos if x.strip()))
    
    if not lista_fornecimentos:
        messagebox.showwarning("Aviso", "Nenhum fornecimento informado.")
        return
    
    if session is None: 
        
        session = sap_logon()
        session.findById("wnd[0]").maximize()

        # Ir para a transação VL02N
        session.findById("wnd[0]/tbar[0]/okcd").text = "vl02n"
        session.findById("wnd[0]").sendVKey(0)
    
    for fornecimento in lista_fornecimentos:
        
        try: 
            session.findById("wnd[0]/usr/ctxtLIKP-VBELN").text = f"{fornecimento}"
            session.findById("wnd[0]").sendVKey(0)
            
            time.sleep(0.2)
            
            try:
                
                aguardar_elemento(session, "wnd[0]/tbar[1]/btn[14]", timeout=15)
                time.sleep(1)
                session.findById("wnd[0]").sendVKey(14)
                
                popup_btn = aguardar_elemento(session, "wnd[1]/usr/btnSPOP-OPTION1", timeout=10)
                popup_btn.press()

            except TimeoutError as e:
                print(e)
                
        except Exception as e:
            print(f"Erro no fornecimento {fornecimento}: {e}")
    
    
   
    resposta = messagebox.askyesno("Concluído", "Deseja limpar mais fornecimentos?")
    
    if resposta:
        texto.delete("1.0", tk.END)  # limpa textbox
    else: 
        fechar_sistema(session)
             

    
# Paleta baseada no sistema ArcelorMittal
COR_DEGRADE_INICIO = "#E63B7A"   # rosa avermelhado
COR_DEGRADE_FIM = "#FF6600"      # laranja
COR_FUNDO = "#E7E7E7"            # fundo cinza claro
COR_CARD = "#FFFFFF"             # branco para área de texto
COR_TEXTO = "#4D4D4D"            # cinza escuro
COR_BOTAO = "#FF6600"            # laranja ArcelorMittal
COR_BOTAO_HOVER = "#e65c00"      # tom mais escuro

# Janela principal
root = tk.Tk()
root.title("Cancelador de saldos")
root.geometry("500x400")
root.configure(bg=COR_FUNDO)
root.resizable(False, False)

# Estilo ttk
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Arial", 10, "bold"),
    foreground="white",
    background=COR_BOTAO,
    padding=6
)
style.map(
    "TButton",
    background=[("active", COR_BOTAO_HOVER)]
)

# Cabeçalho
cabecalho = tk.Frame(root, bg=COR_DEGRADE_FIM, height=50)
cabecalho.pack(fill="x")

titulo = tk.Label(
    cabecalho,
    text="Cancelador de Saldos",
    font=("Arial", 14, "bold"),
    bg=COR_DEGRADE_FIM,
    fg="white"
)
titulo.pack(pady=10)

# Frame estilo "card"
frame_card = tk.Frame(root, bg=COR_CARD)
frame_card.pack(pady=15, padx=20, fill="both", expand=True)

# Campo multilinha SEM borda
texto = tk.Text(
    frame_card,
    width=65,
    height=8,
    font=("Consolas", 9),
    bg="white",
    fg=COR_TEXTO,
    insertbackground=COR_TEXTO,
    bd=0,                  # tira borda
    highlightthickness=0   # tira contorno
)
texto.pack(padx=10, pady=10, fill="both", expand=True)


# Botão estilizado
botao = ttk.Button(root, text="🚫 Cancelar Saldo", command=cancelar_fornecimentos)
botao.pack(pady=10)

# Rodapé
rodape = tk.Label(
    root,
    text="Desenvolvido por Diogo Lana",
    font=("Arial", 9),
    bg=COR_FUNDO,
    fg=COR_TEXTO
)
rodape.pack(side="bottom", pady=5)

try:
    root.protocol("WM_DELETE_WINDOW", lambda: fechar_sistema(session))
except NameError:
    
    root.protocol("WM_DELETE_WINDOW", fechar_sistema)
    
    
root.mainloop()
