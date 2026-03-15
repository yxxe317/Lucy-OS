import os
from pathlib import Path
import logging
from fastapi import HTTPException

logger = logging.getLogger("LucyFileSystem")

WORKSPACE_ROOT = Path(__file__).parent.parent.parent / "workspace"
WORKSPACE_ROOT.mkdir(exist_ok=True)

class FileSystemPlugin:
    def __init__(self):
        logger.info(f"📂 FileSystem Plugin Initialized. Root: {WORKSPACE_ROOT}")

    def _safe_path(self, path: str) -> Path:
        safe = (WORKSPACE_ROOT / path).resolve()
        if not str(safe).startswith(str(WORKSPACE_ROOT.resolve())):
            raise HTTPException(status_code=403, detail="Access Denied: Outside Workspace")
        return safe

    def list_files(self, path: str = "."):
        try:
            safe_path = self._safe_path(path)
            if not safe_path.exists():
                return []
            
            files = []
            for item in safe_path.iterdir():
                files.append({
                    "name": item.name,
                    "is_dir": item.is_dir(),
                    "size": item.stat().st_size if item.is_file() else 0
                })
            return files
        except Exception as e:
            logger.error(f"File List Error: {e}")
            return []

    def read_file(self, path: str) -> str:
        try:
            safe_path = self._safe_path(path)
            if not safe_path.exists():
                raise HTTPException(status_code=404, detail="File not found")
            if safe_path.is_dir():
                raise HTTPException(status_code=400, detail="Cannot read a directory")
            
            return safe_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"File Read Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def write_file(self, path: str, content: str):
        try:
            safe_path = self._safe_path(path)
            safe_path.parent.mkdir(parents=True, exist_ok=True)
            safe_path.write_text(content, encoding='utf-8')
            logger.info(f"✍️ File Written: {path}")
            return {"status": "success", "path": str(path)}
        except Exception as e:
            logger.error(f"File Write Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

filesystem = FileSystemPlugin()