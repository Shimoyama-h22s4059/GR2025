import io

import torch
from flask import Flask, render_template, request, jsonify
from PIL import Image
import base64

from torchvision.transforms import Compose, Resize, Grayscale, ToTensor, Normalize
from transformers import AutoModelForImageClassification, AutoImageProcessor

app = Flask(__name__)

# モデルと前処理
model = AutoModelForImageClassification.from_pretrained("./mnist-vit/checkpoint-5625").to("cuda").eval()
processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")

transform = Compose([
    Resize((224, 224)),
    Grayscale(num_output_channels=3),
    ToTensor(),
    Normalize(mean=processor.image_mean, std=processor.image_std)
])

@app.route("/")
def index():
    return render_template("index-mnist.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json["image"]
    image_data = base64.b64decode(data.split(",")[1])
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    tensor = transform(image).unsqueeze(0).to("cuda")

    # now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    #
    # with open(f"{now}.png", "wb") as f:
    #     f.write(image_data)

    with torch.no_grad():
        outputs = model(pixel_values=tensor)
        prediction = outputs.logits.argmax(-1).item()

        return jsonify({"prediction": prediction})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
