import socket

HOST = "127.0.0.1"
PORT = 37020

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    print(f"UDP test server listening on {HOST}:{PORT}")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            data, address = server.recvfrom(2048)
            message = data.decode("utf-8", errors="replace")
            print(f"{address}: {message}")
            server.sendto(b"ACK: " + data, address)
    except KeyboardInterrupt:
        print("\nServer stopped.")
