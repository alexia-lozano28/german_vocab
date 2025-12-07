from flask import Flask, render_template, request
import pandas as pd
import random
import os

app = Flask(__name__)

# Cargar Excel
df = pd.read_excel("words.xlsx")
words = df.to_dict(orient="records")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    word = random.choice(words)  # palabra al azar

    if request.method == "POST":
        user_answer = request.form["answer"].strip().lower()
        correct_answer = request.form["correct"].strip().lower()
        word = {
            "German": request.form["german"],
            "English": request.form["correct"]
        }

        if user_answer == correct_answer:
            result = "✅ Correcto!"
        else:
            result = f"❌ Incorrecto. La respuesta correcta es: {correct_answer}"

    return render_template("index.html", word=word, result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
