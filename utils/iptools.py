from scapy.all import ARP, Ether, srp, get_if_hwaddr

from ping3 import ping

def get_ip_from_mac(mac_address, iface, pdst):

    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=pdst)

    ans, _ = srp(pkt, iface=iface, timeout=2, verbose=False)

    for snd, rcv in ans:
        if rcv[Ether].src.lower() == mac_address.lower():
            return rcv[ARP].psrc

    return None

def is_ip_reachable(ip_address, iface):
    return bool(ping(ip_address, interface=iface))