# Elli bot

Code running Elli bot and server

## Server

The server serves several roles:

- Webserver - it provides the only website - [index.html](./server/static/index.html)
- Rest Endpoint - rest endpoint for the webclient to talk to
- Socket Endpoint - for the bot to connect to

## Important values

In the top of the [index.html](./server/static/index.html) there is hardcoded IP adress of the rest endpoint.
