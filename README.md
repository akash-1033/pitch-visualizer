# Pitch Visualizer

Transforms a narrative paragraph into a visual storyboard. Each sentence in the input is treated as a scene, expanded into a detailed image-generation prompt, sent to an image model, and assembled into a multi-panel storyboard page served via Flask.

---

## Architecture Overview

```
narrative input
      │
      ▼
segmenter.py          — splits paragraph into scene sentences using NLTK
      │
      ▼
prompt_engine.py      — expands each sentence into a rich visual prompt
      │
      ▼
image_generator.py    — fetches one generated image per scene via Pollinations.ai
      │
      ▼
app.py                — Flask application that orchestrates the pipeline
      │
      ▼
templates/storyboard.html  — rendered multi-panel storyboard page
```

### File Roles

| File | Responsibility |
|---|---|
| `app.py` | Flask routes, pipeline orchestration |
| `segmenter.py` | Sentence segmentation via NLTK |
| `prompt_engine.py` | Prompt expansion with setting and action heuristics |
| `image_generator.py` | Image generation via Pollinations.ai API |
| `templates/storyboard.html` | Jinja2 storyboard template |
| `static/images/` | Generated image output directory |
| `requirements.txt` | Python dependencies |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/akash-1033/pitch-visualizer
cd pitch-visualizer
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

That's it. No API keys, no model downloads, no GPU required.

---

## Running the Application

```bash
python app.py
```

Open `http://localhost:5000` in a browser. Enter a multi-sentence narrative paragraph and click **Generate Storyboard**. One image is generated per sentence.

Generation takes roughly 5–15 seconds per scene depending on Pollinations.ai server load.

---

## Prompt Engineering Approach

Raw sentences from the narrative are not passed directly to the image model. `prompt_engine.py` applies three layers of enrichment:

**1. Setting keyword detection**
The sentence is scanned for environment words (`night`, `city`, `ocean`, `desert`, etc.). Each matched keyword maps to a visual descriptor phrase:
- `"night"` → `"moonlit, deep shadows, ambient glow"`
- `"city"` → `"urban skyline, neon reflections, steel and glass"`

**2. Action keyword detection**
Action verbs (`run`, `fall`, `speak`, `fight`, etc.) are matched with regex to catch conjugations (`running`, `ran`, `runs`). Each maps to a composition cue:
- `"fall"` → `"vertiginous angle, motion, atmospheric depth"`
- `"speak"` → `"expressive gesture, warm portrait lighting"`

**3. Style suffix**
Every prompt ends with a fixed cinematic quality string regardless of content:
```
cinematic composition, dramatic lighting, highly detailed,
photorealistic, 8k, sharp focus, professional photography
```

The result is a prompt substantially longer and more visually directed than the original sentence, with no hallucinated facts added.

---

## Image Generation

`image_generator.py` calls the [Pollinations.ai](https://pollinations.ai) public API — no account or API key needed.

Each prompt is sent as a URL-encoded GET request:
```
https://image.pollinations.ai/prompt/<encoded-prompt>?width=512&height=512&nologo=true&seed=<scene_index>
```

Images are written to `static/images/` and named by scene index and an MD5 digest of the prompt. If a file already exists for a given prompt, the request is skipped (deterministic caching). If the network request fails for any scene, a labeled fallback image is rendered locally via Pillow.

Generated images are excluded from version control via `.gitignore`. The `static/images/.gitkeep` file preserves the directory in the repository.

---

## Project Structure

```
pitch_visualizer/
├── app.py
├── segmenter.py
├── prompt_engine.py
├── image_generator.py
├── templates/
│   └── storyboard.html
├── static/
│   └── images/
│       └── .gitkeep
├── requirements.txt
├── .gitignore
└── README.md
```
