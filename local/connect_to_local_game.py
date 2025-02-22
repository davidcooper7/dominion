from client import Client
import sys

if __name__ == '__main__':

    # Set name
    name = input('What would you like your name to be? ')

    # Set client
    PORT = 3666
    client = Client(PORT, name)
