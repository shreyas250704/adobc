import telegram
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ApplicationBuilder, filters
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
                "items": [
                    {"name": "विमुक्त जाती, भटक्या जमाती व विशेष मागास प्रवर्गासाठीच्या आश्रमशाळा", "details": "विमुक्त जाती, भटक्या जमाती आणि विशेष मागास प्रवर्गातील विद्यार्थ्यांसाठी आश्रमशाळा उपलब्ध करून देणे."},
                    {"name": "ऊसतोड कामगारांच्या मुला मुलींसाठी निवासी आश्रम शाळा", "details": "ऊसतोड कामगारांच्या मुला-मुलींसाठी निवासी आश्रमशाळा सुरू करणे, ज्यामुळे त्यांना शिक्षणाची संधी मिळेल."},
                    {"name": "विद्यानिकेतन शाळा", "details": "विमुक्त जाती आणि भटक्या जमातींसाठी विद्यानिकेतन शाळा स्थापन करणे."}
                ]
            },
            "subcat2": {
                "name": "शिष्यवृत्ती",
                "लाभ घेणारा प्रवर्ग": "इतर मागास वर्ग व VJNT व SBC",
                "items": [
                    {"name": "मॅट्रिक पूर्व शिष्यवृत्ती (Pre Matric Scholarship)", "details": "इतर मागास वर्ग, VJNT आणि SBC प्रवर्गातील विद्यार्थ्यांना मॅट्रिकपूर्व शिक्षणासाठी शिष्यवृत्ती."},
                    {"name": "मॅट्रिकोत्तर शिष्यवृत्ती (Post Matric Scholarship)", "details": "मॅट्रिकोत्तर शिक्षण घेणाऱ्या विद्यार्थ्यांसाठी शिष्यवृत्ती योजना."},
                    {"name": "परदेशात उच्च शिक्षणासाठी शिष्यवृत्ती योजना", "details": "परदेशात उच्च शिक्षण घेण्यासाठी आर्थिक सहाय्य देणारी शिष्यवृत्ती योजना."}
                ]
            },
            "subcat3": {
                "name": "वसतिगृहे/आधार योजना",
                "लाभ घेणारा प्रवर्ग": "OBC, VJNT व SBC",
                "items": [
                    {"name": "राज्यातील इतर मागास प्रवर्ग, विमुक्त जाती, भटक्या जमाती व विशेष मागास प्रवर्ग या प्रवर्गातील विद्यार्थ्यांसाठी जिल्हानिहाय वसतिगृहे सुरू करणेबाबत", "details": "OBC, VJNT आणि SBC प्रवर्गातील विद्यार्थ्यांसाठी जिल्हानिहाय वसतिगृहे सुरू करणे."},
                    {"name": "ज्ञानज्योती सावित्रीबाई फुले आधार योजना", "details": "विद्यार्थ्यांना शिक्षणासाठी आर्थिक आधार देणारी योजना."}
                ]
            }
        }
    },
    "cat2": {
        "name": "घरकुल/पायाभूत सुविधा बाबतच्या योजना",
        "subcategories": {
            "schemes": {
                "name": "योजना",
                "items": [
                    {"name": "वसंतराव नाईक तांडा/वस्ती सुधार योजना", "details": "वसंतराव नाईक तांडा आणि वस्ती सुधारणेसाठी योजना."},
                    {"name": "विमुक्त जाती भटक्या जमाती या घटकांसह यशवंतराव चव्हाण मुक्त वसाहत योजना", "details": "विमुक्त जाती आणि भटक्या जमातींसाठी यशवंतराव चव्हाण मुक्त वसाहत योजना."},
                    {"name": "मोदी आवाज घरकुल योजना", "details": "गरजू कुटुंबांना घरकुले बांधून देणारी योजना."}
                ]
            }
        }
    },
    "cat3": {
        "name": "भटक्या जमाती क प्रवर्ग (धनगर) समाजासाठी राबविण्यात येणाऱ्या विविध योजना",
        "subcategories": {
            "schemes": {
                "name": "योजना",
                "items": [
                    {"name": "धनगर समाजाच्या विद्यार्थ्यांना शहरातील इंग्रजी माध्यमाच्या नामांकित निवासी शाळेत प्रवेश मिळवून देणे", "details": "धनगर समाजाच्या विद्यार्थ्यांना इंग्रजी माध्यमाच्या निवासी शाळेत प्रवेश मिळवून देणे."},
                    {"name": "भटक्या जमाती क (धनगर) प्रवर्गातील मॅट्रिकोत्तर शिक्षण घेणाऱ्या गुणवत्ताधारक विद्यार्थ्यांसाठी राज्याच्या महसुली विभागाच्या मुख्यालयाच्या ठिकाणी वसतीगृह निर्माण करणे", "details": "धनगर प्रवर्गातील विद्यार्थ्यांसाठी वसतीगृह निर्माण करणे."},
                    {"name": "धनगर समाजाच्या विद्यार्थ्यांसाठी पंडित दीनदयाल उपाध्याय स्वयंम योजना", "details": "धनगर समाजाच्या विद्यार्थ्यांसाठी स्वयंम योजना."},
                    {"name": "केंद्र शासनाच्या स्टॅन्ड अप योजनेत भटक्या जमाती क प्रवर्गातील धनगर समाजाच्या महिलांना सहाय्यक करण्यासाठी मार्जिन मनी उपलब्ध करून देणे", "details": "धनगर समाजाच्या महिलांसाठी स्टॅन्ड अप योजनेत मार्जिन मनी."},
                    {"name": "भटक्या जमाती क प्रवर्गातील धनगर समाजाच्या बेघर कुटुंबीयांना घरकुले बांधून देणे", "details": "धनगर समाजाच्या बेघर कुटुंबांना घरकुले बांधून देणे."},
                    {"name": "भटक्या जमाती क या प्रवर्गातील आवश्यक असलेल्या परंतु अर्थसंकल्पीत निधी उपलब्ध नसलेल्या योजना/कार्यक्रम राबविण्यासाठी न्यूक्लियस बजेट योजना", "details": "आवश्यक योजनांसाठी न्यूक्लियस बजेट योजना."},
                    {"name": "राज्यातील भटक्या जमाती क प्रवर्गातील सभासदांच्या सहकारी सूत गिरण्यांना भाग भांडवल मंजूर करणे", "details": "सहकारी सूत गिरण्यांना भाग भांडवल मंजूर करणे."},
                    {"name": "धनगर समाजातील विद्यार्थ्यांसाठी संघ लोकसेवा आयोग/महाराष्ट्र लोकसेवा आयोग यांच्या पूर्व परीक्षेसाठी निवासी प्रशिक्षण देणे", "details": "UPSC/MPSC पूर्व परीक्षेसाठी प्रशिक्षण."},
                    {"name": "धनगर समाजातील बेरोजगार युवक युवतीस लष्करातील सैनिक भरती व राज्यातील पोलीस भरतीसाठी आवश्यक ते मूलभूत प्रशिक्षण देणे", "details": "सैनिक आणि पोलीस भरतीसाठी प्रशिक्षण."},
                    {"name": "भटक्या जमाती क मधील धनगर समाजातील बेरोजगार युवक युवतींना स्पर्धा परीक्षेसाठी परीक्षा शुल्कात आर्थिक सवलती लागू करणे बाबत", "details": "स्पर्धा परीक्षा शुल्कात सवलत."},
                    {"name": "धनगर समाजातील लोकांना ग्रामीण परिसरातील कुकुट पालन संकल्पने अंतर्गत धनगर समाजातील कुटुंबीयांना ७५ टक्के अनुदानावर चार आठवडे वयाच्या सुधारित देशी प्रजातीच्या १०० कुकुट पक्षांच्या खरेदी व संगोपनासाठी अर्थसहाय्य", "details": "कुकुट पालनासाठी ७५ टक्के अनुदान."},
                    {"name": "भटक्या जमाती क या मागास प्रवर्गातील धनगर व तत्सम समाजातील लाभार्थ्यांना राज्यस्तरीय योजनेअंतर्गत भूमिहीन मेंढपाळ कुटुंब साठी अर्धबंदिस्त, बंदिस्त मेंढीपालन करण्याकरिता जागा खरेदीसाठी अनुदान स्वरूपात एकवेळचे एक रकमी अर्थसहाय देणे", "details": "मेंढीपालनासाठी जागा खरेदी अनुदान."},
                    {"name": "भटक्या जमाती क प्रवर्गातील धनगर समाजातील मेंढपाळ कुटुंबांना पावसाळ्यात चराई करण्याकरिता जून ते सप्टेंबर या चार महिन्यांच्या कालावधीसाठी अनुदान देणे", "details": "पावसाळ्यात चराईसाठी अनुदान."}
                ]
            }
        }
    },
    "cat4": {
        "name": "सामाजिक योजना",
        "subcategories": {
            "schemes": {
                "name": "योजना",
                "items": [
                    {"name": "सामूहिक विवाह सोहळ्यामध्ये भाग घेऊन विवाह करण्याच्या विजाभज, इमाव व विमाप्र दंपत्यासाठी कन्यादान योजना", "details": "सामूहिक विवाह सोहळ्यासाठी कन्यादान योजना."},
                    {"name": "महात्मा बसवेश्वर सामाजिक समता शिवा पुरस्कार योजना", "details": "सामाजिक समतेसाठी पुरस्कार योजना."},
                    {"name": "स्व. वसंतराव नाईक गुणवत्ता पुरस्कार", "details": "गुणवत्तेसाठी वसंतराव नाईक पुरस्कार."}
                ]
            }
        }
    },
    "cat5": {
        "name": "कौशल्य विकास व अर्थसाहाय्याच्या योजना",
        "subcategories": {
            "institutions": {
                "name": "संस्था",
                "items": [
                    {"name": "महात्मा ज्योतिबा फुले संशोधन व प्रशिक्षण संस्था (महाज्योती) नागपूर", "details": "संशोधन आणि प्रशिक्षणासाठी महाज्योती संस्था, नागपूर."},
                    {"name": "महाराष्ट्र संशोधन उन्नती व प्रशिक्षण प्रबोधिनी (अमृत)", "details": "संशोधन आणि प्रशिक्षणासाठी अमृत प्रबोधिनी."}
                ]
            },
            "corporations": {
                "name": "महामंडळे",
                "items": [
                    {
                        "name": "महाराष्ट्र राज्य इतर मागासवर्गीय वित्त आणि विकास महामंडळ (मर्यादित)",
                        "subitems": [
                            {"name": "शामराव पेजे आर्थिक विकास महामंडळ (उपकंपनी)", "details": "आर्थिक विकासासाठी शामराव पेजे महामंडळ."},
                            {"name": "जगतज्योती महात्मा बसवेश्वर आर्थिक विकास महामंडळ (उपकंपनी)", "details": "आर्थिक विकासासाठी महात्मा बसवेश्वर महामंडळ."},
                            {"name": "संत काशीबा गुरव युवा आर्थिक विकास महामंडळ (उपकंपनी)", "details": "युवा आर्थिक विकासासाठी संत काशीबा गुरव महामंडळ."},
                            {"name": "संत सेनाजी महाराज केश शिल्पी महामंडळ (उपकंपनी)", "details": "केश शिल्पींसाठी संत सेनाजी महाराज महामंडळ."}
                        ]
                    },
                    {
                        "name": "वसंतराव नाईक विमुक्त जाती व भटक्या जमाती विकास महामंडळ (मर्यादित)",
                        "subitems": [
                            {"name": "पैलवान कै. मारुती चव्हाण वडार आर्थिक विकास महामंडळ (उपकंपनी)", "details": "वडार समाजासाठी आर्थिक विकास महामंडळ."},
                            {"name": "राजे उमाजी नाईक आर्थिक विकास महामंडळ या (उपकंपनी)", "details": "आर्थिक विकासासाठी राजे उमाजी नाईक महामंडळ."}
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
        [InlineKeyboardButton("1. शैक्षणिक योजना", callback_data="cat1")],
        [InlineKeyboardButton("2. घरकुल/पायाभूत सुविधा बाबतच्या योजना", callback_data="cat2")],
        [InlineKeyboardButton("3. भटक्या जमाती क प्रवर्ग (धनगर) समाजासाठी राबविण्यात येणाऱ्या विविध योजना", callback_data="cat3")],
        [InlineKeyboardButton("4. सामाजिक योजना", callback_data="cat4")],
        [InlineKeyboardButton("5. कौशल्य विकास व अर्थसाहाय्याच्या योजना", callback_data="cat5")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    logger.info("Sending reply with menu")
    await update.message.reply_text('विभागा अंतर्गत राबविल्या जाणाऱ्या योजना:\n\nखालीलपैकी एक योजना निवडा:', reply_markup=reply_markup)
    logger.info(f"User {update.effective_user.id} started the bot")

# Handler for "Hi" message
async def handle_hi(update: Update, context):
    if update.message.text.lower() == "hi":
        await start(update, context)

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
        keyboard.append([InlineKeyboardButton("⬅️ मागे", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"{category_name} अंतर्गत:", reply_markup=reply_markup)

    # Handle back to main menu
    elif query.data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("1. शैक्षणिक योजना", callback_data="cat1")],
            [InlineKeyboardButton("2. घरकुल/पायाभूत सुविधा बाबतच्या योजना", callback_data="cat2")],
            [InlineKeyboardButton("3. भटक्या जमाती क प्रवर्ग (धनगर) समाजासाठी राबविण्यात येणाऱ्या विविध योजना", callback_data="cat3")],
            [InlineKeyboardButton("4. सामाजिक योजना", callback_data="cat4")],
            [InlineKeyboardButton("5. कौशल्य विकास व अर्थसाहाय्याच्या योजना", callback_data="cat5")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text('विभागा अंतर्गत राबविल्या जाणाऱ्या योजना:\n\nखालीलपैकी एक योजना निवडा:', reply_markup=reply_markup)

    # Handle subcategory selection
    else:
        parts = query.data.split(":", 2)
        if len(parts) == 2:
            category_id, subcat_id = parts
            category = SCHEMES[category_id]
            subcat_data = category["subcategories"][subcat_id]
            subcat_name = subcat_data["name"]
            response = f"{subcat_name}:\n\n"
            if "लाभ घेणारा प्रवर्ग" in subcat_data:
                response += f"(लाभ घेणारा प्रवर्ग = {subcat_data['लाभ घेणारा प्रवर्ग']})\n\n"
            keyboard = []

            if subcat_id in ["schemes", "institutions"]:
                items = subcat_data.get("items", [])
                for item in items:
                    response += f"- {item['name']}\n"
                    keyboard.append([InlineKeyboardButton(item['name'], callback_data=f"{query.data}:item:{item['name']}")])
            elif subcat_id == "corporations":
                items = subcat_data.get("items", [])
                for item in items:
                    response += f"- {item['name']}\n"
                    keyboard.append([InlineKeyboardButton(item['name'], callback_data=f"{query.data}:corp:{item['name']}")])

            keyboard.append([InlineKeyboardButton("⬅️ मागे", callback_data=f"{category_id}")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(response, reply_markup=reply_markup)

    # Handle individual item selection (schemes, institutions, corporations)
    if len(query.data.split(":")) == 4:
        category_id, subcat_id, item_type, item_name = query.data.split(":", 3)
        category = SCHEMES[category_id]
        subcat = category["subcategories"][subcat_id]
        
        if item_type == "item":
            items = subcat.get("items", [])
            item_data = next((s for s in items if s["name"] == item_name), None)
            if item_data:
                keyboard = [[InlineKeyboardButton("⬅️ मागे", callback_data=f"{category_id}:{subcat_id}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(f"{item_name}:\n{item_data['details']}", reply_markup=reply_markup)
        elif item_type == "corp":
            items = subcat.get("items", [])
            corp_data = next((c for c in items if c["name"] == item_name), None)
            if corp_data and "subitems" in corp_data:
                response = f"{item_name}:\n\n"
                keyboard = []
                for subitem in corp_data["subitems"]:
                    response += f"- {subitem['name']}\n"
                    keyboard.append([InlineKeyboardButton(subitem['name'], callback_data=f"{query.data}:subitem:{subitem['name']}")])
                keyboard.append([InlineKeyboardButton("⬅️ मागे", callback_data=f"{category_id}:{subcat_id}")])
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(response, reply_markup=reply_markup)

    # Handle subitem (subcorporation) selection
    if len(query.data.split(":")) == 6:
        category_id, subcat_id, _, corp_name, _, subitem_name = query.data.split(":", 5)
        category = SCHEMES[category_id]
        subcat = category["subcategories"][subcat_id]
        corp_data = next((c for c in subcat["items"] if c["name"] == corp_name), None)
        if corp_data:
            subitem_data = next((si for si in corp_data["subitems"] if si["name"] == subitem_name), None)
            if subitem_data:
                keyboard = [[InlineKeyboardButton("⬅️ मागे", callback_data=f"{category_id}:{subcat_id}:corp:{corp_name}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(f"{subitem_name}:\n{subitem_data['details']}", reply_markup=reply_markup)

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
    app.add_handler(MessageHandler(filters.Text(["Hi", "hi", "HI"]), handle_hi))
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
