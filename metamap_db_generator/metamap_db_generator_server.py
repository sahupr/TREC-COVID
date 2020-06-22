import config
import mysql.connector
import threading
import time
import socket

def tcp_send(conn, msg):
    conn.sendall((msg + config.STOP_STRING).encode('utf-8'))

def tcp_recv(conn):
    result = bytearray()
    while not result.endswith(config.STOP_STRING.encode('utf-8')):
        result.extend(conn.recv(config.BUF_SIZE))
    return result.decode('utf-8')[:-len(config.STOP_STRING)]

def update_db(a_id, result, stdout_lock):
    db = mysql.connector.connect(
        host = config.HOST,
        user = config.USER,
        passwd = config.PASSWD,
        database = config.DATABASE
    )
    cursor = db.cursor()
    cursor.execute('UPDATE {} SET {} = "{}" WHERE {} = {};'.format(config.TABLE, config.RESULT, result, config.ID, a_id))
    db.commit()
    stdout_lock.acquire()
    print('Doc {} updated to db.'.format(a_id))
    stdout_lock.release()
    cursor.close()
    db.close()

def handle_client(conn, client_id, docs, docs_lock, stdout_lock):
    stdout_lock.acquire()
    print('Client {} connected.'.format(client_id))
    stdout_lock.release()
    threads = []
    while len(docs) > 0:
        docs_lock.acquire()
        doc = docs.pop()
        docs_lock.release()
        a_id = doc[0]
        text = '. '.join(doc[1:-1])
        tcp_send(conn, text)
        stdout_lock.acquire()
        print('Doc {} distributed to client {}. Waiting for response...'.format(a_id, client_id))
        stdout_lock.release()
        result = tcp_recv(conn)
        if result == config.ERROR_STRING:
            stdout_lock.acquire()
            print('Doc {} could not be done by client {}.'.format(a_id, client_id))
            stdout_lock.release()
        else:
            stdout_lock.acquire()
            print('Doc {} done by client {}. Updating db...'.format(a_id, client_id))
            stdout_lock.release()
            thread = threading.Thread(target=update_db, args=(a_id, result, stdout_lock))
            thread.start()
            threads.append(thread)
    for thread in threads:
        thread.join()

if __name__ == '__main__':    
    start_time = time.time()

    print('Preparing tasks...')

    db = mysql.connector.connect(
        host = config.HOST,
        user = config.USER,
        passwd = config.PASSWD,
        database = config.DATABASE
    )
    cursor = db.cursor()
    cursor.execute('SELECT {}, {}, {} from {};'.format(config.ID, ', '.join(config.TEXT), config.RESULT, config.TABLE))
    docs = cursor.fetchall()[::-1]
    cursor.close()
    db.close()

    if not config.OVERWRITE:
        docs = [doc for doc in docs if doc[-1] is None]

    docs_lock = threading.Lock()
    stdout_lock = threading.Lock()

    threads = []
    
    num_clients = 0

    print('Tasks prepared. Waiting for connection...')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((config.SERVER_HOST, config.SERVER_PORT))
        sock.listen(config.MAX_NUM_CLIENTS)
        while len(docs) > 0:
            conn, addr = sock.accept()
            num_clients += 1
            thread = threading.Thread(target=handle_client, args=(conn, num_clients, docs, docs_lock, stdout_lock))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = time.time()

    print('Execution time: {} s'.format(end_time - start_time))
