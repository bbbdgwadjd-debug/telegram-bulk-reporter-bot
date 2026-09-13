#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup.py - سكريبت سهل للتثبيت والإعداد
يقوم بتثبيت المكتبات تلقائياً
"""

import subprocess
import sys
import os

def install_requirements():
    """تثبيت المكتبات من requirements.txt"""
    print("🔧 جاري تثبيت المكتبات المطلوبة...")
    print("="*50)
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✅ تم تثبيت جميع المكتبات بنجاح!")
        print("="*50)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ خطأ في التثبيت: {e}")
        return False

def check_env_file():
    """التحقق من وجود ملف .env"""
    print("\n🔍 التحقق من ملف الإعدادات...")
    print("="*50)
    
    if os.path.exists('.env'):
        print("✅ ملف .env موجود بالفعل")
        return True
    else:
        print("❌ ملف .env غير موجود")
        return False

def main():
    """تشغيل عملية الإعداد"""
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║" + " "*10 + "🚀 إعداد بوت الإبلاغات الجماعية" + " "*6 + "║")
    print("╚" + "="*48 + "╝")
    
    # تثبيت المكتبات
    if not install_requirements():
        print("⚠️ حدث خطأ في التثبيت. حاول مرة أخرى.")
        sys.exit(1)
    
    # التحقق من ملف .env
    if not check_env_file():
        print("⚠️ يرجى التأكد من وجود ملف .env")
        sys.exit(1)
    
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║" + " "*15 + "✅ تم الإعداد بنجاح!" + " "*14 + "║")
    print("╚" + "="*48 + "╝")
    
    print("\n📝 الخطوة التالية:")
    print("  1. افتح ملف .env")
    print("  2. استبدل 'BOT_TOKEN' بـ التوكن من @BotFather")
    print("  3. استبدل 'ADMIN_ID' بـ معرفك من @userinfobot")
    print("\n🚀 ثم شغل البوت:")
    print("   python main.py")
    print()

if __name__ == "__main__":
    main()
