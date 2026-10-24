import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from config import Config

def send_whatsapp_alert(prospect_payload: dict, post_url: str):
    if not Config.TWILIO_ACCOUNT_SID or not Config.TWILIO_AUTH_TOKEN:
        print("⚠️ Twilio no configurado. Omitiendo alerta de WhatsApp.")
        return

    try:
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        message_body = (
            f"🚨 *¡PROSPECTO DE BELLEZA DETECTADO!* 🚨\n\n"
            f"👤 *Usuario:* {prospect_payload['username']} ({prospect_payload['platform']})\n"
            f"⚠️ *Necesidad:* {prospect_payload['problem']}\n"
            f"⚡ *Urgencia:* {prospect_payload['urgency']}\n\n"
            f"💬 *Mensaje Sugerido:* \n{prospect_payload['suggested_message']}\n\n"
            f"🔗 *Enlace:* {post_url}"
        )
        client.messages.create(
            body=message_body,
            from_=Config.TWILIO_WHATSAPP_NUMBER,
            to=Config.MY_WHATSAPP_NUMBER
        )
        print("📱 Alerta de WhatsApp enviada con éxito.")
    except Exception as e:
        print(f"❌ Error al enviar WhatsApp: {str(e)}")

def send_email_alert(prospect_payload: dict, post_url: str):
    if not Config.SENDER_EMAIL or not Config.SENDER_PASSWORD:
        print("⚠️ SMTP no configurado. Omitiendo email.")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = Config.SENDER_EMAIL
        msg['To'] = Config.DESTINATION_EMAIL
        msg['Subject'] = f"✨ Oportunidad de Venta: {prospect_payload['problem']}"

        body = f"""
Nuevo prospecto detectado en {prospect_payload['platform']}:
- Usuario: {prospect_payload['username']}
- Problema: {prospect_payload['problem']}
- Urgencia: {prospect_payload['urgency']}
- Enlace: {post_url}

Texto original:
"{prospect_payload['post_text']}"

Respuesta sugerida:
"{prospect_payload['suggested_message']}"
        """
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.SENDER_EMAIL, Config.SENDER_PASSWORD)
        server.sendmail(Config.SENDER_EMAIL, Config.DESTINATION_EMAIL, msg.as_string())
        server.quit()
        print("📧 Correo de alerta enviado con éxito.")
    except Exception as e:
        print(f"❌ Error en SMTP: {str(e)}")