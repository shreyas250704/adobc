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
        "subcategories": [
            {
                "name": "आश्रमशाळा",
                "लाभ घेणारा प्रवर्ग": "विमुक्त जाती, भटक्या जमाती व विशेष मागास प्रवर्ग",
                "items": [
                    {"name": "विमुक्त जाती, भटक्या जमाती व विशेष मागास प्रवर्गासाठीच्या आश्रमशाळा", 
                     "details": 
                     (      "आश्रमशाळा नाही, हे तर माझं दुसरं घर, जिथे माझ्या स्वप्नांना मिळते नवी नजर.\n\n"
                            "महाराष्ट्रातील विमुक्त जाती, भटक्या जमाती या संवर्गातील बरेच लोक आपला उदरनिर्वाह करण्यासाठी एका ठिकाणाहून दुसऱ्या ठिकाणी भटकत असतात. त्यामुळे त्यांच्या मुलांना शिक्षणापासून वंचित राहावे लागते. या संवर्गातील मुला-मुलींसाठी मोफत निवास, भोजन, शालेय साहित्य व अंथरुण-पांघरुण इत्यादी सोयी उपलब्ध करून दिल्यास आणि व्यक्तिगत लक्ष दिल्यास त्यांच्या शिक्षणावर चांगला परिणाम होईल या दृष्टीकोनातून या मुलांसाठी खास स्वतंत्र आश्रमशाळा अनुदान देऊन स्वयंसेवी संस्थांमार्फत सुरू करण्याची योजना सन १९५३-५४ पासून अस्तित्वात आली.\n\n"
                            "विमुक्त जाती, भटक्या जमाती कल्याण समितीने केलेल्या शिफारशी आणि वेळोवेळी समाविष्ट करण्यात आलेल्या जातींची संख्या लक्षात घेता, शासनाने निवासी आश्रमशाळा उघडण्यासाठी तयार केलेल्या बृहत आराखड्यानुसार आश्रमशाळांना मान्यता देण्यात येते. या आश्रमशाळांतून विद्यार्थ्यांना शासनाकडून मोफत निवास, भोजन, शालेय साहित्य, गणवेश (वर्षातून दोनदा) व अंथरुण-पांघरुण इत्यादी सोयी-सुविधा पुरविल्या जातात.\n\n"
                            "महाराष्ट्रातील विमुक्त जाती, भटक्या जमाती तसेच ऊसतोड कामगारांच्या मुलांसाठी निवासी शिक्षण मिळावे आणि त्यांची सामाजिक, सांस्कृतिक आणि शैक्षणिक प्रगती व्हावी, या उद्देशाने खाजगी संस्थांना अनुदाने देऊन आश्रमशाळा योजना शासनाकडून राबविण्यात येते. राज्यात विजाभज प्रवर्गाच्या विद्यार्थ्यांसाठी ५७३० प्राथमिक आश्रमशाळा, २९७ माध्यमिक आश्रमशाळा व १४८ उच्च माध्यमिक आश्रमशाळा, त्याचप्रमाणे ऊसतोड कामगारांच्या मुला-मुलींसाठी बीड जिल्ह्यामध्ये ४ आश्रमशाळा चालविल्या जातात. याशिवाय लातूर विभागातील नांदेड जिल्ह्यात १ विद्यानिकेतन शाळा चालविली जाते.\n\n"
                            "**योजनेच्या अटी:**\n"
                            "१. स्वयंसेवी संस्था ही सोसायटी रजिस्ट्रेशन अँक्ट १८६० व मुंबई सार्वजनिक विश्वस्त कायदा अधिनियम १९५० अन्वये नोंदणीकृत असावी.\n"
                            "२. संस्थेवर तसेच संस्थेच्या पदाधिकाऱ्यांवर कोणत्याही प्रकारचा पोलीस गुन्हा सिद्ध होऊन शिक्षा झालेली नसावी.\n"
                            "३. संस्था आश्रमशाळा चालविण्यास आर्थिकदृष्ट्या सक्षम असावी.\n"
                            "४. प्रवेशित/लाभधारक विद्यार्थी हा महाराष्ट्राचा रहिवाशी असावा.\n"
                            "५. लाभधारक मुलगा/मुलगी हे विजाभज प्रवर्गातील असावे.\n\n"
                            "**लाभाचे स्वरूप:**\n"
                            "१. या योजनेतर्गत मुला-मुलींसाठी मोफत निवास, भोजन व शिक्षण देण्यात येते. त्याचप्रमाणे बिछाना, शालेय साहित्य, गणवेश, क्रमिक पुस्तके व वैद्यकीय सुविधा देण्यात येतात.\n"
                            "२. या आश्रमशाळा चालविणाऱ्या स्वयंसेवी संस्थेस दरमहा दरडोई मान्य निवासी विद्यार्थ्यांसाठी रु. १५००/- प्रमाणे परिपोषण अनुदान, तसेच इमारत भाडे व मान्य निवासी कर्मचाऱ्यांवर ८% व १२% वेतनेतर अनुदान देण्यात येते.\n"
                            "३. विजाभज आश्रमशाळेतील शैक्षणिक गुणवत्ता वाढीसाठी निपुण भारत योजने अंतर्गत शिक्षकांना प्रशिक्षण देऊन विद्यार्थ्यांना जागतिक दर्जाचे भविष्यवेधी शिक्षण देण्याचे नियोजन व त्याद्वारे शिक्षणाचा दर्जा उंचावण्यात येत आहे.\n"
                            "४. आश्रमशाळांमध्ये निवासी विद्यार्थ्यांसह अनिवासी विद्यार्थ्यांनाही शिक्षण देण्यात येते.\n\n"
                            "**सदर योजनेचा लाभ घेण्यासाठी संपर्क:**\n"
                            "संबंधित जिल्ह्याचे सहायक संचालक, इतर मागास बहुजन कल्याण विभाग\n"
                            "**शासन निर्णय क्रमांक:** विभशा-२00२/प्र.क्र.३९/मावक-६, दिनांक: १६ ऑक्टोबर, २00३, सामाजिक न्याय विशेष सहाय्य विभाग"
                     ),
                     "images": [
                            "https://drive.google.com/uc?export=view&id=1_byNGaMURWcqsfPJowZJIUNF-5-D3WBk",  # Table 1
                            "https://drive.google.com/uc?export=view&id=1z_a0pdXCx8C-szUKi705Vdly4U-eOIxF"   # Table 2
                        ]
                    },
                    
                    {"name": "ऊसतोड कामगारांच्या मुला मुलींसाठी निवासी आश्रम शाळा", 
                     "details":
                     (       "राज्यातील उसतोड कामगारांना रोजगारासाठी सातत्याने भटकंती करावी लागते. यामुळे त्यांच्या मुला-मुलींच्या शिक्षणात स्थिरता राहात नाही. यास्तव उसतोड कामगारांच्या मुला-मुलींच्या शिक्षणात खंड पडू नये किंवा ते शिक्षणापासून वंचित राहू नयेत, त्यांना शिक्षणाची आवड निर्माण व्हावी व त्यांचा सर्वागिण विकास होऊन ते समाजाच्या मुख्य प्रवाहात यावेत, यासाठी सदर विद्यार्थ्यांना मोफत शिक्षण, भोजन, निवास एकाच छत्राखाली देण्याच्या उद्देशाने शासनाने सन १९९६ मध्ये केज व परळी वैजनाथ, जि. बीड येथे इयत्ता १ली ते ७वीच्या दोन प्राथमिक निवासी आश्रमशाळांना मंजूरी दिलेली आहे. तसेच २०१०-११ या वर्षापासून सदर आश्रमशाळांना इयत्ता ८वी ते १०वी चे वर्ग सुरू करण्यास मान्यता दिली आहे.\n\n"
                            "**योजनेच्या अटी व शर्ती:**\n"
                            "१. या योजनेअंतर्गत लाभार्थी विद्यार्थी उसतोड कामगारांचा मुलगा/मुलगी असावा.\n"
                            "२. लाभधारक विद्यार्थी हा महाराष्ट्र राज्याचा रहिवासी असावा.\n\n"
                            "**लाभाचे स्वरूप:**\n"
                            "१. या योजनेंतर्गत उसतोड कामगारांच्या मुला-मुलींसाठी मोफत निवास, भोजन व शिक्षण देण्यात येते. त्याचप्रमाणे बिछाना साहित्य, क्रमिक पुस्तके, वह्या, शालेय साहित्य व वैद्यकीय सुविधा देखील मोफत देण्यात येतात.\n"
                            "२. या आश्रमशाळा चालविणाऱ्या स्वयंसेवी संस्थेस दरमहा दरडोई मान्य निवासी विद्यार्थ्यांसाठी रु.१५००/- प्रमाणे प्राथमिक शाळेस ११ महिन्यासाठी व माध्यमिक शाळेस १० महिन्यासाठी देण्यात येते.\n"
                            "३. सदर आश्रमशाळेतील निवासी विद्यार्थ्यांवरील मान्यताप्राप्त शिक्षक व शिक्षकेत्तर कर्मचाऱ्यांच्या वेतनावर १०० टक्के अनुदान देण्यात येते. तसेच प्राथमिक आश्रमशाळेतीl निवासी विद्यार्थ्यांवरील मान्यताप्राप्त शिक्षक कर्मचाऱ्यांच्या वार्षिक वेतनाच्या ८% व वसतिगृह विभागातील मान्यता प्राप्त कर्मचाऱ्याच्या वार्षिक वेतनाच्या ८% वेतनेतर अनुदान, तसेच माध्यमिक व उच्च माध्यमिक आश्रमशाळेतीl निवासी विद्यार्थ्यांवरील मान्यता प्राप्त कर्मचाऱ्याच्या वार्षिक वेतनाच्या १२% आणि वसतिगृह विभागातील मान्यता प्राप्त कर्मचाऱ्याच्या वार्षिक वेतनाच्या ८% वेतनेतर अनुदान सहाव्या वेतन आयोगानुसार देण्यात येते.\n"
                            "४. सार्वजनिक बांधकाम विभागाने प्रमाणित केलेल्या भाड्याच्या ७५ टक्के अनुदान म्हणून देण्यात येते.\n\n"
                            "**सदर योजनेचा लाभ घेण्यासाठी संपर्क:**\n"
                            "सहायक संचालक बीड, इतर मागास बहुजन कल्याण विभाग\n\n"
                            "**शासन निर्णय क्रमांक:**\n"
                            "- उतोका-१९९५/प्र.क्र.१७७/मावक-६, दि. ७ मार्च, १९९६, सामाजिक न्याय विशेष व सहाय्य विभाग\n"
                            "- विजाभज-२०१४/प्र.क्र.१९८/विजाभज-२, दिनांक: ४ मार्च, २०१५, सामाजिक न्याय विशेष व सहाय्य विभाग"
                     )
                    },
                    {"name": "विद्यानिकेतन शाळा", 
                     "details": 
                     (      "महाराष्ट्रातील विजाभज विद्यार्थ्यांना निवासी शिक्षणाचा फायदा मिळावा आणि त्यांची शैक्षणिक, सामाजिक व आर्थिक उन्नती व्हावी, या उद्देशाने सन १९५३ पासून आश्रमशाळा योजना अंमलात आणली. तथापि विजाभज जमातीतील होतकरू व हुशार गुणवत्ता प्राप्त विद्यार्थ्यांसाठी स्वतंत्र विद्यानिकेतन योजना शासन निर्णय क्रमांक व्हीएएस/१०९०/प्र.क्र.१३५/मावक-६, दिनांक ०६/११/१९९५ अन्वये स्वयंसेवी संस्थांमार्फत विद्यानिकेतन सुरू करण्यास मंजुरी दिली. तसेच शासन निर्णय दिनांक ३१/७/१९९६ अन्वये विमुक्त जाती सेवा समिती, वसंतनगर कोटग्याळ, ता. मुखेड, जि. नांदेड या स्वयंसेवी संस्थेस विद्यानिकेतन सन १९९६-९७ पासून सुरू करण्यास मंजूरी देण्यात आली.\n\n"
                            "सध्या कार्यरत असलेल्या विद्यानिकेतनमध्ये इयत्ता ५वी ते १२वी पर्यंतचे वर्ग सुरू असून ६४० विद्यार्थी शिक्षण घेत आहेत.\n\n"
                            "**सदर योजनेचा लाभ घेण्यासाठी संपर्क:**\n"
                            "सहायक संचालक, इतर मागास बहुजन कल्याण विभाग, नांदेड\n\n"
                            "**शासन निर्णय क्रमांक:**\n"
                            "व्हीएएस/१०९०/प्र.क्र.१३५/मावक-६, दिनांक ०६/११/१९९५, सामाजिक न्याय विशेष सहाय्य विभाग"
                     )
                      }
                ]
            },
            {
                "name": "शिष्यवृत्ती",
                "लाभ घेणारा प्रवर्ग": "इतर मागास वर्ग व VJNT व SBC",
                "items": [
                    {"name": "मॅट्रिक पूर्व शिष्यवृत्ती (Pre Matric Scholarship)", "details": "इतर मागास वर्ग, VJNT आणि SBC प्रवर्गातील विद्यार्थ्यांना मॅट्रिकपूर्व शिक्षणासाठी शिष्यवृत्ती."},
                    {"name": "मॅट्रिकोत्तर शिष्यवृत्ती (Post Matric Scholarship)", "details": "मॅट्रिकोत्तर शिक्षण घेणाऱ्या विद्यार्थ्यांसाठी शिष्यवृत्ती योजना."},
                    {"name": "परदेशात उच्च शिक्षणासाठी शिष्यवृत्ती योजना", "details": "परदेशात उच्च शिक्षण घेण्यासाठी आर्थिक सहाय्य देणारी शिष्यवृत्ती योजना."}
                ]
            },
            {
                "name": "वसतिगृहे/आधार योजना",
                "लाभ घेणारा प्रवर्ग": "OBC, VJNT व SBC",
                "items": [
                    {"name": "राज्यातील इतर मागास प्रवर्ग, विमुक्त जाती, भटक्या जमाती व विशेष मागास प्रवर्ग या प्रवर्गातील विद्यार्थ्यांसाठी जिल्हानिहाय वसतिगृहे सुरू करणेबाबत", "details": "OBC, VJNT आणि SBC प्रवर्गातील विद्यार्थ्यांसाठी जिल्हानिहाय वसतिगृहे सुरू करणे."},
                    {"name": "ज्ञानज्योती सावित्रीबाई फुले आधार योजना", "details": "विद्यार्थ्यांना शिक्षणासाठी आर्थिक आधार देणारी योजना."}
                ]
            }
        ]
    },
    "cat2": {
        "name": "घरकुल/पायाभूत सुविधा बाबतच्या योजना",
        "items": [
            {"name": "वसंतराव नाईक तांडा/वस्ती सुधार योजना", "details": "वसंतराव नाईक तांडा आणि वस्ती सुधारणेसाठी योजना."},
            {"name": "विमुक्त जाती भटक्या जमाती या घटकांसह यशवंतराव चव्हाण मुक्त वसाहत योजना", "details": "विमुक्त जाती आणि भटक्या जमातींसाठी यशवंतराव चव्हाण मुक्त वसाहत योजना."},
            {"name": "मोदी आवाज घरकुल योजना", "details": "गरजू कुटुंबांना घरकुले बांधून देणारी योजना."}
        ]
    },
    "cat3": {
        "name": "भटक्या जमाती क प्रवर्ग (धनगर) समाजासाठी राबविण्यात येणाऱ्या विविध योजना",
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
    },
    "cat4": {
        "name": "सामाजिक योजना",
        "items": [
            {"name": "सामूहिक विवाह सोहळ्यामध्ये भाग घेऊन विवाह करण्याच्या विजाभज, इमाव व विमाप्र दंपत्यासाठी कन्यादान योजना", "details": "सामूहिक विवाह सोहळ्यासाठी कन्यादान योजना."},
            {"name": "महात्मा बसवेश्वर सामाजिक समता शिवा पुरस्कार योजना", "details": "सामाजिक समतेसाठी पुरस्कार योजना."},
            {"name": "स्व. वसंतराव नाईक गुणवत्ता पुरस्कार", "details": "गुणवत्तेसाठी वसंतराव नाईक पुरस्कार."}
        ]
    },
    "cat5": {
        "name": "कौशल्य विकास व अर्थसाहाय्याच्या योजना",
        "subcategories": [
            {
                "name": "संस्था",
                "items": [
                    {"name": "महात्मा ज्योतिबा फुले संशोधन व प्रशिक्षण संस्था (महाज्योती) नागपूर", "details": "संशोधन आणि प्रशिक्षणासाठी महाज्योती संस्था, नागपूर."},
                    {"name": "महाराष्ट्र संशोधन उन्नती व प्रशिक्षण प्रबोधिनी (अमृत)", "details": "संशोधन आणि प्रशिक्षणासाठी अमृत प्रबोधिनी."}
                ]
            },
            {
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
        ]
    }
}

# Start command handler
async def start(update: Update, context):
    logger.info("Received /start command")
    if not update.message:
        logger.error("Update has no message object")
        raise ValueError("Update has no message object")
    keyboard = [
        [InlineKeyboardButton("1", callback_data="cat1")],
        [InlineKeyboardButton("2", callback_data="cat2")],
        [InlineKeyboardButton("3", callback_data="cat3")],
        [InlineKeyboardButton("4", callback_data="cat4")],
        [InlineKeyboardButton("5", callback_data="cat5")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    logger.info("Sending reply with menu")
    response = "विभागा अंतर्गत राबविल्या जाणाऱ्या योजना:\n\n"
    response += "1. शैक्षणिक योजना\n"
    response += "2. घरकुल/पायाभूत सुविधा बाबतच्या योजना\n"
    response += "3. भटक्या जमाती क प्रवर्ग (धनगर) समाजासाठी राबविण्यात येणाऱ्या विविध योजना\n"
    response += "4. सामाजिक योजना\n"
    response += "5. कौशल्य विकास व अर्थसाहाय्याच्या योजना\n\n"
    response += "खालीलपैकी एक योजना निवडा:"
    await update.message.reply_text(response, reply_markup=reply_markup)
    logger.info(f"User {update.effective_user.id} started the bot")

# Handler for "Hi" message
async def handle_hi(update: Update, context):
    if update.message.text.lower() == "hi":
        await start(update, context)

# Callback query handler for menu navigation
# Callback query handler for menu navigation
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    logger.info(f"Received callback query with data: {query.data}")

    # Handle main category selection
    if query.data in SCHEMES:
        category = SCHEMES[query.data]
        category_name = category["name"]
        response = f"{category_name} अंतर्गत:\n\n"
        keyboard = []

        if "subcategories" in category:
            subcategories = category["subcategories"]
            for idx, subcat in enumerate(subcategories, 1):
                response += f"{idx}. {subcat['name']}\n"
                keyboard.append([InlineKeyboardButton(f"{idx}", callback_data=f"{query.data}:{idx-1}")])
        else:
            items = category["items"]
            for idx, item in enumerate(items, 1):
                response += f"{idx}. {item['name']}\n"
                keyboard.append([InlineKeyboardButton(f"{idx}", callback_data=f"{query.data}:item:{idx-1}")])

        keyboard.append([InlineKeyboardButton("⬅️ मागे", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")

    # Handle back to main menu
    elif query.data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("1", callback_data="cat1")],
            [InlineKeyboardButton("2", callback_data="cat2")],
            [InlineKeyboardButton("3", callback_data="cat3")],
            [InlineKeyboardButton("4", callback_data="cat4")],
            [InlineKeyboardButton("5", callback_data="cat5")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        response = "विभागा अंतर्गत राबविल्या जाणाऱ्या योजना:\n\n"
        response += "1. शैक्षणिक योजना\n"
        response += "2. घरकुल/पायाभूत सुविधा बाबतच्या योजना\n"
        response += "3. भटक्या जमाती क प्रवर्ग (धनगर) समाजासाठी राबविण्यात येणाऱ्या विविध योजना\n"
        response += "4. सामाजिक योजना\n"
        response += "5. कौशल्य विकास व अर्थसाहाय्याच्या योजना\n\n"
        response += "खालीलपैकी एक योजना निवडा:"
        await query.message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")

    # Handle subcategory selection
    else:
        parts = query.data.split(":", 2)
        if len(parts) == 2:
            category_id, subcat_idx = parts
            subcat_idx = int(subcat_idx)
            category = SCHEMES[category_id]
            subcat_data = category["subcategories"][subcat_idx]
            subcat_name = subcat_data["name"]
            response = f"{subcat_name}:\n\n"
            if "लाभ घेणारा प्रवर्ग" in subcat_data:
                response += f"(लाभ घेणारा प्रवर्ग = {subcat_data['लाभ घेणारा प्रवर्ग']})\n\n"
            keyboard = []

            items = subcat_data.get("items", [])
            for idx, item in enumerate(items, 1):
                response += f"{idx}. {item['name']}\n"
                keyboard.append([InlineKeyboardButton(f"{idx}", callback_data=f"{query.data}:item:{idx-1}")])

            keyboard.append([InlineKeyboardButton("⬅️ मागे", callback_data=f"{category_id}")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")

    # Handle individual item selection (schemes, institutions, corporations)
    if len(query.data.split(":")) == 4:
        category_id, subcat_idx, item_type, item_idx = query.data.split(":", 3)
        subcat_idx = int(subcat_idx)
        item_idx = int(item_idx)
        category = SCHEMES[category_id]
        items = category["items"] if "items" in category else category["subcategories"][subcat_idx]["items"]
        item_data = items[item_idx]
        
        if item_type == "item":
            keyboard = [[InlineKeyboardButton("⬅️ मागे", callback_data=f"{category_id}" if "items" in category else f"{category_id}:{subcat_idx}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            # Send the text description
            await query.message.reply_text(f"{item_data['name']}:\n{item_data['details']}", reply_markup=reply_markup, parse_mode="Markdown")
            # Send images if they exist
            if "images" in item_data:
                for image_url in item_data["images"]:
                    await context.bot.send_photo(chat_id=query.message.chat_id, photo=image_url, reply_markup=reply_markup)
        elif item_type == "corp":
            corp_data = items[item_idx]
            if "subitems" in corp_data:
                response = f"{corp_data['name']}:\n\n"
                keyboard = []
                for idx, subitem in enumerate(corp_data["subitems"], 1):
                    response += f"{idx}. {subitem['name']}\n"
                    keyboard.append([InlineKeyboardButton(f"{idx}", callback_data=f"{query.data}:subitem:{idx-1}")])
                keyboard.append([InlineKeyboardButton("⬅️ मागे", callback_data=f"{category_id}:{subcat_idx}")])
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text(response, reply_markup=reply_markup, parse_mode="Markdown")

    # Handle subitem (subcorporation) selection
    if len(query.data.split(":")) == 6:
        category_id, subcat_idx, _, corp_idx, _, subitem_idx = query.data.split(":", 5)
        subcat_idx = int(subcat_idx)
        corp_idx = int(corp_idx)
        subitem_idx = int(subitem_idx)
        category = SCHEMES[category_id]
        subcat = category["subcategories"][subcat_idx]
        corp_data = subcat["items"][corp_idx]
        subitem_data = corp_data["subitems"][subitem_idx]
        keyboard = [[InlineKeyboardButton("⬅️ मागे", callback_data=f"{category_id}:{subcat_idx}:corp:{corp_idx}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"{subitem_data['name']}:\n{subitem_data['details']}", reply_markup=reply_markup, parse_mode="Markdown")
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
