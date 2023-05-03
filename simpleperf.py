import argparse
import ipaddress
from server import start_server
from client import run_client
# We validate the port
def valid_port(port):
    try:
        port = int(port)
        if not 1024 < port < 65536:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"{port} is not in the defined range. it should be highet then 1024 and lower then 65536TH")
    return port
# Validate the Ip adress given by the user. 
def valid_ip(ip_adress):
    try: 
        val=ipaddress.ip_address(ip_adress)
    except ValueError:
        raise argparse.ArgumentError(f"{ip_adress} is not valid")
    return ip_adress
# We make sure the tim is positive.
def valid_time(timer_user):
    try:
        time = int(timer_user)
        if time <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive value" % time)
    except ValueError:
                raise argparse.ArgumentTypeError(f"{timer_user} cannot be negative. ")
    return time
# The number of connection must not be higher the 5 and lower then 1. 
def parralell_check(value):
    try:
        num_parrallel=int(value)
        if not 0 <num_parrallel <=5:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not in the defined range. it should be highet then 0 and lower then 5")
    return num_parrallel
def main():
    parser = argparse.ArgumentParser(description="simpleperf measurs the bandwith the shows the amount of trafnser data by the given time.")
    parser.add_argument('-s', '--server',      action='store_true',     help='enter to the server')
    parser.add_argument('-b', '--bind',        type = valid_ip,         default="10.0.0.2",           help='get IP address')
    parser.add_argument('-c', '--client',      action='store_true',     help='client side of socket modell')
    parser.add_argument('-f', '--format',      type=str,                default='MB',                  choices=['BYTES','KB', 'MB', 'GB'] ,   help='choose the format of data')
    parser.add_argument('-I','--server_ip',    type=valid_ip ,          default='10.0.0.2',            help='IP address of the simpleperf server')
    parser.add_argument('-p','--port',         type=valid_port,         default=8088,                  help='Server port to connect to')
    parser.add_argument('-t','--time',         type=valid_time,         default=25,                    help='time of sending data to the server')
    parser.add_argument('-i','--interval',     type=valid_time,         default=None,                  help='interval of data transfering')
    parser.add_argument('-n','--num',          type=str,                default=None,                  help='transfer number of bytes')
    parser.add_argument('-P','--parallel',     type=parralell_check,    default=None,                  help='create parallel connection')
    args = parser.parse_args()
    if args.server and args.client: # If the user invoked -c and -s at the same time.     
        print('Error: you must run in server mode or client mode.')
        exit()
    elif args.server:# If user invoked -s
        try:
            start_server(args)
        except ValueError:
            print("Klarte ikk å starte server")
    elif not args.server and args.client:# if user invok -c and not -s 
        try:
            run_client(args)
        except ValueError:
            print("Klarte ikk å starte server")
    else:
        print('Error: you must run in server mode or client mode.')
        exit()
if __name__ == '__main__':
    main()
