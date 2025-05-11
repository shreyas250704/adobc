import telegram
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ApplicationBuilder
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 8000))

# Scheme index
SCHEMES = {
    "cat1": {
        "name": "शैक्षणिक योजना",
        "subcategories": {
            "subcat1": {
                "name": "आश्रमशाळा",
                "लाभ घेणारा प्रवर्ग": "विमुक्त जाती, भटक्या जमाती व विशेष मागास प्रवर्ग",
                "योजना": [
                    {"name": "विमुक्त जाती, भटक्या जमाती व विशेष मागास प्रवर्गासाठीच्या आश्रमशाळा", "details": "Placeholder: Details to be added"},
                    {"name": "ऊसतोड कामगारांच्या मुला मुलींसाठी निवासी आश्रम शाळा", "details": "Placeholder: Details to be added"},
                    {"name": "विद्यानिकेतन शाळा", "details": "Placeholder: Details to be added"}
                ]
            },
            "subcat2": {
                "name": "शिष्यवृत्ती",
                "लाभ घेणारा प्रवर्ग": "इतर मागास वर्ग व VJNT व SBC",
                "योजना": [
                    {"name": "मॅट्रिक पूर्व शिष्यवृत्ती (Pre Matric Scholarship)", "details": "Placeholder: Details to be added"},
                    {"name": "मॅट्रिकोत्तर शिष्यवृत्ती (Post Matric Scholarship)", "details": "Placeholder: Details to be added"},
                    {"name": "परदेशात उच्च शिक्षणासाठी शिष्यवृत्ती योजना", "details": "Placeholder: Details to be added"}
                ]
            },
            "subcat3": {
                "name": "वसतिगृहे/आधार योजना",
                "लाभ घेणारा प्रवर्ग": "OBC, VJNT व SBC",
                "योजना": [
                    {"name": "जिल्हानिहाय वसतिगृहे", "details": "Placeholder: Details to be added"},
                    {"name": "ज्ञानज्योती सावित्रीबाई फुले आधार योजना", "details": "Placeholder: Details to be added"}
                ]
            }
        }
    },
    "cat2": {
        "name": "घरकुल/पायाभूत सुविधा बाबतच्या योजना",
        "subcategories": {
            "schemes": {
                "name": "योजना",
                "योजना": [
                    {"name": "वसंतराव नाईक तांडा/वस्ती सुधार योजना", "details": "Placeholder: Details to be added"},
                    {"name": "यशवंतराव चव्हाण मुक्त वसाहत योजना", "details": "Placeholder: Details to be added"},
                    {"name": "मोदी आवाज घरकुल योजना", "details": "Placeholder: Details to be added"}
                ]
            }
        }
    },
    "cat3": {
        "name": "भटक्या जमाती क प्रवर्ग (धनगर) समाजासाठी राबविण्यात येणाऱ्या विविध योजना",
        "subcategories": {
            "schemes": {
                "name": "योजना",
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
            }
        }
    },
    "cat4": {
        "name": "सामाजिक योजना",
        "subcategories": {
            "schemes": {
                "name": "योजना",
                "योजना": [
                    {"name": "कन्यादान योजना", "details": "Placeholder: Details to be added"},
                    {"name": "महात्मा बसवेश्वर सामाजिक समता शिवा पुरस्कार", "details": "Placeholder: Details to be added"},
                    {"name": "स्व. वसंतराव नाईक गुणवत्ता पुरस्कार", "details": "Placeholder: Details to be added"}
                ]
            }
        }
    },
    "cat5": {
        "name": "कौशल्य विकास व अर्थसहाय्याच्या योजना",
        "subcategories": {
            "institutions": {
                "name": "संस्था",
                "items": [
                    {"name": "महात्मा ज्योतिबा फुले संशोधन व प्रशिक्षण संस्था (महाज्योती), नागपूर", "details": "Placeholder: Details to be added"},
                    {"name": "महाराष्ट्र संशोधन उन्नती व प्रशिक्षण प्रबोधिनी (अमृत)", "details": "Placeholder: Details to be added"}
                ]
            },
            "corporations": {
                "name": "महामंडळे",
                "items": [
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
    }
}

# Start command handler
async def start(update: Update, context):
    logger.info("Received /start command")
    if not update.message:
        logger.error("Update has no message object")
        raise ValueError("Update has no message object")
    keyboard = [
        [InlineKeyboardButton("📚 शैक्षणिक योजना", callback_data="cat1")],
        [InlineKeyboardButton("🏡 घरकुल/पायाभूत सुविधा", callback_data="cat2")],
        [InlineKeyboardButton("👥 धनगर समाजाच्या योजना", callback_data="cat3")],
        [InlineKeyboardButton("🤝 सामाजिक योजना", callback_data="cat4")],
        [InlineKeyboardButton("💼 कौशल्य विकास व अर्थसहाय्य", callback_data="cat5")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    logger.info("Sending reply with menu")
    await update.message.reply_text(
        'खालीलपैकी एक योजना निवडा:\n(For a white background, switch to Telegram\'s light mode in Settings > Appearance)',
        reply_markup=reply_markup
    )
    logger.info(f"User {update.effective_user.id} started the bot")

# Callback query handler for menu navigation
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    logger.info(f"Received callback query with data: {query.data}")

    # Handle main category selection
    if query.data in SCHEMES:
        category = SCHEMES[query.data]
        category_name = category["name"]
        subcategories = category.get("subcategories", {})
        keyboard = []
        for subcat_id, subcat in subcategories.items():
            keyboard.append([InlineKeyboardButton(subcat["name"], callback_data=f"{query.data}:{subcat_id}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"{category_name} अंतर्गत योजना:", reply_markup=reply_markup)

    # Handle subcategory selection
    else:
        parts = query.data.split(":", 1)
        if len(parts) == 2:
            category_id, subcat_id = parts
            category = SCHEMES[category_id]
            subcat_data = category["subcategories"][subcat_id]
            subcat_name = subcat_data["name"]
            response = f"{subcat_name}:\n\n"
            keyboard = []

            if subcat_id in ["schemes", "institutions"]:
                items = subcat_data.get("योजना", subcat_data.get("items", []))
                for item in items:
                    response += f"- {item['name']}\n"
                    keyboard.append([InlineKeyboardButton(item['name'], callback_data=f"{query.data}:item:{item['name']}")])
            elif subcat_id == "corporations":
                items = subcat_data.get("items", [])
                for item in items:
                    response += f"- {item['name']}\n"
                    keyboard.append([InlineKeyboardButton(item['name'], callback_data=f"{query.data}:corp:{item['name']}")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(response, reply_markup=reply_markup)

    # Handle individual item selection (schemes, institutions, corporations)
    if len(query.data.split(":")) == 4:
        category_id, subcat_id, item_type, item_name = query.data.split(":", 3)
        category = SCHEMES[category_id]
        subcat = category["subcategories"][subcat_id]
        
        if item_type == "item":
            items = subcat.get("योजना", subcat.get("items", []))
            item_data = next((s for s in items if s["name"] == item_name), None)
            if item_data:
                await query.message.reply_text(f"{item_name}:\n{item_data['details']}")
        elif item_type == "corp":
            items = subcat.get("items", [])
            corp_data = next((c for c in items if c["name"] == item_name), None)
            if corp_data and "उपकंपन्या" in corp_data:
                response = f"{item_name}:\n\nउपकंपन्या:\n"
                keyboard = []
                for subcorp in corp_data["उपकंपन्या"]:
                    response += f"- {subcorp['name']}\n"
                    keyboard.append([InlineKeyboardButton(subcorp['name'], callback_data=f"{query.data}:subcorp:{subcorp['name']}")])
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(response, reply_markup=reply_markup)

    # Handle subcorporation selection
    if len(query.data.split(":")) == 6:
        category_id, subcat_id, _, corp_name, _, subcorp_name = query.data.split(":", 5)
        category = SCHEMES[category_id]
        subcat = category["subcategories"][subcat_id]
        corp_data = next((c for c in subcat["items"] if c["name"] == corp_name), None)
        if corp_data:
            subcorp_data = next((sc for sc in corp_data["उपकंपन्या"] if sc["name"] == subcorp_name), None)
            if subcorp_data:
                await query.message.reply_text(f"{subcorp_name}:\n{subcorp_data['details']}")

# Error handler
async def error_handler(update: Update, context):
    logger.error(f"Update {update} caused error: {context.error}")
    if update and update.message:
        await update.message.reply_text("काहीतरी चुकले. कृपया पुन्हा प्रयत्न करा.")

def main():
    # Validate environment variables
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set in environment variables")
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    if not WEBHOOK_URL:
        logger.error("WEBHOOK_URL is not set in environment variables")
        raise ValueError("WEBHOOK_URL is not set")

    # Create the Application with the bot's token
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_error_handler(error_handler)

    # Start the webhook
    logger.info(f"Starting webhook on port {PORT} with URL {WEBHOOK_URL}")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}{TOKEN}"
    )

    logger.info("Bot is running...")

if __name__ == '__main__':
    main()
