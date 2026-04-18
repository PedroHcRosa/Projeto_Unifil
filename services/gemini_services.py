import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_with_gemini(text):
    model = genai.GenerativeModel("gemini-flash-latest")

    prompt = f"""
    Você é um verificador de fatos profissional.

    Analise a afirmação abaixo e responda EXATAMENTE neste formato:

    Classificação: (Verdadeiro, Falso ou Inconclusivo)

    Explicação:
    (explique de forma clara e objetiva)

    Fontes recomendadas:
    - (site confiável 1)
    - (site confiável 2)
    - (site confiável 3)

    Use apenas fontes confiáveis como:
    BBC, G1, Reuters, OMS, universidades, etc.

    Afirmação:
    "{text}"
    """

    response = model.generate_content(prompt)

    return response.text