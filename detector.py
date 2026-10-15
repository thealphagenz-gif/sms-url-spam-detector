from pathlib import Path
from urllib.parse import urlparse
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

DATA = Path(__file__).resolve().parent / "data" / "sms_dataset.csv"

class SpamDetector:
    def __init__(self):
        df = pd.read_csv(DATA).dropna(subset=["label", "message"])
        df["label"] = df["label"].astype(str).str.lower().str.strip()
        df = df[df["label"].isin(["spam", "ham"])]
        if len(df) < 4 or df["label"].nunique() < 2:
            raise ValueError("Dataset needs examples of both spam and ham.")
        self.model = Pipeline([
            ("tfidf", TfidfVectorizer(lowercase=True, strip_accents="unicode",
                                      ngram_range=(1, 2), max_features=12000)),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
        ])
        self.model.fit(df["message"].astype(str), df["label"])

    def predict_sms(self, message):
        probs = self.model.predict_proba([message])[0]
        classes = list(self.model.classes_)
        spam = float(probs[classes.index("spam")])
        label = "Spam" if spam >= .5 else "Not Spam"
        confidence = spam if spam >= .5 else 1 - spam
        patterns = [
            (r"\b(win|winner|won|prize|claim|reward|lottery)\b", "Prize or winning language"),
            (r"\b(urgent|immediately|act now|limited time)\b", "Urgency or pressure language"),
            (r"\b(verify|password|bank|account|otp|pin)\b", "Account or credential-related wording"),
            (r"\b(click|tap|link|visit)\b", "Call to click or visit something"),
            (r"\b(free|cash|offer|bonus)\b", "Promotional or money-related wording"),
            (r"(https?://|www\.)", "Contains a web link")
        ]
        indicators = [desc for pat, desc in patterns if re.search(pat, message, re.I)]
        return {"type":"sms", "label":label, "confidence":round(confidence*100,1),
                "spam_probability":round(spam*100,1),
                "risk":"High" if spam >= .75 else ("Medium" if spam >= .45 else "Low"),
                "indicators":indicators[:5],
                "note":"Machine-learning estimate only; check the sender independently before acting."}

def analyze_url(value):
    original = value.strip()
    normalized = original if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", original) else "https://" + original
    parsed = urlparse(normalized)
    host = (parsed.hostname or "").lower()
    path = parsed.path or ""
    indicators, score = [], 0
    checks = [
        (not host or "." not in host, 35, "Address does not look like a typical domain."),
        (parsed.scheme.lower() == "http", 15, "Uses HTTP rather than encrypted HTTPS."),
        ("@" in original, 25, "Contains an @ symbol that can obscure the destination."),
        (bool(re.search(r"\b(login|verify|secure|account|update|wallet|payment|bank)\b", host+path, re.I)), 15, "Contains account or payment lure wording."),
        (bool(re.search(r"\d{1,3}(?:\.\d{1,3}){3}", host)), 30, "Uses an IP address instead of a regular domain."),
        (len(original) > 100, 10, "Unusually long address."),
        (host.count("-") >= 3, 10, "Domain contains several hyphens."),
        ("xn--" in host, 15, "Contains internationalized-domain encoding."),
        (len(host.split(".")) >= 5, 10, "Has many subdomains.")
    ]
    for matched, points, desc in checks:
        if matched:
            score += points
            indicators.append(desc)
    if not indicators:
        indicators.append("No obvious warning patterns were detected by these basic checks.")
    score = min(score, 100)
    label, risk = ("High Risk", "High") if score >= 50 else (("Suspicious", "Medium") if score >= 20 else ("No obvious warning signs", "Low"))
    return {"type":"url", "label":label, "risk":risk, "risk_score":score,
            "host":host or "Could not identify domain", "indicators":indicators,
            "note":"This URL is checked as text only, not opened or verified online. Low risk does not guarantee safety."}
