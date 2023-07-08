enviroment:
    python3.10
    Ubuntu 22.04 LTS

usage:
    tcp bind 0.0.0.0, port 80 443
        python3 main_tcp_server.py

    tcp bind 0.0.0.0, port 8000 8080
        python3 main_tcp_server.py --port 8000 8080

    udp bind 0.0.0.0 port 80 443
        python3 main_udp_server.py

    udp bind 0.0.0.0 port 8000 8080
        python3 main_udp_server.py --port 8000 8080