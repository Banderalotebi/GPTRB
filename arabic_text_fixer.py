#!/usr/bin/env python3
"""
Arabic Text Fixer - حل مشكلة النصوص العربية المعكوسة
يحل مشكلة الأحرف العربية المفككة والمعكوسة في Python
"""

import os
import sys

# تثبيت المكتبات المطلوبة إذا لم تكن موجودة
def install_arabic_libs():
    """تثبيت مكتبات معالجة النصوص العربية"""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return True
    except ImportError:
        print("📦 تثبيت مكتبات معالجة النصوص العربية...")
        print("Installing Arabic text processing libraries...")
        
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "arabic-reshaper", "python-bidi"])
        
        print("✅ تم تثبيت المكتبات بنجاح!")
        return True

# تأكد من تثبيت المكتبات
install_arabic_libs()

import arabic_reshaper
from bidi.algorithm import get_display

class ArabicTextProcessor:
    """معالج النصوص العربية لحل مشاكل العرض"""
    
    def __init__(self):
        self.reshaper = arabic_reshaper.ArabicReshaper()
    
    def fix_arabic_text(self, text):
        """
        إصلاح النص العربي المعكوس أو المفكك
        Fix reversed or broken Arabic text
        """
        if not text:
            return text
        
        try:
            # إعادة تشكيل الأحرف العربية
            reshaped_text = self.reshaper.reshape(text)
            
            # ضبط اتجاه النص (من اليمين إلى اليسار)
            bidi_text = get_display(reshaped_text)
            
            return bidi_text
        except Exception as e:
            print(f"خطأ في معالجة النص: {e}")
            return text
    
    def process_file(self, input_file, output_file=None):
        """
        معالجة ملف نصي وإصلاح النصوص العربية فيه
        Process a text file and fix Arabic texts
        """
        if not output_file:
            name, ext = os.path.splitext(input_file)
            output_file = f"{name}_fixed{ext}"
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # إصلاح النص
            fixed_content = self.fix_arabic_text(content)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"✅ تم إصلاح الملف: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ خطأ في معالجة الملف {input_file}: {e}")
            return None
    
    def test_arabic_display(self):
        """اختبار عرض النصوص العربية"""
        test_texts = [
            "مرحباً بالعالم",
            "الذكاء الاصطناعي والتعلم الآلي",
            "البرمجة وتطوير البرمجيات",
            "نماذج اللغة الكبيرة مثل GPT و Llama",
            "تدريب النماذج على النصوص العربية"
        ]
        
        print("🧪 اختبار عرض النصوص العربية:")
        print("Testing Arabic text display:")
        print("=" * 50)
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n{i}. النص الأصلي: {text}")
            fixed_text = self.fix_arabic_text(text)
            print(f"   النص المُصلح: {fixed_text}")
            print(f"   Original: {text}")
            print(f"   Fixed: {fixed_text}")

def fix_arabic_in_terminal():
    """إصلاح عرض النصوص العربية في Terminal"""
    print("🔧 إعداد Terminal لعرض النصوص العربية...")
    
    # تحقق من دعم UTF-8
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'ar_SA.UTF-8')
        print("✅ تم تعيين اللغة العربية")
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            print("✅ تم تعيين UTF-8")
        except:
            print("⚠️ قد تحتاج لتثبيت دعم اللغات")
    
    # تعيين متغيرات البيئة
    os.environ['LANG'] = 'en_US.UTF-8'
    os.environ['LC_ALL'] = 'en_US.UTF-8'
    
    print("✅ تم إعداد متغيرات البيئة لدعم UTF-8")

def main():
    print("🔤 أداة إصلاح النصوص العربية")
    print("Arabic Text Fixer Tool")
    print("=" * 40)
    
    # إعداد Terminal
    fix_arabic_in_terminal()
    
    # إنشاء معالج النصوص
    processor = ArabicTextProcessor()
    
    print("\nاختر ما تريد فعله:")
    print("Choose what you want to do:")
    print("1. اختبار عرض النصوص العربية (Test Arabic display)")
    print("2. إصلاح ملف نصي (Fix a text file)")
    print("3. إصلاح نص مُدخل (Fix input text)")
    print("4. إصلاح جميع ملفات التدريب (Fix all training files)")
    print("5. خروج (Exit)")
    
    while True:
        choice = input("\nاختر رقماً (1-5): ").strip()
        
        if choice == '1':
            processor.test_arabic_display()
            
        elif choice == '2':
            file_path = input("مسار الملف: ")
            if os.path.exists(file_path):
                processor.process_file(file_path)
            else:
                print("❌ الملف غير موجود")
                
        elif choice == '3':
            text = input("أدخل النص العربي: ")
            fixed = processor.fix_arabic_text(text)
            print(f"النص المُصلح: {fixed}")
            
        elif choice == '4':
            # إصلاح جميع ملفات التدريب
            training_dir = "training_data"
            if os.path.exists(training_dir):
                for file in os.listdir(training_dir):
                    if file.endswith(('.txt', '.md')):
                        file_path = os.path.join(training_dir, file)
                        processor.process_file(file_path)
            else:
                print("❌ مجلد التدريب غير موجود")
                
        elif choice == '5':
            print("وداعاً! 👋")
            break
            
        else:
            print("❌ اختيار غير صحيح")

if __name__ == "__main__":
    main()
