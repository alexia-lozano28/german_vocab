from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__)

df = pd.read_excel("words.xlsx")
words = df.to_dict(orient="records")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        german = request.form["german"]
        answer = request.form["answer"].strip().lower()
        correct = request.form["correct"].lower()
        result = "correcto" if answer == correct else f"incorrecto (era: {correct})"
    else:
        result = None

    w = random.choice(words)
    return render_template("index.html", word=w, result=result)

app.run(debug=True)
