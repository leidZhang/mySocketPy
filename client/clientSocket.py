import pickle
from socket import * 

from utils import handleFullQueue

class clientSocket: 
    def __init__(self) -> None:
        self.clientSocket = socket(AF_INET, SOCK_STREAM) 
        self.hostName = '10.0.0.3' # your QCar ip
        self.port = 8081 
        self.done = False 

    def terminate(self) -> None: 
        self.done = True 
        self.clientSocket.close()
        print("Socket stopped")

    def run(self, queueLock, dataQueue, responseQueue) -> None: 
        try: 
            # self.hostName = input("Enter QCar IP address: ")  
            self.clientSocket.connect((self.hostName, self.port)) 

            while not self.done: 
                queueLock.acquire() 

                try: 
                    if not dataQueue.empty(): 
                        data = dataQueue.get() # get dict object
                        queueLock.release() 
                        self.clientSocket.sendall(pickle.dumps(data)) 

                        response = self.clientSocket.recv(1024)
                        responseData = pickle.loads(response) 
                        handleFullQueue(responseQueue, responseData) 
                    else: 
                        queueLock.release()
                except ConnectionResetError:
                        # Handle the case where the server closes the connection unexpectedly
                        print("Server connection reset. Reconnecting...")
                        self.terminate()  # Close the socket
                        self.clientSocket = socket(AF_INET, SOCK_STREAM)
                        self.clientSocket.connect((self.hostName, self.port))
        except Exception as e:
            print(f"An error occurred: {e}")
            self.terminate()
                
