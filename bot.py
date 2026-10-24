import os
import random
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv('Telegram_bot_taken')

app = ApplicationBuilder().token(TOKEN).build()

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'time':
        now = datetime.now().strftime('%d.%m.%Y в %H:%M:%S')
        await query.edit_message_text(f'Текущее время: {now}')
    elif query.data == 'fact':
        facts = ['Deadlock''(https://store.steampowered.com/app/1422450/Deadlock/)', 
        'The outlast trials''(https://store.steampowered.com/app/1304930/The_Outlast_Trials?snr=1_7_15__13_1)', 
        'Arc raiders''(https://store.steampowered.com/app/1808500/ARC_Raiders/)']
        await query.edit_message_text(random.choice(facts))

async def roll_dice(update, context):
    result = random.randint(1, 6)
    await update.message.reply_text(f"На кубике выпало: *{result}*", parse_mode='Markdown')

async def start(update, context):
    await update.message.reply_text(
        'Привет! Я твой телеграм-бот по играм. Как я могу помочь тебе?\n'
        'Используй /menu для открытия меню.\n'
        'Используй /help для получения списка команд.'
    )

async def help_command(update, context):
    await update.message.reply_text(
        'Команды:\n'
        '/start - начать\n'
        '/help - помощь\n'
        '/menu - открыть меню\n'
        '/roll - бросить игровой кубик (1-6)\n'
    )

async def menu(update, context):
    button_time = InlineKeyboardButton('Дата и время', callback_data='time')
    button_game = InlineKeyboardButton('Рандомная игра', callback_data='fact')
    button_site = InlineKeyboardButton('Открыть сайт youtube', url='https://youtube.com')
    button_channel = InlineKeyboardButton('Телеграм "Steam community"', url='https://t.me')
    
    keyboard = [
        [button_time, button_game],
        [button_site, button_channel]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

async def send_photo(update, context):
    path = 'images/34.jpg'
    with open(path, 'rb') as f:
        await update.message.reply_photo(f, caption='Вот ваше фото!')


async def send_video(update, context):
    url = 'https://youtube.com/watch?v=c5dIDkZxzDs'
    await update.message.reply_video(url, caption='Прохождения майнкрафта')

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(CommandHandler('menu', menu))  
app.add_handler(CommandHandler('send_photo', send_photo))
app.add_handler(CommandHandler('video', send_video))
app.add_handler(CommandHandler('roll', roll_dice))
app.add_handler(CallbackQueryHandler(button_callback))

if __name__ == '__main__':
    app.run_polling()




