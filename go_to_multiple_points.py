import serial
import time
ser = serial.Serial('/dev/ttyUSB0', 115200)  

def decoder_frame_data( data_received):

    split_index_CMD_start = data_received.index(':')
    split_index_CMD_stop = data_received.index('#',split_index_CMD_start + 1)

    split_index_X_start = data_received.index(':',split_index_CMD_stop+1)
    split_index_X_stop = data_received.index('#',split_index_X_start+1)

    split_index_Y_start = data_received.index(':',split_index_X_stop+1)
    split_index_Y_stop = data_received.index('#',split_index_Y_start+1)

    split_index_Theta_start = data_received.index(':',split_index_Y_stop+1)
    split_index_Theta_stop = data_received.index('#',split_index_Theta_start+1)

    cmd = data_received[split_index_CMD_start+1:split_index_CMD_stop]
    X = float(data_received[split_index_X_start+1:split_index_X_stop])
    Y = float(data_received[split_index_Y_start+1:split_index_Y_stop])
    Theta = float(data_received[split_index_Theta_start+1:split_index_Theta_stop])   
    return cmd,X,Y,Theta

def decoder_frame_vel(data_received):
    split_index_CMD_start = data_received.index(':')
    split_index_CMD_stop = data_received.index('#',split_index_CMD_start + 1)
    split_index_vr_start = data_received.index(':',split_index_CMD_stop+1)
    split_index_vr_stop = data_received.index('#',split_index_vr_start+1)
    split_index_vl_start = data_received.index(':',split_index_vr_stop+1)
    split_index_vl_stop = data_received.index('#',split_index_vl_start+1)

    cmd = data_received[split_index_CMD_start+1:split_index_CMD_stop]
    vr = float(data_received[split_index_vr_start+1 : split_index_vr_stop])
    vl = float(data_received[split_index_vl_start+1 : split_index_vl_stop])
    return cmd ,vr, vl 


# def send_point(x, y, theta):
#     sending_data = "!cmd:RUN#x:{}#y:{}#theta:{}#\n".format(x, y, theta)
#     ser.write(sending_data.encode())
#     print(sending_data)

# def send_destiny(*points):
#     if not points:
#         return
#     temp_point = points.pop(0);
#     send_point(temp_point)

def send_point(points,cmd):
    # global cmd
    if not points:
        return 
    if cmd == "STP":
        # time.sleep(10)
        temp = points.pop(0)

        sending_data = "!cmd:RUN#x:{}#y:{}#theta:0.00#\n".format(temp[0],temp[1])
        ser.write(sending_data.encode())
        # print(sending_data)
        print("################################################ points was sent ##############################33#############################3\n")
        # cmd = "RUN"


try:
    path = []
    path.append([0.4,-0.4])
    path.append([0.8,-0.4])
    path.append([1.2,0.0])
    # my_list.append([0.8,0.4])
    # my_list.append([0.4,0.4])
    # my_list.append([0.0,0.0])
    path.append([1.4,0.0])
    path.append([1.8,0.4])
    path.append([2.2,0.0])

    # points = [(2.0, 0.0,), (2.0, 2.0, 90.0),(0.0, 2.0, -90.0), (0.0, 0.0 , 90.0)]
    # data_send ="!cmd:RUN#v_r:-0.15#v_l:-0.15#" 
    # data_send = "!cmd:RUN#x:0.10#y:0.10#phi:0.00#"
    # data_send +="\n"
    # ser.write(data_send.encode())
    while True:
        data_received = ser.readline().decode('utf-8').strip()
        print(data_received+"\n")
        cmd,X,Y,Theta = decoder_frame_data(data_received)
        send_point(path,cmd)
        # print(f"cmd: {cmd}\nx: {X}\ny: {Y}\ntheta: {Theta}\n")
        # cmd,vr,vl = decoder_frame_vel(data_received);
        # print("cmd: {}\nvr: {}\nvl: {}\n".format(cmd,vr,vl))
        
        

        
except KeyboardInterrupt:
    ser.close()