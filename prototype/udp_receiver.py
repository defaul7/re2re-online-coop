"""UDP receiver for validated player-state JSON messages."""

import socket

from prototype.message_handler import MessageHandler


MAX_PACKET_SIZE = 1024


class UDPStateReceiver:
    """Receive bounded UDP datagrams and pass them to MessageHandler."""

    def __init__(self) -> None:
        self.handler = MessageHandler()

    def process_datagram(self, data: bytes) -> bool:
        """Accept a datagram only if it is bounded and contains a newer state."""
        if not isinstance(data, bytes):
            return False

        if not data or len(data) > MAX_PACKET_SIZE:
            return False

        try:
            payload = data.decode("utf-8")
        except UnicodeDecodeError:
            return False

        return self.handler.handle(payload)


def serve(host: str = "127.0.0.1", port: int = 37021) -> None:
    """Listen locally for player-state datagrams."""
    receiver = UDPStateReceiver()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((host, port))
        print(f"State receiver listening on {host}:{port}")
        print("Press Ctrl+C to stop.")

        try:
            while True:
                # Read one byte beyond the limit to detect oversized datagrams.
                data, address = server.recvfrom(MAX_PACKET_SIZE + 1)
                accepted = receiver.process_datagram(data)
                print(f"{address}: {'accepted' if accepted else 'rejected'}")
        except KeyboardInterrupt:
            print("\nState receiver stopped.")


if __name__ == "__main__":
    serve()
