import serial
import time
import socket

# Serial setup
ser = serial.Serial('/dev/ttyUSB0', 115200)

# Socket setup
HOST = '127.0.0.1'  # Localhost, change to your server IP if needed
PORT = 65432        # Port to listen on
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

def decoder_frame_data(data_received):
    split_index_CMD_start = data_received.index(':')
    split_index_CMD_stop = data_received.index('#', split_index_CMD_start + 1)
    
    split_index_X_start = data_received.index(':', split_index_CMD_stop + 1)
    split_index_X_stop = data_received.index('#', split_index_X_start + 1)
    
    split_index_Y_start = data_received.index(':', split_index_X_stop + 1)
    split_index_Y_stop = data_received.index('#', split_index_Y_start + 1)
    
    split_index_Theta_start = data_received.index(':', split_index_Y_stop + 1)
    split_index_Theta_stop = data_received.index('#', split_index_Theta_start + 1)
    
    cmd = data_received[split_index_CMD_start + 1: split_index_CMD_stop]
    X = float(data_received[split_index_X_start + 1: split_index_X_stop])
    Y = float(data_received[split_index_Y_start + 1: split_index_Y_stop])
    Theta = float(data_received[split_index_Theta_start + 1: split_index_Theta_stop])
    return cmd, X, Y, Theta

def send_point(points, cmd):
    if not points:
        return
    if cmd == "STP":
        temp = points.pop(0)
        sending_data = "!cmd:RUN#x:{}#y:{}#theta:0.00#\n".format(temp[0], temp[1])
        ser.write(sending_data.encode())
        print("################################################ points was sent ##############################33#############################3\n")

try:
    # Accept a connection
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")
    # implement PSO to find the optimze path 
    path = [
        [0.4, -0.4],
        [0.8, -0.4],
        [1.2, 0.0],
        [1.4, 0.0],
        [1.8, 0.4],
        [2.2, 0.0]
    ]


    # main loop
    while True:
        data_received = ser.readline().decode('utf-8').strip()
        print(data_received + "\n")
        cmd, X, Y, Theta = decoder_frame_data(data_received)
        odom_data = "!cmd:{}#x:{}#y:{}#theta:{}#\n".format(cmd,X, Y,Theta)
        send_point(path, cmd)
        # Send odom data to the client
        
        client_socket.sendall(odom_data.encode())
        print("Sent to client:", odom_data)

        

except KeyboardInterrupt:
    ser.close()
    client_socket.close()
    server_socket.close()
    print("Server and serial connection closed.")
