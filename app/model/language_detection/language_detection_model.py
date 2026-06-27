import pickle
import re
from pathlib import Path

__version__ = "0.1.0"
BASE_DIR = Path(__file__).resolve(strict=True).parent

with open(f"{BASE_DIR}/trained_pipeline-{__version__}.pkl", "rb") as f:
    artifact = pickle.load(f)

LANGUAGE_LABELS = [
    "Arabic", "Danish", "Dutch", "English", "French", "German",
    "Greek", "Hindi", "Italian", "Kannada", "Malayalam", "Portugeese",
    "Russian", "Spanish", "Sweedish", "Tamil", "Turkish"
]

model = artifact
classes = LANGUAGE_LABELS


def predict_language(X):
    """
    Function to predict the language of the given text data.

    Args:
        X (list): List of text data.

    Returns:
        list: List of predicted languages for each text in X.
    """
    data_list = []
    for text in X:
        text = re.sub(r'[!@#$(),\n"%^*?\:;~`0-9.]', ' ', text)
        text = re.sub(r'[\[\]]', ' ', text)
        text = text.lower()
        data_list.append(text)

    predictions = model.predict(data_list)
    return [classes[p] for p in predictions]