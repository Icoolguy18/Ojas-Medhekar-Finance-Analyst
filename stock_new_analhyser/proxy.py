import socket
import threading
import sys # Import sys for better error output
import logging # For more structured logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SimpleHTTPProxy:
    def __init__(self, host='127.0.0.1', port=8888, buffer_size=4096):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.server_socket = None
        self._running = False # To control server shutdown

    def _handle_client(self, client_socket, client_address):
        """Handles a single client connection."""
        remote_socket = None
        try:
            # Receive data from the client (first request line)
            request = client_socket.recv(self.buffer_size)
            if not request:
                return # Client disconnected
            first_line = request.split(b'\n')[0]
            parts = first_line.split(b' ')
            
            if len(parts) < 2:
                logging.warning(f"Malformed request from {client_address}: {first_line}")
                return

            method = parts[0]
            url = parts[1]

            if method == b'CONNECT':
                # This proxy doesn't properly handle CONNECT (HTTPS tunneling)
                # It would need to establish a direct tunnel and forward raw bytes.
                # For now, we'll log and close.
                logging.error(f"HTTPS CONNECT request from {client_address}. This proxy does not support HTTPS tunneling yet.")
                client_socket.sendall(b"HTTP/1.1 501 Not Implemented\r\n\r\n")
                return

            # Continue with HTTP parsing
            http_pos = url.find(b"http://")
            if http_pos == -1:
                temp = url
            else:
                temp = url[http_pos + 7:]

            port_pos = temp.find(b":")
            webserver_pos = temp.find(b"/")

            if webserver_pos == -1:
                webserver_pos = len(temp)

            webserver = ""
            port = 80 # Default to HTTP port

            if port_pos == -1 or webserver_pos < port_pos:
                webserver = temp[:webserver_pos].decode('utf-8')
            else:
                try:
                    port = int((temp[port_pos + 1:])[:webserver_pos - port_pos - 1])
                except ValueError:
                    logging.error(f"Invalid port in URL from {client_address}: {temp[port_pos + 1:]}")
                    client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                    return
                webserver = temp[:port_pos].decode('utf-8')
            
            if not webserver:
                logging.warning(f"Could not determine webserver from URL: {url}")
                client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                return

            logging.info(f"Proxying request from {client_address} to {webserver}:{port}")

            # Connect to the destination server
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.settimeout(5) # Set a timeout for connection
            remote_socket.connect((webserver, port))
            remote_socket.sendall(request)

            # Receive data from the destination server and forward it to the client
            while True:
                data = remote_socket.recv(self.buffer_size)
                if data:
                    client_socket.sendall(data)
                else:
                    break

        except socket.timeout:
            logging.error(f"Socket timeout during connection or data transfer for {client_address}")
        except socket.gaierror:
            logging.error(f"Could not resolve destination host for {client_address}: {webserver}")
            try:
                client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
            except Exception as e:
                logging.error(f"Failed to send 502 to {client_address}: {e}")
        except ConnectionRefusedError:
            logging.error(f"Connection refused by destination for {client_address}: {webserver}:{port}")
            try:
                client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
            except Exception as e:
                logging.error(f"Failed to send 502 to {client_address}: {e}")
        except Exception as e:
            logging.error(f"Error handling client {client_address}: {e}", exc_info=True)
        finally:
            client_socket.close()
            if remote_socket:
                remote_socket.close()
            logging.info(f"Connection closed for {client_address}")

    def start(self):
        if self._running:
            logging.warning("Proxy server is already running.")
            return

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self._running = True
            logging.info(f"Proxy server listening on {self.host}:{self.port}")

            while self._running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    logging.info(f"Accepted connection from {client_address}")
                    # Start a new thread to handle the client
                    client_handler = threading.Thread(target=self._handle_client, args=(client_socket, client_address))
                    client_handler.daemon = True # Allow main program to exit even if threads are running
                    client_handler.start()
                except socket.timeout:
                    # This timeout helps in gracefully shutting down if no connections are accepted
                    continue
                except Exception as e:
                    if self._running: # Only log if it's an unexpected error while still running
                        logging.error(f"Error accepting connection: {e}", exc_info=True)
                    break # Break if server socket is closed/error occurs during accept

        except Exception as e:
            logging.critical(f"Failed to start proxy server: {e}", exc_info=True)
        finally:
            self.stop() # Ensure socket is closed if start fails or loop exits

    def stop(self):
        if not self._running:
            logging.info("Proxy server is not running.")
            return

        logging.info("Shutting down proxy server...")
        self._running = False
        if self.server_socket:
            try:
                # This helps unblock the accept() call in the main loop
                self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()
                logging.info("Proxy server socket closed.")
            except Exception as e:
                logging.error(f"Error while closing server socket: {e}")
            finally:
                self.server_socket = None
