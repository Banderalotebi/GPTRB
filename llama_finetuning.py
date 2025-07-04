"""
Fine-tuning Llama Models with Custom Data
ضبط نماذج اللاما بالبيانات المخصصة

This script provides tools for fine-tuning Llama models with your custom text data.
"""

import os
import json
import torch
from pathlib import Path
from typing import Optional, Dict, List
import subprocess

class LlamaFineTuner:
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name
        self.training_dir = Path("training_data")
        self.training_dir.mkdir(exist_ok=True)
        
    def create_modelfile(self, system_prompt: str, training_data_path: str) -> str:
        """
        Create a Modelfile for Ollama fine-tuning
        إنشاء ملف النموذج للضبط الدقيق في Ollama
        """
        modelfile_content = f"""FROM {self.model_name}

# System prompt in Arabic and English
SYSTEM \"\"\"
{system_prompt}

أنت مساعد ذكي مُدرب على بيانات مخصصة. تجيب بدقة وبأسلوب مفيد.
You are an intelligent assistant trained on custom data. You respond accurately and helpfully.
\"\"\"

# Training parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1

# Custom training data
ADAPTER {training_data_path}
"""
        
        modelfile_path = self.training_dir / "Modelfile"
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
        
        return str(modelfile_path)
    
    def fine_tune_with_ollama(self, training_file: str, custom_model_name: str, 
                             system_prompt: str = None) -> bool:
        """
        Fine-tune using Ollama's built-in capabilities
        الضبط الدقيق باستخدام إمكانيات Ollama المدمجة
        """
        if not system_prompt:
            system_prompt = "أنت مساعد ذكي مُدرب على بيانات مخصصة"
        
        print(f"🔧 Fine-tuning {self.model_name} with {training_file}")
        print(f"📝 Creating custom model: {custom_model_name}")
        
        try:
            # Create Modelfile
            modelfile_path = self.create_modelfile(system_prompt, training_file)
            print(f"✅ Created Modelfile: {modelfile_path}")
            
            # Create custom model with Ollama
            cmd = ["ollama", "create", custom_model_name, "-f", modelfile_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            print(f"✅ Successfully created custom model: {custom_model_name}")
            print("🎯 You can now use it with:")
            print(f"   ollama run {custom_model_name}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating model: {e}")
            print(f"Output: {e.stdout}")
            print(f"Error: {e.stderr}")
            return False
    
    def prepare_training_examples(self, jsonl_file: str) -> List[str]:
        """
        Convert JSONL training data to examples for the model
        تحويل بيانات التدريب إلى أمثلة للنموذج
        """
        examples = []
        
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                
                if 'messages' in data:  # Conversation format
                    conversation = ""
                    for msg in data['messages']:
                        if msg['role'] == 'user':
                            conversation += f"المستخدم: {msg['content']}\n"
                        elif msg['role'] == 'assistant':
                            conversation += f"المساعد: {msg['content']}\n"
                    examples.append(conversation)
                
                elif 'instruction' in data:  # Instruction format
                    example = f"التعليمات: {data['instruction']}\n"
                    if 'input' in data and data['input']:
                        example += f"المدخل: {data['input']}\n"
                    example += f"الإخراج: {data['output']}\n"
                    examples.append(example)
                
                elif 'prompt' in data:  # Completion format
                    example = f"المطلوب: {data['prompt']}\nالإجابة: {data['completion']}\n"
                    examples.append(example)
        
        return examples
    
    def test_custom_model(self, model_name: str, test_prompts: List[str]) -> Dict:
        """
        Test the custom model with sample prompts
        اختبار النموذج المخصص بعينات
        """
        from llama_api import LlamaAPI
        
        api = LlamaAPI()
        results = {}
        
        print(f"🧪 Testing custom model: {model_name}")
        print("=" * 40)
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\nTest {i}: {prompt}")
            print("-" * 30)
            
            try:
                response = api.generate(
                    model=model_name,
                    prompt=prompt,
                    options={"temperature": 0.7}
                )
                
                answer = response['response']
                print(f"Response: {answer}")
                results[f"test_{i}"] = {
                    "prompt": prompt,
                    "response": answer,
                    "success": True
                }
                
            except Exception as e:
                print(f"Error: {e}")
                results[f"test_{i}"] = {
                    "prompt": prompt,
                    "error": str(e),
                    "success": False
                }
        
        return results

def create_sample_training_data():
    """Create sample training data in Arabic"""
    sample_conversations = [
        {
            "messages": [
                {"role": "system", "content": "أنت مساعد ذكي متخصص في التكنولوجيا"},
                {"role": "user", "content": "ما هو الذكاء الاصطناعي؟"},
                {"role": "assistant", "content": "الذكاء الاصطناعي هو مجال في علوم الحاسوب يهدف إلى إنشاء أنظمة قادرة على أداء مهام تتطلب عادة ذكاءً بشرياً، مثل التعلم واتخاذ القرارات وحل المشكلات."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "أنت مساعد ذكي متخصص في التكنولوجيا"},
                {"role": "user", "content": "كيف يعمل التعلم الآلي؟"},
                {"role": "assistant", "content": "التعلم الآلي يعمل من خلال تدريب النماذج على كميات كبيرة من البيانات لتتعلم الأنماط والعلاقات، ثم تستخدم هذه المعرفة للتنبؤ أو اتخاذ قرارات بشأن بيانات جديدة."}
            ]
        }
    ]
    
    # Save sample data
    training_dir = Path("training_data")
    training_dir.mkdir(exist_ok=True)
    
    sample_file = training_dir / "sample_conversations.jsonl"
    with open(sample_file, 'w', encoding='utf-8') as f:
        for conv in sample_conversations:
            f.write(json.dumps(conv, ensure_ascii=False) + '\n')
    
    print(f"✅ Created sample training data: {sample_file}")
    return str(sample_file)

def main():
    print("🦙 ضبط نماذج اللاما بالبيانات المخصصة")
    print("Llama Fine-tuning with Custom Data")
    print("=" * 50)
    
    fine_tuner = LlamaFineTuner()
    
    print("\nاختر ما تريد فعله:")
    print("1. إنشاء بيانات تدريب عينة (Create sample training data)")
    print("2. ضبط نموذج بملف موجود (Fine-tune with existing file)")
    print("3. اختبار نموذج مخصص (Test custom model)")
    print("4. خروج (Exit)")
    
    choice = input("\nاختر رقماً (1-4): ").strip()
    
    if choice == "1":
        sample_file = create_sample_training_data()
        print(f"\n📁 ملف العينة: {sample_file}")
        print("يمكنك الآن استخدامه للضبط الدقيق")
    
    elif choice == "2":
        # List available training files
        training_files = list(Path("training_data").glob("*.jsonl"))
        
        if not training_files:
            print("❌ لا توجد ملفات تدريب. استخدم text_data_processor.py أولاً")
            return
        
        print("\nملفات التدريب المتاحة:")
        for i, file in enumerate(training_files, 1):
            print(f"{i}. {file.name}")
        
        try:
            file_choice = int(input("اختر رقم الملف: ")) - 1
            selected_file = training_files[file_choice]
            
            custom_name = input("اسم النموذج المخصص: ").strip()
            if not custom_name:
                custom_name = f"custom-llama-{selected_file.stem}"
            
            system_prompt = input("النظام الأساسي (اختياري): ").strip()
            
            success = fine_tuner.fine_tune_with_ollama(
                str(selected_file), 
                custom_name, 
                system_prompt if system_prompt else None
            )
            
            if success:
                print(f"\n🎉 تم إنشاء النموذج المخصص: {custom_name}")
                
        except (ValueError, IndexError):
            print("❌ اختيار غير صحيح")
    
    elif choice == "3":
        model_name = input("اسم النموذج المخصص للاختبار: ").strip()
        
        test_prompts = [
            "اشرح لي مفهوم البرمجة",
            "ما هي أفضل لغات البرمجة؟",
            "كيف أتعلم الذكاء الاصطناعي؟"
        ]
        
        results = fine_tuner.test_custom_model(model_name, test_prompts)
        
        print(f"\n📊 نتائج الاختبار:")
        success_count = sum(1 for r in results.values() if r.get('success'))
        print(f"نجح {success_count} من {len(results)} اختبارات")
    
    elif choice == "4":
        print("وداعاً! 👋")
    
    else:
        print("❌ اختيار غير صحيح")

if __name__ == "__main__":
    main()
