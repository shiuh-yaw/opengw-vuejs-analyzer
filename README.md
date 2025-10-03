# OpenGW Agentic Transaction Analyzer (Vue.js Edition) - Enhanced

This project is an advanced transaction analysis tool featuring a Vue.js frontend and a Python backend. It has been enhanced with Manus AI integration, detailed transaction flow visualization, and a sophisticated JSON/XML content viewer.

## Key Features

- **Modern Frontend**: A responsive and interactive user interface built with Vue.js 3, Vite, and Tailwind CSS.
- **Powerful Backend**: A robust API built with Python and FastAPI for efficient data processing and analysis.
- **Manus AI Integration**: Seamless integration with Manus AI for intelligent transaction analysis, providing risk scores, key findings, and recommendations.
- **Transaction Flow Visualization**: A step-by-step visualization of the entire transaction flow, parsed directly from OpenGW logs.
- **Beautified Content Viewer**: A sophisticated component for displaying and toggling between beautified JSON and XML content found in logs.
- **Comprehensive Cache Prevention**: A multi-layered strategy to eliminate both frontend and backend caching issues.
- **Easy Development Setup**: A single script to launch the entire development environment.
- **Production-Ready Build**: A script to generate a production-optimized build with cache-busting.

## Enhanced Functionality

### Manus AI Integration

The application now directly integrates with a (mock) Manus AI client to provide in-depth analysis of transactions. This includes:
- **Risk Scoring**: A numerical score representing the potential risk of a transaction.
- **Key Findings**: A list of identified issues or patterns.
- **Recommendations**: Actionable recommendations for handling the transaction.

### Transaction Flow Visualization

The new Transaction Flow view provides a detailed, step-by-step breakdown of each transaction's lifecycle. The backend parses `INFO OPENGW_MESSAGE_LOG -` entries from the log file, and the frontend displays them in a clear, chronological order.

### JSON/XML Content Viewer

A new `ContentViewer` component has been developed to handle the display of structured data within log entries:
- **Automatic Detection**: The backend automatically detects and extracts JSON and XML content from log messages.
- **Beautified Display**: Both JSON and XML are beautified for readability.
- **Toggle Functionality**: If a log entry contains both JSON and XML, the user can easily toggle between the two views.
- **Copy to Clipboard**: Users can copy the beautified content with a single click.

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

