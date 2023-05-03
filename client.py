import socket
import argparse
import time
import threading
# Try to make a socket and connect to the Ip and port given by the user. 
def make_socket(server_ip, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, port))
        print("-------------------------------------------------")
        print(f"a client connected to {server_ip}: {port}")
        print("-------------------------------------------------")
        return client
    except ConnectionRefusedError:
        print("Error: failed to connect to server")
        exit() 
# The default will be invoked when user want to make a normal connection to the server. 
def default(server_ip, port, time_user, format):
    client = make_socket(server_ip, port)
    start_time = time.time()
    total_bytes = 0
    packet = bytearray(1000)# packet size
    while (time.time() - start_time) <= time_user:#We send data as long as the time is less then the user time. 
        sent_packet = client.send(packet)
        total_bytes += sent_packet# We add the number of bytes every time we send a packet to total bytes. 
    elapsed_time=time.time()-start_time
    data_bits = total_bytes * 8 # Total bytes is multplied to change to bits. 
    bandwidth_bps = data_bits /elapsed_time
    bandwidth_mbps = bandwidth_bps / 1000000
    print(f"ID               Interval         Transfer  Bandwidth")
    print(
        f"{server_ip}:{port}   0.0 - {time_user:.1f}      {convert(total_bytes,format)}   {bandwidth_mbps:.2f} Mbps")
    close_socket(client)# We close the sokcet we have made. 
# The interval function will be run when the client wants to see a print of each -i specifiend. 
def interval(server_ip, port, time_user, format, interval):
    client = make_socket(server_ip, port)
    total_send = 0
    start_time = time.time()
    last_print = start_time
    last_send = 0
    packet = bytearray(1000)
    i = 1# We satart by 1 as we cannot divide by zero to find the bandiwwith. 
    print(f"ID             Interval        Transfer    Bandwidth")
    while time.time() - start_time - 1 <= time_user:
        send_packet = client.send(packet)
        total_send += send_packet
        current_time = time.time()
        elapsed_time = current_time - last_print
        if current_time - last_print >= interval:
            interval_send = total_send - last_send
            # Print the stats here. 
            print(
                f"{server_ip}:{port}   {i-1}- {i+interval-1}           {convert(interval_send,format)}    {(interval_send*8)/(elapsed_time*1000000):.2f}Mbps"
            )
            i += interval
            last_print = current_time
            last_send = total_send
    All_elapsed_time=time.time()-start_time
    data_bits = total_send * 8
    bandwidth_bps = data_bits
    bandwidth_mbps = (bandwidth_bps / (All_elapsed_time*1000000))
    print(f"------------------Total sent data---------------------")# A the end we print the total data sent by the user.     
    print(f"{server_ip}:{port}   0.0 - {time_user:.1f}     {convert(total_send,format)}      {(bandwidth_mbps):.2f} Mbps")
    close_socket(client)
# The parrallel will be invoked whel the user wants to make parrallel connection to the server. 
def parallel(parallel, server_ip, port, time, format):
    threads=[]
    for i in range(parallel):# We make as many socket as the number of parrallel
        thread = threading.Thread(target=default, args=(server_ip, port,time,format),)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
# The num function will be run when the user wants to make send a spicific amount of data. 
def num(server_ip, port, num):
    client = make_socket(server_ip, port)
    Data_from_user = num.upper()
    size_data = int(Data_from_user[:-2])
    unit = Data_from_user[-2:]
    # We check what is the type of data comming inn and change to bytes to send to user. 
    if Data_from_user[-2:] in ["KB", "MB"]:
        size_data = int(Data_from_user[:-2])
        unit = Data_from_user[-2:]
        if unit == "KB":
            total_bytes_expected_to_send = size_data * 1000
        elif unit == "MB":
            total_bytes_expected_to_send = size_data * 1000000
    elif Data_from_user[-1:] == "B":
        size_data = int(Data_from_user[:-1])
        unit = "B"
        total_bytes_expected_to_send = size_data
    else:
        raise ValueError(
            "The Type in the amount data you want to send is not specified"
        )
    total_sent = 0
    start_time = time.time()
    packet = bytearray(1000)
    while total_sent <= total_bytes_expected_to_send:
        sent_packet = client.send(packet)
        total_sent += sent_packet
    elapsed_time = time.time() - start_time
    data_bits = total_sent * 8
    bandwidth_bps = data_bits / elapsed_time
    bandwidth_mbps = bandwidth_bps / 1000000
    print(f"ID               Interval        Transfer     Bandwidth")
    print(f"{server_ip}:{port}   0.0 - {elapsed_time:.1f}          {size_data}{unit}        {bandwidth_mbps:.2f} Mbps")
    close_socket(client)
# Extra function to make the code easy to read. 
def close_socket(client):
    client.sendall(bytes("Good bye!", "utf-8"))
    response = client.recv(1024)
    if "Good bye!" in response.decode("utf-8"):                
        print(response)
    else:
        print("Error: Did not receive Goodbye from the server.")
    client.close()
# As the user can choose in what format type the data transferd will be shown we need to convert based
# on what type of fomat the user wants in. 
def convert(total_bytes, format):
    output = ""
    if format == "Bytes":
        total_bytes = total_bytes
        unit = "Bytes"
        output += str(total_bytes) + " " + unit
    elif format == "KB":
        total_bytes = total_bytes / 1000
        out = round(total_bytes, 2)
        unit = "KB"
        output += str(out) + " " + unit
    elif format == "MB":
        total_bytes = total_bytes / 1000000
        unit = "MB"
        out = round(total_bytes, 2)
        output += str(out) + unit
    elif format == "GB":
        total_bytes = total_bytes / 1000000000
        unit = "GB"
        out = round(total_bytes, 2)
        output += str(out) + unit
    return output
def run_client(args): 
    if args.interval:# If client with -i is invoked. 
        interval(args.server_ip, args.port, args.time, args.format, args.interval)
    elif args.num:# If client with -n i is invoked. 
        num(args.server_ip, args.port, args.num)
    elif args.parallel:# If client with -P is invoked. 
        parallel(args.parallel, args.server_ip, args.port, args.time, args.format)
    else:# If ingen av de er invoked. 
        default(args.server_ip, args.port, args.time, args.format)