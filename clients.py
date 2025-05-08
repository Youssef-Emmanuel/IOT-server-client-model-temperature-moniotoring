import socket
import time
import dht
from machine import Pin

# Configure the hardware for each ESP
# Sensor 1 is for ESP1, and sensor 2 is for ESP2
sensor = dht.DHT11(Pin(4))  # Replace with the correct GPIO pin for each ESP
led = Pin(5, Pin.OUT)       # LED connected to a GPIO pin

# Wi-Fi credentials
SSID = "Youssef's iPhone"
PASSWORD = "Youssef5805"

# Server details
SERVER_IP = "172.20.10.2"  # Replace with the actual server IP address
SERVER_PORT = 5605        # Replace with the server's port number

# Connect to Wi-Fi
def connect_to_wifi():
    import network
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    
    while not wifi.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    
    print("Connected to Wi-Fi")
    print(wifi.ifconfig())

# Read sensor data
def read_sensor():
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print("Sensor read error:", e)
        return None, None

# Client function
def main(sensor_id):
    connect_to_wifi()
    
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((SERVER_IP, SERVER_PORT))
            print("Connected to server")
            
            # Read sensor data
            temperature, humidity = read_sensor()
            if temperature is not None and humidity is not None:
                # Include a sensor ID for differentiation
                data = f"{sensor_id},{temperature},{humidity}"
                client_socket.send(data.encode('utf-8'))
                print(f"Sensor {sensor_id} sent data:", data)
                
                # Receive response from server
                response = client_socket.recv(1024).decode('utf-8')
                print(f"Server response for Sensor {sensor_id}:", response)
                
                # Control LED based on server response
                if response == "ALERT":
                    led.on()  # Turn on LED for abnormal readings
                else:
                    led.off()  # Turn off LED for normal readings
                
            time.sleep(1)  # Adjust the timer as needed
        except Exception as e:
            print("Communication error:", e)
        finally:
            client_socket.close()
            print("Connection closed")

# Run the client code for Sensor 1 or Sensor 2
main(sensor_id=1)  # Change to `sensor_id=2` for the second ESP
