from textblob import TextBlob
from translate import Translator

text = input()

def dif(x):
    k = 0
    mrks = [".","?","!"]
    for i in range(1,len(x)):
        if (x[i] in mrks) + (x[i-1].isalpha()) == 2:
           k += 1
    return k

def count_words(x):
    words = x.split()
    return len(words)

def word_vowel(x):
    vowels_ru = ['а', 'у', 'ё', 'е', 'ы', 'о', 'э', 'я', 'и', 'ю']
    vowels_en = ['e', 'u', 'y', 'o', 'a', 'i']
    words = x.lower().split()
    syllable = 0
    for word in words:
        for i in word:
            if i in vowels_ru or i in vowels_en:
                syllable+=1
    return syllable

average_sentences = count_words(text) / dif(text)
average_syllable = word_vowel(text) / count_words(text)

def flesh(x):
    letters = [char for char in x if char.isalpha()]
    average = sum(ord(char) for char in letters) / len(letters)
    if average > 1000:
        return 206.835 - 1.52 * average_sentences - 65.14 * average_syllable
    else:
        return 206.835-1.015 * average_sentences - 84.6 * average_syllable

def polarity_and_objectivity(x):
    translator = Translator(from_lang="ru", to_lang="en")
    eng_text = translator.translate(x)

    polarity = TextBlob(eng_text).sentiment.polarity
    subjectivity = TextBlob(eng_text).sentiment.subjectivity
    objectivity = round((1 - subjectivity) * 100, 2)
    if round(polarity) > 0:
        tonality = 'положительный'
    elif round(polarity) == 0:
        tonality = 'нейтральный'
    else:
        tonality = 'негативный'
    return (f'Тональность текста: {tonality}',
            f'Объективность текста: {objectivity}%')

print(f'Предложений: {dif(text)}')
print(f'Слов: {count_words(text)}')
print(f'Слогов: {word_vowel(text)}')
print(f'Средняя длина предложения в словах: {average_sentences}')
print(f'Средняя длина слова в слогах: {average_syllable}')
print(f'Индекс удобочитаемости Флеша: {flesh(text)}')
print('\n'.join(polarity_and_objectivity(text)))


