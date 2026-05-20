from scapy.all import ARP, Ether, srp, get_if_hwaddr

def get_ip_from_mac(mac_address, iface="eth0", pdst="192.168.1.0/24"):

    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=pdst)

    ans, _ = srp(pkt, iface=iface, timeout=2, verbose=False)

    for snd, rcv in ans:
        if rcv[Ether].src.lower() == mac_address.lower():
            return rcv[ARP].psrc

    return None