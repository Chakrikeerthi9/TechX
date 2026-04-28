from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentiment_analyzer import analyze_sentiment

app = FastAPI(
    title="Sentiment Analysis API",
    description="TextBlob-powered sentiment classifier — TechX Internship",
    version="1.0.0",
)


class TextInput(BaseModel):
    text: str


class SentimentResponse(BaseModel):
    label: str
    polarity: float
    subjectivity: float
    input_text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=SentimentResponse)
def analyze(payload: TextInput):
    try:
        result = analyze_sentiment(payload.text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except TypeError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return SentimentResponse(
        label=result["label"],
        polarity=result["polarity"],
        subjectivity=result["subjectivity"],
        input_text=payload.text,
    )
