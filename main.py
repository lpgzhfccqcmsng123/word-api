# -*- coding: utf-8 -*-
"""
单词本 API

把英文单词和中文释义存在 words.json 里，通过 HTTP 接口增查。
"""

import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATA_FILE = "words.json"


app = FastAPI()


class Word(BaseModel):
    word: str
    meaning: str




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


@app.get("/words")
def get_all():
    """返回全部词条。"""
    return load_words()


# ===== 下面两个接口，你自己写 =====

# 1. GET /words/{word}
#    路径参数 word: str
#    存在 → 返回 {"word": word, "meaning": 释义}
#    不存在 → 返回什么，你自己定（先想清楚理由）
@app.get("/words/{word}")
def get_one(word: str):
    words = load_words()
    if word in words:
        return {"word": word, "meaning": words[word]}
    raise HTTPException(status_code=404, detail="没有这个词")

# 2. POST /words
#    请求体模型 Word（word: str, meaning: str）
#    已存在 → 你怎么处理，自己定
#    不存在 → 加入词库，save_words，返回 {"ok": True}

@app.post("/words")
def add_word_api(item: Word):
    words = load_words()
    if item.word in words:
        raise HTTPException(409, f"{item.word} 已存在")
    words[item.word] = item.meaning
    save_words(words)
    return {"ok": True, "word": item.word}
