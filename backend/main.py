from fastapi import FastAPI, Request, Response, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import io
import time
import uuid
from typing import List, Dict, Any
import xml.dom.minidom

# Internal modules
from manus_ai import manus_ai_client
from log_parser import parse_transaction_flow

# --- Application Setup ---
app = FastAPI(
    title="OpenGW Agentic Analyzer - Enhanced Backend",
    description="Python backend with Manus AI integration, transaction flow parsing, and JSON/XML beautification.",
    version="2.0.0"
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
data_store: Dict[str, List[Dict[str, Any]]] = {}
analysis_history: List[Dict[str, Any]] = []

# --- Helper Functions ---
def beautify_json(content: str) -> str:
    try:
        return json.dumps(json.loads(content), indent=2)
    except (json.JSONDecodeError, TypeError):
        return content

def beautify_xml(content: str) -> str:
    try:
        dom = xml.dom.minidom.parseString(content)
        return dom.toprettyxml(indent="  ")
    except Exception:
        return content

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
    """Handles log file upload and stores the log entries."""
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only JSON log files are accepted.")

    try:
        contents = await file.read()
        log_data = json.loads(contents.decode("utf-8"))
        
        if not isinstance(log_data, list):
            raise ValueError("Log file must contain a JSON array of log entries.")

        file_id = str(uuid.uuid4())
        data_store[file_id] = log_data
        
        # Extract unique transaction IDs for the frontend
        transaction_ids = sorted(list(set(entry.get("transactionId", "unknown") for entry in log_data)))

        return {
            "success": True,
            "message": f"Log file ‘{file.filename}’ uploaded successfully.",
            "file_id": file_id,
            "transactions_count": len(transaction_ids),
            "transaction_ids": transaction_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")

@app.get("/api/transactions/{file_id}", tags=["Data"], response_model=List[str])
async def get_transactions(file_id: str):
    """Retrieves a list of unique transaction IDs from an uploaded log file."""
    if file_id not in data_store:
        raise HTTPException(status_code=404, detail="File not found.")
    
    log_data = data_store[file_id]
    transaction_ids = sorted(list(set(entry.get("transactionId", "unknown") for entry in log_data)))
    return transaction_ids

@app.get("/api/transactions/{file_id}/{transaction_id}/flow", tags=["Transaction Flow"])
async def get_transaction_flow(file_id: str, transaction_id: str):
    """Retrieves and parses the complete step-by-step flow for a single transaction."""
    if file_id not in data_store:
        raise HTTPException(status_code=404, detail="File not found.")

    log_data = data_store[file_id]
    transaction_logs = [entry for entry in log_data if entry.get("transactionId") == transaction_id]

    if not transaction_logs:
        raise HTTPException(status_code=404, detail="Transaction not found in the specified file.")

    flow_steps = parse_transaction_flow(transaction_logs)

    # Beautify content where applicable
    for step in flow_steps:
        if step["has_json"] and step["json_content"]:
            step["json_content"] = beautify_json(step["json_content"])
        if step["has_xml"] and step["xml_content"]:
            step["xml_content"] = beautify_xml(step["xml_content"])

    return {
        "transaction_id": transaction_id,
        "flow": flow_steps
    }

@app.post("/api/analyze/manus/{transaction_id}", tags=["Analysis"])
async def analyze_with_manus_ai(transaction_id: str, file_id: str):
    """Analyzes a single transaction using Manus AI."""
    if file_id not in data_store:
        raise HTTPException(status_code=404, detail="File not found.")

    log_data = data_store[file_id]
    transaction_logs = [entry for entry in log_data if entry.get("transactionId") == transaction_id]

    if not transaction_logs:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    # In a real scenario, you would aggregate and structure the transaction data
    # before sending it to the analysis client.
    sample_transaction_data = transaction_logs[-1] # Using the last entry as a sample

    try:
        manus_analysis = manus_ai_client.analyze_transaction(sample_transaction_data)
        analysis_result = {
            "transaction_id": transaction_id,
            "analysis_provider": "Manus AI",
            "analysis": manus_analysis
        }
        analysis_history.append(analysis_result)
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Manus AI analysis failed: {e}")

@app.get("/api/analysis/history", tags=["Analysis"], response_model=List[Dict[str, Any]])
async def get_analysis_history():
    """Retrieves the history of transaction analyses."""
    return analysis_history

# --- Main Entry Point for Uvicorn ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

