import socket
import time
import threading


#Start esrver med lage en socket på ip og port given by the user. 
def start_server(args):
    server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((args.bind,args.port))
    server_socket.listen()
    print(f'-----------------------------------------------------')
    print('A simpleperf server is listening on port ',args.port)
    print(f'-----------------------------------------------------')
    while True:# We are are listening until the code is interupted. 
        bufsize = 1000
        client_socket, addr = server_socket.accept()
        t = threading.Thread(target=handle_cleint, args=(client_socket, addr, bufsize,args))# We use threading in order to handle multiple client at the same time. 
        t.start()
# We recieve the data and adds it to variabel 
def receive_data(client_socket, bufsize):
    total_bytes_received = 0
    start_time= time.time()
    while True:
        data = client_socket.recv(bufsize)
        if  len(data)<=0:
            break
        if  "Good bye" in data.decode("utf-8"):# We look after any Good in data reciveving 
            client_socket.sendall(bytes("Good bye!", "utf-8"))
            break
        total_bytes_received += len(data)
    elapsed_time = time.time()- start_time
    return total_bytes_received, elapsed_time
# In order to handle multiple client we need to take each of the seprately. 
def handle_cleint(client_socket, addr, bufsize,args):
    print(f'A simpleperf client with {addr[0]}:{addr[1]} is client is connected with {args.bind}:{args.port}')
    total_bytes_received, elapsed_time = receive_data(client_socket, bufsize)
    # Calculate Total_transfer  and format output
    if args.format == 'Bytes':
         Total_transfer= total_bytes_received 
         unit = 'Bytes'
    elif args.format == 'KB':
        Total_transfer  = total_bytes_received  / 1000
        unit = 'KB'
    elif args.format == 'MB':
        Total_transfer  = total_bytes_received  / 1000000
        unit = 'MB'
    else: #args.format == 'GB'
        Total_transfer  = total_bytes_received  / 1000000000
        unit = 'GB'
    databits=total_bytes_received*8
    bandwidth_bps=databits/elapsed_time
    bandwidth_mbps=bandwidth_bps/1000000
                                                                                     
    print(f'ID                   Interval      Receieved      Rate')                                    
    print(f'{addr[0]}:{addr[1]}      0.0-{int(elapsed_time)}        {Total_transfer :.2f} {unit}           {(bandwidth_mbps):.2f}Mbps ')