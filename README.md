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

## Interactive Mode

Test the model live by typing your own sentences:

```bash
python sentiment_analyzer.py --interactive
```

```
Sentiment Analyzer — type 'quit' to exit

Enter text: I love this project!
  Label      : Positive
  Polarity   : +0.5000
  Subjectivity: 0.6000

Enter text: quit
```

---

## Limitations & Observed Failure Cases

TextBlob uses a fixed word-level lexicon — it scores each token independently without understanding sentence context. During manual testing, three interesting failure cases were found:

**1. Idioms ("better luck next time")**
> *"Yesterday I gave an interview and he is very happy about my response and he said better luck next time."*
> Predicted: **Positive (+0.50)** — Expected: Negative

"better" and "happy" score positively, drowning out the rejection implied by "better luck next time." TextBlob has no awareness of idioms.

**2. Emotional ownership ("he is happy" vs "I am happy")**
> The model cannot distinguish *who* is feeling the sentiment. If the interviewer is happy but rejects you, the sentence still scores Positive.

**3. Weak negation ("I am sorry")**
> *"...he said I am sorry"* — Predicted: **Positive (+0.25)**

"happy" in the same sentence outweighs "sorry," so the overall score stays positive despite the negative implication.

**Potential fix:** Replacing TextBlob with a fine-tuned transformer like `cardiffnlp/twitter-roberta-base-sentiment` would handle idioms, negation, and contextual sentiment significantly better. The neutral threshold (`±0.05`) was tuned empirically and could also be calibrated with labelled data.