# OpenGW Multi-Agent Analyzer

This project is an advanced log analysis tool featuring a Vue.js frontend and a Python backend. It has been significantly enhanced to include a multi-agent AI system for comprehensive content analysis and an intelligent log parser that structures raw text into analyzable blocks.

## Key Features

- **Modern Frontend**: A responsive and interactive user interface built with Vue.js 3, Vite, and Tailwind CSS.
- **Powerful Backend**: A robust API built with Python and FastAPI for efficient data processing and analysis.
- **Multi-Agent AI System**: Leverages multiple AI models (simulated) to analyze content from different perspectives: Risk, Compliance, and Fraud.
- **Intelligent Block Parsing**: Automatically parses raw log files into content blocks based on `[` and `]` delimiters.
- **Beautified Content Viewer**: Identifies and pretty-prints JSON and XML within content blocks for enhanced readability.
- **Comprehensive Cache Prevention**: A multi-layered strategy to eliminate both frontend and backend caching issues.
- **Easy Development Setup**: A single script to launch the entire development environment.
- **Production-Ready Build**: A script to generate a production-optimized build with cache-busting.

## Core Enhancements

### Multi-Agent AI System

The application now features a sophisticated backend system that simulates a multi-agent analysis process. Each agent represents a different AI model with a specific focus:

- **Risk Agent (`gpt-4.1-mini`)**: Analyzes content for potential risks and calculates a risk score.
- **Compliance Agent (`gemini-2.5-flash`)**: Checks content for compliance issues and violations.
- **Fraud Agent (`gpt-4.1-nano`)**: Scans content for indicators of fraudulent activity.

The frontend presents these multi-faceted analyses in a clear, organized report for each content block, providing a holistic view of potential issues.

### Intelligent Block Parsing

The new backend parser intelligently processes raw log files:

1.  **Block Separation**: The content of an uploaded file is automatically broken down into distinct blocks, using `[` and `]` as delimiters.
2.  **Content Identification**: Each block is analyzed to determine if it contains JSON, XML, or plain text.
3.  **Pretty-Printing**: JSON and XML content is automatically beautified (pretty-printed) for significantly improved readability.

This allows users to work with structured, easy-to-read data, even from semi-structured or messy log files.

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.11+)

### Development

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd opengw-vuejs-analyzer
    ```

2.  **Set up the backend**:
    ```bash
    cd backend
    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cd ..
    ```

3.  **Set up the frontend**:
    ```bash
    cd frontend
    npm install
    cd ..
    ```

4.  **Run the development server**:
    ```bash
    chmod +x start-dev.sh
    ./start-dev.sh
    ```

    This will start:
    *   The **Vue.js frontend** at `http://localhost:5173`
    *   The **FastAPI backend** at `http://localhost:8000`

### Production Build

To create a production-ready build, run the build script:

```bash
chmod +x build-production.sh
./build-production.sh
```

This will generate a `opengw-analyzer-<hash>.tar.gz` file containing the optimized frontend assets and the backend application, ready for deployment.

