from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests
from database import get_conn
from flask import Flask, render_template, request
from services.gemini_services import analyze_with_gemini
from services.fact_check_service import check_fact_google
from database import get_conn
from services.content_extractor import extract_text_from_url


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/fakenews")
def fakenews():
    return render_template("fakenews.html")

@app.route("/documentation")
def documentation():
    return render_template("documentation.html")

@app.route("/check", methods=["POST"])
def check_news():

    text = request.form.get("text")

    # 🔗 Se for link, extrai conteúdo
    if text.startswith("http"):
        extracted = extract_text_from_url(text)

        if extracted:
            content = extracted
        else:
            content = text
    else:
        content = text

    # 🔎 Serviço Google
    result, claims = check_fact_google(content)

    # 🧠 Serviço Gemini (fallback)
    gemini_analysis = analyze_with_gemini(content)

    if "Falso" in gemini_analysis:
        result = "Falso"
    elif "Verdadeiro" in gemini_analysis:
        result = "Verdadeiro"
    else:
        result = "Inconclusivo"

    # 💾 Banco
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO fact_checks (claim_text, result) VALUES (?, ?)",
        (text, result)
    )

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        claims=claims,
        input=text,
        result=result,
        gemini=gemini_analysis
    )

@app.route("/history")
def history():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM fact_checks ORDER BY created_at DESC")
    rows = cursor.fetchall()

    conn.close()

    return render_template("history.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)