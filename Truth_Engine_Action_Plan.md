# Truth Engine (PVE) - Action Plan

This document outlines the step-by-step implementation plan for the **Truth Engine (PVE)** based on the Final Master Packet.

## Phase 1: Infrastructure & Environment Setup
- [ ] **AWS Setup**
    - [ ] Create AWS Organization/Account structure if not already present.
    - [ ] Configure IAM users and groups with least privilege (separate roles for Lambda execution).
    - [ ] Set up AWS CLI locally and configure credentials.
- [ ] **Repository Setup**
    - [ ] Initialize Git repository.
    - [ ] Create `.gitignore` to exclude node_modules, venv, .env, and AWS credentials.
    - [ ] Set up branch protection rules (main/dev).
- [ ] **CI/CD Pipeline**
    - [ ] Initialize AWS Amplify application for Frontend hosting.
    - [ ] Configure GitHub Actions workflows for deploying Lambda functions and updating Step Functions.

## Phase 2: "The Brain" - AI Logic Layer Integration
- [ ] **API Access Setup**
    - [ ] Obtain API keys for Google AI Studio (Gemini 1.5 Flash).
    - [ ] Obtain API keys for DeepSeek V3 (Fallback).
    - [ ] Obtain API keys for Groq (Llama 3 - Categorizer).
    - [ ] store these keys in AWS Systems Manager Parameter Store or Secrets Manager.
- [ ] **Lambda A (Controller) Implementation**
    - [ ] Create Python Lambda function `pve-controller`.
    - [ ] **Categorization**: Implement `Groq` client to classify errors (Logic vs Syntax).
    - [ ] **Generation**: Implement `Gemini` client to generate:
        - `reproduce_issue.py` (Script that reproduces the error).
        - `fix_candidates` (List of 3 potential fixes).
    - [ ] **Fallback Mechanism**: Implement logic to route to DeepSeek if Gemini fails or returns invalid JSON.
- [ ] **Testing (Brain)**
    - [ ] Write unit tests for the prompt generation logic.
    - [ ] Create mocks for the External APIs to test fallback logic.

## Phase 3: "The Body" - Sandbox Execution Engine
- [ ] **Container Image Creation**
    - [ ] Create `Dockerfile` based on `public.ecr.aws/lambda/python:3.12`.
    - [ ] Install common data science libraries (`pandas`, `numpy`, `scipy`, `scikit-learn`) to minimize runtime install needs.
    - [ ] Implement `main.py` entry point to handle the invocation payload.
- [ ] **Sandbox Logic Implementation (Inside Container)**
    - [ ] Implement file system logic: Write `/tmp/fix.py` (candidate) and `/tmp/test.py` (reproduction script).
    - [ ] Implement `subprocess` execution: Run `python /tmp/test.py`.
    - [ ] Capture `stdout`, `stderr`, and `return_code`.
    - [ ] Implement log sanitization to prevent massive output payloads.
    - [ ] **Security**: Implement pre-flight Regex check for dangerous keywords (`os.system`, `exec`, etc.).
- [ ] **Deployment**
    - [ ] Push Docker image to Amazon ECR.
    - [ ] Create Lambda function `pve-sandbox` using the ECR image.
    - [ ] Configure Memory (1024MB) and Timeout (10s).
    - [ ] Configure Network: Place in Private Subnet; Set NACLs to Deny Inbound / Allow Outbound 443 only (to PyPI mirrors if needed).

## Phase 4: Orchestration (AWS Step Functions)
- [ ] **State Machine Design**
    - [ ] Define `State Machine` using Amazon States Language (ASL).
    - [ ] **Step 1**: Task state triggering **Lambda A (Controller)**.
    - [ ] **Step 2**: Parallel state (Fan-Out) triggering 3 concurrent executions of **Lambda B (Sandbox)**.
    - [ ] **Step 3**: Task state triggering **Lambda C (Notifier/Decision)**.
- [ ] **Lambda C (Notifier) Implementation**
    - [ ] Implement logic to receive results from the Parallel state.
    - [ ] **Decision Logic**: Select winner based on `Exit Code 0` AND `Shortest Execution Time`.
    - [ ] Database Write: Save session details to DynamoDB.
    - [ ] WebSocket Push: Send result payload to the client via API Gateway Management API.

## Phase 5: API & Data Persistence
- [ ] **DynamoDB Setup**
    - [ ] Create Table `PVE_Main`.
    - [ ] Configure Partition Key: `PK` (e.g., `USER#<email>` or `SESSION#<uuid>`).
    - [ ] Configure Sort Key: `SK` (e.g., `PROFILE`, `META`, `FIX#<id>`).
    - [ ] Enable On-Demand Capacity mode.
- [ ] **S3 Setup**
    - [ ] Create bucket for storing large execution logs.
    - [ ] Configure lifecycle rules to delete objects after 24 hours.
- [ ] **API Gateway (WebSocket)**
    - [ ] Create WebSocket API.
    - [ ] Implement routes: `$connect`, `$disconnect`, `onMessage`.
    - [ ] Configure integration to trigger the Step Function upon request.

## Phase 6: Frontend Development (Next.js)
- [ ] **Project Setup**
    - [ ] Initialize Next.js 14 App Router project.
    - [ ] Install `shadcn/ui` and `lucide-react`.
    - [ ] Configure Tailwind CSS.
- [ ] **Authentication**
    - [ ] Wrap app with AWS Amplify configuration.
    - [ ] Implement Cognito flows (Sign In / Sign Up) with Google/GitHub providers.
- [ ] **Core Components**
    - [ ] **Editor**: Implement `@monaco-editor/react`.
    - [ ] **Code Analysis**: Implement "Smart Paste" detector and "Library Detector" (Regex).
    - [ ] **Console**: Build a terminal-like window to display WebSocket messages.
    - [ ] **Diff Viewer**: Implement logic to show diff between original and fixed code.
- [ ] **State Management**
    - [ ] Set up Zustand store for managing WebSocket connection status and verification state.

## Phase 7: User Management & Quotas
- [ ] **Quota System**
    - [ ] Implement DynamoDB logic to decrement user credits on successful verification.
    - [ ] Create a UI component (Bar/Gauge) to show "Daily Verifications Remaining".
- [ ] **History & Sharing**
    - [ ] Implement "My Snippets" page to list past sessions.
    - [ ] Create dynamic route `/s/[id]` for sharing permalinks.

## Phase 8: Final Polish & Verification
- [ ] **Load Testing**: Simulate concurrent users using `wrk` or AWS tools to test Step Function limits.
- [ ] **Security Audit**: Verify IAM roles are tight; verify VPC isolation works.
- [ ] **Documentation**: Complete the `README.md` and API documentation.
