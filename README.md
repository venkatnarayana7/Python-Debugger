# Truth Engine (PVE) - Zero-Trust Python Debugger

A sophisticated AI-powered code repair platform that verifies fixes before presenting them to users.

## 🚀 Features

- **AI-Powered Analysis**: Uses Gemini 1.5 Flash + DeepSeek V3 for intelligent code repair
- **Zero-Trust Verification**: Every fix is executed in a secure sandbox before presentation
- **Real-Time Streaming**: WebSocket-based live updates during verification
- **Modern UI**: Monaco Editor + Dark Theme + Diff Viewer

## 📁 Project Structure

```
├── backend/
│   ├── controller/       # AI Logic Layer (Lambda A)
│   │   ├── ag/           # AI modules (categorizer, brain, fallback)
│   │   └── main.py       # Lambda handler
│   ├── sandbox/          # Execution Sandbox (Lambda B)
│   │   ├── security.py   # Regex sanitization
│   │   ├── runner.py     # Subprocess execution
│   │   └── Dockerfile    # Container definition
│   ├── orchestration/    # Step Functions
│   │   └── state_machine.asl.json
│   └── websocket/        # Real-time API
│       ├── connect.py
│       ├── disconnect.py
│       └── notifier.py
├── frontend/             # Next.js 14 Application
│   ├── app/
│   │   ├── components/   # UI Components
│   │   └── page.tsx      # Main page
│   └── lib/store.ts      # Zustand state
└── README.md
```

## 🛠️ Local Development

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker (optional, for sandbox testing)

### Backend Setup
```bash
cd backend/controller
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

### Run Full Workflow Simulation
```bash
cd backend/orchestration
python simulate_workflow.py
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google AI Studio API Key |
| `GROQ_API_KEY` | Groq Cloud API Key |
| `DEEPSEEK_API_KEY` | DeepSeek API Key |

## 📦 AWS Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed AWS deployment instructions.

## 🏗️ Architecture

```
User Input → Controller (Gemini) → [Candidates]
                                        ↓
                              Fan-Out (Step Functions)
                                        ↓
                    ┌───────────────────┼───────────────────┐
                    ↓                   ↓                   ↓
              Sandbox #1          Sandbox #2          Sandbox #3
                    ↓                   ↓                   ↓
                    └───────────────────┼───────────────────┘
                                        ↓
                              Aggregate Results
                                        ↓
                              WebSocket → Frontend
```

## 📄 License

MIT License - See LICENSE file for details.
