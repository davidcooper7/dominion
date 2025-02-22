from server import Server

s = Server(12342, 2)
s.send_message('This is a test')