from fastapi import FastAPI, Request, Response, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io
import time
import uuid
from typing import List, Dict, Any

# --- Application Setup ---
app = FastAPI(
    title="OpenGW Agentic Analyzer - Backend",
    description="Python backend for analyzing OpenGW transaction logs with cache prevention.",
    version="1.0.0"
)

# --- Cache Prevention Middleware ---
@app.middleware("http")
async def add_cache_control_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["ETag"] = f\"W/\"{uuid.uuid4()}\"\" # Unique ETag for each response
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

# --- In-memory Data Storage (for demonstration) ---
# In a real application, use a database.
data_store: Dict[str, pd.DataFrame] = {}
analysis_history: List[Dict[str, Any]] = []

# --- API Endpoints ---

@app.get("/api/health", tags=["General"])
async def health_check():
    """Provides a health check endpoint with cache prevention."""
    return JSONResponse(
        content={
            "status": "ok",
            "timestamp": time.time(),
            "version": app.version
        },
        headers={
            "X-Custom-Health-Check": "passed"
        }
    )

@app.post("/api/upload", tags=["Data"])
async def upload_transaction_file(file: UploadFile = File(...)):
    """Handles file upload and basic validation."""
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only JSON files are accepted.")

    try:
        contents = await file.read()
        df = pd.read_json(io.StringIO(contents.decode("utf-8")))
        
        # Basic validation of the JSON structure
        if "transactions" not in df.columns:
             df = pd.json_normalize(df.to_dict(orient=\"records\"))

        file_id = str(uuid.uuid4())
        data_store[file_id] = df
        
        return {
            "success": True,
            "message": f"File '{file.filename}' uploaded successfully.",
            "file_id": file_id,
            "transactions_count": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")

@app.get("/api/transactions", tags=["Data"], response_model=List[Dict[str, Any]])
async def get_transactions(file_id: str):
    """Retrieves transactions from an uploaded file."""
    if file_id not in data_store:
        raise HTTPException(status_code=404, detail="File not found.")
    
    df = data_store[file_id]
    return df.to_dict(orient="records")

@app.post("/api/analyze/{transaction_id}", tags=["Analysis"])
async def analyze_transaction(transaction_id: str, file_id: str):
    """Analyzes a single transaction."""
    if file_id not in data_store:
        raise HTTPException(status_code=404, detail="File not found.")

    df = data_store[file_id]
    transaction = df[df["id"] == transaction_id]

    if transaction.empty:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    # Dummy analysis logic
    analysis_result = {
        "transaction_id": transaction_id,
        "analysis": {
            "status": "completed",
            "issues": ["Potential duplicate transaction"],
            "recommendations": ["Review transaction history for duplicates"],
            "risk_score": 0.75,
            "patterns": ["High frequency transactions"]
        }
    }
    analysis_history.append(analysis_result)
    return analysis_result

@app.get("/api/analysis/history", tags=["Analysis"], response_model=List[Dict[str, Any]])
async def get_analysis_history():
    """Retrieves the history of transaction analyses."""
    return analysis_history

# --- Main Entry Point for Uvicorn ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

