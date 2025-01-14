import socket

class tools:
    def show_IP():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address