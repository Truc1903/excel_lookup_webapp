from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def load_data():
    df = pd.read_excel("data.xlsx")
    df = df.fillna("")
    data = []
    for _, row in df.iterrows():
        data.append({
            "question_id": str(row["Câu hỏi"]),
            "question": str(row["Nội dung câu hỏi"]),
            "answer": str(row["Đáp án"]),
            "explanation": str(row["Giải thích"])
        })
    return data

@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()
    selected = None
    keyword = request.form.get("keyword", "").strip().lower()

    if keyword:
        data = [item for item in data if keyword in item["question"].lower() or keyword in item["explanation"].lower()]

    if request.method == "POST" and not keyword:
        selected_id = request.form.get("question_id")
        selected = next((item for item in data if item["question_id"] == selected_id), None)

    return render_template("index.html", data=data, selected=selected, keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)
