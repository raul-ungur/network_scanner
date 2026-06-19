import subprocess
import sqlite3
import xml.etree.ElementTree as ET
import shutil
from network_utils import get_local_network
import os

print(os.path.abspath("network.db"))

if shutil.which("nmap") is None:

    raise Exception(
        "Nmap not found. Install Nmap before using the scanner."
    )

def scan_network():
    print("SCAN STARTED")
    network = str(get_local_network())
    
    comando = [
        "nmap",
        "-sn",
        network,
        "-oX",
        "-"
    ]

    risultato = subprocess.run(
        comando,
        capture_output=True,
        text=True
    )
    
    root = ET.fromstring(risultato.stdout)

    conn = sqlite3.connect("network.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM devices")

    for host in root.findall("host"):

        ip = None
        mac = None
        vendor = None

        for address in host.findall("address"):

            if address.attrib["addrtype"] == "ipv4":
                ip = address.attrib["addr"]

            elif address.attrib["addrtype"] == "mac":
                mac = address.attrib["addr"]
                vendor = address.attrib.get("vendor")

        if ip:

            cursor.execute("""
            INSERT OR REPLACE INTO devices
            (ip, mac, vendor)
            VALUES (?, ?, ?)
            """, (ip, mac, vendor))

            print(ip, mac, vendor)

    conn.commit()
    conn.close()
    return True


if __name__ == "__main__":

    scan_network()