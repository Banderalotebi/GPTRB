#!/usr/bin/env python3
"""
Demo script to test the training monitor interface
"""

import time
import random
from training_monitor import start_monitor

def demo_training_session():
    """Simulate a training session with the monitor"""
    print("🚀 Starting training monitor demo...")
    
    # Start the monitor
    monitor = start_monitor(port=5000, open_browser=True)
    time.sleep(3)  # Give time for the monitor to start
    
    # Initialize a demo training session
    monitor.start_training_session(
        model_name="arabic-llama-demo",
        total_epochs=5,
        dataset_size=1000,
        batch_size=32
    )
    
    print("📊 Training session started. Check your browser at http://localhost:5000")
    print("🔄 Simulating training progress...")
    
    # Simulate training progress
    for epoch in range(1, 6):
        monitor.add_log(f"Starting epoch {epoch}/5")
        monitor.update_training_status(
            'training',
            current_epoch=epoch,
            current_step=(epoch-1) * 32
        )
        
        # Simulate steps within epoch
        for step in range(32):
            current_step = (epoch-1) * 32 + step + 1
            loss = max(0.1, 2.0 - (current_step * 0.001) + random.uniform(-0.1, 0.1))
            learning_rate = 0.001 * (0.95 ** (current_step // 100))
            
            elapsed_time = current_step * 2  # 2 seconds per step simulation
            remaining_time = (160 - current_step) * 2
            
            monitor.update_training_status(
                'training',
                current_step=current_step,
                loss=loss,
                learning_rate=learning_rate,
                elapsed_time=elapsed_time,
                estimated_remaining=remaining_time
            )
            
            if step % 5 == 0:
                monitor.add_log(f"Epoch {epoch}, Step {step+1}: Loss = {loss:.4f}")
            
            time.sleep(0.5)  # Simulate processing time
        
        monitor.add_log(f"Completed epoch {epoch}/5")
    
    # Finish training
    monitor.add_log("Training completed successfully!")
    monitor.finish_training_session()
    
    print("✅ Demo training session completed!")
    print("🌐 Monitor will continue running. Press Ctrl+C to stop.")
    
    try:
        # Keep the monitor running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped.")

if __name__ == "__main__":
    demo_training_session()
