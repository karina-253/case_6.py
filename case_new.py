from textblob import TextBlob
from translate import Translator


def sentences_in_text(x):
    """Считает количество предложений в тексте."""
    k = 0
    marks = [".", "?", "!"]
    for i in range(1, len(x)):
        if (x[i] in marks) + (x[i-1].isalpha()) == 2:
           k += 1
    return k


def count_words(x):
    """Считает количество слов в тексте."""
    words = x.split()
    return len(words)


def word_vowel(x):
    """Считает количество слогов в тексте."""
    vowels_ru = ["а", "у", "ё", "е", "ы", "о", "э", "я", "и", "ю"]
    vowels_en = ["e", "u", "y", "o", "a", "i"]
    words_register = x.lower().split()
    syllable = 0
    for word in words_register:
        for ch in word:
            if ch in vowels_ru or ch in vowels_en:
                syllable += 1
    return syllable


text = input()
average_sentences = count_words(text) / sentences_in_text(text)
average_syllable = word_vowel(text) / count_words(text)


def flesh(x):
    """Определяет на каком языке написан текст.

    Считает индекс Флеша на языке, на котором написан текст.
    """
    letters = [char for char in x if char.isalpha()]
    average = sum(ord(char) for char in letters) / len(letters)
    if average > 1000:
        return 206.835 - 1.52 * average_sentences - 65.14 * average_syllable
    else:
        return 206.835 - 1.015 * average_sentences - 84.6 * average_syllable


def complexity_text(x):
    """Определяет сложность текста для чтения"""
    match flesh(x):
        case _ if flesh(x) > 80:
             return "Текст очень легко читается (для младших школьников)."
        case _ if 50 < flesh(x) <= 80:
             return "Простой текст (для школьников)."
        case _ if 25 < flesh(x) <= 50:
             return "Текст немного трудно читать (для студентов)."
        case _:
            return "Текст трудно читается (для выпускников ВУЗов)."


def polarity_and_objectivity(x):
    """Переводит русский текст на английский.

    Определяет его тональность и степень объективности.
    """
    translator = Translator(from_lang="ru", to_lang="en")
    eng_text = translator.translate(x)

    polarity = TextBlob(eng_text).sentiment.polarity
    subjectivity = TextBlob(eng_text).sentiment.subjectivity
    objectivity = round((1 - subjectivity) * 100, 2)

    if round(polarity) > 0:
        tonality = "положительный"
    elif round(polarity) == 0:
        tonality = "нейтральный"
    else:
        tonality = "негативный"
    return (f"Тональность текста: {tonality}",
            f"Объективность текста: {objectivity}%")


print(f"Предложений: {sentences_in_text(text)}")
print(f"Слов: {count_words(text)}")
print(f"Слогов: {word_vowel(text)}")
print(f"Средняя длина предложения в словах: {average_sentences}")
print(f"Средняя длина слова в слогах: {average_syllable}")
print(f"Индекс удобочитаемости Флеша: {flesh(text)}")
print(complexity_text(text))
print("\n".join(polarity_and_objectivity(text)))
