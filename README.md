# Note: 
	The performance evualtion for this project is been done on other pc then mine because of hardware shortage. 
# Simpelperf

**About The Project**

This code is designed to measure the network performance between a server and multiple clients. It is written in Python and it can be run on any machine that supports Python.The server listens on a specified port number and awaits a connection from a client. Once a client connects, the server receives data from the client and calculates the total transfer rate and the elapsed time for the transfer. The total transfer rate is displayed in the chosen format (Bytes, KB, MB, or GB) along with the interval, received data, and transfer rate.

**Prerequisites**

This code requires Python 3.6 or later version. It also requires the following modules:

    socket
    time
    argparse
    threading
    math


**Usage**

To run the server, use the following command on your terminal:
The code has two modes: server mode and client mode.

You can run the code in server mode by following this command.
    python3 simpleperf.py -s [-b BIND_ADDRESS] [-p PORT] [-f {Bytes,KB,MB,GB}]

You can also run the code in client mode to send data to the server:
    python3 simpleperf -c -I [server_ip] -p [server_port] -t [time]

