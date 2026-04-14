from scapy.all import rdpcap, TCP, IP, Raw
from collections import defaultdict

PCAP_FILE = "capture.pcap"
XOR_KEY = 42

packets = rdpcap(PCAP_FILE)

sessions = defaultdict(bytearray)

for pkt in packets:
    if not pkt.haslayer(TCP) or not pkt.haslayer(Raw):
        continue

    ip = pkt[IP]
    tcp = pkt[TCP]
    payload = bytes(pkt[Raw].load)

    if len(payload) == 0:
        continue

    endpoint1 = (ip.src, tcp.sport)
    endpoint2 = (ip.dst, tcp.dport)
    session_key = tuple(sorted([endpoint1, endpoint2]))

    sessions[session_key] += payload

print(f"{len(sessions)} in total")


id_to_payload = {}

for session_key, stream_data in sessions.items():
    pos = 0
    pending_id = None  

    while pos < len(stream_data):
        if stream_data.startswith(b"GET ", pos) or stream_data.startswith(b"POST ", pos):
            end = stream_data.find(b"\r\n\r\n", pos)
            if end == -1:
                break
            header = stream_data[pos:end]
            request_line = header.split(b"\r\n")[0].decode(errors="ignore")
            if "/encrypt/id/" in request_line:
                try:
                    pending_id = int(request_line.split("/")[3].split()[0])
                except:
                    pass
            pos = end + 4

        elif stream_data.startswith(b"HTTP/1.", pos):
            end = stream_data.find(b"\r\n\r\n", pos)
            if end == -1:
                break
            header = stream_data[pos:end]

            content_length = None
            for line in header.split(b"\r\n"):
                if line.lower().startswith(b"content-length:"):
                    content_length = int(line.split(b":", 1)[1].strip())
                    break

            if content_length is None:
                print(f"{session_key} lack Content-Length")
                pos = end + 4
                continue

            body_start = end + 4
            body_end = body_start + content_length

            if len(stream_data) < body_end:
                break 

            body = stream_data[body_start:body_end]

            if pending_id is not None:
                id_to_payload[pending_id] = body
                print(f"ID {pending_id:3d} ，size {len(body):4d}")
                pending_id = None
            else:
                print(f"no {session_key}")

            pos = body_end

        else:
            pos += 1

ordered_ids = sorted(id_to_payload.keys())
if not ordered_ids:
    exit(1)

cipher = b"".join(id_to_payload[i] for i in ordered_ids)
plain = bytes([b ^ XOR_KEY for b in cipher])

if plain.startswith(b'\x7fELF'):
    output_name = "recovered.elf"
    with open(output_name, "wb") as f:
        f.write(plain)

    
