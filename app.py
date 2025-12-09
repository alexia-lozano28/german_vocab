from flask import Flask, render_template, request
import pandas as pd
import random
import os

app = Flask(__name__)

# Load Excel
df = pd.read_excel("words.xlsx")
words = df.to_dict(orient="records")

# Extract unique types and chapters
types = sorted(df["type"].dropna().unique().tolist())
types.insert(0, "all")

chapters = sorted(df["Kapitel"].dropna().unique().tolist())
chapters.insert(0, "all")

incorrect_log = []

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", types=types, chapters=chapters)


@app.route("/play/<mode>", methods=["GET", "POST"])
def play(mode):
    selected_type = request.args.get("type", "all")
    selected_chapter = request.args.get("chapter", "all")

    result = None

    if request.method == "POST":
        user_answer = request.form["answer"].strip().lower()
        correct_answer = request.form["correct"].strip().lower()
        shown_word = request.form["shown_word"]
        selected_type = request.form["selected_type"]
        selected_chapter = request.form["selected_chapter"]

        if user_answer == correct_answer:
            result = "✅ Correct!"
        else:
            result = f"❌ Incorrect. The correct answer is: {correct_answer}"

            incorrect_log.append({
                "Mode": mode,
                "Shown word": shown_word,
                "Correct answer": correct_answer,
                "Your answer": user_answer
            })

    # Filter by type
    filtered_words = words
    if selected_type != "all":
        filtered_words = [w for w in filtered_words if str(w["type"]) == selected_type]

    # Filter by chapter
    if selected_chapter != "all":
        filtered_words = [w for w in filtered_words if str(w["Kapitel"]) == str(selected_chapter)]

    # Pick a random word
    word = random.choice(filtered_words)

    # Select direction
    if mode == "de-en":
        shown = word["German"]
        correct = word["English"]
    else:
        shown = word["English"]
        correct = word["German"]

    return render_template(
        "play.html",
        mode=mode,
        shown_word=shown,
        correct_answer=correct,
        result=result,
        selected_type=selected_type,
        selected_chapter=selected_chapter,
        types=types,
        chapters=chapters
    )


@app.route("/fallos")
def fallos():
    return render_template("mistakes.html", fallos=incorrect_log)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
