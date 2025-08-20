# MoFA_Stage

English | [中文](README_cn.md)

MoFA_Stage is a visual management platform built for the MoFA (Modular Framework for Agents) framework. Through a simple and intuitive web interface, you can create, edit, and run Agents without directly operating the command line.

## Main Features

- **Agent Management**
  - Browse and search existing Agents
  - Create new Agents based on templates, or duplicate existing Agents
  - Modify Agent code and configuration
  - Start/stop Agent execution
  - Delete unwanted Agents

- **Terminal Integration**
  - Web SSH access (no additional SSH client required)
  - ttyd terminal directly integrated into the page
  - Convenient command-line environment

- **Editor Features**
  - Monaco-based code editing (same editor engine as VS Code)
  - Code highlighting and auto-completion
  - Markdown instant preview
  - Project file navigation

## Technology Stack

**Backend**
- Python + Flask
- WebSocket support
- SSH terminal integration
- RESTful API

**Frontend**
- Vue 3 
- Element Plus component library
- Monaco editor
- XTerm.js terminal emulation
- Multi-language support
- Pinia state management

**Third-party Dependencies**
- ttyd terminal service (optional)

## Quick Start

### Environment Requirements

- Python 3.8 or higher
- Node.js 14 or higher
- MoFA framework installed

### Installation and Run Scripts

The project provides two scripts:

- **install.sh**: One-click installation of all dependencies
  ```bash
  chmod +x install.sh
  ./install.sh
  ```
  Automatically installs backend/frontend dependencies, and installs ttyd and builds the frontend as needed.

- **run.sh**: One-click service startup
  ```bash
  chmod +x run.sh
  ./run.sh
  ```

### Development Mode

1. Start the backend
```bash
cd backend
python app.py
```

2. Start the frontend (development mode)
```bash
cd frontend
npm run dev
```

Access http://localhost:3000.

### Production Deployment

1. Build the frontend
```bash
cd frontend
npm run build  # Generates in the dist directory
```

2. Deployment methods (choose one)

**Using Nginx**

```nginx
server {
    listen 80;
    
    # Static files
    location / {
        root /path/to/mofa_stage/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API forwarding
    location /api {
        proxy_pass http://localhost:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # WebSocket
    location /api/webssh {
        proxy_pass http://localhost:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

**Simple Deployment**

Using Python's built-in HTTP server:
```bash
cd frontend/dist
python -m http.server 3000
```

Start the backend:
```bash
cd backend
python app.py
```

## Common Issues

### Port Occupation

If you encounter port occupation issues, you can use this command to release ports:

```bash
for port in 3000 5001 5002 7681; do
    pid=$(lsof -t -i:$port)
    if [ -n "$pid" ]; then
        kill -9 $pid
        echo "Released port $port"
    fi
done
```

### Port Description

- 3000: Frontend service
- 5001: WebSSH service
- 5002: Main backend API
- 7681: ttyd terminal

### ttyd Installation Failure

If ttyd automatic installation fails, you can refer to the [ttyd GitHub page](https://github.com/tsl0922/ttyd) for manual installation.

## Directory Structure

Core directories and files:

```
MoFA_Stage/
├── backend/                # Flask backend
│   ├── app.py              # Main application entry
│   ├── routes/             # API routes
│   │   ├── agents.py       # Agent API
│   │   ├── dataflows.py    # Dataflow API
│   │   ├── webssh.py       # SSH API, etc.
│   ├── utils/              # Utility functions
│   │   ├── mofa_cli.py     # mofa command line wrapper
│   │   ├── dataflow_engine.py # Dataflow engine
│   └── models/             # Data models
├── frontend/               # Vue3 frontend
│   ├── src/
│       ├── views/          # Page views
│       ├── components/     # Components
│       ├── api/            # API calls
├── install.sh              # Installation script
├── run.sh                  # Service startup script
└── README.md               
```