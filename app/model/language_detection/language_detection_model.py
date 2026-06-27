import pickle
import re
from pathlib import Path

__version__ = "0.1.0"
BASE_DIR = Path(__file__).resolve(strict=True).parent

with open(f"{BASE_DIR}/trained_pipeline-{__version__}.pkl", "rb") as f:
    artifact = pickle.load(f)

if hasattr(artifact, 'steps'):
    # If it's a Pipeline, the last step is our classifier
    model = artifact.steps[-1][1]
elif isinstance(artifact, dict):
    model = artifact["model"]
else:
    model = artifact

try:
    classes = model.classes_.tolist()
except AttributeError:
    classes = []



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
        text = re.sub(r'[[]]', ' ', text)
        text = text.lower()
        data_list.append(text)

    predictions = model.predict(data_list)
    return [classes[p] for p in predictions]