from textblob import TextBlob


def analyze_sentiment(text) -> dict:
    """
    Accepts text input and returns sentiment label + confidence score.

    Args:
        text: Input to analyze (must be a non-empty string)

    Returns:
        dict with keys: label, polarity, subjectivity

    Raises:
        TypeError: if input is not a string
        ValueError: if input is empty or whitespace-only
    """
    # --- Input validation ---
    if not isinstance(text, str):
        raise TypeError(f"Input must be a string, got {type(text).__name__}.")
    if not text.strip():
        raise ValueError("Input text must not be empty or whitespace-only.")

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity        # range: [-1.0, +1.0]
    subjectivity = blob.sentiment.subjectivity  # range: [0.0, 1.0]

    if polarity > 0.05:
        label = "Positive"
    elif polarity < -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label": label,
        "polarity": round(polarity, 4),
        "subjectivity": round(subjectivity, 4),
    }


# ---------------------------------------------------------------------------
# Test suite — 12 sentences (4 positive, 4 negative, 4 neutral)
# ---------------------------------------------------------------------------
TEST_SENTENCES = [
    # Positive
    ("The product exceeded all my expectations — absolutely fantastic!", "Positive"),
    ("I had a wonderful time at the concert last night.", "Positive"),
    ("This is the best coffee I have ever tasted.", "Positive"),
    ("She passed her exams with flying colors. So proud of her!", "Positive"),
    # Negative
    ("The customer service was rude and completely unhelpful.", "Negative"),
    ("I regret buying this laptop; it breaks down every week.", "Negative"),
    ("The movie was dull, predictable, and a waste of two hours.", "Negative"),
    ("Terrible experience — the food was cold and the staff ignored us.", "Negative"),
    # Neutral
    ("The meeting is scheduled for 3 PM on Thursday.", "Neutral"),
    ("Water boils at 100 degrees Celsius at sea level.", "Neutral"),
    ("The package was delivered to the front desk.", "Neutral"),
    ("The report contains twelve pages and three appendices.", "Neutral"),
]


def run_tests():
    print("=" * 70)
    print("  Sentiment Analysis — Test Results")
    print("  Model: TextBlob  |  Author: Keerthi Chakri")
    print("=" * 70)

    correct = 0
    results = []

    for sentence, expected in TEST_SENTENCES:
        result = analyze_sentiment(sentence)
        predicted = result["label"]
        match = predicted == expected
        if match:
            correct += 1
        status = "✓" if match else "✗"
        results.append((sentence, expected, predicted, result["polarity"], match, status))
        print(f"\n[{status}] \"{sentence[:65]}{'...' if len(sentence)>65 else ''}\"")
        print(f"     Expected: {expected:<10}  Predicted: {predicted:<10}  Polarity: {result['polarity']:+.4f}")

    accuracy = correct / len(TEST_SENTENCES) * 100
    print("\n" + "=" * 70)
    print(f"  Results: {correct}/{len(TEST_SENTENCES)} correct  |  Accuracy: {accuracy:.1f}%")
    print("=" * 70)

    # --- Analysis of uncertain/incorrect predictions ---
    print("\n📊 Analysis of Uncertain / Incorrect Predictions")
    print("-" * 70)

    incorrect = [(s, e, p, pol) for s, e, p, pol, m, _ in results if not m]

    if not incorrect:
        # Pick two borderline cases to analyze even if all are correct
        print("\nAll 12 predictions were correct! Analyzing 2 borderline cases:\n")
        borderline = sorted(results, key=lambda r: abs(r[3]))[:2]
        for sentence, expected, predicted, polarity, *_ in borderline:
            _print_analysis(sentence, expected, predicted, polarity)
    else:
        for sentence, expected, predicted, polarity in incorrect[:2]:
            _print_analysis(sentence, expected, predicted, polarity)


def _print_analysis(sentence, expected, predicted, polarity):
    print(f"Sentence : \"{sentence}\"")
    print(f"Expected : {expected}   |   Predicted: {predicted}   |   Polarity: {polarity:+.4f}")
    if abs(polarity) <= 0.05:
        print("Analysis : Polarity is extremely close to zero (the Neutral threshold).")
        print("           TextBlob may miss implicit sentiment in factual phrasing.")
    elif expected == "Neutral" and predicted != "Neutral":
        print("Analysis : The sentence contains words with strong lexical sentiment,")
        print("           causing TextBlob to miscategorize an objectively neutral statement.")
    else:
        print("Analysis : TextBlob's lexicon-based scoring may miss sarcasm, negation,")
        print("           or domain-specific language, leading to an incorrect prediction.")
    print()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        print("Sentiment Analyzer — type 'quit' to exit\n")
        while True:
            text = input("Enter text: ").strip()
            if text.lower() == "quit":
                break
            try:
                result = analyze_sentiment(text)
                print(f"  Label      : {result['label']}")
                print(f"  Polarity   : {result['polarity']:+.4f}")
                print(f"  Subjectivity: {result['subjectivity']:.4f}\n")
            except ValueError as e:
                print(f"  Error: {e}\n")
    else:
        run_tests()