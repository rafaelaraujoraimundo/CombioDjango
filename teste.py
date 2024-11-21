import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações de ambiente

# Criar a mensagem
message = MIMEMultipart("alternative")
message["Subject"] = "Teste de e-mail com STARTTLS"
message["From"] = 'mla@combio.com.br'
message["To"] = "rafael.araujo@combio.com.br"

# Corpo do e-mail
text = "Este é um e-mail enviado via STARTTLS com Python!"
html = "<html><body><p>Este é um e-mail enviado via <b>STARTTLS</b> com Python!</p></body></html>"

# Anexar o texto e o HTML
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
message.attach(part1)
message.attach(part2)

# Conexão ao servidor SMTP com STARTTLS
try:
    with smtplib.SMTP('smtp-mail.outlook.com', '587') as server:
        server.ehlo()  # Identifica o cliente para o servidor
        server.starttls()  # Inicializa a criptografia STARTTLS
        server.ehlo()  # Reidentifica após iniciar TLS
        server.login('mla@combio.com.br', 'D@tasul123!!!!autorizacao')  # Autenticação
        server.sendmail('mla@combio.com.br', 'rafael.araujo@combio.com.br', message.as_string())  # Envia o e-mail
        print("E-mail enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")