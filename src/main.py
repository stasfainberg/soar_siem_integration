import sys


def init_db():
    pass


def check_ip_reputation(ip):
    pass

def save_ip_reputation(ip, ip_type, score):
    pass



if "__name__" == "__main__":

    # Check number of arguments
    if len(sys.argv) != 2:
        print(f"Usage: main.py <IP_ADDRESS>")
        sys.exit(1)
    
    # Get IP Address
    ip = sys.argv[1]

    # Init DB
    init_db()

    # Check ip reputation
    ip_type, score = check_ip_reputation(ip)

    # Save data in DB
    save_ip_reputation(ip, ip_type, score)

    # print exit message
    print(f"IP: {ip}, Type: {ip_type}, Reputation Score: {score}")

