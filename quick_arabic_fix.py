#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
حل سريع لمشكلة النصوص العربية
Quick fix for Arabic text display issues
"""

def fix_arabic_text_simple(text):
    """إصلاح بسيط للنصوص العربية"""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        # إعادة تشكيل النص العربي
        reshaped = arabic_reshaper.reshape(text)
        
        # تطبيق اتجاه RTL
        bidi_text = get_display(reshaped)
        
        return bidi_text
    except ImportError:
        print("المكتبات غير متوفرة. جاري التثبيت...")
        import subprocess
        subprocess.run(["pip", "install", "arabic-reshaper", "python-bidi"])
        return fix_arabic_text_simple(text)

def main():
    print("🔤 اختبار النصوص العربية")
    print("=" * 40)
    
    # نصوص تجريبية
    test_texts = [
        "مرحباً بك في عالم الذكاء الاصطناعي",
        "البرمجة باللغة العربية",
        "تدريب نماذج اللاما",
        "معالجة النصوص العربية"
    ]
    
    print("النصوص الأصلية:")
    for i, text in enumerate(test_texts, 1):
        print(f"{i}. {text}")
    
    print("\n" + "=" * 40)
    print("النصوص المُصححة:")
    
    for i, text in enumerate(test_texts, 1):
        fixed = fix_arabic_text_simple(text)
        print(f"{i}. {fixed}")

if __name__ == "__main__":
    main()
