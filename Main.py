import os
import re
import asyncio
import static_ffmpeg
try:
    static_ffmpeg.add_paths()
except Exception as e:
    print("Static FFmpeg setup notice:", e)
from urllib.parse import quote
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    BotCommand
)
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from config import TOKEN, ADMIN_ID, FORCE_CHANNEL, FORCE_CHANNEL_LINK, SUPPORTED_DOMAINS, FFMPEG_PATH
from database import (
    record_user_activity,
    set_user_language,
    get_user_language,
    get_user_stats,
    load_data
)
from translations import get_trans
from downloader import (
    clean_url,
    run_ytdlp_download,
    find_downloaded_files,
    compress_video_if_needed,
    extract_audio_from_video,
    convert_thumbnail_to_jpg,
    fetch_pinterest_direct_image
)
from keep_alive import keep_alive
# Helper Functions
def get_bot_username(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.bot.username or "mame_posts_bot"
def get_main_menu_keyboard(bot_username: str, user_id: int):
    keyboard = [
        [InlineKeyboardButton(get_trans(user_id, "btn_add"), url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton(get_trans(user_id, "btn_order"), callback_data="cmd_order")],
        [
            InlineKeyboardButton(get_trans(user_id, "btn_price"), callback_data="cmd_price"),
            InlineKeyboardButton(get_trans(user_id, "btn_payment"), callback_data="cmd_payment")
        ],
        [
            InlineKeyboardButton(get_trans(user_id, "btn_status"), callback_data="cmd_status"),
            InlineKeyboardButton(get_trans(user_id, "btn_lang"), callback_data="cmd_change_lang")
        ],
        [InlineKeyboardButton(get_trans(user_id, "btn_support"), callback_data="cmd_support")]
    ]
    return InlineKeyboardMarkup(keyboard)
def get_language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang_am"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ],
        [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")]
    ])
def get_back_keyboard(user_id: int):
    return InlineKeyboardMarkup([[InlineKeyboardButton(get_trans(user_id, "btn_back"), callback_data="cmd_back")]])
async def post_init(application):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("menu", "Main menu"),
        BotCommand("status", "Check status"),
        BotCommand("rate", "Advertising rates"),
        BotCommand("payment", "Payment methods"),
        BotCommand("help", "Help and support")
    ]
    await application.bot.set_my_commands(commands)
async def is_joined(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=FORCE_CHANNEL, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return True
async def show_force_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = get_trans(user_id, "force_join")
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=FORCE_CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")]
    ]
    await update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
async def send_main_menu(chat_id: int, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    bot_username = get_bot_username(context)
    text = get_trans(user_id, "welcome")
    await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=get_main_menu_keyboard(bot_username, user_id),
        parse_mode="HTML"
    )
# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = update.effective_user.id
    record_user_activity(user_id)
    setup_keyboard = ReplyKeyboardMarkup([["🏠 Menu"]], resize_keyboard=True, input_field_placeholder="Send link 🔗")
    user_lang = get_user_language(user_id)
    if not user_lang:
        await update.message.reply_text(
            "
🌐 SELECT LANGUAGE
\n"
            "Please select your language / እባክዎ ቋንቋ ይምረጡ / اختر لغتك፦",
            reply_markup=get_language_keyboard(),
            parse_mode="HTML"
        )
        return
    await update.message.reply_text("🏠", reply_markup=setup_keyboard)
    await send_main_menu(update.effective_chat.id, context, user_id)
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user = update.effective_user
    record_user_activity(user.id)
    total_users, user_msg_count = get_user_stats(user.id)
    username_text = f"@{user.username}" if user.username else "None"
    msg = (
        "
📊 [STATUS] USER ENGAGEMENT
\n\n"
        f"👤 Username: {username_text}\n"
        f"🆔 ID: {user.id}\n\n"
        f"💬 Your Messages: {user_msg_count}\n"
        f"👥 Total Bot Users: {total_users}\n\n"
        "🔥 Status: Active"
    )
    await update.message.reply_text(msg, parse_mode="HTML")
async def rates_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(get_trans(update.effective_user.id, "price"), parse_mode="HTML")
async def payment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(get_trans(update.effective_user.id, "payment"), parse_mode="HTML")
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(get_trans(update.effective_user.id, "support"), parse_mode="HTML")
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.effective_user.id != ADMIN_ID:
        return
    reply_msg = update.message.reply_to_message
    has_args = bool(context.args)
    if not reply_msg and not has_args:
        await update.message.reply_text("❌ Reply to a message or use:\n/broadcast your message", parse_mode="HTML")
        return
    data = load_data()
    success_count = 0
    fail_count = 0
    status_msg = await update.message.reply_text("📢 Broadcasting in progress...", parse_mode="HTML")
    for uid_str in data.keys():
        try:
            chat_id = int(uid_str)
            if reply_msg:
                await reply_msg.copy(chat_id=chat_id)
            else:
                text_to_send = " ".join(context.args)
                await context.bot.send_message(chat_id=chat_id, text=text_to_send, parse_mode="HTML")
            success_count += 1
            await asyncio.sleep(0.05)
        except Exception:
            fail_count += 1
    await status_msg.edit_text(
        "
🟢 [SUCCESS] BROADCAST COMPLETED
\n\n"
        f"✅ Successful: {success_count}\n"
        f"❌ Failed: {fail_count}",
        parse_mode="HTML"
    )
# Media Processing Handlers
async def convert_video_to_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = update.effective_user.id
    record_user_activity(user_id)
    if not await is_joined(update, context):
        await show_force_join(update, context)
        return
    video = update.message.video or update.message.video_note
    if not video:
        document = update.message.document
        if document and document.mime_type and document.mime_type.startswith("video/"):
            video = document
    if not video:
        return
    file_id = update.message.message_id
    input_path = f"input_vid_{user_id}_{file_id}.mp4"
    output_path = f"output_aud_{user_id}_{file_id}.mp3"
    status_msg = None
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.RECORD_VOICE)
        status_msg = await update.message.reply_text(get_trans(user_id, "loading"), parse_mode="HTML")
        tg_file = await video.get_file()
        await tg_file.download_to_drive(input_path)
        cmd = [FFMPEG_PATH, "-y", "-i", input_path, "-vn", "-acodec", "libmp3lame", "-q:a", "2", output_path]
        result = await asyncio.to_thread(subprocess.run, cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, timeout=300)
        if result.returncode != 0 or not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise RuntimeError("FFmpeg conversion error")
        bot_username = get_bot_username(context)
        share_url = f"https://t.me/share/url?url={quote(f'https://t.me/{bot_username}?start=share')}&text={quote('Try this awesome Bot!🔥')}"
        keyboard_share = [[InlineKeyboardButton("🔗 Share Bot 🚀", url=share_url)]]
        caption_text = get_trans(user_id, "video_converted").format(bot_username=bot_username)
        with open(output_path, "rb") as audio_file:
            await update.message.reply_audio(
                audio=audio_file,
                caption=caption_text,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard_share)
            )
        if status_msg:
            await status_msg.delete()
    except Exception as e:
        print("Video to Audio Error:", e)
        if status_msg:
            await status_msg.edit_text(get_trans(user_id, "fail_download"), parse_mode="HTML")
    finally:
        for path in [input_path, output_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
async def handle_url_download(update: Update, context: ContextTypes.DEFAULT_TYPE, raw_url: str):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    bot_username = get_bot_username(context)
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    status_msg = await update.message.reply_text(get_trans(user_id, "loading"), parse_mode="HTML")
    target_url = clean_url(raw_url)
    prefix = f"media_{user_id}_{update.message.message_id}"
    template = f"{prefix}.%(ext)s"
    share_url = f"https://t.me/share/url?url=https://t.me/{bot_username}?start=share&text=Try%20this%20awesome%20Downloader%20Bot!🔥"
    reply_markup_share = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Share Bot 🚀", url=share_url)]])
    # Direct Pinterest Image Extraction
    if "pinterest.com" in target_url or "pin.it" in target_url:
        direct_img = fetch_pinterest_direct_image(target_url)
        if direct_img:
            await update.message.reply_photo(
                photo=direct_img,
                caption=get_trans(user_id, "photo_download").format(bot_username=bot_username),
                reply_markup=reply_markup_share,
                parse_mode="HTML"
            )
            await status_msg.delete()
            return
    sent_any = False
    try:
        await asyncio.to_thread(run_ytdlp_download, target_url, template)
        actual_video, actual_thumb = find_downloaded_files(prefix)
        # 1. Send Thumbnail
        if actual_thumb and os.path.exists(actual_thumb):
            clean_thumb = actual_thumb
            try:
                if actual_thumb.lower().endswith(".webp"):
                    clean_thumb = f"{prefix}_thumb.jpg"
                    await convert_thumbnail_to_jpg(actual_thumb, clean_thumb)
                if os.path.exists(clean_thumb) and os.path.getsize(clean_thumb) > 1000:
                    with open(clean_thumb, 'rb') as tf:
                        await update.message.reply_photo(
                            photo=tf,
                            caption=get_trans(user_id, "photo_download").format(bot_username=bot_username),
                            reply_markup=reply_markup_share,
                            parse_mode="HTML"
                        )
                    sent_any = True
            except Exception as te:
                print("Thumbnail send failed:", te)
        # 2. Compress & Send Video
        if actual_video and os.path.exists(actual_video):
            video_to_send = await compress_video_if_needed(actual_video, prefix)
            file_size = os.path.getsize(video_to_send)
            print(f"Ready to upload video: {video_to_send} ({file_size / (1024*1024):.2f} MB)")
            caption_text = get_trans(user_id, "video_downloaded").format(bot_username=bot_username)
            video_sent = False
            try:
                await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_VIDEO)
                with open(video_to_send, 'rb') as vf:
                    await update.message.reply_video(
                        video=vf,
                        caption=caption_text,
                        reply_markup=reply_markup_share,
                        parse_mode="HTML",
                        supports_streaming=True
                    )
                video_sent = True
                sent_any = True
            except Exception as vid_err:
                print("reply_video failed, falling back to document:", vid_err)
            if not video_sent:
                try:
                    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_DOCUMENT)
                    with open(video_to_send, 'rb') as doc_file:
                        await update.message.reply_document(
                            document=doc_file,
                            caption=caption_text,
                            reply_markup=reply_markup_share,
                            parse_mode="HTML"
                        )
                    sent_any = True
                except Exception as doc_err:
                    print("Document fallback error:", doc_err)
            # 3. Extract & Send Audio (MP3)
            audio_output = f"audio_{user_id}_{update.message.message_id}.mp3"
            success_audio = await extract_audio_from_video(actual_video, audio_output)
            if success_audio:
                await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.RECORD_VOICE)
                with open(audio_output, 'rb') as af:
                    await update.message.reply_audio(
                        audio=af,
                        caption=f"
🟢 [SUCCESS] BGM EXTRACTED
\n\n🎧 Extracted Audio / BGM (MP3)\n\n✨ Downloaded with: @{bot_username}",
                        reply_markup=reply_markup_share,
                        parse_mode="HTML"
                    )
                sent_any = True
    except Exception as e:
        print("Download engine error:", e)
    finally:
        for f in os.listdir('.'):
            if f.startswith(prefix) or f.startswith(f"audio_{user_id}_{update.message.message_id}"):
                try:
                    os.remove(f)
                except Exception:
                    pass
    if sent_any:
        try:
            await status_msg.delete()
        except Exception:
            pass
    else:
        try:
            await status_msg.edit_text(get_trans(user_id, "fail_download"), parse_mode="HTML")
        except Exception:
            pass
# Callback & Message Dispatchers
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    bot_username = get_bot_username(context)
    if data.startswith("lang_"):
        lang_code = data.split("_", 1)[1]
        set_user_language(user_id, lang_code)
        await query.answer()
        try:
            await query.message.delete()
        except Exception:
            pass
        await context.bot.send_message(
            chat_id=user_id,
            text=get_trans(user_id, "done_msg"),
            reply_markup=ReplyKeyboardMarkup([["🏠 Menu"]], resize_keyboard=True),
            parse_mode="HTML"
        )
        await context.bot.send_message(
            chat_id=user_id,
            text=get_trans(user_id, "welcome"),
            reply_markup=get_main_menu_keyboard(bot_username, user_id),
            parse_mode="HTML"
        )
        return
    if data == "cmd_change_lang":
        await query.answer()
        await query.edit_message_text(
            "
🌐 SELECT LANGUAGE
\n"
            "Please select your language / እባክዎ ቋንቋ ይምረጡ / اختر لغتك፦",
            reply_markup=get_language_keyboard(),
            parse_mode="HTML"
        )
        return
    if data == "cmd_back":
        await query.answer()
        await query.edit_message_text(
            get_trans(user_id, "welcome"),
            reply_markup=get_main_menu_keyboard(bot_username, user_id),
            parse_mode="HTML"
        )
        return
    for k in ["price", "order", "payment", "support"]:
        if data == f"cmd_{k}":
            await query.answer()
            await query.edit_message_text(
                get_trans(user_id, k),
                reply_markup=get_back_keyboard(user_id),
                parse_mode="HTML"
            )
            return
    if data == "cmd_status":
        await query.answer()
        total, count = get_user_stats(user_id)
        username_text = f"@{query.from_user.username}" if query.from_user.username else "None"
        msg = (
            "
📊 [STATUS] USER ENGAGEMENT
\n\n"
            f"👤 Username: {username_text}\n"
            f"🆔 ID: {user_id}\n\n"
            f"💬 Your Messages: {count}\n"
            f"👥 Total Bot Users: {total}\n\n"
            "🔥 Status: Active"
        )
        await query.edit_message_text(msg, reply_markup=get_back_keyboard(user_id), parse_mode="HTML")
        return
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if await is_joined(update, context):
        await query.answer()
        await query.edit_message_text(
            "
🟢 [SUCCESS] ACCESS GRANTED
\n"
            "✅ You have joined! Please resend your link now.",
            parse_mode="HTML"
        )
    else:
        await query.answer("❌ You must join the channel first!", show_alert=True)
async def handle_user_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = update.effective_user.id
    record_user_activity(user_id)
    if update.message.video or update.message.video_note or (update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith("video/")):
        await convert_video_to_audio(update, context)
        return
    text = update.message.text or update.message.caption or ""
    if text.strip() == "🏠 Menu":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_trans(user_id, "welcome"),
            reply_markup=get_main_menu_keyboard(get_bot_username(context), user_id),
            parse_mode="HTML"
        )
        return
    if any(d in text.lower() for d in SUPPORTED_DOMAINS):
        if not await is_joined(update, context):
            await show_force_join(update, context)
            return
        m = re.search(r"https?://[^\s]+", text)
        target = m.group(0).rstrip(".,!?)]}") if m else text.strip()
        await handle_url_download(update, context, target)
        return
    # Admin Forwarding
    try:
        header = f"📩 New User Message\n\n👤 Name: {update.effective_user.full_name}\n🆔 ID: {user_id}"
        h_msg = await context.bot.send_message(chat_id=ADMIN_ID, text=header, parse_mode="HTML")
        f_msg = await update.message.forward(chat_id=ADMIN_ID)
        if "user_mapping" not in context.bot_data:
            context.bot_data["user_mapping"] = {}
        context.bot_data["user_mapping"][str(h_msg.message_id)] = user_id
        context.bot_data["user_mapping"][str(f_msg.message_id)] = user_id
        await update.message.reply_text("✅ መልዕክትዎ ተቀብለናል። Admin ያነበበውን መልስ ይልክልዎታል።", parse_mode="HTML")
    except Exception:
        pass
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.effective_user.id != ADMIN_ID:
        return
    r_msg = update.message.reply_to_message
    if not r_msg:
        return
    mapping = context.bot_data.get("user_mapping", {})
    uid = mapping.get(str(r_msg.message_id))
    if uid:
        try:
            await update.message.copy(chat_id=uid)
            await update.message.reply_text("✅ Reply sent to the user.", parse_mode="HTML")
        except Exception as e:
            await update.message.reply_text(f"❌ Delivery failed: {e}", parse_mode="HTML")
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    if "Conflict: terminated by other getUpdates request" not in str(context.error):
        print("❌ Telegram Application Error:", context.error)
# Entrypoint
def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing!")
    keep_alive()
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(post_init)
        .connect_timeout(60.0)
        .read_timeout(300.0)
        .write_timeout(300.0)
        .build()
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("rates", rates_command))
    application.add_handler(CommandHandler("rate", rates_command))
    application.add_handler(CommandHandler("payment", payment_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CallbackQueryHandler(check_join, pattern=r"^check_join$"))
    application.add_handler(CallbackQueryHandler(button_callback, pattern=r"^(cmd_|lang_)"))
    admin_filter = filters.User(user_id=ADMIN_ID) & filters.REPLY & ~filters.COMMAND
    application.add_handler(MessageHandler(admin_filter, admin_reply))
    application.add_handler(MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, convert_video_to_audio))
    type_filter = (filters.TEXT | filters.PHOTO | filters.Document.ALL | filters.VOICE | filters.AUDIO | filters.Sticker.ALL) & ~filters.COMMAND
    application.add_handler(MessageHandler(type_filter, handle_user_messages))
    application.add_error_handler(error_handler)
    print("🤖 Mame Posts Downloader Bot is running...")
    application.run_polling(drop_pending_updates=True)
if __name__ == "__main__":
    main()
