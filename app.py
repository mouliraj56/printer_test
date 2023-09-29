import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
import PyPDF2  # Import the PyPDF2 library
import io

# Your provided BOT_TOKEN
BOT_TOKEN = '6573536783:AAFxDVflga8vYXdqhJG-14zjhdmvOrtbQuQ'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize the updater and dispatcher
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the start command handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the PDF Bot! Send me a PDF file, and I will send it back to you. "
                              "You can also say hello, and I will respond with a greeting.")

# Define a custom filter to check if a message contains a PDF file
def is_pdf(update: Update) -> bool:
    return update.message.document and update.message.document.file_name.endswith('.pdf')

# Define a function to handle greetings and other user messages
def handle_user_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()
    if user_message == 'hello':
        update.message.reply_text("Hello! How can I assist you today?")
    elif 'thank you' in user_message:
        update.message.reply_text("You're welcome!")
    elif 'how are you' in user_message:
        update.message.reply_text("I'm just a bot, but I'm here to help you!")
    else:
        update.message.reply_text("I can handle PDF files. Please send me a PDF file.")

# Define the echo handler to handle PDF files
def echo(update: Update, context: CallbackContext):
    # Get the PDF file
    file = context.bot.get_file(update.message.document.file_id)
    # Send the same file back to the user
    context.bot.send_document(chat_id=update.message.chat_id, document=file.file_id)
    
    # Get the PDF file's name
    pdf_name = update.message.document.file_name
    
    # Download the PDF file as a bytearray
    pdf_file = file.download_as_bytearray()
    
    # Use PyPDF2's PdfReader to calculate the number of pages
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
    num_pages = len(pdf_reader.pages)  # Use len to get the number of pages

    # Send a message with PDF details
    response_message = f"Here is the PDF file: {pdf_name}\nNumber of pages: {num_pages}"
    context.bot.send_message(chat_id=update.message.chat_id, text=response_message)

# Add the command handler and message handlers to the dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_user_message))  # Handles greetings and more
dispatcher.add_handler(MessageHandler(Filters.document & Filters.update, echo))  # Handles PDFs

# Start the bot
updater.start_polling()
updater.idle()
