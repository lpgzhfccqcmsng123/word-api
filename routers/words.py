from fastapi import APIRouter, HTTPException

from models import Word
from storage import load_words, save_words

router = APIRouter()


@router.get("/words")
def get_all():
    """返回全部词条。"""
    return load_words()


@router.get("/words/{word}")
def get_one(word: str):
    """按单词查释义。不存在返回 404。"""
    words = load_words()
    if word in words:
        return {"word": word, "meaning": words[word]}
    raise HTTPException(status_code=404, detail="没有这个词")


@router.post("/words")
def add_word_api(item: Word):
    """新增词条。已存在返回 409。"""
    words = load_words()
    if item.word in words:
        raise HTTPException(status_code=409, detail=f"{item.word} 已存在")
    words[item.word] = item.meaning
    save_words(words)
    return {"ok": True, "word": item.word}
