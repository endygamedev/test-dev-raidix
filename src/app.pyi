from socket import socket
from typing import List

class Server:
    def __init__(self, *, ipaddr: str, port: int) -> None:
        self.ipaddr = str
        self.port = int
        self.users = int
        self.clients = List[socket]
        self._BUFSIZE = int
        self._CONNCNT = int
        self.server = socket
        ...

    def server_setup(self) -> None: ...
    def client_thread(self, conn: socket, user_id: int) -> None: ...
    def broadcast(self, message: bytes, connection: socket, user_id: int) -> None: ...
    def remove(self, connection: socket, user_id: int) -> None: ...
    def mainloop(self) -> None: ...


class Client:
    def __init__(self, *, ipaddr: str, port: int) -> None:
        self.ipaddr = str
        self.port = int
        self._BUFSIZE = int
        self.server = socket
        ...

    def connect(self) -> None: ...
    def mainloop(self) -> None: ...