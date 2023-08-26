# 🔐 Subscriby

Easy deployable system (API) for creating subscription based applications.

# Usage

- Deploy API on the yours server
- Query your subscription key from user inside your application
- [additional] Create new subscription for yours (by hand or implementing any management applications, like Telegram bot or any website).

# Deployment

Project currently only deployable with docker-compose (`docker-compose.yml` exists).
Just run docker compose and all will start for you (Database, Server)

# Running under proxy

TBD. Just follow default configuration

# Configuration

Look inside `.example.env` for example configuration (write own inside `.env`)

# Features

- Creating new subscriptions
- Checking subscription status
- Revoking subscriptions
- Auth for system methods (publish, revoke)

# Roadmap

- Deployment and configuration guide
- More features to deal with subscription based - applications
- Included management system (bots, website)
