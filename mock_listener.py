import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_incoming_posts():
    posts = []
    print("🌐 Escaneando fuentes públicas en busca de consultas sobre belleza y piel...")
    
    query = "necesito crema arrugas lineas de expresion pano cutis"
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='result')
            
            counter = 1
            for r in results[:5]:
                title_elem = r.find('a', class_='result__snippet')
                title_text = title_elem.get_text() if title_elem else ""
                link_elem = r.find('a', class_='result__url')
                link = link_elem['href'] if link_elem else "https://duckduckgo.com"
                
                if title_text:
                    posts.append({
                        "id": f"beauty_post_{counter:03d}",
                        "username": f"prospecto_web_{counter}",
                        "platform": "Foros / Web Pública",
                        "post_text": title_text,
                        "post_url": link
                    })
                    counter += 1
                    
        print(f"🔍 Se capturaron {len(posts)} publicaciones de la web.")
    except Exception as e:
        print(f"⚠️ Error al conectar con fuentes reales: {str(e)}")

    # 🛡️ Sistema de Respaldo (Fallback): Si la web no arroja datos, 
    # usamos ejemplos controlados para que el agente nunca se detenga en pruebas.
    if len(posts) == 0:
        print("💡 Activando modo de respaldo: cargando publicaciones de prueba para validar el flujo...")
        posts = [
            {
                "id": "beauty_fallback_001",
                "username": "claudia_Perez92",
                "platform": "Foro de Belleza",
                "post_text": "Hola a todos, últimamente he estado notando líneas de expresión muy marcadas alrededor de los ojos y algo de paño en las mejillas por el sol. ¿Qué crema o tratamiento me recomiendan?",
                "post_url": "https://duckduckgo.com"
            },
            {
                "id": "beauty_fallback_002",
                "username": "mariana_skincare",
                "platform": "Blog de Salud",
                "post_text": "Busco recomendaciones urgentes para mejorar la textura de mi cutis, tengo la piel seca y siento que las cremas comerciales ya no me quitan la tirantez ni las arrugas finas.",
                "post_url": "https://duckduckgo.com"
            }
        ]

    return posts