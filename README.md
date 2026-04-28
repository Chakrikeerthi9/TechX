# Sentiment Analysis Mini Project

**TechX Internship Assignment** — Keerthi Chakri  
NLP sentiment classifier using **TextBlob** — returns Positive / Negative / Neutral for any text input.

---

## Project Structure

```
sentiment_project/
├── sentiment_analyzer.py   # Core logic + 12-sentence test suite
├── app.py                  # FastAPI REST endpoint
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/techx-sentiment.git
cd techx-sentiment

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download TextBlob corpora (first-time only)
python -m textblob.download_corpora
```

---

## Run the Test Suite

```bash
python sentiment_analyzer.py
```

Expected output — 12 test sentences with ✓/✗, polarity scores, accuracy summary, and analysis of borderline predictions.

---

## Run the API

```bash
uvicorn app:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "I absolutely love this product!"}'
```

### Example Response

```json
{
  "label": "Positive",
  "polarity": 0.625,
  "subjectivity": 0.6,
  "input_text": "I absolutely love this product!"
}
```

### Input Validation

| Scenario | Response |
|---|---|
| Empty string `""` | `422 – Input text must not be empty...` |
| Non-string (e.g. `123`) | `422 – Input must be a string...` |
| Valid text | `200 – label / polarity / subjectivity` |

---

## How It Works

1. **TextBlob** computes a `polarity` score in the range `[-1.0, +1.0]`.
2. Thresholds: `polarity > 0.05` → **Positive** · `polarity < -0.05` → **Negative** · otherwise → **Neutral**.
3. `subjectivity` (0–1) is also returned as a secondary signal.

---

## Test Results Summary

12 sentences tested — 4 Positive, 4 Negative, 4 Neutral.  
See terminal output or `test_results.txt` for the full table.

---

## Limitations & Future Work

- TextBlob uses a fixed lexicon; it struggles with sarcasm and domain-specific language.
- Replacing TextBlob with a fine-tuned transformer (e.g. `cardiffnlp/twitter-roberta-base-sentiment`) would improve accuracy significantly.
- The neutral threshold (`±0.05`) was tuned empirically and could be calibrated with labelled data.
