from fastapi import FastAPI, Request, Response, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import io
import time
import uuid
from typing import List, Dict, Any

# Internal modules
from multi_agent_system import multi_agent_system
from log_parser import parse_input_into_blocks

# --- Application Setup ---
app = FastAPI(
    title="OpenGW Multi-Agent Analyzer",
    description="Backend with a multi-agent AI system for comprehensive log analysis.",
    version="3.0.0"
)

# --- Cache Prevention Middleware ---
@app.middleware("http")
async def add_cache_control_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["ETag"] = f'W/"'{uuid.uuid4()}'"' # Unique ETag for each response
    response.headers["Last-Modified"] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    return response

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Allow frontend dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# --- In-memory Data Storage ---
data_store: Dict[str, str] = {}

# --- API Endpoints ---

@app.get("/api/health", tags=["General"])
async def health_check():
    """Provides a health check endpoint."""
    return JSONResponse(
        content={
            "status": "ok",
            "timestamp": time.time(),
            "version": app.version
        }
    )

@app.post("/api/upload", tags=["Data"])
async def upload_log_file(file: UploadFile = File(...)):
    """Handles log file upload and stores the raw content."""
    try:
        contents = await file.read()
        raw_content = contents.decode("utf-8")
        
        file_id = str(uuid.uuid4())
        data_store[file_id] = raw_content
        
        return {
            "success": True,
            "message": f"Log file ‘{file.filename}’ uploaded successfully.",
            "file_id": file_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")

@app.get("/api/file/{file_id}/blocks", tags=["Parsing"])
async def get_parsed_blocks(file_id: str):
    """Parses the uploaded file content into blocks and returns them."""
    if file_id not in data_store:
        raise HTTPException(status_code=404, detail="File not found.")

    raw_content = data_store[file_id]
    parsed_blocks = parse_input_into_blocks(raw_content)
    
    return {
        "file_id": file_id,
        "blocks": parsed_blocks
    }

@app.post("/api/analyze/multi-agent", tags=["Analysis"])
async def analyze_with_multi_agent_system(request_data: Dict[str, Any]):
    """Analyzes a block of content using the multi-agent system."""
    content = request_data.get("content")
    if not content:
        raise HTTPException(status_code=400, detail="Content is required for analysis.")

    try:
        multi_agent_analysis = multi_agent_system.analyze_content(content, request_data.get("psp"))
        return {
            "analysis_provider": "Multi-Agent System",
            "analysis": multi_agent_analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-agent analysis failed: {e}")

# --- Main Entry Point for Uvicorn ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

