# Atlantis IP Gate
This container allows forwarding of IPs based on OAuth-Authentication into internal networks, it consists of two container, a flask App/API-Server, which manages the state and takes requets, and nginx-container which does the actual forwarding:

    version: '3'
    services:
      flask:
        restart: always
        image: harbor-registry.atlantishq.de/atlantishq/atlantis-ip-gate-listener:latest
        ports:
            - 8001:5000
        volumes:
          - vpn-gate-data:/app/data/
        environment:
          - APP_SECRET=<SECRET_FOR_API_REQUESTS>
      nginx:
        restart: always
        image: harbor-registry.atlantishq.de/atlantishq/atlantis-ip-gate-nginx:latest
        volumes:
          - vpn-gate-data:/data/
        ports:
          - 8000:8000
        environment:
          - TARGET=<INTERNAL_URL_AND_PORT>
    volumes:
      vpn-gate-data:

If you want to use this to forward into a VPN, make sure this container runs on the same host as the VPN or otherwise has access to it.

You can use [this repository](https://github.com/FAUSheppy/atlantis-management/) to interface with it.

# Endpoints
- `/activate` - Allow IP access
- `/am-i-unlocked` - Check if your IP has access
- `/one-time-token` - Get a one time token for a client to use, to unlock itself
