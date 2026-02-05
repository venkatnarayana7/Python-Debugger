$ErrorActionPreference = "Stop"

Write-Host "--- Truth Engine WebSocket API Deployer ---" -ForegroundColor Cyan
Write-Host "This script helps create a WebSocket API in AWS API Gateway." -ForegroundColor Yellow
Write-Host ""

# 1. Collect Inputs
$ApiName = Read-Host "Enter API Name (e.g., pve-websocket)"
$StageName = Read-Host "Enter Stage Name (e.g., dev)"

$ConnectLambdaArn = Read-Host "Enter the ARN for the Connect Lambda"
$DisconnectLambdaArn = Read-Host "Enter the ARN for the Disconnect Lambda"

# 2. Create WebSocket API
Write-Host "`nCreating WebSocket API..."
$CreateApiResult = aws apigatewayv2 create-api `
    --name $ApiName `
    --protocol-type WEBSOCKET `
    --route-selection-expression '$request.body.action' `
    --output json | ConvertFrom-Json

$ApiId = $CreateApiResult.ApiId
Write-Host "Created API: $ApiId" -ForegroundColor Green

# 3. Create Integrations
Write-Host "`nCreating $connect integration..."
$ConnectIntegration = aws apigatewayv2 create-integration `
    --api-id $ApiId `
    --integration-type AWS_PROXY `
    --integration-uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$ConnectLambdaArn/invocations" `
    --output json | ConvertFrom-Json

$ConnectIntegrationId = $ConnectIntegration.IntegrationId

Write-Host "Creating $disconnect integration..."
$DisconnectIntegration = aws apigatewayv2 create-integration `
    --api-id $ApiId `
    --integration-type AWS_PROXY `
    --integration-uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$DisconnectLambdaArn/invocations" `
    --output json | ConvertFrom-Json

$DisconnectIntegrationId = $DisconnectIntegration.IntegrationId

# 4. Create Routes
Write-Host "`nCreating routes..."
aws apigatewayv2 create-route --api-id $ApiId --route-key '$connect' --target "integrations/$ConnectIntegrationId" | Out-Null
aws apigatewayv2 create-route --api-id $ApiId --route-key '$disconnect' --target "integrations/$DisconnectIntegrationId" | Out-Null

# 5. Deploy
Write-Host "`nDeploying to stage: $StageName..."
aws apigatewayv2 create-stage --api-id $ApiId --stage-name $StageName --auto-deploy | Out-Null

# 6. Output
$Endpoint = "wss://$ApiId.execute-api.us-east-1.amazonaws.com/$StageName"
Write-Host "`n--- DEPLOYMENT COMPLETE ---" -ForegroundColor Green
Write-Host "WebSocket Endpoint: $Endpoint" -ForegroundColor Cyan
Write-Host "Use this endpoint in your frontend to connect."
