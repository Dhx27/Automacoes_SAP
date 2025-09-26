import time

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
