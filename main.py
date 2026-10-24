from mock_listener import get_incoming_posts
from evaluator import evaluate_post
from notifier import send_whatsapp_alert, send_email_alert

processed_ids = set()

def run_agent():
    print("🚀 Iniciando Agente de Prospección Comercial (Nichos de Belleza)...")
    posts = get_incoming_posts()

    for post in posts:
        post_id = post["id"]
        if post_id in processed_ids:
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

            send_whatsapp_alert(payload, post["post_url"])
            send_email_alert(payload, post["post_url"])
        else:
            print(f"❌ Descartado: {analysis.reasoning}")

        processed_ids.add(post_id)

if __name__ == "__main__":
    run_agent()