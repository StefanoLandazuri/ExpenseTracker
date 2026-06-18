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
docker compose -f docker-compose.prod.yml logs -f
```

## Production compose file

The EC2 runs `docker-compose.prod.yml` (checked into this repo), **not**
`docker-compose.yml` — that one is dev-only: it builds from local source
and bind-mounts `./backend`, which would make the EC2 run whatever happens
to be on its disk instead of the image you tested and pushed to ECR.

`docker-compose.prod.yml` only references `image:` (no `build:`, no
bind-mount) and drops the `--reload` flag, so a deploy is always an
immutable image swap.

It expects two variables, supplied via a `.env` file living next to it on
the EC2 (gitignored, never committed):

```bash
# /home/ec2-user/app/.env on the EC2 — not in git
ECR_IMAGE=ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/expense-tracker-backend:latest
JWT_SECRET=<real secret, rotate via your secrets manager>
```

## Redeploy procedure

```bash
# Local — build and push
docker build -t expense-tracker-backend ./backend
docker tag expense-tracker-backend:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/expense-tracker-backend:latest
docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/expense-tracker-backend:latest

# EC2 — pull and restart
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml down && docker compose -f docker-compose.prod.yml up -d
```