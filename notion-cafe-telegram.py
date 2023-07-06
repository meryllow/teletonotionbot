#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import requests
from dotenv import load_dotenv

load_dotenv()

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

NAME, LOCATION = range(2)
cafe_name = None
cafe_location = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    # reply_keyboard = [["start"]]

    await update.message.reply_text(
        "hi! got a new cafe to add? send it to me 🤍"
    )

    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the cafe name and asks for a location."""
    user = update.message.from_user
    global cafe_name
    cafe_name = update.message.text
    logger.info("Name of cafe: %s", update.message.text)
    await update.message.reply_text(
        "thank you! do you have the location of the cafe?",
        reply_markup=ReplyKeyboardRemove(),
    )

    return LOCATION

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and updates the notion database."""
    user = update.message.from_user
    global cafe_location
    cafe_location = update.message.text
    logger.info("Location of cafe: %s", cafe_location)

    url = "https://api.notion.com/v1/pages"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + os.getenv("NOTION_KEY"),
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }

    params = {
        "parent": {
            "database_id": os.getenv("NOTION_DATABASE_ID")
        },
        "properties": {
            "location": {
                "id": "pyuU",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": cafe_location
                        }
                    }
                ]
            },
            "name":
            {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": cafe_name
                        }
                }]
            }
        }
    }

    print(params)

    response = requests.post(url, headers=headers, json=params)

    
    await update.message.reply_text(
        "yay! added to the notion database"
    )
    logger.info("Request response: %s", response.text)


    return LOCATION

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END



def main():
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT, name)],
            LOCATION: [
                MessageHandler(filters.TEXT, location),
                # CommandHandler("skip", skip_location),
            ],
            # BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == '__main__':
    main()