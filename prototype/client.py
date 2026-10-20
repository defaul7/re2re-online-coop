import socket

SERVER = ("127.0.0.1", 37020)
MESSAGE = b"Hello from RE2 co-op prototype"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    client.settimeout(3)
    client.sendto(MESSAGE, SERVER)

    try:
        data, address = client.recvfrom(2048)
        print(f"Response from {address}: {data.decode()}")
    except socket.timeout:
        print("No response: server may not be running.")
