import config
import threading
import socket
import subprocess
import os

def tcp_send(conn, msg):
    conn.sendall(msg.encode('utf-8') + config.STOP_STRING.encode('utf-8'))

def tcp_recv(conn):
    result = bytearray()
    while not result.endswith(config.STOP_STRING.encode('utf-8')):
        data = conn.recv(config.BUF_SIZE)
        if len(data) == 0:
            return None
        result.extend(data)
    return result.decode('utf-8')[:-len(config.STOP_STRING)]

def make_connection():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((config.SERVER_HOST, config.SERVER_PORT))
        while True:
            text = tcp_recv(sock)
            if text is None:
                break
            try:
                proc = subprocess.run(['./metamaplite.sh', '--'], input=text, encoding='utf-8', stdout=subprocess.PIPE, timeout=config.METAMAP_TIMEOUT)
                output_str = proc.stdout
            except Exception as e:
                print(e)
                output_str = config.ERROR_STRING
            tcp_send(sock, output_str)

if __name__ == '__main__':
    os.chdir(config.METAMAP_DIR)
    threads = [threading.Thread(target=make_connection) for _ in range(config.NUM_THREADS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
