"""
Task Executor - Execute and manage tasks
"""

import time
import random
import threading
from typing import Dict, List, Optional, Callable
from datetime import datetime

class TaskExecutor:
    """
    Executes and manages tasks
    """
    
    def __init__(self):
        self.tasks = {}
        self.running_tasks = {}
        self.task_queue = []
        self.task_history = []
        self.is_running = False
        self.worker_thread = None
        
    def add_task(self, name: str, function: Callable = None,
                  args: tuple = None, priority: int = 1,
                  estimated_time: int = 60) -> str:
        """
        Add a task to the queue
        """
        import uuid
        task_id = str(uuid.uuid4())[:8]
        
        task = {
            'id': task_id,
            'name': name,
            'function': function,
            'args': args or (),
            'priority': priority,
            'estimated_time': estimated_time,
            'status': 'queued',
            'created': datetime.now().isoformat(),
            'started': None,
            'completed': None,
            'result': None,
            'error': None
        }
        
        self.tasks[task_id] = task
        self.task_queue.append(task_id)
        
        # Sort queue by priority
        self.task_queue.sort(key=lambda tid: self.tasks[tid]['priority'], reverse=True)
        
        return task_id
    
    def execute_task(self, task_id: str) -> Dict:
        """
        Execute a specific task
        """
        if task_id not in self.tasks:
            return {'error': 'Task not found'}
        
        task = self.tasks[task_id]
        task['status'] = 'running'
        task['started'] = datetime.now().isoformat()
        self.running_tasks[task_id] = task
        
        try:
            # Simulate task execution
            if task['function']:
                result = task['function'](*task['args'])
            else:
                # Default simulated execution
                time.sleep(min(2, task['estimated_time'] / 10))
                result = f"Task '{task['name']}' completed successfully"
            
            task['result'] = result
            task['status'] = 'completed'
            task['completed'] = datetime.now().isoformat()
            
        except Exception as e:
            task['error'] = str(e)
            task['status'] = 'failed'
            task['completed'] = datetime.now().isoformat()
        
        # Remove from running and add to history
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]
        
        self.task_history.append(task)
        
        return task
    
    def start_worker(self):
        """
        Start background worker to process queue
        """
        self.is_running = True
        
        def worker():
            while self.is_running:
                if self.task_queue:
                    task_id = self.task_queue.pop(0)
                    self.execute_task(task_id)
                else:
                    time.sleep(1)
        
        self.worker_thread = threading.Thread(target=worker, daemon=True)
        self.worker_thread.start()
    
    def stop_worker(self):
        """Stop background worker"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=2)
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get task status"""
        return self.tasks.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a queued task
        """
        if task_id in self.task_queue:
            self.task_queue.remove(task_id)
            self.tasks[task_id]['status'] = 'cancelled'
            return True
        return False
    
    def get_queue_length(self) -> int:
        """Get queue length"""
        return len(self.task_queue)
    
    def get_running_tasks(self) -> List[Dict]:
        """Get currently running tasks"""
        return list(self.running_tasks.values())
    
    def get_task_history(self, limit: int = 10) -> List[Dict]:
        """Get task history"""
        return self.task_history[-limit:]
    
    def estimate_completion_time(self) -> int:
        """
        Estimate total completion time for queue
        """
        total = 0
        for task_id in self.task_queue:
            total += self.tasks[task_id]['estimated_time']
        return total
    
    def create_scheduled_task(self, name: str, function: Callable,
                                interval: int, args: tuple = None) -> str:
        """
        Create a recurring scheduled task
        """
        import uuid
        task_id = str(uuid.uuid4())[:8]
        
        def scheduled_wrapper():
            while True:
                time.sleep(interval)
                result = function(*args) if args else function()
                print(f"[Scheduled] {name}: {result}")
        
        thread = threading.Thread(target=scheduled_wrapper, daemon=True)
        thread.start()
        
        return task_id
    
    def batch_execute(self, task_ids: List[str]) -> List[Dict]:
        """
        Execute multiple tasks in batch
        """
        results = []
        for task_id in task_ids:
            results.append(self.execute_task(task_id))
        return results
    
    def retry_failed(self, max_attempts: int = 3) -> List[str]:
        """
        Retry failed tasks
        """
        retried = []
        for task in self.task_history:
            if task['status'] == 'failed':
                for attempt in range(max_attempts):
                    print(f"Retrying task {task['id']} (attempt {attempt+1})")
                    result = self.execute_task(task['id'])
                    if result['status'] == 'completed':
                        retried.append(task['id'])
                        break
        return retried