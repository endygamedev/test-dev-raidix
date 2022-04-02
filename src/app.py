# @name:    TCP Chat Server
# @author:  Egor Bronnikov
# @licence: MIT
# @edited:  03-04-2022


# Modules
import socket
import select
import sys
from _thread import *
import syslog

from style import Color, Style


class Server:
    def __init__(self, *, ipaddr, port):
        """
            @Synopsis
            import socket

            def __init__(self, *, ipaddr: str, port: int) -> None

            @Description
            Class that creates server socket and listen requests.

            @param ipaddr: IP address on which the server socket will be opened
            @type ipaddr: str
            @param port: Port on which the server socket will be opened
            @type port: int

            @return: `side effect`: Creates a server socket and listens for requests
            @rtype: None
        """
        self.ipaddr = ipaddr
        self.port = port
        self.users = 0              # The number of users, to be used for ID
        self.clients = []           # List of active connections
        self._BUFSIZE = 4096        # The maximum amount of data to be received at once
        self._CONNCNT = 100         # Listens for 100 active connections

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_setup()
        self.mainloop()

    def server_setup(self):
        """
            @Synopsis
            import socket
            import syslog

            def server_setup(self) -> None

            @Description
            Binds the server to an entered IP address and the specified port number. Start listening connections.
            If this port is busy, it prints an error message and write it in syslog.

            @return: `side effect`: Implement bind and listen for server
            @rtype: None
        """
        try:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.ipaddr, self.port))
            self.server.listen(self._CONNCNT)
        except OSError as e:
            print(f"{Style.BOLD}{Color.RED}Failed to start the server: {e}.{Color.DEFAULT}{Style.NORMAL}")
            syslog.syslog(syslog.LOG_ERR, f"Failed to start the server: {e}")
            exit()

    def client_thread(self, conn, user_id):
        """
            @Synopsis
            import socket
            import syslog

            def client_thread(self, conn: socket.socket, user_id: int) -> None

            @Description
            Works with the client. New process for the client, which will receive messages from the server and server
            will receive messages from this client. Print on the screen and write all received messages from clients
            in the syslog.

            @param conn: Client's socket
            @type conn: socket.socket
            @param user_id: User ID of this socket, this is needed for a nice output
            @type user_id: int

            @return: `side effect`: Exchanges data with clients
            @rtype: None
        """
        conn.send((f"{Style.BOLD}{Color.HEADER}Welcome to this chat room!{Color.DEFAULT}{Style.NORMAL}\n").encode())
        print(f"{Style.UNDERLINE}{Style.DIM}{Color.GREEN}User {user_id} connected{Color.DEFAULT}{Style.NORMAL}")
        syslog.syslog(syslog.LOG_INFO, f"User: {user_id}, Connected")
        conn.send((f"{Color.CYAN}>> You (User {user_id}): {Color.DEFAULT}").encode())
        while True:
            try:
                message = conn.recv(self._BUFSIZE).decode("utf-8")      # Get message from the client
                if message:
                    syslog.syslog(syslog.LOG_DEBUG, f"User: {user_id}, Message: {message}")     # Write message in syslog
                    message_to_send = f"{Color.YELLOW}<<User {user_id}>>:{Color.DEFAULT} {message}"
                    print(message_to_send, end="")
                    self.broadcast(("\n\t" + message_to_send).encode(), conn, user_id)      # Send this message to other clients
                    conn.send((f"{Color.CYAN}>> You (User {user_id}): {Color.DEFAULT}").encode())
                else:
                    self.remove(conn, user_id)
            except:
                continue

    def broadcast(self, message, connection, user_id):
        """
            @Synopsis
            import socket

            def broadcast(self, message: bytes, connection: socket.socket, user_id: int) -> None

            @Description
            Transfer a message from one client to all others clients.

            @param message: The client's message
            @type message: bytes
            @param connection: The socket of the client who sent the message
            @type connection: socket.socket
            @param user_id: The User ID of the client who sent the message
            @type user_id: int

            @return: `side effect`: Send message to other clients
            @rtype: None
        """
        for i in range(len(self.clients)):
            if self.clients[i] != connection:
                try:
                    self.clients[i].send(message)
                    self.clients[i].send((f"{Color.CYAN}>> You (User {i + 1}): {Color.DEFAULT}").encode())
                except:
                    self.clients[i].close()
                    self.remove(self.clients[i], user_id)
            else:
                # Notifies the user that the message has been successfully delivered
                self.clients[i].send((f"\t{Style.DIM}{Color.GREEN}Your message was successfully delivered{Color.DEFAULT}{Style.NORMAL}\n").encode())

    def remove(self, connection, user_id):
        """
            @Synopsis
            import socket
            import syslog

            def remove(self, connection: socket.socket, user_id: int) -> None

            @Description
            Remove the active connection (client) if something goes wrong.

            @param connection: Broken connection socket
            @type connection: socket.socket
            @param user_id: The User ID of broken connection
            @type user_id: int

            @return: `side effect`: Remove the user from the list of active connections
            @rtype: None
        """
        if connection in self.clients:
            print(f"{Style.UNDERLINE}{Style.DIM}{Color.RED}User {user_id} disconnected{Color.DEFAULT}{Style.NORMAL}")
            syslog.syslog(syslog.LOG_INFO, f"User: {user_id}, Disconnected")
            self.clients.remove(connection)

    def mainloop(self):
        """
            @Synopsis
            import socket
            from _thread import *
            import syslog

            def mainloop(self) -> None

            @Description
            The main loop that handles all clients connections and, if necessary, creates a new thread for a new user.
            You can stop the server with the `KeyboardInterrupt` and this information will be recorded in syslog.

            @return: `side effect`: Handles new connections
            @rtype: None
        """
        print(f"{Style.BOLD}{Color.HEADER}Server on {ipaddr}:{port} is ready!\nWaiting for users...\n{Color.DEFAULT}{Style.NORMAL}")

        while True:
            try:
                conn, _ = self.server.accept()  # Accept a connection request and store a socket object of that user
                self.clients.append(conn)       # Append new client in list of active connections
                self.users += 1                 # Increase the Used ID

                # Start new thread for new connection
                start_new_thread(self.client_thread, (conn, self.users))
            except KeyboardInterrupt:   # Stopping the server
                print(f"\n{Style.BOLD}{Color.RED}You closed the server{Color.RED}{Style.NORMAL}")
                syslog.syslog(syslog.LOG_INFO, "The server was shut down")
                break

        for client in self.clients:
            client.send((f"\n\t{Style.BOLD}{Color.RED}The server stopped working{Color.DEFAULT}{Style.NORMAL}").encode())
            client.close()

        self.server.close()


class Client:
    def __init__(self, *, ipaddr, port):
        """
            @Synopsis
            import socket

            def __init__(self, *, ipaddr: str, port: int) -> None

            @Description
            Class that creates client socket and connects to the server socket.

            @param ipaddr: IP address on which the server socket opened
            @type ipaddr: str
            @param port: Port on which the server socket opened
            @type port: int

            @return: `side effect`: Creates a new client socket and connects to the server socket
            @rtype: None
        """
        self.ipaddr = ipaddr
        self.port = port
        self._BUFSIZE = 4096    # The maximum amount of data to be received at once

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.mainloop()

    def connect(self):
        """
            @Synopsis
            import socket
            import syslog

            def connect(self) -> None

            @Description
            Connects on a given IP address and port to the server. If the connection is impossible, it prints an error message
            and writes to the syslog.

            @return: `side effect`: Connects to the server
            @rtype: None
        """
        try:
            self.server.connect((self.ipaddr, self.port))
        except ConnectionRefusedError as e:
            print(f"{Style.BOLD}{Color.RED}Failed to connect to the server: {e} {Color.DEFAULT}{Style.NORMAL}")
            syslog.syslog(syslog.LOG_ERR, f"Failed to connect to the server: {e}")

    def mainloop(self):
        """
            @Synopsys
            import socket
            import select

            def mainloop(self) -> None

            @Description
            The main loop in which the client sends messages to the server and receives messages from the server to other
            clients.

            @return: `side effect`: Exchanges data with the server
            @rtype: None
        """
        while True:
            try:
                sockets_list = [sys.stdin, self.server]     # Maintains a list of possible input streams (sent and receive)

                read_sockets, _, _ = select.select(sockets_list, [], [])

                for socks in read_sockets:
                    if socks == self.server:
                        message = socks.recv(self._BUFSIZE)
                        sys.stdout.write(message.decode("utf-8"))
                        sys.stdout.flush()
                    else:
                        message = sys.stdin.readline()
                        self.server.send(message.encode())
            except KeyboardInterrupt:       # Left from the char room and close connection
                print(f"\n{Style.BOLD}{Color.RED}You left from this chat room{Color.DEFAULT}{Style.NORMAL}")
                break
            except BrokenPipeError:         # The case when the server is down
                break

        self.server.close()


if __name__ == "__main__":
    # Checks whether sufficient arguments have been provided
    if len(sys.argv) != 4:
        print(f"{Style.BOLD}{Color.RED}Correct usage: script, mode (s | c), IP address, port number{Color.DEFAULT}{Style.NORMAL}")
        exit()

    mode = sys.argv[1]      # `s` for server and `c` for client
    ipaddr = sys.argv[2]
    port = int(sys.argv[3])

    if mode == "s":
        Server(ipaddr=ipaddr, port=port)
    elif mode == "c":
        Client(ipaddr=ipaddr, port=port)
    else:
        print(f"{Style.BOLD}{Color.RED}Unknown operation mode. You need to use `s` for server mode and `c` for client mode.{Color.DEFAULT}{Style.NORMAL}")
        exit()
