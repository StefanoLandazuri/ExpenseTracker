# Operations Runbook

## Infrastructure

- **EC2 IP:** <EC2IP>
- **Region:** <your-region>
- **DynamoDB table:** expenses-prod

## SSH Access

```bash
ssh -i ~/.ssh/expense-tracker-key.pem ec2-user@<EC2IP>
```

## View logs

```bash
docker compose logs -f
```

## Redeploy procedure

```bash
# Local — build and push
docker build -t expense-tracker-backend ./backend
docker tag expense-tracker-backend:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/expense-tracker-backend:latest
docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/expense-tracker-backend:latest

# EC2 — pull and restart
docker compose pull
docker compose down && docker compose up -d
```