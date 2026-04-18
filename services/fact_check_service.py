import requests
import os

API_KEY = os.getenv("GOOGLE_FACTCHECK_API_KEY")

def check_fact_google(text):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    
    params = {
        "query": text,
        "key": API_KEY
    }

    response = requests.get(url, params=params).json()
    claims = response.get("claims", [])

    result = "Nenhuma checagem encontrada em bases oficiais"

    try:
        first_claim = claims[0]
        first_review = first_claim["claimReview"][0]
        result = first_review.get("textualRating", "Desconhecido")
    except (IndexError, KeyError):
        result = "Sem verificação oficial"

    return result, claims