# python bot.py --token 8943117629:AAH5NnarfA6MdSA182kngR43z5dqWZ5pbAU

import sys
import re
import argparse
import telebot
from telebot import types
import content

def parse_args():
    parser = argparse.ArgumentParser(description="Portfolio Telegram Bot")
    parser.add_argument(
        "--token", "-t",
        required=True,
        help="Telegram Bot API token (получить у @BotFather)"
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Включить отладочный вывод"
    )
    return parser.parse_args()


args = parse_args()
DEBUG = args.debug
BOT_TOKEN = args.token

if DEBUG:
    print(f"[DEBUG] Запуск бота. Debug mode: ON")
    print(f"[DEBUG] sys.argv: {sys.argv}")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

MAX_INPUT_LEN = 200
URL_PATTERN = re.compile(
    r"https?://[^\s]+"
)
GREETING_PATTERN = re.compile(
    r"\b(привет|хай|hello|hi|здравствуй|салам|ку|кук|пивет|дратути|здрасте|хайюхай|нихао|бь|бъ)\b",
    re.IGNORECASE
)


def is_valid_input(text: str) -> bool:
    return bool(text) and len(text.strip()) <= MAX_INPUT_LEN


def looks_like_greeting(text: str) -> bool:
    return bool(GREETING_PATTERN.search(text))


def build_works_text() -> str:
    lines = ["🏆 *Мои лучшие работы*\n"]
    for i, work in enumerate(content.BEST_WORKS, 1):
        lines.append(f"*{i}. {work['title']}*")
        lines.append(work["description"])
        if URL_PATTERN.match(work.get("link", "")):
            lines.append(f"🔗 [Посмотреть]({work['link']})")
        lines.append("")
    return "\n".join(lines)


def main_keyboard() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "👤 О себе",             "🎯 Цель",
        "🚀 Как я пришёл в IT",  "🧑‍🏫 Ментор",
        "📈 Прогресс",           "🎮 Хобби",
        "🏆 Мои работы",         "💻 GitHub",
    ]

    kb.add(*[types.KeyboardButton(b) for b in buttons])
    return kb


def inline_nav() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🏠 Главное меню", callback_data="menu"))
    return kb


@bot.message_handler(commands=["start", "menu"])
def cmd_start(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Команда /{message.text.split()[0][1:]} от {message.from_user.id} ({message.from_user.username})")
    name = message.from_user.first_name or "друг"
    text = (
        f"Привет, {name}! 👋\n\n"
        "Это моё портфолио в виде Telegram-бота.\n"
        "Выбери раздел кнопкой или командой:\n\n"
        "/about — О себе\n"
        "/goal — Моя цель\n"
        "/itcame — Как я пришёл в IT\n"
        "/mentor — Мой ментор\n"
        "/progress — Точка А → Точка Б\n"
        "/hobbies — Хобби и интересы\n"
        "/works — Мои лучшие работы\n"
        "/github — Ссылка на GitHub"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

@bot.message_handler(commands=["about"])
def cmd_about(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Команда /about от {message.from_user.id} ({message.from_user.username})")
    bot.send_message(message.chat.id, content.ABOUT, reply_markup=inline_nav())


@bot.message_handler(commands=["goal"])
def cmd_goal(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Команда /goal от {message.from_user.id} ({message.from_user.username})")
    bot.send_message(message.chat.id, content.GOAL, reply_markup=inline_nav())


@bot.message_handler(commands=["itcame"])
def cmd_itcame(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Команда /itcame от {message.from_user.id} ({message.from_user.username})")
    bot.send_message(message.chat.id, content.HOW_I_CAME, reply_markup=inline_nav())


@bot.message_handler(commands=["mentor"])
def cmd_mentor(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Команда /mentor от {message.from_user.id} ({message.from_user.username})")
    bot.send_message(message.chat.id, content.MENTOR, reply_markup=inline_nav())


@bot.message_handler(commands=["progress"])
def cmd_progress(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Команда /progress от {message.from_user.id} ({message.from_user.username})")
    bot.send_message(message.chat.id, content.PROGRESS, reply_markup=inline_nav())


@bot.message_handler(commands=["hobbies"])
def cmd_hobbies(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Команда /hobbies от {message.from_user.id} ({message.from_user.username})")
    bot.send_message(message.chat.id, content.HOBBIES, reply_markup=inline_nav())


@bot.message_handler(commands=["works"])
def cmd_works(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Команда /works от {message.from_user.id} ({message.from_user.username})")
    bot.send_message(message.chat.id, build_works_text(), reply_markup=inline_nav())


@bot.message_handler(commands=["github"])
def cmd_github(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Команда /github от {message.from_user.id} ({message.from_user.username})")
    text = f"💻 *GitHub*\n\nВесь код проекта здесь:\n{content.GITHUB_LINK}"
    bot.send_message(message.chat.id, text, reply_markup=inline_nav())


BUTTON_MAP = {
    "👤 О себе":             content.ABOUT,
    "🎯 Цель":               content.GOAL,
    "🚀 Как я пришёл в IT":  content.HOW_I_CAME,
    "🧑‍🏫 Ментор":             content.MENTOR,
    "📈 Прогресс":           content.PROGRESS,
    "🎮 Хобби":              content.HOBBIES,
}


@bot.message_handler(func=lambda m: m.text in BUTTON_MAP)
def handle_reply_buttons(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Нажата кнопка меню '{message.text}' от {message.from_user.id} ({message.from_user.username})")
    bot.send_message(
        message.chat.id,
        BUTTON_MAP[message.text],
        reply_markup=inline_nav()
    )


@bot.message_handler(func=lambda m: m.text == "🏆 Мои работы")
def handle_works_button(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Нажата кнопка меню '🏆 Мои работы' от {message.from_user.id} ({message.from_user.username})")
    bot.send_message(message.chat.id, build_works_text(), reply_markup=inline_nav())


@bot.message_handler(func=lambda m: m.text == "💻 GitHub")
def handle_github_button(message: types.Message):
    if DEBUG:
        print(f"[DEBUG] Нажата кнопка меню '💻 GitHub' от {message.from_user.id} ({message.from_user.username})")
    text = f"💻 *GitHub*\n\nВесь код проекта здесь:\n{content.GITHUB_LINK}"
    bot.send_message(message.chat.id, text, reply_markup=inline_nav())

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def callback_menu(call: types.CallbackQuery):
    if DEBUG:
        print(f"[DEBUG] Нажата инлайн-кнопка назад к меню от {call.from_user.id} ({call.from_user.username})")
    bot.answer_callback_query(call.id)
    cmd_start(call.message)

@bot.message_handler(func=lambda m: True)
def handle_text(message: types.Message):
    text = message.text or ""

    if not is_valid_input(text):
        if DEBUG:
            print(f"[DEBUG] Отклонено по длине от {message.from_user.id}: {len(text)} симв.")
        bot.send_message(
            message.chat.id,
            "⚠️ Слишком длинное сообщение. Попробуй покороче.",
            reply_markup=main_keyboard()
        )
        return

    if looks_like_greeting(text):
        if DEBUG:
            print(f"[DEBUG] Получено приветствие '{text}' от {message.from_user.id} ({message.from_user.username})")
        name = message.from_user.first_name or "друг"
        bot.send_message(
            message.chat.id,
            f"Привет, {name}! 😊 Выбери раздел кнопкой или напиши /start",
            reply_markup=main_keyboard()
        )
        return

    if DEBUG:
        print(f"[DEBUG] Неизвестное сообщение от {message.from_user.id} ({message.from_user.username}): {text!r}")

    bot.send_message(
        message.chat.id,
        "Не понял команду 🤔 Используй кнопки или /start для меню.",
        reply_markup=main_keyboard()
    )

    if DEBUG:
        print(f"[DEBUG] Неизвестное сообщение от {message.from_user.id}: {text!r}")

if __name__ == "__main__":
    print("✅ Бот запущен. Нажми Ctrl+C для остановки.")
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

# （づ￣3￣）づ╭❤️～