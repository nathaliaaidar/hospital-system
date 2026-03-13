import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage
from datetime import timedelta
import os

# --- CONFIGURAÇÕES E CREDENCIAIS ---
ARQUIVO_PLANILHA = '/home/nathalia/nathaliaproject/RTCON/PlanilhaFormulario/FormularioRTCONmensal2025_IBCCOncologia.xlsx'
NOME_DA_ABA = 'Gerais'

EMAIL_REMETENTE = "naorespondartcon@gmail.com"
SENHA_REMETENTE = "pmve ugnp jefg kwgh"

EMAILS_DESTINATARIOS = ['arthur@gruportcon.com', 'andre@gruportcon.com']
EMAILS_COPIA = ['lucas@gruportcon.com', 'herminiane@gruportcon.com']

# Função auxiliar para envio real (precisa ser definida caso vá descomentar o código abaixo)
def enviar_email_real(item, vencimento):
    # Implemente a lógica de SMTP aqui se necessário
    pass

def processar_dados(disparar=False):
    """
    Lê a planilha, verifica prazos e retorna um DataFrame com o status.
    Se disparar=True, tenta enviar e-mails.
    """
    try:
        if not os.path.exists(ARQUIVO_PLANILHA):
            return f"Erro: Arquivo não encontrado no caminho: {ARQUIVO_PLANILHA}"

        df = pd.read_excel(ARQUIVO_PLANILHA, sheet_name=NOME_DA_ABA, header=2)
        
        # Tratamento básico de dados
        df = df.dropna(subset=['Item', 'Vencimento'])
        df['Vencimento'] = pd.to_datetime(df['Vencimento'], errors='coerce')
        
        hoje = pd.Timestamp.now().normalize()
        resultados = []

        for i, linha in df.iterrows():
            item = linha['Item']
            venc = linha['Vencimento']
            
            if pd.isna(venc): 
                continue

            # Regra de negócio: 120 dias para o primeiro item, 30 para os demais
            dias = 120 if i == 0 else 30
            limite = hoje + timedelta(days=dias)
            
            status = "🟢 No Prazo"
            log = "-"

            # Lógica de verificação de datas
            if hoje <= venc <= limite:
                status = "🔴 ALERTA"
                if disparar:
                    # Simulação de segurança
                    if "sua_senha" in SENHA_REMETENTE:
                        log = "❌ Configure a Senha no Código"
                    else:
                        # Aqui chamaria a função de envio real
                        # enviar_email_real(item, venc) 
                        log = "✅ E-mail Enviado (Simulado)"
                else:
                    log = "⚠️ Pendente"
            elif venc < hoje:
                status = "⚫ Vencido"

            resultados.append({
                "Status": status,
                "Item": item,
                "Vencimento": venc.strftime('%d/%m/%Y'),
                "Log": log
            })
            
        return pd.DataFrame(resultados)
    
    except Exception as e:
        # Retorna a mensagem de erro como string para ser tratada no frontend
        return str(e)