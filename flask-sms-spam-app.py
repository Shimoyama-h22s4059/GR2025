from flask import Flask, request, render_template
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Flask アプリ作成
app = Flask(__name__)

# モデル読み込み
model_path = "./bert-sms-spam/checkpoint-837"
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# ラベル名
label_names = ["ham", "spam"]

@app.route("/", methods=["GET", "POST"])
def index():
    text = None
    result = None

    if request.method == "POST":
        text = request.form["text"]

        # トークナイズしてモデルに渡す
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()
        result = label_names[pred]

        print(outputs)

    return render_template("index-sms-spam.html", text=text, result=result)


# Flask 実行
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
