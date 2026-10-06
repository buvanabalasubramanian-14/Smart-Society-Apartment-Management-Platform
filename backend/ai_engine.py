import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "ai_training_data.csv"
)

data = pd.read_csv(DATA_FILE)


category_vectorizer = TfidfVectorizer(
    ngram_range=(1, 2)
)

category_features = category_vectorizer.fit_transform(
    data["complaint"]
)

category_model = LogisticRegression(
    max_iter=2000
)

category_model.fit(
    category_features,
    data["category"]
)


risk_vectorizer = TfidfVectorizer(
    ngram_range=(1, 2)
)

risk_features = risk_vectorizer.fit_transform(
    data["complaint"]
)

risk_model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)

risk_model.fit(
    risk_features,
    data["risk"]
)


def detect_category(text):

    text = text.lower()

    if any(word in text for word in [
        "parking",
        "vehicle",
        "car parking",
        "bike parking",
        "parking area"
    ]):
        return "Parking"

    if any(word in text for word in [
        "lift",
        "elevator",
        "lift stopped",
        "lift stuck"
    ]):
        return "Lift"

    if any(word in text for word in [
        "short circuit",
        "electric",
        "electrical",
        "current",
        "electricity",
        "fan",
        "light",
        "switch",
        "socket",
        "power"
    ]):
        return "Electrical"

    if any(word in text for word in [
        "security",
        "unknown person",
        "stranger",
        "theft",
        "robbery",
        "gate",
        "visitor",
        "suspicious person"
    ]):
        return "Security"

    if any(word in text for word in [
        "crack",
        "wall damage",
        "building damage",
        "structural",
        "ceiling damage"
    ]):
        return "Structural"

    if any(word in text for word in [
        "garbage",
        "cleaning",
        "waste",
        "dirty",
        "dust",
        "trash"
    ]):
        return "Cleaning"

    if any(word in text for word in [
        "water",
        "pipe",
        "tap",
        "leak",
        "leakage",
        "sewage",
        "drain",
        "drainage"
    ]):
        return "Plumbing"

    category_input = category_vectorizer.transform(
        [text]
    )

    return category_model.predict(
        category_input
    )[0]


def analyze_complaint(complaint):

    text = complaint.lower()

    category = detect_category(text)


    critical_words = [
        "fire",
        "smoke",
        "short circuit",
        "electric shock",
        "gas leak",
        "gas leakage",
        "lift stopped",
        "lift stuck",
        "sewage overflow",
        "sewage leakage",
        "major crack",
        "building crack",
        "emergency",
        "dangerous",
        "flooding",
        "flooded",
        "burst pipe",
        "water burst"
    ]


    high_words = [
        "overflow",
        "water flooding",
        "security breach",
        "unknown person",
        "heavy leakage",
        "heavy leak",
        "continuous leakage",
        "continuous leak"
    ]


    medium_words = [
        "leak",
        "leaking",
        "leakage",
        "not working",
        "broken",
        "damage",
        "damaged",
        "garbage",
        "cleaning",
        "water supply",
        "fan",
        "light",
        "tap",
        "pipe"
    ]


    low_words = [
        "parking",
        "paint",
        "minor",
        "small issue",
        "cosmetic",
        "general issue"
    ]


    if any(
        word in text
        for word in critical_words
    ):

        risk = "Critical"
        risk_score = 95


    elif (
        "water leakage" in text
        or "water leak" in text
        or "leakage" in text
    ):

        risk = "High"
        risk_score = 75


    elif any(
        word in text
        for word in high_words
    ):

        risk = "High"
        risk_score = 80


    elif "parking" in text:

        risk = "Low"
        risk_score = 25


    elif "water supply" in text:

        risk = "Medium"
        risk_score = 50


    elif any(
        word in text
        for word in medium_words
    ):

        risk = "Medium"
        risk_score = 55


    elif any(
        word in text
        for word in low_words
    ):

        risk = "Low"
        risk_score = 25


    else:

        risk_input = risk_vectorizer.transform(
            [text]
        )

        risk = risk_model.predict(
            risk_input
        )[0]

        probabilities = risk_model.predict_proba(
            risk_input
        )[0]

        confidence = max(probabilities)

        risk_scores = {
            "Low": 25,
            "Medium": 50,
            "High": 75,
            "Critical": 95
        }

        risk_score = (
            risk_scores.get(
                risk,
                50
            ) * 0.7
            + confidence * 100 * 0.3
        )


    recommendations = {

        "Plumbing":
            "Assign plumbing maintenance team and inspect the affected area.",

        "Electrical":
            "Assign electrical maintenance team and inspect electrical connections.",

        "Lift":
            "Contact lift maintenance team and inspect the lift immediately.",

        "Cleaning":
            "Assign housekeeping team and resolve the cleaning issue.",

        "Security":
            "Alert security staff and verify the affected location.",

        "Structural":
            "Arrange immediate building inspection.",

        "Parking":
            "Notify parking management team and inspect the parking area.",

        "General":
            "Review the complaint and assign the appropriate maintenance team."
    }


    return {
        "category": category,
        "risk": risk,
        "risk_score": round(risk_score, 2),
        "recommendation": recommendations.get(
            category,
            "Review the complaint and assign the appropriate team."
        )
    }