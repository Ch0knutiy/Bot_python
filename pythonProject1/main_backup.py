# -*- coding: utf8 -*-

import config
import random
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

corpus = []
y = []
for intent, intent_data in config.BOT_CONFIG['intents'].items():
    for example in intent_data['examples']:
        corpus.append(example)
        y.append(intent)

vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
X = vectorizer.fit_transform(corpus)

clf_proba = LogisticRegression()
clf_proba.fit(X, y)

clf = LinearSVC()
clf.fit(X, y)

LinearSVC()


def get_intent(question):
    best_intent = clf.predict(vectorizer.transform([question]))[0]

    index_of_best_intent = list(clf_proba.classes_).index(best_intent)
    probabilities = clf_proba.predict_proba(vectorizer.transform([question]))[0]

    best_intent_proba = probabilities[index_of_best_intent]
    if best_intent_proba > 0.09:
        return best_intent


def get_answer_by_intent(intent):
    phrases = config.BOT_CONFIG['intents'][intent]['responses']
    return random.choice(phrases)


with open('dialogues.txt') as f:
    content = f.read()

dialogues = content.split('\n\n')


def clear_question(question):
    question = question.lower().strip()
    alphabet = ' -1234567890йцукенгшщзхъфывапролджэёячсмитьбю'
    question = ''.join(c for c in question if c in alphabet)
    return question


questions = set()
dataset = {}  # {word1: [[q1, a1], [q2, a2], ...], ...}

for dialogue in dialogues:
    replicas = dialogue.split('\n')[:2]
    if len(replicas) == 2:
        question, answer = replicas
        question = clear_question(question[2:])
        answer = answer[2:]

        if question and question not in questions:
            questions.add(question)
            words = question.split(' ')
            for word in words:
                if word not in dataset:
                    dataset[word] = []
                dataset[word].append([question, answer])

too_popular = set()
for word in dataset:
    if len(dataset[word]) > 10000:
        too_popular.add(word)

for word in too_popular:
    dataset.pop(word)


def get_generative_answer(replica):
    replica = clear_question(replica)
    words = replica.split(' ')

    mini_dataset = []
    for word in words:
        if word in dataset:
            mini_dataset += dataset[word]

    candidates = []

    for question, answer in mini_dataset:
        if abs(len(question) - len(replica)) / len(question) < 0.4:
            d = nltk.edit_distance(question, replica)
            diff = d / len(question)
            if diff < 0.4:
                candidates.append([question, answer, diff])

    winner = min(candidates, key=lambda candidate: candidate[2])
    return winner[1]


stats = {'intent': 0, 'generative': 0, 'failure': 0}


def get_failure_phrase():
    phrases = config.BOT_CONFIG['failure_phrases']
    return random.choice(phrases)


def bot(question):
    #
    # NLU
    intent = get_intent(question)

    #
    # Получение ответа

    # Заготовленный ответ
    if intent:
        stats['intent'] += 1
        return get_answer_by_intent(intent)

#    # Применяем генеративную модель
#   answer = get_generative_answer(question)
#   if answer:
#        stats['generative'] += 1
#        return answer

    # Ответ-заглушка
    stats['failure'] += 1
    return get_failure_phrase()


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Ready to chat!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    question = update.message.text
    answer = bot(question)
    update.message.reply_text(answer)
    print(question)
    print(answer)
    print(stats)
    print()


def main():
    updater = Updater(
        config.Token,
        use_context=True
    )

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
