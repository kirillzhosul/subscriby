# 🔐 Subscriby

Easy deployable system (API) for creating subscription based applications

# Use case

- You have desktop or other application that requires subscription
- You want to use subscription-like tokens/keys

# How to use

- Deploy API on the your server (WIP: Cloud delivered usage)
- Query your subscription key from user inside your application (fetch API call)
- Create and manage new subscription for users (by hand, implementing own management tool, or use premade inside `frontends` directory)

# Deployment

(How to deploy API)

- Do `git clone` on your server
- Edit `.example.env` and copy to `.env`
- Run `docker compose up -d` inside `backend` directory

# Configuration

Main fields is `SUBSCRIBY_AUTH_METHOD` and `SUBSCRIBY_AUTH_SECRET`
where `SUBSCRIBY_AUTH_METHOD` should be `none` or `secret`, when you use `secret`, management API calls require user to pass `secret` field which should be equals to `SUBSCRIBY_AUTH_SECRET` (and `none` will not require any)

# Features

- Creating new subscriptions
- Checking subscription status
- Revoking subscriptions
- Auth for system methods (publish, revoke)
