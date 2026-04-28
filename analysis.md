# Analysis of Uncertain Predictions

**Model:** TextBlob | **Author:** Keerthi Chakri | **Project:** TechX Internship — Sentiment Analysis

---

## Case 1 — Mixed Emotion Sentence Scored Incorrectly

**Input:**
> "My friend said that when he eats a candy he will feel happy and also regret that he does not maintain his diet."

| | |
|---|---|
| Predicted | Positive (+0.80) |
| Actual sentiment | Mixed (both positive and negative) |

**Why it failed:**

The sentence contains two emotions — happiness ("happy") and regret ("regret"). TextBlob picked up "happy" as a strong positive token and scored it +0.80, completely ignoring "regret" as a negative signal. The result is heavily skewed Positive when the true sentiment is mixed. TextBlob cannot handle sentences where two contrasting emotions coexist.

**What a better model would do:**

A transformer-based model would read the full sentence and recognize the contrast between "happy" and "regret", likely returning a lower confidence mixed or neutral prediction rather than a confident Positive.

---

## Case 2 — Negation Not Understood ("not enough")

**Input:**
> "In my last interview when I was explaining about my projects he said my performance is not enough."

| | |
|---|---|
| Predicted | Neutral (0.0000) |
| Actual sentiment | Negative |

**Why it failed:**

"Not enough" is clearly a negative judgment, but TextBlob scored the sentence as Neutral with 0.0 polarity. TextBlob's lexicon does not recognize "not enough" as a negative phrase — it sees "not" and "enough" as separate tokens with no strong sentiment weight. Negation handling is one of the most well-known weaknesses of lexicon-based models.

**What a better model would do:**

A context-aware model trained on real human feedback would recognize "not enough" as a negative evaluation phrase and return a Negative prediction.

---

## Bonus Observations

**Typo sensitivity — "awful" vs "awfull"**

| Input | Predicted | Polarity |
|---|---|---|
| "I ate pizza it tastes awfull" | Neutral | 0.0000 |
| "I ate pizza it tastes bad" | Negative | -0.7000 |

A single spelling mistake ("awfull" instead of "awful") caused TextBlob to return Neutral instead of Negative — because "awfull" is not in its lexicon dictionary. Real-world user input is messy, and lexicon models are highly sensitive to spelling errors.

**Sarcasm / context blindness — "my friend is happy because I broke his mobile"**

| Input | Predicted | Polarity |
|---|---|---|
| "My friend is happy cuz I broke his mobile" | Positive (+0.80) | — |

The sentence is clearly negative in real-world context — breaking someone's phone is bad. But TextBlob only sees "happy" and returns a confident Positive. It has no understanding of cause and effect or real-world knowledge.

---

## Key Takeaway

All failures share the same root cause — TextBlob is a **lexicon-based model** with no understanding of:

- **Mixed emotions** — two contrasting feelings in one sentence
- **Negation** — "not enough", "not great", "didn't like"
- **Typos** — unrecognized words get a score of 0
- **Cause and effect** — "happy because something bad happened"
- **Context and sarcasm** — surface words don't always reflect true sentiment

For production use, a fine-tuned transformer model such as `cardiffnlp/twitter-roberta-base-sentiment` would handle these cases significantly better.