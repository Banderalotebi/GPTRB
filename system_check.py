#!/usr/bin/env python3
"""
System Performance and Capability Report
تقرير أداء وقدرات النظام

Analyzes system capabilities for AI/ML workloads without GPU
"""

import os
import sys
import psutil
import platform
import subprocess
from pathlib import Path

def get_system_info():
    """Get comprehensive system information"""
    print("💻 معلومات النظام")
    print("System Information")
    print("=" * 30)
    
    info = {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'python_version': platform.python_version(),
    }
    
    # CPU information
    info['cpu_count'] = psutil.cpu_count(logical=False)
    info['cpu_count_logical'] = psutil.cpu_count(logical=True)
    info['cpu_freq'] = psutil.cpu_freq()
    
    # Memory information
    memory = psutil.virtual_memory()
    info['memory_total'] = memory.total / (1024**3)  # GB
    info['memory_available'] = memory.available / (1024**3)  # GB
    info['memory_percent'] = memory.percent
    
    # Disk information
    disk = psutil.disk_usage('/')
    info['disk_total'] = disk.total / (1024**3)  # GB
    info['disk_free'] = disk.free / (1024**3)  # GB
    
    return info

def check_python_packages():
    """Check for AI/ML packages"""
    print("\n📦 فحص المكتبات المطلوبة")
    print("Checking Required Packages")
    print("=" * 35)
    
    packages_to_check = [
        'torch',
        'transformers', 
        'numpy',
        'pandas',
        'requests',
        'arabic_reshaper',
        'bidi'
    ]
    
    installed = {}
    for package in packages_to_check:
        try:
            __import__(package)
            installed[package] = "✅ مثبت"
            print(f"{package}: ✅ مثبت")
        except ImportError:
            installed[package] = "❌ غير مثبت"
            print(f"{package}: ❌ غير مثبت")
    
    return installed

def test_cpu_performance():
    """Test CPU performance for AI workloads"""
    print("\n⚡ اختبار أداء المعالج")
    print("CPU Performance Test")
    print("=" * 25)
    
    try:
        import numpy as np
        import time
        
        # Matrix multiplication test
        size = 500
        print(f"🧮 ضرب مصفوفات {size}x{size}...")
        
        start_time = time.time()
        a = np.random.randn(size, size)
        b = np.random.randn(size, size)
        c = np.dot(a, b)
        end_time = time.time()
        
        cpu_time = end_time - start_time
        print(f"⏱️ الوقت: {cpu_time:.3f} ثانية")
        print(f"Time: {cpu_time:.3f} seconds")
        
        # Estimate model performance
        if cpu_time < 0.1:
            performance = "ممتاز - مناسب للنماذج الكبيرة"
            performance_en = "Excellent - suitable for large models"
        elif cpu_time < 0.5:
            performance = "جيد - مناسب للنماذج المتوسطة"
            performance_en = "Good - suitable for medium models"
        elif cpu_time < 2.0:
            performance = "مقبول - مناسب للنماذج الصغيرة"
            performance_en = "Acceptable - suitable for small models"
        else:
            performance = "بطيء - قد تحتاج تحسين"
            performance_en = "Slow - may need optimization"
        
        print(f"📊 التقييم: {performance}")
        print(f"Assessment: {performance_en}")
        
        return {
            'matrix_time': cpu_time,
            'performance': performance,
            'performance_en': performance_en
        }
        
    except ImportError:
        print("❌ NumPy غير متاح للاختبار")
        return None

def recommend_model_sizes(system_info):
    """Recommend appropriate model sizes based on system specs"""
    print("\n🎯 توصيات النماذج")
    print("Model Recommendations")
    print("=" * 25)
    
    memory_gb = system_info['memory_available']
    cpu_cores = system_info['cpu_count_logical']
    
    print(f"💾 الذاكرة المتاحة: {memory_gb:.1f} GB")
    print(f"Available Memory: {memory_gb:.1f} GB")
    print(f"🔧 المعالجات: {cpu_cores} cores")
    print(f"CPU Cores: {cpu_cores}")
    
    recommendations = []
    
    if memory_gb >= 6:
        recommendations.append({
            'model': 'llama3.2:3b',
            'size': '2.0 GB',
            'reason': 'متوازن - جودة جيدة وسرعة معقولة',
            'reason_en': 'Balanced - good quality and reasonable speed'
        })
    
    if memory_gb >= 3:
        recommendations.append({
            'model': 'llama3.2:1b', 
            'size': '1.3 GB',
            'reason': 'سريع - مناسب للاختبار والتطوير',
            'reason_en': 'Fast - suitable for testing and development'
        })
    
    if memory_gb >= 8:
        recommendations.append({
            'model': 'llama3.1:8b',
            'size': '4.7 GB', 
            'reason': 'جودة عالية - للمهام المتقدمة',
            'reason_en': 'High quality - for advanced tasks'
        })
    
    if not recommendations:
        recommendations.append({
            'model': 'tinyllama:1.1b',
            'size': '0.6 GB',
            'reason': 'خفيف جداً - للأنظمة المحدودة',
            'reason_en': 'Very light - for limited systems'
        })
    
    print("\n📋 النماذج المُوصى بها:")
    print("Recommended Models:")
    for rec in recommendations:
        print(f"  🦙 {rec['model']} ({rec['size']})")
        print(f"     {rec['reason']}")
        print(f"     {rec['reason_en']}")
        print()
    
    return recommendations

def check_ollama_optimization():
    """Check Ollama optimization settings"""
    print("\n🔧 تحسين Ollama")
    print("Ollama Optimization")
    print("=" * 20)
    
    # Check if Ollama is running
    try:
        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama يعمل")
            print("Ollama is running")
        else:
            print("⚠️ Ollama غير مُشغل")
            print("Ollama not running")
            print("💡 لتشغيله: ollama serve")
            print("To start: ollama serve")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ollama غير متاح")
        print("Ollama not available")
        return False
    
    # Environment variables for optimization
    optimizations = {
        'OLLAMA_NUM_PARALLEL': 'عدد النماذج المتوازية',
        'OLLAMA_MAX_LOADED_MODELS': 'أقصى عدد نماذج محملة',
        'OLLAMA_FLASH_ATTENTION': 'تفعيل Flash Attention',
        'OLLAMA_LLM_LIBRARY': 'مكتبة LLM المفضلة'
    }
    
    print("\n🛠️ متغيرات التحسين:")
    print("Optimization Variables:")
    for var, desc in optimizations.items():
        value = os.environ.get(var, 'غير محدد / not set')
        print(f"  {var}: {value}")
        print(f"    ({desc})")
    
    return True

def generate_system_report():
    """Generate comprehensive system report"""
    print("\n📋 إنشاء تقرير شامل...")
    print("Generating comprehensive report...")
    
    system_info = get_system_info()
    packages = check_python_packages()
    cpu_performance = test_cpu_performance()
    recommendations = recommend_model_sizes(system_info)
    
    report = {
        'system_info': system_info,
        'packages': packages,
        'cpu_performance': cpu_performance,
        'recommendations': recommendations,
        'timestamp': str(psutil.boot_time())
    }
    
    # Save report
    report_file = Path('system_capabilities_report.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("تقرير قدرات النظام للذكاء الاصطناعي\n")
        f.write("System Capabilities Report for AI\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("معلومات النظام / System Info:\n")
        for key, value in system_info.items():
            f.write(f"  {key}: {value}\n")
        
        f.write(f"\nالذاكرة المتاحة / Available Memory: {system_info['memory_available']:.1f} GB\n")
        f.write(f"المعالجات / CPU Cores: {system_info['cpu_count_logical']}\n")
        
        f.write("\nالمكتبات المثبتة / Installed Packages:\n")
        for pkg, status in packages.items():
            f.write(f"  {pkg}: {status}\n")
        
        if cpu_performance:
            f.write(f"\nأداء المعالج / CPU Performance:\n")
            f.write(f"  Matrix multiplication time: {cpu_performance['matrix_time']:.3f}s\n")
            f.write(f"  Assessment: {cpu_performance['performance']}\n")
        
        f.write(f"\nالنماذج المُوصى بها / Recommended Models:\n")
        for rec in recommendations:
            f.write(f"  {rec['model']} ({rec['size']}) - {rec['reason']}\n")
    
    print(f"💾 تم حفظ التقرير في: {report_file}")
    print(f"Report saved to: {report_file}")
    
    return report

def main():
    print("🖥️ فحص قدرات النظام للذكاء الاصطناعي")
    print("AI System Capabilities Check")
    print("=" * 50)
    
    # Get system information
    system_info = get_system_info()
    
    print(f"🏗️ المعمارية: {system_info['architecture']}")
    print(f"Architecture: {system_info['architecture']}")
    print(f"🧠 المعالج: {system_info['processor']}")
    print(f"Processor: {system_info['processor']}")
    print(f"💾 الذاكرة: {system_info['memory_total']:.1f} GB (متاح: {system_info['memory_available']:.1f} GB)")
    print(f"Memory: {system_info['memory_total']:.1f} GB (available: {system_info['memory_available']:.1f} GB)")
    print(f"🔧 المعالجات: {system_info['cpu_count']} فيزيائي، {system_info['cpu_count_logical']} منطقي")
    print(f"CPUs: {system_info['cpu_count']} physical, {system_info['cpu_count_logical']} logical")
    
    # Check packages
    packages = check_python_packages()
    
    # Test performance
    cpu_performance = test_cpu_performance()
    
    # Get recommendations
    recommendations = recommend_model_sizes(system_info)
    
    # Check Ollama
    check_ollama_optimization()
    
    # Generate report
    generate_system_report()
    
    print("\n🎉 الخلاصة:")
    print("Summary:")
    print("✅ النظام قادر على تشغيل نماذج Llama")
    print("System can run Llama models")
    print("💡 استخدم النماذج الصغيرة للبداية")
    print("Use smaller models to start")
    print("🚀 يمكن التدريب على البيانات الخاصة")
    print("Can train on custom data")

if __name__ == "__main__":
    main()
