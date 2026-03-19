---
name: aws-iam-access
description: Configure and operate AWS access from local machine using AWS CLI + IAM Identity Center (SSO), validate identity, inspect IAM/account permissions, and run safe IAM/EC2/SSM operational diagnostics. Use when user asks for AWS IAM access, SSO setup, credential validation, or autonomous AWS troubleshooting.
---

# AWS IAM Access

Use this skill when the user needs AWS IAM access configured locally, wants autonomous AWS diagnostics, or needs operational actions gated by IAM permissions.

## Default Behavior

- Prefer IAM Identity Center (SSO) profile `codex-ops`.
- Validate auth before any AWS operation.
- Default to read/diagnostic operations first.
- Ask explicit confirmation before destructive changes (delete, terminate, policy detach, permission narrowing/widening).

## Prerequisites

- AWS CLI v2 installed at `C:\Program Files\Amazon\AWSCLIV2\aws.exe`.
- Session Manager plugin installed.
- SSO profile configured (`codex-ops` by default).

## Fast Auth Check (mandatory)

Run this before AWS commands:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\aleco\bin\aws-sso-ensure.ps1 -Profile codex-ops
```

If token is expired, script triggers `aws sso login` and re-validates with `sts get-caller-identity`.

## SSO Bootstrap (if profile not configured)

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\aleco\bin\aws-sso-bootstrap.ps1 \
  -StartUrl "https://YOUR.awsapps.com/start" \
  -AccountId "123456789012" \
  -RoleName "AdministratorAccess" \
  -SsoRegion "us-east-1" \
  -Region "us-east-1" \
  -Profile "codex-ops"
```

## Common Read Diagnostics

```powershell
aws sts get-caller-identity --profile codex-ops
aws iam get-account-summary --profile codex-ops
aws ec2 describe-instances --max-items 20 --profile codex-ops
aws ssm describe-instance-information --profile codex-ops
```

## Saira Prod Connectivity Triage

When host SSH times out but AWS auth is valid:

1. Check instance state and SG/NACL path for port 22.
2. Check if SSM is available to bypass SSH for diagnostics.
3. If SSM unavailable, verify IAM instance profile and SSM agent prerequisites.
4. Propose minimal corrective action; execute only after user confirmation for impactful changes.

## Expected Output Style

- Report exact commands run.
- Report what worked, what failed, and why.
- Include next action with minimum-risk order.
