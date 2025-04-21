import os
import zipfile

# Tạo thư mục và nội dung các file cho dự án
project_name = "excel_lookup_github_ready"
base_path = f"/mnt/data/{project_name}"

# Tạo thư mục và các file cần thiết
os.makedirs(f"{base_path}/templates", exist_ok=True)

# Nội dung app.py
app_py = """from flask import Flask, render_template, request
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
"""

# Nội dung index.html
index_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Tra cứu câu hỏi</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f7fa; margin: 0; padding: 0; }
        .container { max-width: 800px; margin: 40px auto; background: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border-radius: 12px; }
        h1 { text-align: center; color: #2c3e50; }
        select, input[type="text"], button { width: 100%; padding: 10px; margin-top: 10px; font-size: 16px; border-radius: 6px; border: 1px solid #ccc; }
        .result { margin-top: 30px; background: #ecf0f1; padding: 20px; border-radius: 10px; }
        .result h3 { margin-bottom: 5px; color: #34495e; }
        .result p { background: white; padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
        .footer { text-align: center; margin-top: 40px; color: #aaa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Tra cứu câu hỏi từ Excel</h1>

        <form method="post">
            <label for="keyword">Tìm theo từ khóa:</label>
            <input type="text" name="keyword" id="keyword" value="{{ keyword }}">
            <button type="submit">Tìm kiếm</button>
        </form>

        <form method="post">
            <label for="question_id">Chọn câu hỏi:</label>
            <select name="question_id" id="question_id">
                {% for item in data %}
                    <option value="{{ item.question_id }}">{{ item.question_id }}</option>{% endfor %}
            </select>
            <button type="submit">Tra cứu</button>
        </form>

        {% if selected %}
            <div class="result">
                <h3>Nội dung câu hỏi:</h3>
                <p>{{ selected.question }}</p>

                <h3>Đáp án:</h3>
                <p>{{ selected.answer }}</p>

                <h3>Giải thích:</h3>
                <p>{{ selected.explanation }}</p>
            </div>
        {% endif %}
    </div>

    <div class="footer">
        © 2025 - Ứng dụng tra cứu Python & Flask
    </div>
</body>
</html>
"""

# Nội dung requirements.txt
requirements = "flask\npandas\nopenpyxl"

# Nội dung Procfile
procfile = "web: gunicorn app:app"

# Nội dung runtime.txt
runtime = "python-3.10.8"

# Ghi các file vào thư mục
with open(f"{base_path}/app.py", "w", encoding="utf-8") as f:
    f.write(app_py)

with open(f"{base_path}/templates/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

with open(f"{base_path}/requirements.txt", "w", encoding="utf-8") as f:
    f.write(requirements)

with open(f"{base_path}/Procfile", "w", encoding="utf-8") as f:
    f.write(procfile)

with open(f"{base_path}/runtime.txt", "w", encoding="utf-8") as f:
    f.write(runtime)

# Tạo file ZIP
zip_path = f"{base_path}.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(base_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            arcname = os.path.relpath(file_path, base_path)
            zipf.write(file_path, arcname)

zip_path