# Script temporário

import os
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_REMETENTE = os.getenv("SENHA_REMETENTE")

DESTINATARIOS = [
    os.getenv("EMAIL_DESTINATARIO_1"),
]

print("EMAIL:", EMAIL_REMETENTE)
print("DESTINATARIOS:", DESTINATARIOS)

assunto = "Teste de alerta cardíaco"

mensagem = """
Teste de envio de email do sistema ML_CarePlus.

Se você recebeu esta mensagem:
- SMTP está funcionando
- Variáveis de ambiente foram carregadas
- O sistema está pronto para alertas
"""

email = MIMEMultipart()

email["From"] = EMAIL_REMETENTE
email["To"] = ", ".join(DESTINATARIOS)
email["Subject"] = assunto

email.attach(MIMEText(mensagem, "plain"))

try:
    servidor = smtplib.SMTP("smtp.gmail.com", 587)

    print("[1] Conectado ao servidor SMTP")

    servidor.starttls()

    print("[2] TLS iniciado")

    servidor.login(EMAIL_REMETENTE, SENHA_REMETENTE)

    print("[3] Login realizado")

    servidor.sendmail(
        EMAIL_REMETENTE,
        DESTINATARIOS,
        email.as_string()
    )

    print("[4] Email enviado com sucesso")

    servidor.quit()

    print("[5] Conexão encerrada")

except Exception as e:
    print("ERRO:")
    print(e)