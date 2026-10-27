from mock_listener import get_incoming_posts
from evaluator import evaluate_post
from notifier import send_whatsapp_alert, send_email_alert
from database import init_db, is_already_processed, mark_as_processed

def run_agent():
    print("🚀 Iniciando Agente de Prospección Comercial (Andalucía Beauty)...")
    
    # Inicializar la base de datos SQLite persistente
    init_db()
    
    posts = get_incoming_posts()

    if not posts:
        print("⚠️ No hay nuevos prospectos pendientes de procesar.")
        return

    for post in posts:
        post_id = post["id"]
        
        # Validación con SQLite: si ya se procesó en el pasado, se omite
        if is_already_processed(post_id):
            print(f"⏭️ El post {post_id} ya fue procesado anteriormente. Saltando...")
            continue

        print(f"\n🔍 Analizando consulta de {post['username']}...")
        analysis = evaluate_post(post["post_text"])

        if analysis.is_valid_prospect:
            print(f"✅ ¡PROSPECTO VÁLIDO! [{analysis.problem_detected}]")
            
            payload = {
                "username": post["username"],
                "platform": post["platform"],
                "problem": analysis.problem_detected,
                "urgency": analysis.urgency,
                "post_text": post["post_text"],
                "suggested_message": analysis.suggested_message
            }

            # Disparar alertas reales
            send_whatsapp_alert(payload, post["post_url"])
            send_email_alert(payload, post["post_url"])
            
            # 🛡️ ¡IMPORTANTE!: Guardar en SQLite para que nunca se repita
            mark_as_processed(post_id, post["username"])
            
        else:
            print(f"❌ Descartado: {analysis.reasoning}")
            # Opcional: También podemos marcar los descartados si no quieres que los reintente evaluar
            mark_as_processed(post_id, post["username"])

if __name__ == "__main__":
    run_agent()