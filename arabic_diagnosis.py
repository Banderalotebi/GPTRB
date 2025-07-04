#!/usr/bin/env python3
"""
تشخيص سريع لمشاكل النصوص العربية
Quick diagnosis for Arabic text issues
"""

import sys
import os
import locale

def check_system_arabic_support():
    """فحص دعم النظام للنصوص العربية"""
    print("🔍 فحص دعم النظام للنصوص العربية")
    print("Checking system Arabic support")
    print("=" * 40)
    
    # فحص ترميز النظام
    print(f"1. ترميز النظام: {sys.getdefaultencoding()}")
    print(f"   System encoding: {sys.getdefaultencoding()}")
    
    # فحص متغيرات البيئة
    lang = os.environ.get('LANG', 'غير محدد')
    lc_all = os.environ.get('LC_ALL', 'غير محدد')
    print(f"2. LANG: {lang}")
    print(f"   LC_ALL: {lc_all}")
    
    # فحص اللغات المتاحة
    try:
        current_locale = locale.getlocale()
        print(f"3. اللغة الحالية: {current_locale}")
        print(f"   Current locale: {current_locale}")
    except:
        print("3. ❌ خطأ في قراءة إعدادات اللغة")
    
    # فحص دعم UTF-8
    try:
        test_arabic = "مرحباً بالعالم"
        encoded = test_arabic.encode('utf-8')
        decoded = encoded.decode('utf-8')
        if test_arabic == decoded:
            print("4. ✅ دعم UTF-8 يعمل بشكل صحيح")
        else:
            print("4. ❌ مشكلة في دعم UTF-8")
    except Exception as e:
        print(f"4. ❌ خطأ في UTF-8: {e}")
    
    return True

def test_arabic_libraries():
    """اختبار مكتبات معالجة النصوص العربية"""
    print("\n📚 فحص مكتبات معالجة النصوص العربية")
    print("Testing Arabic text processing libraries")
    print("=" * 45)
    
    # اختبار arabic_reshaper
    try:
        import arabic_reshaper
        print("1. ✅ arabic_reshaper متاح")
        
        reshaper = arabic_reshaper.ArabicReshaper()
        test_text = "مرحباً بالعالم"
        reshaped = reshaper.reshape(test_text)
        print(f"   اختبار إعادة التشكيل: {test_text} → {reshaped}")
        
    except ImportError:
        print("1. ❌ arabic_reshaper غير متاح")
        print("   تثبيت: pip install arabic-reshaper")
    except Exception as e:
        print(f"1. ⚠️ خطأ في arabic_reshaper: {e}")
    
    # اختبار python-bidi
    try:
        from bidi.algorithm import get_display
        print("2. ✅ python-bidi متاح")
        
        test_text = "Hello مرحباً World"
        bidi_text = get_display(test_text)
        print(f"   اختبار اتجاه النص: {test_text} → {bidi_text}")
        
    except ImportError:
        print("2. ❌ python-bidi غير متاح")
        print("   تثبيت: pip install python-bidi")
    except Exception as e:
        print(f"2. ⚠️ خطأ في python-bidi: {e}")

def test_terminal_display():
    """اختبار عرض النصوص في Terminal"""
    print("\n💻 اختبار عرض النصوص في Terminal")
    print("Testing terminal text display")
    print("=" * 40)
    
    test_texts = [
        "نص عربي بسيط",
        "الذكاء الاصطناعي",
        "Hello مرحباً World",
        "123 عدد ٤٥٦",
        "نماذج اللغة الكبيرة LLM"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"{i}. {text}")
        # محاولة عرض النص بترميزات مختلفة
        try:
            encoded_utf8 = text.encode('utf-8').decode('utf-8')
            print(f"   UTF-8: {encoded_utf8}")
        except:
            print("   UTF-8: ❌ فشل")

def fix_terminal_settings():
    """إصلاح إعدادات Terminal للنصوص العربية"""
    print("\n🔧 إصلاح إعدادات Terminal")
    print("Fixing terminal settings")
    print("=" * 35)
    
    # تعيين متغيرات البيئة
    os.environ['LANG'] = 'en_US.UTF-8'
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    
    print("✅ تم تعيين LANG=en_US.UTF-8")
    print("✅ تم تعيين LC_ALL=en_US.UTF-8")
    
    # محاولة تعيين اللغة العربية
    try:
        import locale
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        print("✅ تم تعيين locale بنجاح")
    except Exception as e:
        print(f"⚠️ تحذير في locale: {e}")
    
    print("\n📋 نصائح إضافية:")
    print("1. تأكد من أن Terminal يدعم UTF-8")
    print("2. استخدم خط يدعم العربية (مثل Noto Sans Arabic)")
    print("3. في VS Code: File → Preferences → Settings → search 'encoding'")

def comprehensive_test():
    """اختبار شامل مع الإصلاح"""
    print("🌟 اختبار شامل للنصوص العربية مع الإصلاح")
    print("Comprehensive Arabic text test with fixes")
    print("=" * 50)
    
    # النص الاختباري
    original_text = "مرحباً بكم في عالم الذكاء الاصطناعي ونماذج اللغة الكبيرة"
    
    print(f"النص الأصلي: {original_text}")
    print(f"Original: {original_text}")
    
    # محاولة إصلاح النص
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        
        # إعادة تشكيل
        reshaper = arabic_reshaper.ArabicReshaper()
        reshaped = reshaper.reshape(original_text)
        print(f"بعد إعادة التشكيل: {reshaped}")
        
        # ضبط الاتجاه
        bidi_text = get_display(reshaped)
        print(f"النص المُصلح: {bidi_text}")
        
        # مقارنة الطول
        print(f"طول النص الأصلي: {len(original_text)}")
        print(f"طول النص المُصلح: {len(bidi_text)}")
        
        if len(original_text) == len(bidi_text):
            print("✅ الطول متطابق - الإصلاح ناجح")
        else:
            print("⚠️ الطول مختلف - قد توجد مشكلة")
            
    except Exception as e:
        print(f"❌ خطأ في الإصلاح: {e}")
        print("حاول تثبيت المكتبات: pip install arabic-reshaper python-bidi")

def main():
    print("🔤 أداة تشخيص النصوص العربية")
    print("Arabic Text Diagnosis Tool")
    print("=" * 40)
    
    # فحص النظام
    check_system_arabic_support()
    
    # فحص المكتبات
    test_arabic_libraries()
    
    # اختبار Terminal
    test_terminal_display()
    
    # إصلاح الإعدادات
    fix_terminal_settings()
    
    # اختبار شامل
    comprehensive_test()
    
    print("\n🎯 التوصيات:")
    print("1. شغل: python3 arabic_text_fixer.py لإصلاح النصوص")
    print("2. استخدم ترميز UTF-8 دائماً")
    print("3. تأكد من تثبيت: pip install arabic-reshaper python-bidi")
    print("4. في VS Code اضبط encoding على UTF-8")

if __name__ == "__main__":
    main()
