from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID
from database import init_database, add_account, get_user_accounts, add_template, get_user_templates

# Initialize database
init_database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء البوت - الواجهة الرئيسية"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("➕ إضافة حساب", callback_data="add_account")],
        [InlineKeyboardButton("📝 إضافة كليشة", callback_data="add_template")],
        [InlineKeyboardButton("📊 بدء إبلاغات", callback_data="start_report")],
        [InlineKeyboardButton("📈 الحسابات", callback_data="show_accounts")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 مرحباً {user.first_name}!\n\n"
        "🤖 مرحباً بك في بوت الإبلاغات الجماعية\n\n"
        "اختر أحد الخيارات أدناه:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الأزرار"""
    query = update.callback_query
    user_id = query.from_user.id
    
    await query.answer()
    
    if query.data == "add_account":
        await query.edit_message_text(
            text="📱 أرسل رقم الهاتف للحساب الذي تريد إضافته:\n\nمثال: +966501234567"
        )
        context.user_data['action'] = 'add_account'
    
    elif query.data == "add_template":
        await query.edit_message_text(
            text="📝 أرسل اسم الكليشة أولاً:\n\nمثال: كليشة 1"
        )
        context.user_data['action'] = 'add_template_name'
    
    elif query.data == "show_accounts":
        accounts = get_user_accounts(user_id)
        if accounts:
            text = "📊 حساباتك:\n\n"
            for acc_id, name, status in accounts:
                text += f"✅ {name} - {status}\n"
        else:
            text = "❌ لا توجد حسابات مضافة بعد"
        
        await query.edit_message_text(text=text)
    
    elif query.data == "start_report":
        await query.edit_message_text(
            text="🎯 أدخل اسم المستخدم المراد الإبلاغ عليه:\n\nمثال: @username"
        )
        context.user_data['action'] = 'start_report_username'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الرسائل النصية"""
    user_id = update.effective_user.id
    text = update.message.text
    action = context.user_data.get('action')
    
    if action == 'add_account':
        # حفظ الحساب
        account_id = add_account(user_id, text, f"حساب {text}")
        await update.message.reply_text(
            f"✅ تمت إضافة الحساب بنجاح!\n"
            f"رقم الهاتف: {text}\n\n"
            f"الآن يمكنك استخدام هذا الحساب في الإبلاغات"
        )
        context.user_data['action'] = None
    
    elif action == 'add_template_name':
        context.user_data['template_name'] = text
        context.user_data['action'] = 'add_template_text'
        await update.message.reply_text(
            f"الآن أرسل نص الكليشة:\n\nمثال: هذا محتوى مسيء"
        )
    
    elif action == 'add_template_text':
        template_name = context.user_data.get('template_name')
        template_id = add_template(user_id, template_name, text)
        await update.message.reply_text(
            f"✅ تمت إضافة الكليشة بنجاح!\n"
            f"الاسم: {template_name}\n\n"
            f"النص: {text}"
        )
        context.user_data['action'] = None
    
    elif action == 'start_report_username':
        context.user_data['target_username'] = text
        context.user_data['action'] = 'start_report_count'
        await update.message.reply_text(
            f"📊 كم عدد الإبلاغات؟\n\nمثال: 10"
        )
    
    elif action == 'start_report_count':
        try:
            count = int(text)
            context.user_data['report_count'] = count
            context.user_data['action'] = 'start_report_delay'
            await update.message.reply_text(
                f"⏱️ كم التأخير بين الإبلاغات (بالثواني)؟\n\nمثال: 1 أو 0.5"
            )
        except ValueError:
            await update.message.reply_text("❌ أدخل رقم صحيح")

async def main():
    """تشغيل البوت"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CommandHandler("message", handle_message))
    
    # Run the bot
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
