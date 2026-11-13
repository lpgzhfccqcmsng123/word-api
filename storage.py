import json

DATA_FILE = "words.json"


def load_words():
    """读 words.json 返回字典。文件不存在返回 {}。"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_words(words):
    """把字典写回 words.json。"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
