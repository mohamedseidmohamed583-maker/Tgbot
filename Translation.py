from database import get_user_language
TRANSLATIONS = {
    "am": {
        "btn_add": "➕ ቦቱን ወደ ቻትዎ ለመጨመር",
        "btn_order": "📢 ማስታወቂያ ለማሰራት",
        "btn_price": "💰 Price | ዋጋ",
        "btn_payment": "💳 Payment Method",
        "btn_status": "📊 My Status & Stats",
        "btn_lang": "🌐 Language | ቋንቋ",
        "btn_support": "💬 Support | ድጋፍ",
        "btn_back": "🔙 Back to Menu",
        "done_msg": (
            "<blockquote><b>🟢 [SUCCESS]</b></blockquote>\n"
            "✅ <b>ተጠናቋል! ቋንቋዎ በተሳካ ሁኔታ ተስተካክሏል።</b>"
        ),
        "loading": (
            "<blockquote><b>🔵 [PRIMARY] PROCESSING</b></blockquote>\n"
            "⏳ <b>እባክዎ ይጠብቁ... ሚዲያው እየተዘጋጀ ነው።</b>"
        ),
        "video_converted": (
            "<blockquote><b>🟢 [SUCCESS] AUDIO EXTRACTED</b></blockquote>\n"
            "🎵 <b>ከቪዲዮ የተቀየረው (MP3 Audio)</b>\n\n"
            "✨ <b>Converted with:</b> @{bot_username} &amp; @mame_posts"
        ),
        "video_downloaded": (
            "<blockquote><b>🟢 [SUCCESS] DOWNLOAD COMPLETE</b></blockquote>\n"
            "🚀 <b>Downloaded with:</b> @{bot_username} &amp; @mame_posts\n\n"
            "🎉 <b>Enjoy your media!</b>"
        ),
        "size_limit": (
            "<blockquote><b>🔴 [DANGER] LIMIT EXCEEDED</b></blockquote>\n"
            "⚠️ <b>ቪዲዮው ከቴሌግራም 50MB ገደብ በላይ ስለሆነ መላክ አይቻልም!</b>"
        ),
        "fail_download": (
            "<blockquote><b>🔴 [DANGER] DOWNLOAD FAILED</b></blockquote>\n"
            "💔 <b>የፈለጉትን File ማግኘት አልቻልኩም!</b>\n"
            "እባክዎ ሊንኩ ትክክለኛ እና Public መሆኑን ያረጋግጡ።"
        ),
        "photo_download": (
            "<blockquote><b>🟢 [SUCCESS] PHOTO READY</b></blockquote>\n"
            "📸 <b>Downloaded Thumbnail/Photo</b>\n\n"
            "✨ <b>Downloaded with:</b> @{bot_username}"
        ),
        "welcome": (
            "<blockquote><b>🔵 [PRIMARY] ALL-IN-ONE DOWNLOADER</b></blockquote>\n"
            "👋 <b>ሰላም! እንኳን ወደ ዳውንሎደር ቦት በደህና መጡ!</b>\n\n"
            "<b>የሚደገፉ ማህበራዊ ሚዲያዎች:</b>\n"
            "• 🎵 <b>TikTok &amp; Likee:</b> Videos &amp; Photos\n"
            "• 📸 <b>Instagram &amp; Pinterest:</b> Reels, Photos &amp; Stories\n"
            "• ▶️ <b>YouTube:</b> Full Videos, Shorts &amp; Music\n"
            "• ✖️ <b>Twitter (X):</b> Videos &amp; Voices\n"
            "• 📘 <b>Facebook, Reddit, Twitch &amp; Others</b>\n\n"
            "📹 <b>Video to Audio:</b> ማንኛውንም ቪዲዮ ይላኩ፤ ወደ MP3 ይቀየርልዎታል!"
        ),
        "price": (
            "<blockquote><b>🟡 [WARNING] RATES &amp; PRICING</b></blockquote>\n"
            "💰 <b>የማስታወቂያ ዋጋዎች:</b>\n\n"
            "📌 <b>12 Hours:</b> በስምምነት\n"
            "📌 <b>24 Hours:</b> 500 ETB\n"
            "📌 <b>48 Hours:</b> 700 ETB"
        ),
        "order": (
            "<blockquote><b>🔵 [PRIMARY] PROMOTION</b></blockquote>\n"
            "📢 <b>@mame_posts ቻናል ላይ ማስታወቂያ ለማሰራት:</b>\n"
            "እባክዎ ማስተዋወቅ የሚፈልጉትን ፖስት በቀጥታ እዚህ ይላኩ።"
        ),
        "payment": (
            "<blockquote><b>🟢 [SUCCESS] PAYMENT METHODS</b></blockquote>\n"
            "💳 <b>የክፍያ አማራጮች:</b>\n\n"
            "🏦 <b>ንግድ ባንክ (CBE):</b> <code>1000528274394</code>\n"
            "👤 <i>Mohammed Seid</i>\n\n"
            "📱 <b>ቴሌብር (Telebirr):</b> <code>+251963266849</code>\n\n"
            "⚠️ <i>ክፍያውን ሲፈጽሙ ደረሰኙን እዚህ ይላኩ!</i>"
        ),
        "support": (
            "<blockquote><b>🔵 [PRIMARY] HELP &amp; SUPPORT</b></blockquote>\n"
            "💬 <b>እርዳታ ከፈለጉ:</b> ሊንክዎን በቀጥታ ይላኩ። ለአድሚን መልዕክት መጻፍም ይችላሉ።"
        ),
        "force_join": (
            "<blockquote><b>🔴 [DANGER] ACCESS RESTRICTED</b></blockquote>\n"
            "🔒 <b>ቦቱን ለመጠቀም መጀመሪያ ከታች ያለውን ቻናል ይቀላቀሉ!</b>"
        )
    },
    "en": {
        "btn_add": "➕ Add to Group / Channel",
        "btn_order": "📢 Advertise / Promote",
        "btn_price": "💰 Pricing & Rates",
        "btn_payment": "💳 Payment Options",
        "btn_status": "📊 User Stats",
        "btn_lang": "🌐 Language",
        "btn_support": "💬 Help & Support",
        "btn_back": "🔙 Back to Menu",
        "done_msg": (
            "<blockquote><b>🟢 [SUCCESS]</b></blockquote>\n"
            "✅ <b>Language successfully updated!</b>"
        ),
        "loading": (
            "<blockquote><b>🔵 [PRIMARY] PROCESSING</b></blockquote>\n"
            "⏳ <b>Please wait... Fetching and processing your media.</b>"
        ),
        "video_converted": (
            "<blockquote><b>🟢 [SUCCESS] AUDIO EXTRACTED</b></blockquote>\n"
            "🎵 <b>Extracted Audio (MP3)</b>\n\n"
            "✨ <b>Converted with:</b> @{bot_username} &amp; @mame_posts"
        ),
        "video_downloaded": (
            "<blockquote><b>🟢 [SUCCESS] DOWNLOAD COMPLETE</b></blockquote>\n"
            "🚀 <b>Downloaded with:</b> @{bot_username} &amp; @mame_posts\n\n"
            "🎉 <b>Enjoy your media!</b>"
        ),
        "size_limit": (
            "<blockquote><b>🔴 [DANGER] FILE LIMIT EXCEEDED</b></blockquote>\n"
            "⚠️ <b>Video exceeds the 50MB Telegram file size limit!</b>"
        ),
        "fail_download": (
            "<blockquote><b>🔴 [DANGER] DOWNLOAD FAILED</b></blockquote>\n"
            "💔 <b>Unable to download the requested media.</b>\n"
            "Please ensure the link is public and accessible."
        ),
        "photo_download": (
            "<blockquote><b>🟢 [SUCCESS] PHOTO READY</b></blockquote>\n"
            "📸 <b>Downloaded Photo / Thumbnail</b>\n\n"
            "✨ <b>Downloaded with:</b> @{bot_username}"
        ),
        "welcome": (
            "<blockquote><b>🔵 [PRIMARY] ALL-IN-ONE DOWNLOADER</b></blockquote>\n"
            "👋 <b>Welcome to the Ultimate Media Downloader!</b>\n\n"
            "<b>Supported Platforms:</b>\n"
            "• 🎵 <b>TikTok &amp; Likee:</b> Videos &amp; Photos\n"
            "• 📸 <b>Instagram &amp; Pinterest:</b> Reels, Photos &amp; Stories\n"
            "• ▶️ <b>YouTube:</b> Full Videos, Shorts &amp; Music\n"
            "• ✖️ <b>Twitter (X):</b> Videos &amp; Audio\n"
            "• 📘 <b>Facebook, Reddit, Twitch &amp; More</b>\n\n"
            "📹 <b>Video to Audio:</b> Send any video directly to convert it into MP3!"
        ),
        "price": (
            "<blockquote><b>🟡 [WARNING] ADVERTISING RATES</b></blockquote>\n"
            "💰 <b>Channel Promotion Pricing:</b>\n\n"
            "📌 <b>12 Hours:</b> Negotiable\n"
            "📌 <b>24 Hours:</b> 500 ETB\n"
            "📌 <b>48 Hours:</b> 700 ETB"
        ),
        "order": (
            "<blockquote><b>🔵 [PRIMARY] SPONSORSHIP</b></blockquote>\n"
            "📢 <b>Promote on @mame_posts:</b>\n"
            "Send your promotion post directly here to get started."
        ),
        "payment": (
            "<blockquote><b>🟢 [SUCCESS] PAYMENT GATEWAYS</b></blockquote>\n"
            "💳 <b>Payment Methods:</b>\n\n"
            "🏦 <b>CBE Bank:</b> <code>1000528274394</code>\n"
            "👤 <i>Mohammed Seid</i>\n\n"
            "📱 <b>Telebirr:</b> <code>+251963266849</code>\n\n"
            "⚠️ <i>Please upload a screenshot of your transfer receipt after paying.</i>"
        ),
        "support": (
            "<blockquote><b>🔵 [PRIMARY] CUSTOMER SERVICE</b></blockquote>\n"
            "💬 <b>Assistance:</b> Send your media link to download, or leave a message for the admin."
        ),
        "force_join": (
            "<blockquote><b>🔴 [DANGER] ACCESS RESTRICTED</b></blockquote>\n"
            "🔒 <b>You must join our channel before using the bot!</b>"
        )
    },
    "ar": {
        "btn_add": "➕ إضافة إلى المجموعة",
        "btn_order": "📢 طلب إعلان",
        "btn_price": "💰 الأسعار والخطط",
        "btn_payment": "💳 طرق الدفع",
        "btn_status": "📊 إحصائيات الحساب",
        "btn_lang": "🌐 اللغة",
        "btn_support": "💬 الدعم الفني",
        "btn_back": "🔙 العودة للقائمة",
        "done_msg": (
            "<blockquote><b>🟢 [SUCCESS]</b></blockquote>\n"
            "✅ <b>تم تحديث اللغة بنجاح!</b>"
        ),
        "loading": (
            "<blockquote><b>🔵 [PRIMARY] جاري المعالجة</b></blockquote>\n"
            "⏳ <b>يرجى الانتظار... يتم الآن تجهيز المحتوى.</b>"
        ),
        "video_converted": (
            "<blockquote><b>🟢 [SUCCESS] تم استخراج الصوت</b></blockquote>\n"
            "🎵 <b>ملف صوتي مستخرج (MP3)</b>\n\n"
            "✨ <b>بواسطة:</b> @{bot_username}"
        ),
        "video_downloaded": (
            "<blockquote><b>🟢 [SUCCESS] اكتمل التحميل</b></blockquote>\n"
            "🚀 <b>تم التحميل بواسطة:</b> @{bot_username}\n\n"
            "🎉 <b>استمتع بمشاهدة المحتوى!</b>"
        ),
        "size_limit": (
            "<blockquote><b>🔴 [DANGER] تم تجاوز الحد</b></blockquote>\n"
            "⚠️ <b>حجم الملف أكبر من 50 ميغابايت!</b>"
        ),
        "fail_download": (
            "<blockquote><b>🔴 [DANGER] فشل التحميل</b></blockquote>\n"
            "💔 <b>تعذر تحميل الرابط المطلوب. يرجى التأكد من أنه عام وصالح.</b>"
        ),
        "photo_download": (
            "<blockquote><b>🟢 [SUCCESS] تم تحميل الصورة</b></blockquote>\n"
            "📸 <b>الصورة المصغرة</b>\n\n"
            "✨ <b>بواسطة:</b> @{bot_username}"
        ),
        "welcome": (
            "<blockquote><b>🔵 [PRIMARY] بوت التحميل الشامل</b></blockquote>\n"
            "👋 <b>مرحباً بك في بوت تحميل الميديا الشامل!</b>\n\n"
            "<b>المنصات المدعومة:</b>\n"
            "• 🎵 <b>تيك توك &amp; لايكي:</b> مقاطع وصور\n"
            "• 📸 <b>إنستغرام &amp; بينترست:</b> ريلز، ستوري وصور\n"
            "• ▶️ <b>يوتيوب:</b> مقاطع كاملة، شورتس وموسيقى\n"
            "• ✖️ <b>تويتر (X):</b> مقاطع وتغريدات صوتية\n"
            "• 📘 <b>فيسبوك، ريديت، تويتش والمزيد</b>"
        ),
        "price": (
            "<blockquote><b>🟡 [WARNING] أسعار الإعلانات</b></blockquote>\n"
            "💰 <b>باقات الإعلانات:</b>\n\n"
            "📌 <b>24 ساعة:</b> 500 ETB\n"
            "📌 <b>48 ساعة:</b> 700 ETB"
        ),
        "order": (
            "<blockquote><b>🔵 [PRIMARY] طلب إعلان</b></blockquote>\n"
            "📢 <b>للإعلان على قناتنا:</b> أرسل تفاصيل منشورك هنا مباشرة."
        ),
        "payment": (
            "<blockquote><b>🟢 [SUCCESS] بوابات الدفع</b></blockquote>\n"
            "💳 <b>طرق الدفع:</b>\n\n"
            "🏦 <b>البنك التجاري (CBE):</b> <code>1000528274394</code>\n"
            "📱 <b>تلي بر (Telebirr):</b> <code>+251963266849</code>"
        ),
        "support": (
            "<blockquote><b>🔵 [PRIMARY] الدعم</b></blockquote>\n"
            "💬 أرسل رابط الميديا مباشرة للتحميل الفوري."
        ),
        "force_join": (
            "<blockquote><b>🔴 [DANGER] الاشتراك إجباري</b></blockquote>\n"
            "🔒 <b>يجب عليك الاشتراك في القناة أولاً لاستخدام البوت!</b>"
        )
    }
}
def get_trans(user_id: int, key: str) -> str:
    lang = get_user_language(user_id)
    if not lang or lang not in TRANSLATIONS:
        lang = "am"
    return TRANSLATIONS.get(lang, TRANSLATIONS["am"]).get(key, "")
