import logging
import io
import sys
import traceback
import json
from pathlib import Path
from datetime import datetime
import re

logger = logging.getLogger("LucyCode")

class CodeExecutor:
    def __init__(self):
        self.workspace = Path(__file__).parent.parent / "workspace"
        self.workspace.mkdir(exist_ok=True)
        self.max_execution_time = 30  # seconds
        self.allowed_modules = [
            'math', 'random', 'datetime', 'json', 're', 'os', 'pathlib',
            'collections', 'itertools', 'functools', 'statistics',
            'httpx', 'beautifulsoup4', 'pandas', 'numpy'
        ]
        logger.info("⚡ Code Executor Initialized")
    
    def _sanitize_code(self, code: str) -> str:
        """Remove dangerous operations"""
        dangerous = ['__import__', 'eval(', 'exec(', 'compile(', 'open(', 
                    'subprocess', 'sys.modules', 'globals()', 'locals()']
        
        for danger in dangerous:
            if danger in code:
                raise ValueError(f"Dangerous operation detected: {danger}")
        
        return code
    
    def execute_python(self, code: str, user_id: int = 1) -> dict:
        """Execute Python code safely"""
        try:
            # Sanitize code
            self._sanitize_code(code)
            
            # Capture output
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            
            result = None
            success = False
            error = None
            
            try:
                # Create safe namespace
                safe_globals = {
                    '__builtins__': __builtins__,
                    'math': __import__('math'),
                    'random': __import__('random'),
                    'datetime': __import__('datetime'),
                    'json': __import__('json'),
                    're': __import__('re'),
                    'os': __import__('os'),
                    'pathlib': __import__('pathlib'),
                    'Path': Path,
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    'sum': sum,
                    'min': min,
                    'max': max,
                    'abs': abs,
                    'round': round,
                }
                
                # Try to import pandas/numpy if available
                try:
                    safe_globals['pd'] = __import__('pandas')
                    safe_globals['np'] = __import__('numpy')
                except:
                    pass
                
                local_ns = {}
                exec(code, safe_globals, local_ns)
                
                # Get last expression result
                if '_' in local_ns:
                    result = local_ns['_']
                
                success = True
                
            except Exception as e:
                error = str(e)
                traceback.print_exc(file=stderr_capture)
            
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
            
            output = stdout_capture.getvalue()
            errors = stderr_capture.getvalue()
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"code_{user_id}_{timestamp}.py"
            filepath = self.workspace / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            logger.info(f"✅ Code executed by user {user_id}: {filename}")
            
            return {
                "success": success,
                "output": output,
                "error": error or errors,
                "result": str(result) if result is not None else None,
                "filename": filename,
                "filepath": str(filepath),
                "timestamp": timestamp
            }
            
        except ValueError as e:
            logger.error(f"❌ Security error: {e}")
            return {"success": False, "error": f"Security Error: {str(e)}"}
        except Exception as e:
            logger.error(f"❌ Execution error: {e}")
            return {"success": False, "error": str(e)}
    
    def read_file(self, path: str, user_id: int = 1) -> dict:
        """Read file from workspace"""
        try:
            # Security: Only allow workspace files
            full_path = (self.workspace / path).resolve()
            if not str(full_path).startswith(str(self.workspace.resolve())):
                return {"success": False, "error": "Access denied: Outside workspace"}
            
            if not full_path.exists():
                return {"success": False, "error": "File not found"}
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {"success": True, "content": content, "path": str(full_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_file(self, path: str, content: str, user_id: int = 1) -> dict:
        """Write file to workspace"""
        try:
            full_path = (self.workspace / path).resolve()
            if not str(full_path).startswith(str(self.workspace.resolve())):
                return {"success": False, "error": "Access denied: Outside workspace"}
            
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ File written: {path}")
            return {"success": True, "path": str(full_path)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_files(self, user_id: int = 1) -> dict:
        """List files in workspace"""
        try:
            files = []
            for f in self.workspace.iterdir():
                if f.is_file():
                    files.append({
                        "name": f.name,
                        "size": f.stat().st_size,
                        "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                    })
            return {"success": True, "files": files}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def calculate(self, expression: str) -> dict:
        """Safe math calculation"""
        try:
            # Only allow math characters
            if not re.match(r'^[\d+\-*/().\s]+$', expression):
                return {"success": False, "error": "Invalid characters in expression"}
            
            result = eval(expression, {"__builtins__": {}}, {})
            return {"success": True, "result": result, "expression": expression}
        except Exception as e:
            return {"success": False, "error": str(e)}

code_executor = CodeExecutor()