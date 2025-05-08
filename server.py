import socket
import threading


port = 5605
MaxTemp = 27
MinTemp = 25

# Function to handle each client connection
def handle_client(client, addr):
    print(f'Connected to client {addr}')
    while True:
        message = client.recv(1024) #Recives the message from the client
        if not message:
            break
        char_message = message.decode() #Decode the message
        sensor_id, temperature= map(float, char_message.split(',')) # Split the message by ',' and convert values to float
        print(f"Received from Sensor {int(sensor_id)}: Temp={temperature} ")
        if temperature < MinTemp: #checks if the temperature less than the threshold
            response = "LowTemp"
        elif MinTemp<= temperature <= MaxTemp: #checks if the temperature within the normal range
            response = "NORMAL"
        else:
            response = "HighTemp"
        client.send(response.encode()) #sends the message to the client
    print(f'Disconnected from client {addr}')
    client.close() # close the connection with the client


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port)) # binds the socket to all available network interfaces on the specified port
    server_socket.listen()
    print(f"Server is listening on port {port}...")

    while True:
        client, addr = server_socket.accept() 
        threading.Lock().acquire() # Acquire a lock to prevent simultaneous access by multiple threads
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start() # Starts the thread

if __name__ == '__main__':
    main()
