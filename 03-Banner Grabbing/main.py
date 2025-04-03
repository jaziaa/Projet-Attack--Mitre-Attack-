import socket
import threading


# Fonction pour scanner un port et récupérer la bannière
def grab_banner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))

            # Bannière spécifique pour HTTP/HTTPS
            if port in [80, 443]:
                s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")

            banner = s.recv(1024).decode().strip()
            if banner:
                print(f"[+] Port {port} ouvert – Service détecté : {banner}")

    except (socket.timeout, ConnectionRefusedError):
        pass
    except Exception as e:
        print(f"[-] Erreur sur le port {port} : {e}")


# Fonction pour scanner une plage de ports
def scan_ports(ip, start_port, end_port):
    threads = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=grab_banner, args=(ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


# Programme principal
def main():
    ip = input("Entrez l'adresse IP à scanner : ")
    start_port = int(input("Port de début : "))
    end_port = int(input("Port de fin : "))

    print(f"\n[***] Scan des ports {start_port} à {end_port} sur {ip}...\n")
    scan_ports(ip, start_port, end_port)


if __name__ == "__main__":
    main()
