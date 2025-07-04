#!/usr/bin/env python3
"""
Arabic Books Processor for Llama Training
معالج الكتب العربية لتدريب نماذج اللاما

This script processes Arabic books and texts for training Llama models.
يعالج هذا السكريبت الكتب والنصوص العربية لتدريب نماذج اللاما
"""

import os
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import argparse

# Arabic text processing
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
    print("✅ Arabic text processing libraries loaded successfully")
except ImportError:
    ARABIC_SUPPORT = False
    print("❌ Arabic libraries not found")

class ArabicBooksProcessor:
    def __init__(self, data_dir: str = "training_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Arabic text patterns
        self.arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+')
        
    def clone_arabic_repo(self, repo_url: str = "git@github.com:Banderalotebi/arb.git") -> bool:
        """
        Clone the Arabic books repository
        استنساخ مستودع الكتب العربية
        """
        repo_name = "arb"
        
        if Path(repo_name).exists():
            print(f"✅ Repository {repo_name} already exists")
            return True
            
        print(f"📥 Cloning Arabic books repository...")
        
        try:
            # Try HTTPS first (more compatible)
            https_url = "https://github.com/Banderalotebi/arb.git"
            result = subprocess.run(
                ["git", "clone", https_url], 
                capture_output=True, text=True, check=True
            )
            print(f"✅ Successfully cloned repository to {repo_name}/")
            return True
            
        except subprocess.CalledProcessError:
            try:
                # Fallback to SSH
                result = subprocess.run(
                    ["git", "clone", repo_url], 
                    capture_output=True, text=True, check=True
                )
                print(f"✅ Successfully cloned repository to {repo_name}/")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to clone repository: {e}")
                print("Please ensure you have git installed and access to the repository")
                return False
    
    def copy_training_files(self, source_path: str = None) -> List[Path]:
        """
        Copy text files from desktop/training or specified path
        نسخ الملفات النصية من مجلد التدريب
        """
        possible_paths = []
        
        if source_path:
            possible_paths.append(source_path)
        
        # Add common paths
        possible_paths.extend([
            "desktop/training",
            "Desktop/training", 
            os.path.expanduser("~/Desktop/training"),
            os.path.expanduser("~/desktop/training"),
            "./arb",  # Cloned repository
            "../arb"
        ])
        
        source_dir = None
        for path in possible_paths:
            if os.path.exists(path):
                source_dir = Path(path)
                break
        
        if not source_dir:
            print("❌ Training files directory not found")
            print("Possible locations checked:")
            for path in possible_paths:
                print(f"  - {path}")
            return []
        
        print(f"📁 Found training files in: {source_dir}")
        
        # Find all text files recursively
        text_extensions = ['.txt', '.md', '.pdf', '.docx', '.doc', '.rtf']
        copied_files = []
        
        for ext in text_extensions:
            files = list(source_dir.rglob(f"*{ext}"))
            for file_path in files:
                if file_path.is_file():
                    try:
                        dest_name = f"{file_path.parent.name}_{file_path.name}"
                        dest_path = self.data_dir / dest_name
                        
                        # Copy and convert to UTF-8 text
                        if ext == '.txt' or ext == '.md':
                            content = self._read_text_file(file_path)
                        else:
                            content = self._extract_text_from_file(file_path)
                        
                        if content and self._contains_arabic(content):
                            # Process Arabic text
                            processed_content = self._process_arabic_text(content)
                            
                            with open(dest_path, 'w', encoding='utf-8') as f:
                                f.write(processed_content)
                            
                            copied_files.append(dest_path)
                            print(f"  ✅ {file_path.name} → {dest_name}")
                        
                    except Exception as e:
                        print(f"  ❌ Error processing {file_path.name}: {e}")
        
        print(f"\n🎉 Copied {len(copied_files)} Arabic text files")
        return copied_files
    
    def _read_text_file(self, file_path: Path) -> str:
        """Read text file with multiple encoding attempts"""
        encodings = ['utf-8', 'utf-16', 'cp1256', 'iso-8859-6']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        
        # Last resort - ignore errors
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            return ""
    
    def _extract_text_from_file(self, file_path: Path) -> str:
        """Extract text from various file formats"""
        ext = file_path.suffix.lower()
        
        if ext == '.pdf':
            return self._extract_from_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self._extract_from_word(file_path)
        elif ext == '.rtf':
            return self._extract_from_rtf(file_path)
        else:
            return self._read_text_file(file_path)
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF (placeholder - requires PyPDF2)"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except ImportError:
            print(f"⚠️ PyPDF2 not installed, skipping PDF: {file_path.name}")
            return ""
        except Exception as e:
            print(f"❌ Error reading PDF {file_path.name}: {e}")
            return ""
    
    def _extract_from_word(self, file_path: Path) -> str:
        """Extract text from Word documents (placeholder - requires python-docx)"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            print(f"⚠️ python-docx not installed, skipping Word doc: {file_path.name}")
            return ""
        except Exception as e:
            print(f"❌ Error reading Word doc {file_path.name}: {e}")
            return ""
    
    def _extract_from_rtf(self, file_path: Path) -> str:
        """Extract text from RTF files"""
        # Simple RTF text extraction
        try:
            content = self._read_text_file(file_path)
            # Remove RTF formatting codes (basic)
            text = re.sub(r'\\[a-z]+\d*', ' ', content)
            text = re.sub(r'[{}]', '', text)
            return text
        except:
            return ""
    
    def _contains_arabic(self, text: str) -> bool:
        """Check if text contains Arabic characters"""
        return bool(self.arabic_pattern.search(text))
    
    def _process_arabic_text(self, text: str) -> str:
        """Process Arabic text for better display and processing"""
        if not ARABIC_SUPPORT:
            return text
        
        try:
            # Clean up the text
            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
            text = text.strip()
            
            # Reshape Arabic text if needed
            if self._needs_reshaping(text):
                reshaped = arabic_reshaper.reshape(text)
                return get_display(reshaped)
            
            return text
        except Exception as e:
            print(f"⚠️ Error processing Arabic text: {e}")
            return text
    
    def _needs_reshaping(self, text: str) -> bool:
        """Check if Arabic text needs reshaping"""
        # Simple heuristic - if text contains Arabic and appears broken
        return bool(self.arabic_pattern.search(text))
    
    def analyze_arabic_corpus(self) -> Dict:
        """
        Analyze the Arabic text corpus
        تحليل مجموعة النصوص العربية
        """
        files = list(self.data_dir.glob("*.txt"))
        
        if not files:
            return {"error": "No text files found"}
        
        analysis = {
            "total_files": len(files),
            "files": [],
            "total_characters": 0,
            "total_words": 0,
            "total_arabic_words": 0,
            "total_lines": 0,
            "languages_detected": set(),
            "sample_texts": []
        }
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                arabic_words = len(self.arabic_pattern.findall(content))
                total_words = len(content.split())
                
                file_info = {
                    "name": file_path.name,
                    "size_bytes": file_path.stat().st_size,
                    "characters": len(content),
                    "words": total_words,
                    "arabic_words": arabic_words,
                    "arabic_percentage": (arabic_words / total_words * 100) if total_words > 0 else 0,
                    "lines": len(content.splitlines()),
                    "preview": content[:300] + "..." if len(content) > 300 else content
                }
                
                analysis["files"].append(file_info)
                analysis["total_characters"] += file_info["characters"]
                analysis["total_words"] += file_info["words"]
                analysis["total_arabic_words"] += arabic_words
                analysis["total_lines"] += file_info["lines"]
                
                # Detect languages
                if arabic_words > 0:
                    analysis["languages_detected"].add("Arabic")
                if total_words > arabic_words:
                    analysis["languages_detected"].add("Other")
                
                # Sample texts for training preview
                sentences = content.split('.')[:3]
                analysis["sample_texts"].extend([s.strip() for s in sentences if s.strip()])
                
            except Exception as e:
                print(f"❌ Error analyzing {file_path.name}: {e}")
        
        analysis["languages_detected"] = list(analysis["languages_detected"])
        analysis["arabic_percentage"] = (analysis["total_arabic_words"] / analysis["total_words"] * 100) if analysis["total_words"] > 0 else 0
        
        return analysis
    
    def prepare_arabic_training_data(self, format_type: str = "conversation") -> str:
        """
        Prepare Arabic texts for Llama training
        إعداد النصوص العربية لتدريب اللاما
        """
        files = list(self.data_dir.glob("*.txt"))
        
        if not files:
            return None
        
        if format_type == "conversation":
            return self._prepare_arabic_conversation_format(files)
        elif format_type == "instruction":
            return self._prepare_arabic_instruction_format(files)
        elif format_type == "completion":
            return self._prepare_arabic_completion_format(files)
        else:
            print("❌ نوع غير معروف. استخدم: conversation, instruction, أو completion")
            return None
    
    def _prepare_arabic_conversation_format(self, files: List[Path]) -> str:
        """Prepare Arabic conversation format"""
        conversations = []
        
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            chunks = self._split_arabic_text(content, max_length=400)
            
            for chunk in chunks:
                if self._contains_arabic(chunk) and len(chunk.strip()) > 50:
                    conversation = {
                        "messages": [
                            {
                                "role": "system",
                                "content": f"أنت مساعد ذكي متخصص في اللغة العربية والأدب العربي. لديك معرفة واسعة من الكتب العربية. المصدر: {file_path.name}"
                            },
                            {
                                "role": "user", 
                                "content": f"اشرح لي هذا النص أو أجب عن أسئلة حوله: {chunk[:100]}..."
                            },
                            {
                                "role": "assistant",
                                "content": chunk
                            }
                        ]
                    }
                    conversations.append(conversation)
        
        output_file = self.data_dir / "arabic_conversations.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for conv in conversations:
                f.write(json.dumps(conv, ensure_ascii=False) + '\n')
        
        print(f"✅ تم إنشاء ملف المحادثات العربية: {output_file}")
        print(f"📊 تم توليد {len(conversations)} محادثة")
        return str(output_file)
    
    def _prepare_arabic_instruction_format(self, files: List[Path]) -> str:
        """Prepare Arabic instruction format"""
        instructions = []
        
        instruction_templates = [
            "لخص هذا النص:",
            "اشرح الفكرة الرئيسية في هذا النص:",
            "ما هي النقاط المهمة في هذا المقطع؟",
            "اكتب تعليقاً على هذا النص:",
            "ما هو موضوع هذا النص؟"
        ]
        
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            chunks = self._split_arabic_text(content, max_length=300)
            
            for chunk in chunks:
                if self._contains_arabic(chunk) and len(chunk.strip()) > 30:
                    for template in instruction_templates:
                        instruction = {
                            "instruction": template,
                            "input": chunk,
                            "output": self._generate_arabic_response(template, chunk),
                            "source": file_path.name
                        }
                        instructions.append(instruction)
        
        output_file = self.data_dir / "arabic_instructions.jsonl"
        with open(output_file, 'w', encoding='utf-8') as f:
            for inst in instructions:
                f.write(json.dumps(inst, ensure_ascii=False) + '\n')
        
        print(f"✅ تم إنشاء ملف التعليمات العربية: {output_file}")
        print(f"📊 تم توليد {len(instructions)} تعليمة")
        return str(output_file)
    
    def _split_arabic_text(self, text: str, max_length: int = 400) -> List[str]:
        """Split Arabic text into meaningful chunks"""
        # Split by sentences first
        sentences = re.split(r'[.!?؟۔]', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if current_length + len(sentence) <= max_length:
                current_chunk.append(sentence)
                current_length += len(sentence)
            else:
                if current_chunk:
                    chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = len(sentence)
        
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        
        return [chunk for chunk in chunks if len(chunk.strip()) > 20]
    
    def _generate_arabic_response(self, instruction: str, text: str) -> str:
        """Generate appropriate Arabic response based on instruction"""
        if "لخص" in instruction:
            sentences = text.split('.')
            return sentences[0] + '.' if sentences else text[:100] + "..."
        
        elif "الفكرة الرئيسية" in instruction:
            return f"الفكرة الرئيسية في هذا النص تتعلق بـ {text[:80]}..."
        
        elif "النقاط المهمة" in instruction:
            return f"النقاط المهمة تشمل: {text[:100]}..."
        
        elif "تعليق" in instruction:
            return f"هذا نص مهم يتناول {text[:60]}... ويقدم معلومات قيمة حول الموضوع."
        
        elif "موضوع" in instruction:
            return f"موضوع هذا النص يدور حول {text[:80]}..."
        
        else:
            return text[:150] + "..."

def main():
    print("📚 معالج الكتب العربية لتدريب اللاما")
    print("Arabic Books Processor for Llama Training")
    print("=" * 60)
    
    processor = ArabicBooksProcessor()
    
    while True:
        print("\nاختر ما تريد فعله:")
        print("1. استنساخ مستودع الكتب العربية (Clone Arabic books repo)")
        print("2. نسخ ملفات التدريب (Copy training files)")
        print("3. تحليل النصوص العربية (Analyze Arabic texts)")
        print("4. إعداد بيانات التدريب (Prepare training data)")
        print("5. خروج (Exit)")
        
        choice = input("\nاختر رقماً (1-5): ").strip()
        
        if choice == "1":
            repo_url = input("رابط المستودع (اتركه فارغاً للافتراضي): ").strip()
            if not repo_url:
                repo_url = "git@github.com:Banderalotebi/arb.git"
            
            success = processor.clone_arabic_repo(repo_url)
            if success:
                print("✅ تم استنساخ المستودع بنجاح")
        
        elif choice == "2":
            source_path = input("مسار ملفات التدريب (اتركه فارغاً للبحث التلقائي): ").strip()
            if not source_path:
                source_path = None
            
            copied_files = processor.copy_training_files(source_path)
            print(f"✅ تم نسخ {len(copied_files)} ملف")
        
        elif choice == "3":
            analysis = processor.analyze_arabic_corpus()
            print("\n📊 تحليل النصوص العربية:")
            print("=" * 40)
            print(f"إجمالي الملفات: {analysis.get('total_files', 0)}")
            print(f"إجمالي الكلمات: {analysis.get('total_words', 0)}")
            print(f"الكلمات العربية: {analysis.get('total_arabic_words', 0)}")
            print(f"نسبة العربية: {analysis.get('arabic_percentage', 0):.1f}%")
            print(f"اللغات المكتشفة: {', '.join(analysis.get('languages_detected', []))}")
            
            # Show file details
            if analysis.get('files'):
                print(f"\nتفاصيل الملفات:")
                for file_info in analysis['files'][:5]:  # Show first 5
                    print(f"  📄 {file_info['name']}: {file_info['words']} كلمة ({file_info['arabic_percentage']:.1f}% عربية)")
        
        elif choice == "4":
            print("\nاختر نوع التنسيق:")
            print("1. محادثة (Conversation)")
            print("2. تعليمات (Instruction)")
            print("3. إكمال (Completion)")
            
            format_choice = input("اختر (1-3): ").strip()
            format_map = {"1": "conversation", "2": "instruction", "3": "completion"}
            
            if format_choice in format_map:
                output_file = processor.prepare_arabic_training_data(format_map[format_choice])
                if output_file:
                    print(f"✅ تم إنشاء ملف التدريب: {output_file}")
                    print("🚀 يمكنك الآن استخدام llama_finetuning.py للتدريب")
        
        elif choice == "5":
            print("وداعاً! مع تحياتي 👋")
            break
        
        else:
            print("❌ اختيار غير صحيح")

if __name__ == "__main__":
    main()
