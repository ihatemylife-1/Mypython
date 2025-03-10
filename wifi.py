import subprocess

SSID = "MyHotspot"
PASSWORD = "mypassword"
INTERFACE = "wlan0"  # Change this based on your Wi-Fi adapter

def create_hotspot():
    # Write the hostapd config
    with open("/etc/hostapd/hostapd.conf", "w") as f:
        f.write(f"""
interface={INTERFACE}
driver=nl80211
ssid={SSID}
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={PASSWORD}
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
""")

    # Enable IP forwarding
    subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"], check=True)

    # Set up NAT (firewall rules)
    subprocess.run(["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", "eth0", "-j", "MASQUERADE"], check=True)

    # Start dnsmasq for DHCP
    with open("/etc/dnsmasq.conf", "w") as f:
        f.write(f"""
interface={INTERFACE}
dhcp-range=192.168.1.10,192.168.1.100,12h
""")
    subprocess.run(["service", "dnsmasq", "restart"], check=True)

    # Start hostapd
    subprocess.run(["hostapd", "/etc/hostapd/hostapd.conf"])

try:
    create_hotspot()
except KeyboardInterrupt:
    print("Stopping hotspot...")