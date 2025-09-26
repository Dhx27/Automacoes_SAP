import win32com.client
import time
import sys

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


def fechar_sistema_sap(session=None, root=None):
    try:
        if session:  
            session.findById("wnd[0]").close()
    except:
        pass

    if not root:
        root.destroy()
    sys.exit()
    
