import requests
import pandas as pd
import smtplib
import ssl
import json
import os
import time
from email.message import EmailMessage
from datetime import timedelta

# =========================================================
# CONFIGURATION — loaded from environment and config file
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOME_DA_ABA = "Gerais"

EMAIL_REMETENTE = 
SENHA_REMETENTE = 

# CC list for all alerts — configure as needed
EMAILS_COPIA_GERAL = os.getenv("CC", "").split(",")

# Load hospital list from external config file (not committed to version control)
def load_hospitals():
    config_path = os.path.join(BASE_DIR, "hospitals_config.json")
    if not os.path.exists(config_path):
        print("❌ hospitals_config.json not found.")
        print("   Copy hospitals_config.example.json to hospitals_config.json and fill it in.")
        return []
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

# =========================================================
# EMAIL SENDER
# =========================================================

def enviar_email(nome_hospital, nome_item, dias_restantes, data_venc, destinatarios):
    if not EMAIL_REMETENTE or not SENHA_REMETENTE:
        print("   ⚠️  Email credentials not set. Skipping send.")
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Alert RTCON ({nome_hospital}): {nome_item} expires in {dias_restantes} days"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = ", ".join(destinatarios)
    if EMAILS_COPIA_GERAL:
        msg["Cc"] = ", ".join(EMAILS_COPIA_GERAL)

    corpo = f"""
    <html>
      <body>
        <p>Hello,</p>
        <p>This is an automated reminder for <strong>{nome_hospital}</strong>.</p>
        <p>
            Item <strong>{nome_item}</strong>
            expires in <strong>{dias_restantes} days</strong>.
            <br>(Expiration date: {data_venc})
        </p>
        <p>Please arrange the required documentation.</p>
        <p>Best regards,<br>RTCON System</p>
      </body>
    </html>
    """
    msg.add_alternative(corpo, subtype="html")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
            server.send_message(msg)
        print(f"   ✅ Email sent: {nome_item}")
        return True
    except Exception as e:
        print(f"   ❌ Email error: {e}")
        return False

# =========================================================
# HOSPITAL PROCESSOR
# =========================================================

def processar_hospital(hospital):
    nome = hospital["nome"]
    planilha_id = hospital["id_planilha"]
    emails_destino = hospital["emails"]

    print(f"\n🏥 Processing: {nome}...")

    url = f"GOOGLE PLANILHA"
    arquivo_temp = os.path.join(BASE_DIR, f"temp_{nome.replace(' ', '_')}.xlsx")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(arquivo_temp, "wb") as f:
            f.write(resp.content)

        df = pd.read_excel(arquivo_temp, sheet_name=NOME_DA_ABA, header=2)
        hoje = pd.Timestamp.now().normalize()

        for i, linha in df.iterrows():
            item = str(linha["Item"]).strip()
            venc = pd.to_datetime(linha["Vencimento"], errors="coerce")

            if pd.isna(venc):
                continue

            dias_restantes = (venc - hoje).days
            eh_autorizacao = i == 0

            disparar = (eh_autorizacao and dias_restantes == 120) or \
                       (not eh_autorizacao and dias_restantes == 30)

            if disparar:
                print(f"   🔔 ALERT: {item} ({dias_restantes} days)")
                enviar_email(nome, item, dias_restantes, venc.strftime("%d/%m/%Y"), emails_destino)

        os.remove(arquivo_temp)
        print(f"✅ {nome} completed.")

    except Exception as e:
        print(f"❌ CRITICAL ERROR in {nome}: {e}")

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    HOSPITAIS = load_hospitals()

    if not HOSPITAIS:
        exit(1)

    if not EMAIL_REMETENTE or not SENHA_REMETENTE:
        print("⚠️  EMAIL and SENHA environment variables not set.")
        print("   Set them in your .env file or GitHub Actions secrets.")

    print(f"🔄 Processing {len(HOSPITAIS)} hospitals...")

    for hospital in HOSPITAIS:
        processar_hospital(hospital)
        time.sleep(2)

    print("\n🏁 Processing complete.")
