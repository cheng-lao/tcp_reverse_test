### tcp_reverse_test


*please ensure that your computer have the python3 installed.* :yum:

### Usage

please run the server first :airplane:
```bash
python reversetcpserver.py -p <your-server-port>
```

then run the client :rocket:

```bash
python reversetcpclient.py -ip <your-server-ip> -p <your-server-port> -f <your-txt-filepath>
# please ensure that the file path is correct and the file exists.
```

- note that the client will send the file to the server and the server will send the reversed string back to the client. the client will print the reversed string to the console and save it to a file in the same directory as the client script. :ok_hand:

- please ensure that the server is running before running the client.**And the os is different between the server and the client.** :)

# END :kissing_closed_eyes: :+1: :wave:
