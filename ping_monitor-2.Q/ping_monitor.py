import threading
import time
from ping3 import ping

# Kontrol edilecek IP adresleri
ip_addresses = [f'192.168.1.{i}' for i in range(1, 513)]  # 192.168.1.1 ile 192.168.1.512 arasında IP adresleri

# Ulaşılamayan IP adreslerini tutacak liste
unreachable_ips = []

def ping_ip(ip):
    """Belirtilen IP adresine ping atar."""
    while True:
        response = ping(ip)
        if response is None:
            if ip not in unreachable_ips:
                unreachable_ips.append(ip)
                print(f"{ip} - Ulaşılamıyor")
        else:
            if ip in unreachable_ips:
                unreachable_ips.remove(ip)
        time.sleep(1)  # Her ping arasında 1 saniye bekle

def start_pinging():
    """Tüm IP adreslerine ping atmak için thread oluşturur."""
    threads = []
    for ip in ip_addresses:
        thread = threading.Thread(target=ping_ip, args=(ip,))
        thread.daemon = True  # Arka planda çalışacak şekilde ayarla
        threads.append(thread)
        thread.start()

    # Thread'leri takip et
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_pinging()
