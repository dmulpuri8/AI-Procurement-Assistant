from typing import Tuple
import re, difflib

_HAVE_ST=False; _HAVE_HF=False
_embedder=None; _summarizer=None

def _try_load_models():
    global _HAVE_ST, _HAVE_HF, _embedder, _summarizer
    try:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
        _HAVE_ST = True
    except Exception:
        _HAVE_ST = False; _embedder=None
    try:
        from transformers import pipeline
        _summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        _HAVE_HF = True
    except Exception:
        _HAVE_HF = False; _summarizer=None

def nlp_status() -> Tuple[bool,str]:
    if _embedder is None and _summarizer is None:
        _try_load_models()
    if _HAVE_ST or _HAVE_HF:
        return True, None
    return True, "Running in NLP-lite mode (no ML backends found)."

def summarize(text: str, max_len: int = 140) -> str:
    if not text:
        return ""
    if _summarizer is None and _embedder is None:
        _try_load_models()
    if _summarizer:
        try:
            return _summarizer(text[:2000], max_length=max_len, min_length=40, do_sample=False)[0]["summary_text"]
        except Exception:
            pass
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(parts[:4])

def semantic_similarity(a: str, b: str) -> float:
    if not a or not b: return 0.0
    if _embedder is None and _summarizer is None:
        _try_load_models()
    if _embedder:
        try:
            from sentence_transformers import util
            ea = _embedder.encode(a, convert_to_tensor=True)
            eb = _embedder.encode(b, convert_to_tensor=True)
            score = util.cos_sim(ea, eb).item()
            return round(max(0.0, min(1.0, score))*100.0, 2)
        except Exception:
            pass
    ta = " ".join(sorted(set(a.lower().split())))
    tb = " ".join(sorted(set(b.lower().split())))
    return round(difflib.SequenceMatcher(None, ta, tb).ratio()*100.0, 2)
