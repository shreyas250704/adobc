import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ApplicationBuilder, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import os
from aiohttp import web
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Scheme index (unchanged)
SCHEMES = {
    "1. शैक्षणिक योजना": {
        "1. आश्रमशाळा": {
            "लाभ घेणारा प्रवर्ग": "विमुक्त जाती, भटक्या जमाती व विशेष मागास प्रवर्ग",
            "योजना": [
                {"name": "विमुक्त जाती, भटक्या जमाती व विशेष मागास प्रवर्गासाठीच्या आश्रमशाळा", "details": "Placeholder: Details to be added"},
                {"name": "ऊसतोड कामगारांच्या मुला मुलींसाठी निवासी आश्रम शाळा", "details": "Placeholder: Details to be added"},
                {"name": "विद्यानिकेतन शाळा", "details": "Placeholder: Details to be added"}
            ]
        },
        "2. शिष्यवृत्ती": {
            "लाभ घेणारा प्रवर्ग": "इतर मागास वर्ग व VJNT व SBC",
            "योजना": [
                {"name": "मॅट्रिक पूर्व शिष्यवृत्ती (Pre Matric Scholarship)", "details": "Placeholder: Details to be added"},
                {"name": "मॅट्रिकोत्तर शिष्यवृत्ती (Post Matric Scholarship)", "details": "Placeholder: Details to be added"},
                {"name": "परदेशात उच्च शिक्षणासाठी शिष्यवृत्ती योजना", "details": "Placeholder: Details to be added"}
            ]
        },
        "3. वसतिगृहे/आधार योजना": {
            "लाभ घेणारा प्रवर्ग": "OBC, VJNT व SBC",
            "योजना": [
                {"name": "जिल्हानिहाय वसतिगृहे", "details": "Placeholder: Details to be added"},
                {"name": "ज्ञानज्योती सावित्रीबाई फुले आधार योजना", "details": "Placeholder: Details to be added"}
            ]
        }
    },
    "2. घरकुल/पायाभूत सुविधा बाबतच्या योजना": {
        "योजना": [
            {"name": "वसंतराव नाईक तांडा/वस्ती सुधार योजना", "details": "Placeholder: Details to be added"},
            {"name": "यशवंतराव चव्हाण मुक्त वसाहत योजना", "details": "Placeholder: Details to be added"},
            {"name": "मोदी आवाज घरकुल योजना", "details": "Placeholder: Details to be added"}
        ]
    },
    "3. भटक्या जमाती क प्रवर्ग (धनगर) समाजासाठी राबविण्यात येणाऱ्या विविध योजना": {
        "योजना": [
            {"name": "इंग्रजी माध्यमाच्या निवासी शाळेत प्रवेश", "details": "Placeholder: Details to be added"},
            {"name": "महसुली विभागाच्या मुख्यालयाच्या ठिकाणी वसतीगृह", "details": "Placeholder: Details to be added"},
            {"name": "पंडित दीनदयाल उपाध्याय स्वयंम योजना", "details": "Placeholder: Details to be added"},
            {"name": "स्टॅन्ड अप योजनेत मार्जिन मनी", "details": "Placeholder: Details to be added"},
            {"name": "बेघर कुटुंबीयांना घरकुले", "details": "Placeholder: Details to be added"},
            {"name": "न्यूक्लियस बजेट योजना", "details": "Placeholder: Details to be added"},
            {"name": "सहकारी सूत गिरण्यांना भाग भांडवल", "details": "Placeholder: Details to be added"},
            {"name": "UPSC/MPSC पूर्व परीक्षेसाठी निवासी प्रशिक्षण", "details": "Placeholder: Details to be added"},
            {"name": "सैनिक व पोलीस भरतीसाठी मूलभूत प्रशिक्षण", "details": "Placeholder: Details to be added"},
            {"name": "स्पर्धा परीक्षेसाठी परीक्षा शुल्कात सवलत", "details": "Placeholder: Details to be added"},
            {"name": "कुकुट पालन संकल्पनेत अर्थसहाय्य", "details": "Placeholder: Details to be added"},
            {"name": "मेंढीपालनासाठी जागा खरेदी अनुदान", "details": "Placeholder: Details to be added"},
            {"name": "पावसाळ्यात चराईसाठी अनुदान", "details": "Placeholder: Details to be added"}
        ]
    },
    "4. सामाजिक योजना": {
        "योजना": [
            {"name": "कन्यादान योजना", "details": "Placeholder: Details to be added"},
            {"name": "महात्मा बसवेश्वर सामाजिक समता शिवा पुरस्कार", "details": "Placeholder: Details to be added"},
            {"name": "स्व. वसंतराव नाईक गुणवत्ता पुरस्कार", "details": "Placeholder: Details to be added"}
        ]
    },
    "5. कौशल्य विकास व अर्थसहाय्याच्या योजना": {
        "संस्था": [
            {"name": "महात्मा ज्योतिबा फुले संशोधन व प्रशिक्षण संस्था (महाज्योती), नागपूर", "details": "Placeholder: Details to be added"},
            {"name": "महाराष्ट्र संशोधन उन्नती व प्रशिक्षण प्रबोधिनी (अमृत)", "details": "Placeholder: Details to be added"}
        ],
        "महामंडळे": [
            {
                "name": "महाराष्ट्र राज्य इतर मागासवर्गीय वित्त आणि विकास महामंडळ (मर्यादित)",
                "उपकंपन्या": [
                    {"name": "शामराव पेजे आर्थिक विकास महामंडळ", "details": "Placeholder: Details to be added"},
                    {"name": "जगतज्योती महात्मा बसवेश्वर आर्थिक विकास महामंडळ", "details": "Placeholder: Details to be added"},
                    {"name": "संत काशीबा गुरव युवा आर्थिक विकास महामंडळ", "details": "Placeholder: Details to be added"},
                    {"name": "संत सेनाजी महाराज केश शिल्पी महामंडळ", "details": "Placeholder: Details to be added"}
                ]
            },
            {
                "name": "वसंतराव नाईक विमुक्त जाती व भटक्या जमाती विकास महामंडळ (मर्यादित)",
                "उपकंपन्या": [
                    {"name": "पैलवान कै. मारुती चव्हाण वडार आर्थिक विकास महामंडळ", "details": "Placeholder: Details to be added"},
                    {"name": "राजे उमाजी नाईक आर्थिक विकास महामंडळ", "details": "Placeholder: Details to be added"}
                ]
            }
        ]
    }
}

# Start command handler
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("शैक्षणिक योजना", callback_data="1. शैक्षणिक योजना")],
        [InlineKeyboardButton("घरकुल/पायाभूत सुविधा", callback_data="2. घरकुल/पायाभूत सुविधा बाबतच्या योजना")],
        [InlineKeyboardButton("धनगर समाजाच्या योजना", callback_data="3. भटक्या जमाती क प्रवर्ग (धनगर) समाजासाठी राबविण्यात येणाऱ्या विविध योजना")],
        [InlineKeyboardButton("सामाजिक योजना", callback_data="4. सामाजिक योजना")],
        [InlineKeyboardButton("कौशल्य विकास व अर्थसहाय्य", callback_data="5. कौशल्य विकास व अर्थसहाय्याच्या योजना")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('खालीलपैकी एक योजना निवडा:', reply_markup=reply_markup)
    logger.info(f"User {update.effective_user.id} started the bot")

# Callback query handler for menu navigation
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    # Handle main category selection
    if query.data in SCHEMES:
        category = SCHEMES[query.data]
        keyboard = []
        for sub_category in category:
            if sub_category != "लाभ घेणारा प्रवर्ग":
                keyboard.append([InlineKeyboardButton(sub_category, callback_data=f"{query.data}:{sub_category}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"{query.data} अंतर्गत योजना:", reply_markup=reply_markup)

    # Handle sub-category selection
    else:
        parts = query.data.split(":", 1)
        if len(parts) == 2:
            category, sub_category = parts
            sub_cat_data = SCHEMES[category].get(sub_category, {}).get("योजना", SCHEMES[category].get(sub_category, []))
            response = f"{sub_category}:\n\n"
            keyboard = []
            for scheme in sub_cat_data:
                if isinstance(scheme, dict):
                    response += f"- {scheme['name']}\n"
                    keyboard.append([InlineKeyboardButton(scheme['name'], callback_data=f"{query.data}:{scheme['name']}")])
                else:
                    response += f"- {scheme['name']}\n"
                    keyboard.append([InlineKeyboardButton(scheme['name'], callback_data=f"{query.data}:{scheme['name']}")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(response, reply_markup=reply_markup)

    # Handle individual scheme selection
    if len(query.data.split(":")) == 3:
        category, sub_category, scheme_name = query.data.split(":", 2)
        scheme_data = next((s for s in SCHEMES[category][sub_category]["योजना"] if s["name"] == scheme_name), None)
        if scheme_data:
            await query.message.reply_text(f"{scheme_name}:\n{scheme_data['details']}")

# Error handler
async def error_handler(update, context):
    logger.error(f"Error occurred: {context.error}")
    if update.message:
        await update.message.reply_text("काहीतरी चुकले. कृपया पुन्हा प्रयत्न करा.")

# Webhook handler
async def webhook(request):
    app = request.app['bot']
    update = Update.de_json(await request.json(), app.bot)
    await app.process_update(update)
    return web.Response()

def main():
    # Create the Application with the bot's token
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_error_handler(error_handler)

    # Initialize the application
    app.initialize()

    # Create aiohttp server
    web_app = web.Application()
    web_app['bot'] = app
    web_app.router.add_post(f'/{TOKEN}', webhook)

    # Start the webhook
    port = int(os.getenv('PORT', 8000))  # Render provides PORT
    logger.info(f"Starting webhook on port {port}")
    web.run_app(web_app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
