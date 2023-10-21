## `Subscriby` backend

API (Backend) implementation of the `Subscriby`. Core service for managing subscriptions, provides HTTP-interface for interacting with subscriptions, analytics

### Configuration

Look inside `.example.env`, simply copy into `.env` and edit there. For now, there is no configuration documentation, TODO!

## Deploy / running

Backend should be started from Docker, simply do `docker compose up` after you finished configuring all other stuff

## Running under HTTPS / Reverse Proxy

For running under HTTPS, you should use reverse proxy (for example, NGINX), there will never be native support for SSL. Example NGINX configuration may be released soon. TODO

## Database migrations

- TODO

## Documentation

- TODO

## Something else?

Feel free to open issues for any questions / bugs!
