#!/usr/bin/env python3
"""
Text Data Processor for Llama Training
معالج البيانات النصية لتدريب نماذج اللاما

This script helps process text files for training or fine-tuning Llama models.
يساعد هذا السكريبت في معالجة الملفات النصية لتدريب أو ضبط نماذج اللاما
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
import argparse

# Arabic text processing libraries
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False
    print("⚠️ Arabic text processing libraries not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "arabic-reshaper", "python-bidi"])
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True

class TextDataProcessor:
    def __init__(self, data_dir: str = "training_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # إعداد معالج النصوص العربية
        if ARABIC_SUPPORT:
            self.arabic_reshaper = arabic_reshaper.ArabicReshaper()
    
    def copy_desktop_files(self, desktop_path: str = None) -> List[Path]:
        """
        Copy text files from desktop to training data directory
        نسخ الملفات النصية من سطح المكتب إلى مجلد بيانات التدريب
        """
        if not desktop_path:
            # Try common desktop paths
            possible_paths = [
                os.path.expanduser("~/Desktop"),
                os.path.expanduser("~/سطح المكتب"),
                "/mnt/c/Users/*/Desktop",  # WSL
                "/home/*/Desktop"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    desktop_path = path
                    break
        
        if not desktop_path or not os.path.exists(desktop_path):
            print("❌ Desktop path not found. Please specify the path manually.")
            return []
        
        print(f"📁 Looking for text files in: {desktop_path}")
        
        # Find text files
        text_extensions = ['.txt', '.md', '.csv', '.json', '.tsv']
        text_files = []
        
        for ext in text_extensions:
            text_files.extend(Path(desktop_path).glob(f"*{ext}"))
        
        if not text_files:
            print("❌ No text files found on desktop")
            return []
        
        print(f"📋 Found {len(text_files)} text files:")
        copied_files = []
        
        for file_path in text_files:
            print(f"  - {file_path.name}")
            
            # Copy to training data directory
            dest_path = self.data_dir / file_path.name
            try:
                with open(file_path, 'r', encoding='utf-8') as src:
                    content = src.read()
                
                with open(dest_path, 'w', encoding='utf-8') as dst:
                    dst.write(content)
                
                copied_files.append(dest_path)
                print(f"  ✅ Copied to {dest_path}")
                
            except Exception as e:
                print(f"  ❌ Error copying {file_path.name}: {e}")
        
        return copied_files
    
    def analyze_text_files(self) -> Dict:
        """
        Analyze the text files to understand the data
        تحليل الملفات النصية لفهم البيانات
        """
        files = list(self.data_dir.glob("*.txt")) + list(self.data_dir.glob("*.md"))
        
        if not files:
            return {"error": "No text files found in training_data directory"}
        
        analysis = {
            "total_files": len(files),
            "files": [],
            "total_characters": 0,
            "total_words": 0,
            "total_lines": 0
        }
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_info = {
                    "name": file_path.name,
                    "size_bytes": file_path.stat().st_size,
                    "characters": len(content),
                    "words": len(content.split()),
                    "lines": len(content.splitlines()),
                    "preview": content[:200] + "..." if len(content) > 200 else content
                }
                
                analysis["files"].append(file_info)
                analysis["total_characters"] += file_info["characters"]
                analysis["total_words"] += file_info["words"]
                analysis["total_lines"] += file_info["lines"]
                
            except Exception as e:
                print(f"❌ Error reading {file_path.name}: {e}")
        
        return analysis
    
    def prepare_training_data(self, format_type: str = "conversation") -> str:
        """
        Prepare text data for training in different formats
        إعداد البيانات النصية للتدريب بصيغ مختلفة
        """
        files = list(self.data_dir.glob("*.txt")) + list(self.data_dir.glob("*.md"))
        
        if not files:
            return None
        
        if format_type == "conversation":
            return self._prepare_conversation_format(files)
        elif format_type == "instruction":
            return self._prepare_instruction_format(files)
        elif format_type == "completion":
            return self._prepare_completion_format(files)
        else:
            print("❌ Unknown format type. Use: conversation, instruction, or completion")
            return None
    
    def _prepare_conversation_format(self, files: List[Path]) -> str:
        """Prepare data in conversation format for chat training"""
        conversations = []
        
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content into chunks
            chunks = self._split_text_into_chunks(content, max_length=500)
            
            for i, chunk in enumerate(chunks):
                conversation = {
                    "messages": [
                        {
                            "role": "system",
                            "content": f"أنت مساعد ذكي يجيب بناءً على المحتوى من الملف: {file_path.name}"
                        },
                        {
                            "role": "user", 
                            "content": f"اشرح لي المحتوى التالي أو أجب عن الأسئلة المتعلقة به: {chunk[:100]}..."
                        },
                        {
                            "role": "assistant",
                            "content": chunk
                        }
                    ]
                }
                conversations.append(conversation)
        
        output_file = self.data_dir / "conversations.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for conv in conversations:
                f.write(json.dumps(conv, ensure_ascii=False) + '\n')
        
        print(f"✅ Created conversation format: {output_file}")
        print(f"📊 Generated {len(conversations)} conversations")
        return str(output_file)
    
    def _prepare_instruction_format(self, files: List[Path]) -> str:
        """Prepare data in instruction format"""
        instructions = []
        
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create different types of instructions
            chunks = self._split_text_into_chunks(content, max_length=300)
            
            for chunk in chunks:
                # Summary instruction
                instructions.append({
                    "instruction": f"لخص المحتوى التالي من ملف {file_path.name}:",
                    "input": chunk,
                    "output": self._generate_summary(chunk)
                })
                
                # Question answering instruction
                instructions.append({
                    "instruction": "أجب عن الأسئلة بناءً على النص المُعطى:",
                    "input": f"النص: {chunk}\nالسؤال: ما الفكرة الرئيسية في هذا النص؟",
                    "output": self._extract_main_idea(chunk)
                })
        
        output_file = self.data_dir / "instructions.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for inst in instructions:
                f.write(json.dumps(inst, ensure_ascii=False) + '\n')
        
        print(f"✅ Created instruction format: {output_file}")
        print(f"📊 Generated {len(instructions)} instructions")
        return str(output_file)
    
    def _prepare_completion_format(self, files: List[Path]) -> str:
        """Prepare data in completion format"""
        completions = []
        
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into sentences or paragraphs
            sentences = re.split(r'[.!?]+', content)
            
            for i in range(len(sentences) - 1):
                if len(sentences[i].strip()) > 10 and len(sentences[i+1].strip()) > 10:
                    completion = {
                        "prompt": sentences[i].strip() + ".",
                        "completion": " " + sentences[i+1].strip() + "."
                    }
                    completions.append(completion)
        
        output_file = self.data_dir / "completions.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for comp in completions:
                f.write(json.dumps(comp, ensure_ascii=False) + '\n')
        
        print(f"✅ Created completion format: {output_file}")
        print(f"📊 Generated {len(completions)} completions")
        return str(output_file)
    
    def _split_text_into_chunks(self, text: str, max_length: int = 500) -> List[str]:
        """Split text into chunks of specified maximum length"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_chunk.append(word)
                current_length += len(word) + 1
            else:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _generate_summary(self, text: str) -> str:
        """Generate a simple summary (placeholder - can be enhanced)"""
        sentences = text.split('.')
        if len(sentences) > 1:
            return sentences[0] + '.'
        return text[:100] + "..."
    
    def _extract_main_idea(self, text: str) -> str:
        """Extract main idea (placeholder - can be enhanced)"""
        words = text.split()
        if len(words) > 10:
            return "الفكرة الرئيسية تتعلق بـ " + ' '.join(words[:15]) + "..."
        return "النص يتحدث عن " + text[:50] + "..."
    
    def fix_arabic_text(self, text: str) -> str:
        """
        إصلاح النص العربي المعكوس أو المفكك
        Fix reversed or broken Arabic text
        """
        if not text or not ARABIC_SUPPORT:
            return text
        
        try:
            # إعادة تشكيل الأحرف العربية
            reshaped_text = self.arabic_reshaper.reshape(text)
            
            # ضبط اتجاه النص (من اليمين إلى اليسار)
            bidi_text = get_display(reshaped_text)
            
            return bidi_text
        except Exception as e:
            print(f"⚠️ خطأ في معالجة النص العربي: {e}")
            return text

def main():
    parser = argparse.ArgumentParser(description="Process text files for Llama training")
    parser.add_argument("--desktop", type=str, help="Path to desktop directory")
    parser.add_argument("--format", choices=["conversation", "instruction", "completion"], 
                       default="conversation", help="Training data format")
    parser.add_argument("--analyze", action="store_true", help="Analyze text files only")
    
    args = parser.parse_args()
    
    processor = TextDataProcessor()
    
    print("🦙 معالج البيانات النصية لتدريب اللاما")
    print("Text Data Processor for Llama Training")
    print("=" * 50)
    
    # Interactive mode if no arguments
    if not any(vars(args).values()):
        print("\n1. نسخ ملفات من سطح المكتب (Copy files from desktop)")
        print("2. تحليل الملفات الموجودة (Analyze existing files)")
        print("3. إعداد بيانات التدريب (Prepare training data)")
        print("4. خروج (Exit)")
        
        choice = input("\nاختر رقماً (Choose a number): ").strip()
        
        if choice == "1":
            desktop_path = input("مسار سطح المكتب (Desktop path, press Enter for auto): ").strip()
            if not desktop_path:
                desktop_path = None
            copied_files = processor.copy_desktop_files(desktop_path)
            print(f"\n✅ تم نسخ {len(copied_files)} ملف")
            
        elif choice == "2":
            analysis = processor.analyze_text_files()
            print("\n📊 تحليل الملفات:")
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
            
        elif choice == "3":
            print("\nاختر نوع التنسيق:")
            print("1. محادثة (Conversation)")
            print("2. تعليمات (Instruction)")
            print("3. إكمال (Completion)")
            
            format_choice = input("اختر (1-3): ").strip()
            format_map = {"1": "conversation", "2": "instruction", "3": "completion"}
            
            if format_choice in format_map:
                output_file = processor.prepare_training_data(format_map[format_choice])
                if output_file:
                    print(f"\n✅ تم إنشاء ملف التدريب: {output_file}")
            
        elif choice == "4":
            print("وداعاً! 👋")
            return
    else:
        # Command line mode
        if args.desktop:
            processor.copy_desktop_files(args.desktop)
        
        if args.analyze:
            analysis = processor.analyze_text_files()
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
        else:
            processor.prepare_training_data(args.format)

if __name__ == "__main__":
    main()
