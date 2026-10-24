import json
from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

class AnalysisResult:
    def __init__(self, is_valid_prospect, problem_detected=None, urgency=None, suggested_message=None, reasoning=None):
        self.is_valid_prospect = is_valid_prospect
        self.problem_detected = problem_detected
        self.urgency = urgency
        self.suggested_message = suggested_message
        self.reasoning = reasoning

def evaluate_post(post_text: str) -> AnalysisResult:
    prompt = f"""
    Analiza la siguiente publicación de redes sociales para determinar si es un cliente potencial (prospecto válido) que busca soluciones para problemas de belleza, líneas de expresión, arrugas, paño, manchas o cuidado facial antienvejecimiento. Descarta spam, memes o temas ajenos.

    Publicación: "{post_text}"

    Responde estrictamente en formato JSON con la siguiente estructura exacta:
    {{
        "is_valid_prospect": true o false,
        "problem_detected": "breve descripción del problema estético o cutáneo detectado, o null si no aplica",
        "urgency": "Alta", "Media" o "Baja",
        "suggested_message": "Un mensaje amable, empático y profesional sugiriendo rutinas o productos de dermocosmética/skincare, o null si no aplica",
        "reasoning": "Breve explicación de por qué es o no es un prospecto válido"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        
        return AnalysisResult(
            is_valid_prospect=data.get("is_valid_prospect", False),
            problem_detected=data.get("problem_detected"),
            urgency=data.get("urgency"),
            suggested_message=data.get("suggested_message"),
            reasoning=data.get("reasoning")
        )
    except Exception as e:
        return AnalysisResult(
            is_valid_prospect=False,
            reasoning=f"Error en la API de OpenAI: {str(e)}"
        )