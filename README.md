## Start the Yubico U2F sample server

```sh
$ git clone https://github.com/Yubico/python-u2flib-server
$ python python-u2flib-server/examples/u2f_server.py
[18/Feb/2018 18:47:57] Starting server on http://localhost:8081
```
## Register your U2F device against the server

You can register a U2F device using the following python snippet:

[Source link](https://github.com/mirzlab/python-yubico-u2f-authn/blob/master/u2f-register.py)

```sh
$ git clone https://github.com/mirzlab/u2f-authn.git
$ python u2f-authn/u2f-register.py

Touch the U2F device you wish to register...
```

After touching your U2F device, the following message is printed:

```sh
Registration sucessful
```

## Authenticate your U2F device against the server

You can authenticate a U2F device using the following python snippet:

[Source link](https://github.com/mirzlab/python-yubico-u2f-authn/blob/master/u2f-authn.py)

```sh
$ git clone https://github.com/mirzlab/u2f-authn.git
$ python u2f-authn/u2f-authn.py

Touch the U2F device you wish to authenticate...
```

If the authentication is successful, the following message is printed:

```sh
Authentication successful
```
