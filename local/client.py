import socket

HOST = 'localhost'  

class Client():
    def __init__(self, PORT, name):
        self.name = name
        print('Welcome', self.name)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.connect((HOST, PORT))
            self.s.sendall(self.name.encode())
            print(f"Connected to {HOST} with {PORT}")

            while True:
                msg_r = self.receive_message()
                if msg_r == 'exit':
                    break
                try:
                    msg, r = msg_r.split('_')
                    print(msg)
                except:
                    raise Exception(msg_r)
                if r == 'y':
                    response = input('RESPONSE>>>')
                    print('Sending response:', response)
                    self.send_message(response)

    def send_message(self, msg):
        data = msg.encode()
        self.s.sendall(data)

    def receive_message(self):
        data = self.s.recv(1024)
        return data.decode()
                