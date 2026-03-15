import uvicorn
from core.kernel import app

if __name__ == "__main__":
    print("🚀 Starting Lucy OS v5.0 Kernel...")
    print("🌐 Access Dashboard at: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)