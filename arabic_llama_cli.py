#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
واجهة التحكم الرئيسية لنظام اللاما العربي
Main CLI Control Interface for Arabic Llama System
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# إضافة مكتبات إضافية للواجهة
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.layout import Layout
    from rich.live import Live
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

class ArabicLlamaCLI:
    def __init__(self):
        if RICH_AVAILABLE:
            self.console = Console()
        self.models_dir = Path("models")
        self.training_dir = Path("training_data")
        self.results_dir = Path("results")
        
        # إنشاء المجلدات
        self.models_dir.mkdir(exist_ok=True)
        self.training_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        
        self.available_models = [
            "llama3.2:1b",
            "llama3.2:3b", 
            "llama3.1:8b",
            "arabic-assistant-1b"
        ]
        
    def print_header(self):
        """طباعة رأس الواجهة"""
        if RICH_AVAILABLE:
            header = Panel.fit(
                "[bold blue]🦙 واجهة التحكم في نظام اللاما العربي[/bold blue]\n"
                "[yellow]Arabic Llama Control Interface[/yellow]\n"
                f"[green]التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}[/green]",
                border_style="blue"
            )
            self.console.print(header)
        else:
            print("=" * 60)
            print("🦙 واجهة التحكم في نظام اللاما العربي")
            print("Arabic Llama Control Interface")
            print(f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            print("=" * 60)
    
    def show_system_status(self):
        """عرض حالة النظام"""
        if RICH_AVAILABLE:
            table = Table(title="🔧 حالة النظام - System Status")
            table.add_column("المكون", style="cyan")
            table.add_column("الحالة", style="green")
            table.add_column("التفاصيل", style="yellow")
            
            # فحص Ollama
            ollama_status = self.check_ollama()
            table.add_row("Ollama", 
                         "✅ يعمل" if ollama_status else "❌ متوقف",
                         "خدمة تشغيل النماذج")
            
            # فحص النماذج
            models = self.get_installed_models()
            table.add_row("النماذج المثبتة", 
                         f"✅ {len(models)}" if models else "❌ لا يوجد",
                         f"{', '.join(models[:3])}" if models else "لا توجد نماذج")
            
            # فحص ملفات التدريب
            training_files = list(self.training_dir.glob("*.txt")) + list(self.training_dir.glob("*.jsonl"))
            table.add_row("ملفات التدريب", 
                         f"✅ {len(training_files)}" if training_files else "❌ لا يوجد",
                         f"{len(training_files)} ملف")
            
            # فحص المساحة
            import shutil
            free_space = shutil.disk_usage(".").free / (1024**3)
            table.add_row("المساحة الحرة", 
                         f"✅ {free_space:.1f} GB" if free_space > 5 else f"⚠️ {free_space:.1f} GB",
                         "مساحة القرص الصلب")
            
            self.console.print(table)
        else:
            print("\n🔧 حالة النظام:")
            print("-" * 30)
            print(f"Ollama: {'✅ يعمل' if self.check_ollama() else '❌ متوقف'}")
            models = self.get_installed_models()
            print(f"النماذج: {'✅ ' + str(len(models)) if models else '❌ لا يوجد'}")
            training_files = list(self.training_dir.glob("*.txt")) + list(self.training_dir.glob("*.jsonl"))
            print(f"ملفات التدريب: {len(training_files)}")
    
    def check_ollama(self):
        """فحص حالة Ollama"""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def get_installed_models(self):
        """الحصول على قائمة النماذج المثبتة"""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # تخطي الرأس
                models = []
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                return models
            return []
        except:
            return []
    
    def show_main_menu(self):
        """عرض القائمة الرئيسية"""
        if RICH_AVAILABLE:
            menu_panel = Panel(
                "[bold cyan]📋 القائمة الرئيسية - Main Menu[/bold cyan]\n\n"
                "[1] 🔧 إدارة النماذج (Model Management)\n"
                "[2] 📚 معالجة النصوص العربية (Arabic Text Processing)\n"
                "[3] 🚀 تدريب النماذج (Model Training)\n"
                "[4] 💬 اختبار النماذج (Model Testing)\n"
                "[5] 📊 النتائج والتقارير (Results & Reports)\n"
                "[6] ⚙️ إعدادات النظام (System Settings)\n"
                "[7] 🔍 تشخيص المشاكل (Diagnostics)\n"
                "[8] ❓ مساعدة (Help)\n"
                "[9] 🚪 خروج (Exit)",
                border_style="green"
            )
            self.console.print(menu_panel)
        else:
            print("\n📋 القائمة الرئيسية:")
            print("1. 🔧 إدارة النماذج")
            print("2. 📚 معالجة النصوص العربية")
            print("3. 🚀 تدريب النماذج")
            print("4. 💬 اختبار النماذج")
            print("5. 📊 النتائج والتقارير")
            print("6. ⚙️ إعدادات النظام")
            print("7. 🔍 تشخيص المشاكل")
            print("8. ❓ مساعدة")
            print("9. 🚪 خروج")
    
    def model_management(self):
        """إدارة النماذج"""
        while True:
            if RICH_AVAILABLE:
                self.console.print("\n[bold blue]🔧 إدارة النماذج[/bold blue]")
                table = Table()
                table.add_column("الخيار", style="cyan")
                table.add_column("الوصف", style="white")
                
                table.add_row("1", "عرض النماذج المثبتة")
                table.add_row("2", "تحميل نموذج جديد")
                table.add_row("3", "حذف نموذج")
                table.add_row("4", "معلومات النموذج")
                table.add_row("0", "عودة للقائمة الرئيسية")
                
                self.console.print(table)
            else:
                print("\n🔧 إدارة النماذج:")
                print("1. عرض النماذج المثبتة")
                print("2. تحميل نموذج جديد")
                print("3. حذف نموذج")
                print("4. معلومات النموذج")
                print("0. عودة للقائمة الرئيسية")
            
            choice = input("\nاختر (0-4): ").strip()
            
            if choice == "1":
                self.list_installed_models()
            elif choice == "2":
                self.download_model()
            elif choice == "3":
                self.remove_model()
            elif choice == "4":
                self.show_model_info()
            elif choice == "0":
                break
            else:
                print("❌ اختيار غير صحيح")
    
    def list_installed_models(self):
        """عرض النماذج المثبتة مع التفاصيل"""
        models = self.get_installed_models()
        
        if RICH_AVAILABLE:
            if models:
                table = Table(title="📋 النماذج المثبتة")
                table.add_column("النموذج", style="cyan")
                table.add_column("الحجم", style="yellow")
                table.add_column("التاريخ", style="green")
                table.add_column("الحالة", style="blue")
                
                for model in models:
                    # محاولة الحصول على معلومات إضافية
                    size = self.get_model_size(model)
                    status = "✅ جاهز"
                    table.add_row(model, size, "غير محدد", status)
                
                self.console.print(table)
            else:
                self.console.print("[red]❌ لا توجد نماذج مثبتة[/red]")
        else:
            print("\n📋 النماذج المثبتة:")
            if models:
                for i, model in enumerate(models, 1):
                    print(f"{i}. {model}")
            else:
                print("❌ لا توجد نماذج مثبتة")
    
    def get_model_size(self, model_name):
        """الحصول على حجم النموذج"""
        try:
            result = subprocess.run(['ollama', 'show', model_name], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # محاولة استخراج الحجم من المخرجات
                return "غير محدد"
            return "غير متوفر"
        except:
            return "غير متوفر"
    
    def download_model(self):
        """تحميل نموذج جديد"""
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]📥 تحميل نموذج جديد[/bold blue]")
            
            table = Table()
            table.add_column("رقم", style="cyan")
            table.add_column("النموذج", style="yellow")
            table.add_column("الحجم", style="green")
            table.add_column("الوصف", style="white")
            
            models_info = [
                ("llama3.2:1b", "1.3 GB", "الأسرع - مناسب للاختبار"),
                ("llama3.2:3b", "2.0 GB", "متوازن - جودة جيدة"),
                ("llama3.1:8b", "4.7 GB", "جودة عالية - يحتاج ذاكرة أكبر"),
                ("llama3.1:70b", "40 GB", "أفضل جودة - يحتاج موارد كبيرة")
            ]
            
            for i, (model, size, desc) in enumerate(models_info, 1):
                table.add_row(str(i), model, size, desc)
            
            self.console.print(table)
            
            choice = Prompt.ask("اختر رقم النموذج (1-4)", choices=["1", "2", "3", "4"])
            model_name = models_info[int(choice)-1][0]
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task(f"جاري تحميل {model_name}...", total=None)
                result = subprocess.run(['ollama', 'pull', model_name])
                progress.remove_task(task)
            
            if result.returncode == 0:
                self.console.print(f"[green]✅ تم تحميل {model_name} بنجاح![/green]")
            else:
                self.console.print(f"[red]❌ فشل تحميل {model_name}[/red]")
        else:
            print("\n📥 النماذج المتاحة:")
            models_info = [
                ("llama3.2:1b", "1.3 GB", "الأسرع"),
                ("llama3.2:3b", "2.0 GB", "متوازن"),
                ("llama3.1:8b", "4.7 GB", "جودة عالية"),
            ]
            
            for i, (model, size, desc) in enumerate(models_info, 1):
                print(f"{i}. {model} ({size}) - {desc}")
            
            choice = input("اختر رقم النموذج (1-3): ").strip()
            
            if choice in ["1", "2", "3"]:
                model_name = models_info[int(choice)-1][0]
                print(f"جاري تحميل {model_name}...")
                result = subprocess.run(['ollama', 'pull', model_name])
                
                if result.returncode == 0:
                    print(f"✅ تم تحميل {model_name} بنجاح!")
                else:
                    print(f"❌ فشل تحميل {model_name}")
    
    def test_model_interactive(self):
        """اختبار النموذج تفاعلياً"""
        models = self.get_installed_models()
        
        if not models:
            if RICH_AVAILABLE:
                self.console.print("[red]❌ لا توجد نماذج مثبتة[/red]")
            else:
                print("❌ لا توجد نماذج مثبتة")
            return
        
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]💬 اختبار النماذج[/bold blue]")
            
            table = Table()
            table.add_column("رقم", style="cyan")
            table.add_column("النموذج", style="yellow")
            
            for i, model in enumerate(models, 1):
                table.add_row(str(i), model)
            
            self.console.print(table)
            
            choice = Prompt.ask(f"اختر النموذج (1-{len(models)})")
            model_name = models[int(choice)-1]
            
            self.console.print(f"\n[green]🚀 بدء اختبار {model_name}[/green]")
            self.console.print("[yellow]اكتب 'خروج' للعودة للقائمة[/yellow]")
            
            while True:
                question = Prompt.ask("\n[cyan]سؤالك")
                
                if question.lower() in ['خروج', 'exit', 'quit']:
                    break
                
                # حفظ السؤال والوقت
                test_result = {
                    "model": model_name,
                    "question": question,
                    "timestamp": datetime.now().isoformat(),
                    "response": ""
                }
                
                with Live(Panel("جاري المعالجة...", border_style="yellow"), 
                         console=self.console) as live:
                    try:
                        result = subprocess.run([
                            'ollama', 'run', model_name, question
                        ], capture_output=True, text=True, timeout=60)
                        
                        if result.returncode == 0:
                            response = result.stdout.strip()
                            test_result["response"] = response
                            
                            # عرض النتيجة
                            response_panel = Panel(
                                f"[bold blue]الإجابة:[/bold blue]\n{response}",
                                title=f"🤖 {model_name}",
                                border_style="green"
                            )
                            live.update(response_panel)
                            
                            # حفظ النتيجة
                            self.save_test_result(test_result)
                            
                        else:
                            live.update(Panel(
                                f"[red]❌ خطأ في النموذج: {result.stderr}[/red]",
                                border_style="red"
                            ))
                    
                    except subprocess.TimeoutExpired:
                        live.update(Panel(
                            "[red]❌ انتهت مهلة الانتظار[/red]",
                            border_style="red"
                        ))
                
                time.sleep(2)  # توقف قصير لقراءة النتيجة
        else:
            print("\n💬 النماذج المتاحة:")
            for i, model in enumerate(models, 1):
                print(f"{i}. {model}")
            
            choice = input(f"اختر النموذج (1-{len(models)}): ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(models):
                model_name = models[int(choice)-1]
                print(f"\n🚀 اختبار {model_name}")
                print("اكتب 'خروج' للعودة")
                
                while True:
                    question = input("\nسؤالك: ").strip()
                    
                    if question.lower() in ['خروج', 'exit']:
                        break
                    
                    print("جاري المعالجة...")
                    result = subprocess.run([
                        'ollama', 'run', model_name, question
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"\n🤖 الإجابة:\n{result.stdout.strip()}")
                    else:
                        print(f"❌ خطأ: {result.stderr}")
    
    def save_test_result(self, result):
        """حفظ نتائج الاختبار"""
        results_file = self.results_dir / "test_results.jsonl"
        
        with open(results_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    def show_results_reports(self):
        """عرض النتائج والتقارير"""
        if RICH_AVAILABLE:
            self.console.print("\n[bold blue]📊 النتائج والتقارير[/bold blue]")
        else:
            print("\n📊 النتائج والتقارير:")
        
        results_file = self.results_dir / "test_results.jsonl"
        
        if not results_file.exists():
            if RICH_AVAILABLE:
                self.console.print("[yellow]⚠️ لا توجد نتائج محفوظة[/yellow]")
            else:
                print("⚠️ لا توجد نتائج محفوظة")
            return
        
        # قراءة النتائج
        results = []
        with open(results_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    results.append(json.loads(line))
                except:
                    continue
        
        if RICH_AVAILABLE:
            table = Table(title=f"📋 نتائج الاختبارات ({len(results)} نتيجة)")
            table.add_column("التاريخ", style="cyan")
            table.add_column("النموذج", style="yellow")
            table.add_column("السؤال", style="white")
            table.add_column("الإجابة", style="green")
            
            for result in results[-10:]:  # آخر 10 نتائج
                timestamp = result.get('timestamp', 'غير محدد')
                if timestamp != 'غير محدد':
                    timestamp = timestamp.split('T')[0]  # التاريخ فقط
                
                question = result.get('question', '')[:30] + "..." if len(result.get('question', '')) > 30 else result.get('question', '')
                response = result.get('response', '')[:50] + "..." if len(result.get('response', '')) > 50 else result.get('response', '')
                
                table.add_row(
                    timestamp,
                    result.get('model', 'غير محدد'),
                    question,
                    response
                )
            
            self.console.print(table)
        else:
            print(f"📋 آخر {min(10, len(results))} نتائج:")
            for i, result in enumerate(results[-10:], 1):
                print(f"\n{i}. النموذج: {result.get('model', 'غير محدد')}")
                print(f"   السؤال: {result.get('question', '')[:50]}...")
                print(f"   الإجابة: {result.get('response', '')[:100]}...")
    
    def run(self):
        """تشغيل الواجهة الرئيسية"""
        try:
            # تثبيت rich إذا لم تكن متوفرة
            if not RICH_AVAILABLE:
                print("جاري تثبيت مكتبة rich لتحسين الواجهة...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'rich'])
                print("يرجى إعادة تشغيل البرنامج للاستفادة من الواجهة المحسنة")
            
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                self.print_header()
                self.show_system_status()
                self.show_main_menu()
                
                choice = input("\nاختر من القائمة (1-9): ").strip()
                
                if choice == "1":
                    self.model_management()
                elif choice == "2":
                    self.process_arabic_text()
                elif choice == "3":
                    self.train_models()
                elif choice == "4":
                    self.test_model_interactive()
                elif choice == "5":
                    self.show_results_reports()
                elif choice == "6":
                    self.system_settings()
                elif choice == "7":
                    self.run_diagnostics()
                elif choice == "8":
                    self.show_help()
                elif choice == "9":
                    if RICH_AVAILABLE:
                        if Confirm.ask("هل تريد الخروج؟"):
                            self.console.print("[green]شكراً لاستخدام النظام! 👋[/green]")
                            break
                    else:
                        confirm = input("هل تريد الخروج؟ (y/n): ")
                        if confirm.lower() in ['y', 'yes', 'نعم']:
                            print("شكراً لاستخدام النظام! 👋")
                            break
                else:
                    if RICH_AVAILABLE:
                        self.console.print("[red]❌ اختيار غير صحيح[/red]")
                    else:
                        print("❌ اختيار غير صحيح")
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            if RICH_AVAILABLE:
                self.console.print("\n[yellow]تم إيقاف البرنامج[/yellow]")
            else:
                print("\nتم إيقاف البرنامج")
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[red]خطأ: {str(e)}[/red]")
            else:
                print(f"خطأ: {str(e)}")
    
    def process_arabic_text(self):
        """معالجة النصوص العربية"""
        if RICH_AVAILABLE:
            self.console.print("[bold blue]📚 معالجة النصوص العربية[/bold blue]")
        else:
            print("📚 معالجة النصوص العربية")
        
        subprocess.run([sys.executable, 'text_data_processor.py'])
    
    def train_models(self):
        """تدريب النماذج"""
        if RICH_AVAILABLE:
            self.console.print("[bold blue]🚀 تدريب النماذج[/bold blue]")
        else:
            print("🚀 تدريب النماذج")
        
        subprocess.run([sys.executable, 'llama_finetuning.py'])
    
    def system_settings(self):
        """إعدادات النظام"""
        if RICH_AVAILABLE:
            self.console.print("[bold blue]⚙️ إعدادات النظام[/bold blue]")
        else:
            print("⚙️ إعدادات النظام")
        
        # عرض إعدادات النظام الحالية
        print("الإعدادات الحالية:")
        print("- مجلد التدريب:", self.training_dir)
        print("- مجلد النتائج:", self.results_dir)
        print("- مجلد النماذج:", self.models_dir)
    
    def run_diagnostics(self):
        """تشخيص المشاكل"""
        if RICH_AVAILABLE:
            self.console.print("[bold blue]🔍 تشخيص المشاكل[/bold blue]")
        else:
            print("🔍 تشخيص المشاكل")
        
        subprocess.run([sys.executable, 'system_check.py'])
    
    def show_help(self):
        """عرض المساعدة"""
        if RICH_AVAILABLE:
            help_text = Panel(
                "[bold blue]❓ مساعدة النظام[/bold blue]\n\n"
                "[yellow]🔧 إدارة النماذج:[/yellow] تحميل وإدارة نماذج اللاما\n"
                "[yellow]📚 معالجة النصوص:[/yellow] تحويل وإصلاح النصوص العربية\n"
                "[yellow]🚀 تدريب النماذج:[/yellow] إنشاء نماذج مخصصة\n"
                "[yellow]💬 اختبار النماذج:[/yellow] اختبار النماذج تفاعلياً\n"
                "[yellow]📊 النتائج:[/yellow] عرض نتائج الاختبارات\n"
                "[yellow]⚙️ الإعدادات:[/yellow] تخصيص إعدادات النظام\n"
                "[yellow]🔍 التشخيص:[/yellow] فحص مشاكل النظام",
                border_style="blue"
            )
            self.console.print(help_text)
        else:
            print("\n❓ مساعدة النظام:")
            print("🔧 إدارة النماذج: تحميل وإدارة نماذج اللاما")
            print("📚 معالجة النصوص: تحويل وإصلاح النصوص العربية")
            print("🚀 تدريب النماذج: إنشاء نماذج مخصصة")
            print("💬 اختبار النماذج: اختبار النماذج تفاعلياً")
            print("📊 النتائج: عرض نتائج الاختبارات")
            print("⚙️ الإعدادات: تخصيص إعدادات النظام")
            print("🔍 التشخيص: فحص مشاكل النظام")
        
        input("\nاضغط Enter للمتابعة...")
    
    def remove_model(self):
        """حذف نموذج"""
        models = self.get_installed_models()
        if not models:
            print("❌ لا توجد نماذج لحذفها")
            return
        
        print("\nالنماذج المثبتة:")
        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")
        
        choice = input(f"اختر النموذج للحذف (1-{len(models)}): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            model_name = models[int(choice)-1]
            confirm = input(f"هل تريد حذف {model_name}؟ (y/n): ")
            
            if confirm.lower() in ['y', 'yes', 'نعم']:
                result = subprocess.run(['ollama', 'rm', model_name])
                if result.returncode == 0:
                    print(f"✅ تم حذف {model_name}")
                else:
                    print(f"❌ فشل حذف {model_name}")
    
    def show_model_info(self):
        """عرض معلومات النموذج"""
        models = self.get_installed_models()
        if not models:
            print("❌ لا توجد نماذج مثبتة")
            return
        
        print("\nالنماذج المثبتة:")
        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")
        
        choice = input(f"اختر النموذج (1-{len(models)}): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            model_name = models[int(choice)-1]
            print(f"\n📋 معلومات {model_name}:")
            
            result = subprocess.run(['ollama', 'show', model_name], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(result.stdout)
            else:
                print("❌ لا يمكن الحصول على معلومات النموذج")

def main():
    """تشغيل واجهة التحكم"""
    cli = ArabicLlamaCLI()
    cli.run()

if __name__ == "__main__":
    main()
