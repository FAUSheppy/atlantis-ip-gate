# Description
This is a two-container setup, one flask container, which will listen for a secret and one nginx container which will only allow any ip through, which previously submitted the secret to the flask server.
For setup information consult the `docker-compose.yaml`.

# Endpoints
## listener (flask)

    curl server:port/activate?secret=secret
    curl server:port/list?secret=secret

## nginx

  curl server:port/ip
  curl server:port/    # the main location
