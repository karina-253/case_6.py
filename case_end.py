#Part of a case-study #6: Text Analysis
# Developers: Lagoda K., Zheravina A., Pinoeva K., Mozhaitseva M.


import local as lcl
from textblob import TextBlob
from translate import Translator


def sentences_in_text(line):
    """The function counts the number of sentences in the text."""
    k = 0
    marks = [".", "?", "!"]
    for i in range(1, len(line)):
        if (line[i] in marks) + (line[i-1].isalpha()) == 2:
           k += 1
    return k


def count_words(word):
    """The function counts the number of words in the text."""
    words = word.split()
    return len(words)


def word_vowel(syllable):
    """The function counts the number of syllables in the text."""
    vowels_ru = ["а", "у", "ё", "е", "ы", "о", "э", "я", "и", "ю"]
    words_register = syllable.lower().split()
    cnt_syllable = 0
    for every_word in words_register:
        for ch in every_word:
            if ch in vowels_ru:
                cnt_syllable += 1
    return cnt_syllable


def ending_e(word):
    if len(word) > 3 and word[-1] == 'e' and word[-2] != 'l' and word[-2] not in vowels_en:
        word = word[:-1]
    elif len(word) == 3 and word[0] in vowels_en and word[-1] == 'e':
        word = word[:-1]
    return word


def starting_y(word):
    if word[0] == 'y':
        word = 'j' + word[1:]
    return word


def delete_u(word):
    i = 0
    while i < len(word) - 2:
        if word[i] == 'g' and word[i+1] == 'u' and word[i+2] in vowels_en:
            word = word[:i+1] + word[i+2:]
        i+=1
    return word


def with_ld_nd(word):
    if 'ld' in word:
        word = word.replace('ld','lid')
    if 'nd' in word:
        word = word.replace('nd', 'nid')
    return word


def two_vowels(word):
    i = 0
    while i < len(word) - 1:
        if word[i] == 'a' and word[i+1] in ['i', 'y', 'u', 'w']:
            word = word[:i] + word[i+1:]
            i += 2
        elif word[i] == 'o' and word[i+1] in ['i', 'y', 'a', 'o', 'u', 'w']:
            word = word[:i] + word[i+1:]
            i += 2
        elif word[i] == 'e' and word[i + 1] in ['a', 'e', 'i', 'u', 'w']:
            word = word[:i] + word[i + 1:]
            i += 2
        elif word[i] == 'i' and word[i + 1] == 'e':
            word = word[:i] + word[i + 1:]
            i += 2
        else:
            i += 1
    return word


def count_syllable(text):
    syllable = 0
    for letter in ''.join(text):
       if letter in vowels_en:
            syllable += 1
    return syllable


text = input()
words = text.lower().split()
vowels_en = ['e', 'u', 'y', 'o', 'a', 'i']


without_e = []
for word in words:
    without_e.append(ending_e(word))

without_e_y = []
for word in without_e:
    without_e_y.append(starting_y(word))

without_e_y_u = []
for word in without_e_y:
    without_e_y_u.append(delete_u(word))

with_i = []
for word in without_e_y_u:
    with_i.append(with_ld_nd(word))

without_two_vowel = []
for word in with_i:
    without_two_vowel.append(two_vowels(word))

new_text = without_two_vowel

average_sentences = count_words(text) / sentences_in_text(text)


def language(x):
    """The function determines which language the text is written in."""
    letter = [ord(ch) for ch in x if ch.isalpha()]
    average_un = sum(letter) // len(letter)
    if average_un > 1000:
        text_language = "russian"
    else:
        text_language = "english"
    return text_language


def average_len(word):
    """The function counts the average length of a word in syllables."""
    if language(word) == "russian":
        return word_vowel(text) / count_words(text)
    else:
        return count_syllable(new_text) / len(new_text)


def flesh(text):
    """The function counts the Flush index."""
    if language(text) == "russian":
        return 206.835 - 1.52 * average_sentences - 65.14 * average_len(text)
    else:
        return 206.835 - 1.015 * average_sentences - 84.6 * average_len(text)


def complexity_text(text):
    """The function determines the difficulty of the text to read."""
    match flesh(text):
        case _ if flesh(text) > 80:
             return f"{lcl.VERY_EASY}"
        case _ if 50 < flesh(text) <= 80:
             return f"{lcl.EASY}"
        case _ if 25 < flesh(text) <= 50:
             return f"{lcl.HARD}"
        case _:
            return f"{lcl.VERY_HARD}"


def polarity_and_objectivity(text):
    """The function translates Russian text into English.

    Determines its tone and degree of objectivity.
    """
    translator = Translator(from_lang = "ru", to_lang = "en")
    eng_text = translator.translate(text)

    polarity = TextBlob(eng_text).sentiment.polarity
    subjectivity = TextBlob(eng_text).sentiment.subjectivity
    objectivity = round((1 - subjectivity) * 100, 2)

    if round(polarity) > 0:
        tonality = f"{lcl.POSITIVE}"
    elif round(polarity) == 0:
        tonality = f"{lcl.NEUTRAL}"
    else:
        tonality = f"{lcl.NEGATIVE}"
    return (f"{lcl.TEXT_TONE} {tonality}",
            f"{lcl.OBJECTIVITY_OF_THE_TEXT} {objectivity}%")


def main():
    print(f"{lcl.SENTENCES} {sentences_in_text(text)}")
    print(f"{lcl.WORDS} {count_words(text)}")
    print(f"{lcl.SYLLABLES} {word_vowel(text)}")
    print(f"{lcl.AVARANGE_SENTENCES_LENGTH_IN_WORDS} {average_sentences}")
    print(f"{lcl.AVARAGE_WORD_LENGTH_IN_SYLLABLES} {average_len(text)}")
    print(f"{lcl.FLASH_READABILITY_INDEX} {flesh(text)}")
    print(complexity_text(text))
    print("\n".join(polarity_and_objectivity(text)))


if __name__ == '__main__':
    main()
