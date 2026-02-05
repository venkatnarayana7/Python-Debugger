$ErrorActionPreference = "Stop"

Write-Host "--- Truth Engine State Machine Deployer ---" -ForegroundColor Cyan

# 1. Ask for Lambda ARNs
$ControllerArn = Read-Host "Enter the ARN for the Controller Lambda (pve-controller)"
$SandboxArn = Read-Host "Enter the ARN for the Sandbox Lambda (pve-sandbox)"
$RoleArn = Read-Host "Enter the ARN for the Step Functions IAM Role"

# 2. Read and Replace in JSON
$JsonContent = Get-Content -Path "state_machine.asl.json" -Raw
$JsonContent = $JsonContent -replace "arn:aws:lambda:us-east-1:123456789012:function:pve-controller", $ControllerArn
$JsonContent = $JsonContent -replace "arn:aws:lambda:us-east-1:123456789012:function:pve-sandbox", $SandboxArn

$JsonPath = "state_machine.final.json"
$JsonContent | Set-Content -Path $JsonPath
Write-Host "Created $JsonPath with your ARNs." -ForegroundColor Green

# 3. Deploy
Write-Host "Deploying to AWS Step Functions..."
aws stepfunctions create-state-machine --name "TruthEngineOrchestrator" --definition (Get-Content $JsonPath -Raw) --role-arn $RoleArn

if ($?) {
    Write-Host "Deployment Verification Successful!" -ForegroundColor Green
} else {
    Write-Host "Deployment Failed." -ForegroundColor Red
}
