import socket
import time
from machine import Pin
import dht

# Server configuration
SERVER_IP = '192.168.1.9'  
SERVER_PORT = 5605          

# Hardware
normal_led = Pin(5, Pin.OUT)    # LED for high temperature
low_temp_led = Pin(0, Pin.OUT)  # LED for low temperature
sensor = dht.DHT11(Pin(14)) 

# Wi-Fi configuration
SSID = "SSID"                   # WI-FI SSID      
PASSWORD = "pass"               # Wi-Fi password

# Connect to Wi-Fi
def connect_wifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print(f"Connecting to Wi-Fi: {SSID}")
    while not wlan.isconnected():
        pass
    print(f"Connected to Wi-Fi. IP Address: {wlan.ifconfig()[0]}")

# Connect to the server
def connect_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
    return client

# Main loop
def main():
    connect_wifi()  # Ensure Wi-Fi connection
    client = connect_server()  # Connect to the server
    
    sensor_id = 1  # Assign a unique sensor ID for this client
    while True:
        # Read temperature from DHT11 sensor
        sensor.measure()
        temperature = sensor.temperature()
        print(f"Readings - Temperature: {temperature}°C")
        
        # Send data to the server
        message = f"{sensor_id},{temperature}"
        client.send(message.encode())
        
        # Receive and handle server response
        response = client.recv(1024).decode()
        print(f"Server response: {response}")
        
        # Control LEDs based on server response
        if response == "HighTemp":
            normal_led.on()
            low_temp_led.off()
        elif response == "LowTemp":
            normal_led.off()
            low_temp_led.on()
        else:
            normal_led.off()
            low_temp_led.off()
        
        # Wait for the next reading
        time.sleep(5)

# Run the program
if __name__ == "__main__":
    main()
