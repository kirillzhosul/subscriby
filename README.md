# 🔐 Subscriby

Easy deployable system (API) for creating subscription based applications

# Use case

- You have desktop or other application that requires subscription
- You want to use subscription-like tokens/keys

# How to use

- Deploy API on the your server (WIP: Cloud delivered usage)
- Query your subscription key from user inside your application (fetch API call)
- Create and manage new subscription for users (by hand, implementing own management tool, or use premade inside `frontends` directory)

# Configuration

- `SUBSCRIBY_AUTH_METHOD`: Auth methods to use (See `Authorization`)

# Authorization

- `none`: No additional authorization
- `secret`: Require `secret` GET field or `Authorization` header (with or without `Bearer`) which should equals to `SUBSCRIBY_AUTH_SECRET`
- `custom`: Will call `plugins/custom_auth` plugin with your own code.

# Frontends

- Telegram bot [`frontends/telegram`](frontends/telegram)

# Features

- Creating new subscriptions
- Checking subscription status
- Revoking subscriptions
- Analytics (KPI, even for your payload via plugin)
- Custom payload injected within subscriptions
- Auth for system methods (publish, revoke)

# Plugins

There is support for custom plugins for:

- Auth (Check own custom auth)
- Payload (Inject custom payload with or without validation)
- Analytics (Inject own KPI trackers)

# Deployment

(How to deploy API)

- Do `git clone` on your server
- Edit `.example.env` and copy to `.env`
- Run `docker compose up -d` inside `backend` directory

# Built stack

- Python (FastAPI)
- PostgreSQL (SQLAlchemy)
- Docker
- Gunicorn with Uvicorn under the hood

# Running behing a proxy

Should be same as default deployment but you have to declare proxy to the API (Like, for NGINX)
