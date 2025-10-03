# OpenGW Agentic Transaction Analyzer (Vue.js Edition)

This project is an advanced transaction analysis tool featuring a Vue.js frontend and a Python backend. It is specifically engineered with comprehensive cache prevention strategies to ensure that users always interact with the most up-to-date data and application version.

## Key Features

- **Modern Frontend**: A responsive and interactive user interface built with Vue.js 3, Vite, and Tailwind CSS.
- **Powerful Backend**: A robust API built with Python and FastAPI for efficient data processing and analysis.
- **Comprehensive Cache Prevention**: A multi-layered strategy to eliminate both frontend and backend caching issues.
- **AI-Powered Analysis**: (Simulated) Integration with Manus AI for intelligent transaction insights.
- **Easy Development Setup**: A single script to launch the entire development environment.
- **Production-Ready Build**: A script to generate a production-optimized build with cache-busting.

## Cache Prevention Strategies

This project implements a robust set of strategies to prevent caching at every level of the application stack.

### Frontend (Vue.js + Vite)

1.  **Vite Build Configuration (`vite.config.ts`)**:
    *   **Content-Based Hashing**: All generated assets (JS, CSS) have unique filenames based on their content hash (`[name]-[hash].js`). This ensures that browsers only download new assets when they have actually changed.
    *   **Disabled Dev Server Cache**: The Vite development server is configured to send `Cache-Control: no-cache` headers to prevent caching during development.

2.  **HTML Meta Tags (`index.html`)**:
    *   Explicit `Cache-Control`, `Pragma`, and `Expires` meta tags are included to instruct browsers not to cache the main HTML file.

3.  **API Client (axios)**:
    *   All API requests sent from the frontend automatically include cache-busting parameters (`_cb=timestamp`) and headers (`Cache-Control: no-cache`).

4.  **Vue Router**:
    *   A navigation guard adds a unique cache-busting meta tag to the document head on every route change, further preventing stale views.

### Backend (Python + FastAPI)

1.  **Cache-Control Middleware**:
    *   A FastAPI middleware is implemented to automatically add the following headers to **every** API response:
        *   `Cache-Control: no-cache, no-store, must-revalidate, private`
        *   `Pragma: no-cache`
        *   `Expires: 0`
    *   A unique `ETag` is generated for every response to prevent conditional caching.

2.  **Disabled Python Caching**:
    *   The development server runs with `PYTHONDONTWRITEBYTECODE=1` to prevent the creation of `.pyc` cache files.

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

