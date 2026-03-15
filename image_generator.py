import hashlib
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "static" / "images"


def _prompt_to_filename(prompt: str, index: int) -> str:
    digest = hashlib.md5(prompt.encode()).hexdigest()[:8]
    return f"scene_{index:02d}_{digest}.png"


def generate_image(prompt: str, scene_index: int) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filename = _prompt_to_filename(prompt, scene_index)
    filepath = OUTPUT_DIR / filename

    if filepath.exists():
        return filename

    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true&seed={scene_index}"

    req = urllib.request.Request(url, headers={"User-Agent": "PitchVisualizer/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()

    with open(filepath, "wb") as f:
        f.write(data)

    return filename


def generate_placeholder(scene_index: int, label: str) -> str:
    from PIL import Image, ImageDraw

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"placeholder_{scene_index:02d}.png"
    filepath = OUTPUT_DIR / filename

    img = Image.new("RGB", (512, 512), color=(28, 28, 38))
    draw = ImageDraw.Draw(img)

    draw.rectangle([12, 12, 499, 499], outline=(70, 70, 95), width=2)
    draw.rectangle([12, 12, 130, 38], fill=(180, 50, 42))
    draw.text((71, 25), f"SCENE {scene_index + 1:02d}", fill=(245, 240, 232), anchor="mm")

    words = label.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        if len(test) <= 42:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    lines = lines[:6]

    start_y = 256 - (len(lines) * 22) // 2
    for i, line in enumerate(lines):
        draw.text((256, start_y + i * 22), line, fill=(190, 185, 210), anchor="mm")

    img.save(str(filepath))
    return filename
