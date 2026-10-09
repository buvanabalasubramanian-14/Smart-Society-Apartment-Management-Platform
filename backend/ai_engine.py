import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "ai_training_data.csv")

data = pd.read_csv(DATA_FILE)

category_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
category_features = category_vectorizer.fit_transform(data["complaint"])

category_model = LogisticRegression(max_iter=2000)
category_model.fit(category_features, data["category"])

risk_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
risk_features = risk_vectorizer.fit_transform(data["complaint"])

risk_model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)
risk_model.fit(risk_features, data["risk"])


def detect_category(text):
    text = text.lower()

    rules = {
        "Parking": [
            "parking", "vehicle", "car parking", "bike parking"
        ],
        "Lift": [
            "lift", "elevator", "lift stopped", "lift stuck"
        ],
        "Electrical": [
            "short circuit", "electric", "electrical", "current",
            "electricity", "fan", "light", "switch", "socket", "power"
        ],
        "Security": [
            "security", "unknown person", "stranger", "theft",
            "robbery", "gate", "visitor", "suspicious person"
        ],
        "Structural": [
            "crack", "wall damage", "building damage",
            "structural", "ceiling damage"
        ],
        "Cleaning": [
            "garbage", "cleaning", "waste", "dirty", "dust", "trash"
        ],
        "Plumbing": [
            "water", "pipe", "tap", "leak", "leakage",
            "sewage", "drain", "drainage"
        ]
    }

    for category, words in rules.items():
        if any(word in text for word in words):
            return category

    features = category_vectorizer.transform([text])
    return category_model.predict(features)[0]


def analyze_complaint(complaint):
    text = complaint.lower()
    category = detect_category(text)

    critical_words = [
        "fire", "smoke", "short circuit", "electric shock",
        "gas leak", "gas leakage", "lift stopped", "lift stuck",
        "sewage overflow", "sewage leakage", "major crack",
        "building crack", "emergency", "dangerous", "flooding",
        "flooded", "burst pipe", "water burst"
    ]

    high_words = [
        "overflow", "water flooding", "security breach",
        "unknown person", "heavy leakage", "heavy leak",
        "continuous leakage", "continuous leak"
    ]

    medium_words = [
        "leak", "leaking", "leakage", "not working", "broken",
        "damage", "damaged", "garbage", "cleaning", "water supply",
        "fan", "light", "tap", "pipe"
    ]

    low_words = [
        "parking", "paint", "minor", "small issue",
        "cosmetic", "general issue"
    ]

    if any(word in text for word in critical_words):
        risk = "Critical"
        risk_score = 95
    elif any(word in text for word in high_words):
        risk = "High"
        risk_score = 80
    elif "water leakage" in text or "water leak" in text:
        risk = "High"
        risk_score = 75
    elif "parking" in text:
        risk = "Low"
        risk_score = 25
    elif "water supply" in text:
        risk = "Medium"
        risk_score = 50
    elif any(word in text for word in medium_words):
        risk = "Medium"
        risk_score = 55
    elif any(word in text for word in low_words):
        risk = "Low"
        risk_score = 25
    else:
        features = risk_vectorizer.transform([text])
        risk = risk_model.predict(features)[0]
        probabilities = risk_model.predict_proba(features)[0]
        confidence = max(probabilities)

        risk_scores = {
            "Low": 25,
            "Medium": 50,
            "High": 75,
            "Critical": 95
        }

        risk_score = (
            risk_scores.get(risk, 50) * 0.7
            + confidence * 100 * 0.3
        )

    recommendations = {
        "Plumbing": "Assign the plumbing team to inspect pipes and water supply.",
        "Electrical": "Ask the electrical team to inspect the affected connections.",
        "Lift": "Contact the lift maintenance team for an inspection.",
        "Cleaning": "Assign housekeeping to clean the affected area.",
        "Security": "Alert security staff and verify the reported incident.",
        "Structural": "Arrange a building inspection by qualified personnel.",
        "Parking": "Notify parking management and check the parking area.",
        "General": "Review the complaint and assign the appropriate team."
    }

    priorities = {
        "Critical": {
            "priority": "P1 - Immediate",
            "urgency": "Immediate attention",
            "action": "Escalate immediately to the responsible team."
        },
        "High": {
            "priority": "P2 - Urgent",
            "urgency": "Urgent attention",
            "action": "Arrange inspection as soon as possible."
        },
        "Medium": {
            "priority": "P3 - Normal",
            "urgency": "Scheduled maintenance",
            "action": "Add to the maintenance team's work queue."
        },
        "Low": {
            "priority": "P4 - Routine",
            "urgency": "Routine attention",
            "action": "Plan this task during routine maintenance."
        }
    }

    maintenance = priorities.get(risk, priorities["Medium"])

    return {
        "category": category,
        "risk": risk,
        "risk_score": round(risk_score, 2),
        "recommendation": recommendations.get(
            category,
            "Review the complaint and assign the appropriate team."
        ),
        "maintenance_priority": maintenance["priority"],
        "maintenance_urgency": maintenance["urgency"],
        "maintenance_action": maintenance["action"]
    }