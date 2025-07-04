#!/usr/bin/env python3
"""
Real-time Training Monitor Web Interface
Shows training progress, metrics, and logs in real-time
"""

import json
import time
import threading
import webbrowser
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import logging

class TrainingMonitor:
    def __init__(self, port=5000):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'training_monitor_secret'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.port = port
        
        # Training state
        self.training_data = {
            'status': 'idle',
            'current_epoch': 0,
            'total_epochs': 0,
            'current_step': 0,
            'total_steps': 0,
            'loss': 0.0,
            'learning_rate': 0.0,
            'elapsed_time': 0,
            'estimated_remaining': 0,
            'model_name': '',
            'dataset_size': 0,
            'batch_size': 0,
            'logs': [],
            'metrics_history': {
                'loss': [],
                'learning_rate': [],
                'timestamps': []
            }
        }
        
        self.setup_routes()
        self.setup_socketio()
        
        # Logging setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('training_monitor.html')
        
        @self.app.route('/api/status')
        def get_status():
            return jsonify(self.training_data)
        
        @self.app.route('/static/<path:filename>')
        def static_files(filename):
            return send_from_directory('static', filename)

    def setup_socketio(self):
        @self.socketio.on('connect')
        def handle_connect():
            emit('status_update', self.training_data)
            self.logger.info("Client connected to training monitor")

        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.logger.info("Client disconnected from training monitor")

    def update_training_status(self, status, **kwargs):
        """Update training status and broadcast to connected clients"""
        self.training_data['status'] = status
        
        # Update provided fields
        for key, value in kwargs.items():
            if key in self.training_data:
                self.training_data[key] = value
        
        # Add timestamp
        self.training_data['last_update'] = datetime.now().isoformat()
        
        # Add to metrics history if loss is provided
        if 'loss' in kwargs:
            self.training_data['metrics_history']['loss'].append(kwargs['loss'])
            self.training_data['metrics_history']['timestamps'].append(datetime.now().isoformat())
            
            # Keep only last 100 points
            if len(self.training_data['metrics_history']['loss']) > 100:
                self.training_data['metrics_history']['loss'].pop(0)
                self.training_data['metrics_history']['timestamps'].pop(0)
        
        if 'learning_rate' in kwargs:
            self.training_data['metrics_history']['learning_rate'].append(kwargs['learning_rate'])
        
        # Broadcast to all connected clients
        self.socketio.emit('status_update', self.training_data)

    def add_log(self, message, level='info'):
        """Add a log message and broadcast to clients"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        
        self.training_data['logs'].append(log_entry)
        
        # Keep only last 100 logs
        if len(self.training_data['logs']) > 100:
            self.training_data['logs'].pop(0)
        
        self.socketio.emit('log_update', log_entry)

    def start_training_session(self, model_name, total_epochs, dataset_size, batch_size):
        """Initialize a new training session"""
        self.training_data.update({
            'status': 'starting',
            'model_name': model_name,
            'total_epochs': total_epochs,
            'dataset_size': dataset_size,
            'batch_size': batch_size,
            'current_epoch': 0,
            'current_step': 0,
            'total_steps': (dataset_size // batch_size) * total_epochs,
            'start_time': time.time(),
            'logs': [],
            'metrics_history': {
                'loss': [],
                'learning_rate': [],
                'timestamps': []
            }
        })
        
        self.add_log(f"Starting training session for {model_name}")
        self.add_log(f"Total epochs: {total_epochs}, Dataset size: {dataset_size}, Batch size: {batch_size}")

    def finish_training_session(self):
        """Mark training as completed"""
        self.update_training_status('completed')
        self.add_log("Training session completed!")

    def run(self, debug=False, open_browser=True):
        """Run the training monitor server"""
        if open_browser:
            # Open browser after a short delay
            def open_browser_delayed():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{self.port}')
            
            threading.Thread(target=open_browser_delayed, daemon=True).start()
        
        self.logger.info(f"Starting training monitor on http://localhost:{self.port}")
        self.socketio.run(self.app, host='0.0.0.0', port=self.port, debug=debug, allow_unsafe_werkzeug=True)

# Global monitor instance
monitor = TrainingMonitor()

def start_monitor(port=5000, open_browser=True):
    """Start the training monitor in a separate thread"""
    def run_monitor():
        monitor.run(debug=False, open_browser=open_browser)
    
    thread = threading.Thread(target=run_monitor, daemon=True)
    thread.start()
    return monitor

if __name__ == "__main__":
    monitor.run(debug=True)
