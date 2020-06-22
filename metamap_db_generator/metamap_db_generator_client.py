import config
import threading
import socket
import subprocess

def tcp_send(conn, msg):
    conn.sendall(msg.encode('utf-8') + config.STOP_STRING.encode('utf-8'))

def tcp_recv(conn):
    result = bytearray()
    while not result.endswith(config.STOP_STRING.encode('utf-8')):
        result.extend(conn.recv(config.BUF_SIZE))
    return result.decode('utf-8')[:-len(config.STOP_STRING)]

def make_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        while True:
            text = tcp_recv(sock)
            try:
                proc = subprocess.run(['./' + config.METAMAP_PATH, '--'], input=text, encoding='utf-8', stdout=subprocess.PIPE, timeout=config.METAMAP_TIMEOUT)
                output_str = proc.stdout
            except Exception as e:
                print(e)
                output_str = config.ERROR_STRING
            tcp_send(sock, output_str)

if __name__ == '__main__':
    threads = [threading.Thread(target=make_connection) for _ in range(NUM_THREADS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
