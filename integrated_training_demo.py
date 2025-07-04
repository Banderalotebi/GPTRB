#!/usr/bin/env python3
"""
Integration demo showing the complete Arabic Llama training system with real-time monitoring
"""

import time
import subprocess
import threading
from pathlib import Path
from training_monitor import start_monitor

def run_training_with_monitor():
    """Run a complete training session with real-time monitoring"""
    print("🚀 إطلاق نظام تدريب اللاما العربي المتكامل")
    print("🚀 Launching Integrated Arabic Llama Training System")
    print("=" * 60)
    
    # Check if training data exists
    training_dir = Path("training_data")
    if not training_dir.exists() or not list(training_dir.glob("*.jsonl")):
        print("📁 Creating sample training data...")
        from llama_finetuning import create_sample_training_data
        create_sample_training_data()
    
    print("🌐 Starting real-time training monitor...")
    print("📊 Monitor will be available at: http://localhost:5000")
    
    # Start the monitor in a separate thread
    def start_monitor_thread():
        monitor = start_monitor(port=5000, open_browser=True)
        
        # Simulate a training process
        time.sleep(3)
        
        monitor.start_training_session(
            model_name="arabic-llama-custom",
            total_epochs=3,
            dataset_size=500,
            batch_size=16
        )
        
        monitor.add_log("Starting Arabic Llama fine-tuning process")
        monitor.add_log("تم بدء عملية الضبط الدقيق للاما العربي")
        
        # Simulate training steps
        for epoch in range(1, 4):
            monitor.add_log(f"Starting epoch {epoch}/3 - بدء العصر {epoch}/3")
            
            for step in range(32):
                current_step = (epoch-1) * 32 + step + 1
                loss = max(0.2, 1.5 - (current_step * 0.01))
                learning_rate = 0.001 * (0.98 ** (current_step // 10))
                
                monitor.update_training_status(
                    'training',
                    current_epoch=epoch,
                    current_step=current_step,
                    loss=loss,
                    learning_rate=learning_rate,
                    elapsed_time=current_step * 3
                )
                
                if step % 8 == 0:
                    monitor.add_log(f"Epoch {epoch}, Step {step+1}: Loss = {loss:.4f}")
                
                time.sleep(0.2)
            
            monitor.add_log(f"Completed epoch {epoch}/3 - اكتمل العصر {epoch}/3")
        
        monitor.add_log("Training completed successfully! - اكتمل التدريب بنجاح!")
        monitor.finish_training_session()
    
    # Start monitor in background
    monitor_thread = threading.Thread(target=start_monitor_thread, daemon=True)
    monitor_thread.start()
    
    print("\n📋 Training Options:")
    print("1. Continue with simulated training (for demo)")
    print("2. Start real Ollama fine-tuning")
    print("3. Just monitor interface (no training)")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        print("🎬 Running demo simulation...")
        print("✅ Check the browser for real-time training progress!")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Demo stopped.")
    
    elif choice == "2":
        print("🔄 Starting real Ollama training...")
        try:
            from llama_finetuning import LlamaFineTuner
            fine_tuner = LlamaFineTuner()
            
            # Get available training files
            training_files = list(Path("training_data").glob("*.jsonl"))
            if training_files:
                selected_file = training_files[0]  # Use first available file
                custom_name = "arabic-llama-realtime"
                
                print(f"📂 Using training file: {selected_file}")
                print(f"🎯 Creating model: {custom_name}")
                
                # This will use the monitor we already started
                fine_tuner.fine_tune_with_ollama(
                    str(selected_file), 
                    custom_name,
                    enable_monitor=False  # Monitor already running
                )
            else:
                print("❌ No training files found!")
        
        except Exception as e:
            print(f"❌ Error during training: {e}")
    
    elif choice == "3":
        print("📊 Monitor interface running...")
        print("✅ Visit http://localhost:5000 to view the training dashboard")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Monitor stopped.")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    run_training_with_monitor()
