import os
from pathlib import Path
from flask import Flask, render_template, request

from segmenter import segment_narrative
from prompt_engine import build_prompt
from image_generator import generate_image, generate_placeholder

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024


def build_storyboard(narrative: str) -> list[dict]:
    scenes = segment_narrative(narrative)
    panels = []

    for i, scene_text in enumerate(scenes):
        prompt = build_prompt(scene_text)

        try:
            image_file = generate_image(prompt, i)
        except Exception:
            image_file = generate_placeholder(i, scene_text)

        panels.append(
            {
                "index": i + 1,
                "scene": scene_text,
                "prompt": prompt,
                "image": image_file,
            }
        )

    return panels


@app.route("/", methods=["GET"])
def index():
    return render_template("storyboard.html", panels=None, narrative="")


@app.route("/generate", methods=["POST"])
def generate():
    narrative = request.form.get("narrative", "").strip()
    error = None
    panels = None

    if not narrative:
        error = "Please enter a narrative paragraph."
    else:
        try:
            panels = build_storyboard(narrative)
        except Exception as exc:
            error = str(exc)

    return render_template(
        "storyboard.html",
        panels=panels,
        narrative=narrative,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
