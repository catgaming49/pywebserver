import socket
import json
import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def format_http(info: dict, content: bytes = b'') -> bytes:
    formatted_str = info['Response'] + '\n'
    for k, v in info.items():
        if k != 'Response':
            formatted_str += f"{k}: {v}\n"
    formatted_str += '\n' + content.decode('utf-8')
    return formatted_str.encode('utf-8')

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def get_file_path(request_path):
    base_path = os.path.join(os.getcwd(), config['SERVER_ROOT'])
    file_path = os.path.join(base_path, request_path.lstrip("/"))
    return file_path

def serve_file(conn, file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        encoded_content = content.encode('utf-8')
        http_res = {
            'Response': 'HTTP/1.1 200 OK',
            'Content-Type': 'text/html',
            'Content-Length': str(len(encoded_content)),
        }
        response = format_http(http_res, encoded_content)
        conn.sendall(response)
    except FileNotFoundError:
        if file_path.endswith("/"):
            default_file_path = os.path.join(file_path, config['DEFAULT_INDEX_FILE'])
            serve_file(conn, default_file_path)
        else:
            http_res = {
                'Response': 'HTTP/1.1 404 Not Found',
                'Content-Type': 'text/plain',
                'Content-Length': '0',
            }
            response = format_http(http_res)
            conn.sendall(response)

CONFIG_FILE = "config.json"
config = load_config(CONFIG_FILE)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((config['IP'], config['PORT']))
sock.listen()

while True:
    conn, addr = sock.accept()
    data = conn.recv(1024).decode()
    if data:
        request_line = data.split('\n')[0]
        request_path = request_line.split()[1]
        if request_path == '/':
            default_file_path = os.path.join(config['SERVER_ROOT'], config['DEFAULT_INDEX_FILE'])
            serve_file(conn, default_file_path)
        else:
            file_path = get_file_path(request_path)
            serve_file(conn, file_path)
    conn.close()

