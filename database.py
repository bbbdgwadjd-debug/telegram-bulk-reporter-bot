import sqlite3
import os
from config import DB_NAME

def init_database():
    """إنشاء قاعدة البيانات والجداول"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # جدول الحسابات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            phone_number TEXT NOT NULL,
            account_name TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول الكليشات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            template_name TEXT NOT NULL,
            template_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # جدول الإبلاغات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target_username TEXT NOT NULL,
            template_id INTEGER,
            num_reports INTEGER,
            delay REAL,
            status TEXT DEFAULT 'pending',
            success_count INTEGER DEFAULT 0,
            failed_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_account(user_id, phone_number, account_name):
    """إضافة حساب جديد"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO accounts (user_id, phone_number, account_name)
        VALUES (?, ?, ?)
    ''', (user_id, phone_number, account_name))
    conn.commit()
    account_id = cursor.lastrowid
    conn.close()
    return account_id

def get_user_accounts(user_id):
    """الحصول على حسابات المستخدم"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, account_name, status FROM accounts WHERE user_id = ?', (user_id,))
    accounts = cursor.fetchall()
    conn.close()
    return accounts

def add_template(user_id, template_name, template_text):
    """إضافة كليشة جديدة"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO templates (user_id, template_name, template_text)
        VALUES (?, ?, ?)
    ''', (user_id, template_name, template_text))
    conn.commit()
    template_id = cursor.lastrowid
    conn.close()
    return template_id

def get_user_templates(user_id):
    """الحصول على كليشات المستخدم"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, template_name FROM templates WHERE user_id = ?', (user_id,))
    templates = cursor.fetchall()
    conn.close()
    return templates
