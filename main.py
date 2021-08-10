import logging, sqlite3, datetime, io
from PIL import Image, ImageDraw, ImageFont
from config import Token

from telegram import Update, ForceReply, message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text('BCIE Bot, command: /bcie')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('command: /bcie')


def bcie_command(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        user = update.message.reply_to_message.from_user
    elif update.message.from_user:
        user = update.message.from_user
    else:
        return

    bg = Image.open('BCIE.png')
    # 字体大小
    font_size = 148
    # 文字内容
    if user is None:
        update.message.reply_text("请设置用户名.")
        return
    elif len(user['username']) == 0:
        update.message.reply_text("请设置用户名.")
        return
    text = user['username']
    uid = user['id']

    conn = sqlite3.connect('BCIE.db')
    cursor = conn.cursor()
    cursor.execute('select * from BCIE where UID=?', (uid,))
    values = cursor.fetchall()
    if len(values) == 1:
        time = values[0][2]
        bid = values[0][0]
        date = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        date = datetime.datetime.strftime(date, "%B %d, %Y")
    else:
        cursor.execute('insert into BCIE (UID) values (?)', (uid,))
        conn.commit()
        cursor.execute('select * from BCIE where UID=?', (uid,))
        values = cursor.fetchall()
        bid = values[0][0]
        today = datetime.date.today()
        date = datetime.datetime.strftime(today, "%B %d, %Y")

    cursor.close()
    conn.close()

    # 设置字体
    font = ImageFont.truetype('GT-Haptik-Regular.ttf', font_size)
    # 计算使用该字体占据的空间
    # 返回一个 tuple (width, height)
    # 分别代表这行字占据的宽和高
    text_width = font.getsize(text)
    draw = ImageDraw.Draw(bg)
    # 计算字体位置
    text_coordinate = int((bg.size[0]-text_width[0])/2), int((bg.size[1]-text_width[1])/3.6)
    # 写字
    draw.text(text_coordinate, text,(0,0,0), font=font)

    font = ImageFont.truetype('ITC-Franklin-Gothic-Book-Regular.otf', 58)
    bid_str = str(bid)
    while(len(bid_str) < 5):
        bid_str = '0' + bid_str
    logging.info(bid_str)
    draw.text((1550, 1665), bid_str,(0,0,0), font=font)
    draw.text((1550, 1725), date,(0,0,0), font=font)

    # 保存图片
    # bg.save('center_text.png')
    imgByteArr = io.BytesIO()
    bg.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    if update.message.chat['type'] == 'private':
        update.message.reply_document(imgByteArr)
    else:
        update.message.reply_photo(imgByteArr)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(Token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("bcie", bcie_command))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()