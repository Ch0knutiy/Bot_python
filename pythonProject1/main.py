# -*- coding: utf8 -*-

import config
import random
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


button_mail = 'Бот не помог'
stats = {'intent': 0, 'failure': 0}


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
    if best_intent_proba > 0.0001:
        return best_intent


def get_styp_info(words):
    return 'Стипендии не назначено'


def bot(question):
    words = question.split(' ')
    if words[0] == 'Стипендия?':
        return get_styp_info(words)

    intent = get_intent(question)

    if intent:
        stats['intent'] += 1
        return get_answer_by_intent(intent)

    stats['failure'] += 1
    return get_failure_phrase()


def get_answer_by_intent(intent):
    phrases = config.BOT_CONFIG['intents'][intent]['responses']
    return random.choice(phrases)


def get_failure_phrase():
    phrases = config.BOT_CONFIG['failure_phrases']
    return random.choice(phrases)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Ready to chat!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Информация об назначенной стипендии: /styp')


def styp_command(update: Update, context: CallbackContext):
    update.message.reply_text('Для получения информации о стипендии пришли мне "Стипендия? Фамилия Имя Курс Группа"')


def button_mail_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Если бот не помог пишите не почту: mail@mail.ru',
        reply_markup=ReplyKeyboardRemove(),
    )


def message_handler(update: Update, context: CallbackContext):
    question = update.message.text
    if question == button_mail:
        return button_mail_handler(update=update, context=context)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_mail),
            ],
        ],
        resize_keyboard=True,

    )

    answer = bot(question)

    update.message.reply_text(
        text=answer,
        reply_markup=reply_markup,
    )
    print(question)
    print(answer)
    print(stats)
    print()


def main():

    updater = Updater(
        config.Token,
        use_context=True
    )

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(CommandHandler("styp", styp_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
