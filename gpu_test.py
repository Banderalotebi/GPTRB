#!/usr/bin/env python3
"""
GPU Detection and Testing Tool
أداة فحص واختبار كرت الرسوميات

This script detects and tests GPU capabilities for AI/ML workloads.
هذا السكريبت يفحص ويختبر قدرات كرت الرسوميات للذكاء الاصطناعي
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class GPUTester:
    def __init__(self):
        self.gpu_info = {}
        self.cuda_available = False
        self.rocm_available = False
        
    def detect_gpu_hardware(self):
        """Detect GPU hardware information"""
        print("🔍 فحص كرت الرسوميات...")
        print("Detecting GPU hardware...")
        print("=" * 50)
        
        system = platform.system().lower()
        
        if system == "linux":
            self._detect_linux_gpu()
        elif system == "windows":
            self._detect_windows_gpu()
        elif system == "darwin":  # macOS
            self._detect_macos_gpu()
        
        return self.gpu_info
    
    def _detect_linux_gpu(self):
        """Detect GPU on Linux"""
        try:
            # Check for NVIDIA GPUs
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.free', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        parts = line.split(', ')
                        if len(parts) >= 3:
                            self.gpu_info[f'nvidia_gpu_{i}'] = {
                                'type': 'NVIDIA',
                                'name': parts[0],
                                'total_memory': f"{parts[1]} MB",
                                'free_memory': f"{parts[2]} MB",
                                'driver': 'NVIDIA'
                            }
                print(f"✅ وُجد {len(lines)} كرت NVIDIA")
                print(f"Found {len(lines)} NVIDIA GPU(s)")
        except FileNotFoundError:
            print("❌ NVIDIA drivers not found")
        
        try:
            # Check for AMD GPUs
            result = subprocess.run(['rocm-smi'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ وُجد كرت AMD ROCm")
                print("Found AMD ROCm GPU")
                self.rocm_available = True
        except FileNotFoundError:
            pass
        
        # Check general GPU info with lspci
        try:
            result = subprocess.run(['lspci'], capture_output=True, text=True)
            gpu_lines = [line for line in result.stdout.split('\n') if 'VGA' in line or 'Display' in line or '3D' in line]
            
            for i, line in enumerate(gpu_lines):
                if f'general_gpu_{i}' not in [k for k in self.gpu_info.keys() if k.startswith('general')]:
                    self.gpu_info[f'general_gpu_{i}'] = {
                        'type': 'General',
                        'name': line.split(': ')[-1] if ': ' in line else line,
                        'info': 'Detected via lspci'
                    }
            
            print(f"📋 إجمالي كروت الرسوميات: {len(gpu_lines)}")
            print(f"Total graphics cards detected: {len(gpu_lines)}")
            
        except FileNotFoundError:
            print("❌ lspci not available")
    
    def _detect_windows_gpu(self):
        """Detect GPU on Windows"""
        try:
            # Check NVIDIA on Windows
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        parts = line.split(', ')
                        if len(parts) >= 2:
                            self.gpu_info[f'nvidia_gpu_{i}'] = {
                                'type': 'NVIDIA',
                                'name': parts[0],
                                'total_memory': f"{parts[1]} MB"
                            }
        except:
            pass
        
        # Use wmic for general GPU detection on Windows
        try:
            result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                lines = [line.strip() for line in result.stdout.split('\n') if line.strip() and line.strip() != 'Name']
                for i, name in enumerate(lines):
                    if name:
                        self.gpu_info[f'windows_gpu_{i}'] = {
                            'type': 'Windows GPU',
                            'name': name
                        }
        except:
            pass
    
    def _detect_macos_gpu(self):
        """Detect GPU on macOS"""
        try:
            result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.gpu_info['macos_gpu'] = {
                    'type': 'macOS GPU',
                    'info': 'Detected via system_profiler'
                }
                print("✅ macOS GPU detected")
        except:
            pass
    
    def check_cuda_support(self):
        """Check CUDA support"""
        print("\n🔧 فحص دعم CUDA...")
        print("Checking CUDA support...")
        print("=" * 30)
        
        try:
            import torch
            if torch.cuda.is_available():
                self.cuda_available = True
                device_count = torch.cuda.device_count()
                print(f"✅ CUDA متاح! عدد الأجهزة: {device_count}")
                print(f"CUDA available! Device count: {device_count}")
                
                for i in range(device_count):
                    device_name = torch.cuda.get_device_name(i)
                    memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
                    print(f"  🎯 جهاز {i}: {device_name} ({memory:.1f} GB)")
                    print(f"  Device {i}: {device_name} ({memory:.1f} GB)")
                
                return True
            else:
                print("❌ CUDA غير متاح")
                print("CUDA not available")
                return False
                
        except ImportError:
            print("❌ PyTorch غير مثبت")
            print("PyTorch not installed")
            return False
    
    def test_gpu_performance(self):
        """Test GPU performance with a simple benchmark"""
        print("\n⚡ اختبار أداء GPU...")
        print("Testing GPU performance...")
        print("=" * 30)
        
        try:
            import torch
            import time
            
            if torch.cuda.is_available():
                device = torch.device('cuda')
                print(f"🚀 اختبار على: {torch.cuda.get_device_name()}")
                print(f"Testing on: {torch.cuda.get_device_name()}")
                
                # Simple matrix multiplication test
                size = 1000
                print(f"📊 ضرب مصفوفات {size}x{size}...")
                print(f"Matrix multiplication {size}x{size}...")
                
                # CPU test
                start_time = time.time()
                a_cpu = torch.randn(size, size)
                b_cpu = torch.randn(size, size)
                c_cpu = torch.mm(a_cpu, b_cpu)
                cpu_time = time.time() - start_time
                
                # GPU test
                start_time = time.time()
                a_gpu = torch.randn(size, size, device=device)
                b_gpu = torch.randn(size, size, device=device)
                torch.cuda.synchronize()  # Wait for GPU operations
                c_gpu = torch.mm(a_gpu, b_gpu)
                torch.cuda.synchronize()
                gpu_time = time.time() - start_time
                
                speedup = cpu_time / gpu_time
                print(f"⏱️  وقت CPU: {cpu_time:.3f} ثانية")
                print(f"CPU time: {cpu_time:.3f} seconds")
                print(f"⚡ وقت GPU: {gpu_time:.3f} ثانية")
                print(f"GPU time: {gpu_time:.3f} seconds")
                print(f"🚀 تسريع GPU: {speedup:.2f}x")
                print(f"GPU speedup: {speedup:.2f}x")
                
                return {
                    'cpu_time': cpu_time,
                    'gpu_time': gpu_time,
                    'speedup': speedup
                }
            else:
                print("❌ لا يمكن اختبار GPU - غير متاح")
                print("Cannot test GPU - not available")
                return None
                
        except Exception as e:
            print(f"❌ خطأ في الاختبار: {e}")
            print(f"Test error: {e}")
            return None
    
    def check_ollama_gpu_support(self):
        """Check if Ollama can use GPU"""
        print("\n🦙 فحص دعم GPU في Ollama...")
        print("Checking Ollama GPU support...")
        print("=" * 35)
        
        try:
            # Check if Ollama is installed
            result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Ollama غير مثبت")
                print("Ollama not installed")
                return False
            
            print("✅ Ollama مثبت")
            print("Ollama installed")
            
            # Check environment variables for GPU
            cuda_visible = os.environ.get('CUDA_VISIBLE_DEVICES', 'not set')
            print(f"🔧 CUDA_VISIBLE_DEVICES: {cuda_visible}")
            
            # Try to get Ollama GPU info (this might not work in all versions)
            try:
                result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True, timeout=5)
                print("✅ يمكن الاتصال بـ Ollama")
                print("Can connect to Ollama")
            except subprocess.TimeoutExpired:
                print("⚠️ Ollama قد يكون غير مُشغل")
                print("Ollama may not be running")
            
            return True
            
        except FileNotFoundError:
            print("❌ Ollama غير موجود")
            print("Ollama not found")
            return False
    
    def generate_gpu_report(self):
        """Generate a comprehensive GPU report"""
        print("\n📋 تقرير شامل عن GPU...")
        print("Comprehensive GPU Report...")
        print("=" * 40)
        
        report = {
            'system_info': {
                'platform': platform.system(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor()
            },
            'gpu_hardware': self.gpu_info,
            'cuda_available': self.cuda_available,
            'rocm_available': self.rocm_available
        }
        
        # Save report to file
        report_file = Path('gpu_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 تم حفظ التقرير في: {report_file}")
        print(f"Report saved to: {report_file}")
        
        return report

def install_gpu_packages():
    """Install GPU-related packages"""
    print("📦 تثبيت مكتبات GPU...")
    print("Installing GPU packages...")
    
    packages = [
        "torch",
        "torchvision", 
        "torchaudio"
    ]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
            print(f"✅ تم تثبيت {package}")
        except subprocess.CalledProcessError:
            print(f"❌ فشل تثبيت {package}")

def main():
    print("🎮 أداة فحص واختبار GPU")
    print("GPU Detection and Testing Tool")
    print("=" * 50)
    
    tester = GPUTester()
    
    # Detect hardware
    gpu_info = tester.detect_gpu_hardware()
    
    if not gpu_info:
        print("\n❌ لم يُعثر على كرت رسوميات")
        print("No GPU detected")
        return
    
    print(f"\n📊 تفاصيل GPU:")
    print("GPU Details:")
    for key, info in gpu_info.items():
        print(f"  {key}: {info}")
    
    # Check CUDA
    cuda_available = tester.check_cuda_support()
    
    # Performance test
    if cuda_available:
        tester.test_gpu_performance()
    
    # Check Ollama GPU support
    tester.check_ollama_gpu_support()
    
    # Generate report
    tester.generate_gpu_report()
    
    print("\n🎯 توصيات:")
    print("Recommendations:")
    
    if cuda_available:
        print("✅ يمكنك استخدام GPU للتدريب السريع")
        print("You can use GPU for fast training")
        print("💡 استخدم: --device cuda في التدريب")
        print("Use: --device cuda in training")
    else:
        print("⚠️ سيتم استخدام CPU - قد يكون أبطأ")
        print("Will use CPU - may be slower")
        print("💡 فكر في تثبيت CUDA drivers")
        print("Consider installing CUDA drivers")

if __name__ == "__main__":
    main()
