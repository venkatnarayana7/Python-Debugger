# AWS Deployment Guide

## Prerequisites
- AWS CLI configured with appropriate permissions
- Docker installed (for building Lambda container images)
- IAM Role with Lambda, Step Functions, API Gateway, and DynamoDB permissions

## 1. Deploy Controller Lambda (Lambda A)

```bash
cd backend/controller

# Create deployment package
pip install -r requirements.txt -t package/
cp -r ag package/
cp main.py package/
cd package && zip -r ../controller.zip . && cd ..

# Deploy
aws lambda create-function \
    --function-name pve-controller \
    --runtime python3.12 \
    --handler main.lambda_handler \
    --zip-file fileb://controller.zip \
    --role arn:aws:iam::YOUR_ACCOUNT:role/PVE-Lambda-Role \
    --timeout 30 \
    --memory-size 512 \
    --environment Variables="{GEMINI_API_KEY=xxx,GROQ_API_KEY=xxx,DEEPSEEK_API_KEY=xxx}"
```

## 2. Deploy Sandbox Lambda (Lambda B)

```bash
cd backend/sandbox

# Build Docker image
docker build -t pve-sandbox .

# Push to ECR
aws ecr create-repository --repository-name pve-sandbox
docker tag pve-sandbox:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/pve-sandbox:latest
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/pve-sandbox:latest

# Create Lambda from container
aws lambda create-function \
    --function-name pve-sandbox \
    --package-type Image \
    --code ImageUri=YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/pve-sandbox:latest \
    --role arn:aws:iam::YOUR_ACCOUNT:role/PVE-Lambda-Role \
    --timeout 10 \
    --memory-size 256
```

## 3. Create DynamoDB Table

```bash
aws dynamodb create-table \
    --table-name PVE_Connections \
    --attribute-definitions AttributeName=connectionId,AttributeType=S \
    --key-schema AttributeName=connectionId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

## 4. Deploy WebSocket API

Run the helper script:
```powershell
cd backend/websocket
.\deploy.ps1
```

## 5. Deploy Step Functions

```bash
cd backend/orchestration
.\deploy.ps1
```

## 6. Frontend Deployment

```bash
cd frontend
npm run build

# Deploy to Vercel (recommended)
npx vercel --prod

# Or to AWS Amplify
amplify push
```

## Environment Variables for Production

Update Lambda environment variables with production values:
- `WEBSOCKET_API_ENDPOINT`: Your WebSocket API endpoint
- `TABLE_NAME`: DynamoDB table name
