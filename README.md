# Elli bot

Elli is a simple car like platform capable to move based on the instructions recieved over the internet.

Here is a diagram of sommunication flow:

<p align="center">
  <img src="./assets/connections.png"/>
</p>

## Server

The server serves several roles:

- Webserver - it provides the only website - [index.html](./server/static/index.html)
- Rest Endpoint - rest endpoint for the webclient to talk to
- Socket Endpoint - for the bot to connect to

### Important values

In the top of the [index.html](./server/static/index.html) there is hardcoded IP adress of the rest endpoint.

### Run

To should do following to get the required packages (1) and start the server (2) after that the webserver is accassible on [127.0.0.1:5000](http://127.0.0.1:5000)

```bash
cd server
python setup.py install # (1)
python app.py # (2)
```

## Elli code

This code should run on the raspberry PI on the bot.

### Important value

On top of the [main file](./elli/elli.py) there is a server IP address that should match the real address.
