# Basic Networking for Release QA

A plain-English networking primer for a new-grad release QA interview: what a
network is, how data moves, what the models mean, and how to talk about
networks without hand-waving.

## Contents

- [Part 1 — Networking Fundamentals and Models](#part-1--networking-fundamentals-and-models)
- [Part 2 — Topologies and Devices](#part-2--topologies-and-devices)
- [Part 3 — Addressing and Subnetting](#part-3--addressing-and-subnetting)
- [Part 4 — Protocols and Ports](#part-4--protocols-and-ports)
- [Part 5 — Troubleshooting and Commands](#part-5--troubleshooting-and-commands)

## Part 1 — Networking Fundamentals and Models

### What a network is

A network is two or more devices connected so they can exchange data. Each
device is a **node**; the connection is a **link**, which can be wired
(Ethernet, fiber) or wireless (Wi-Fi, cellular). Data does not travel as one
continuous stream: it is split into **packets**, each carrying a header with
addressing and control information plus a payload.

Networks are often described by size:

| Type | Scope | Example |
|---|---|---|
| PAN | A person's devices | Phone and earbuds over Bluetooth |
| LAN | One building or campus | Office Ethernet and Wi-Fi |
| MAN | A city | A provider's metro fiber ring |
| WAN | Countries or global | The internet, a company's branch network |

An **intranet** is a private network inside an organization; the **internet**
is the public network of networks. A packet on the internet may cross several
provider networks before it arrives.

### Client-server vs peer-to-peer

In a **client-server** network, clients request services and a server responds.
The server is centralized, easier to control and back up, and often the
bottleneck. Web, email, and most enterprise applications work this way.

In a **peer-to-peer** network, devices share directly without a dedicated
server. Each peer can act as both client and server. File-sharing and some
collaboration tools use this model; it is harder to control but has no single
point of failure.

For QA, the difference matters: a client-server bug may be a server capacity
or configuration problem, while a peer-to-peer bug may depend on which peer is
reachable and which version it runs.

### The OSI model

The OSI model is a teaching model with seven layers. Each layer has one job and
uses the layer below it.

| # | Layer | Plain-English job | Examples |
|---|---|---|---|
| 7 | Application | What the user's software does | HTTP, DNS, SMTP |
| 6 | Presentation | Data format, encryption, compression | TLS, character encoding |
| 5 | Session | Start, maintain, and end conversations | Session tokens, connection setup |
| 4 | Transport | End-to-end delivery, reliability, ports | TCP, UDP |
| 3 | Network | Logical addressing and routing | IP, ICMP |
| 2 | Data Link | Local delivery on one link, MAC addresses | Ethernet, Wi-Fi, ARP |
| 1 | Physical | Bits on a wire or through the air | Cables, pins, radio |

A memory aid for layers 7 down to 1 is **Please Do Not Throw Sausage Pizza
Away** (Physical, Data Link, Network, Transport, Session, Presentation,
Application is the reverse order). Use whichever direction you find easier.

The model is a map, not a law. Real protocols blur layers: TLS sits between
transport and application, and ARP is often described as crossing layers 2 and
3. For interviews, know the layer names, the job of each, and a couple of
example protocols per layer.

### The TCP/IP model

The TCP/IP model is the model the internet actually uses. It has four layers
and collapses the top three OSI layers into one application layer.

```text
OSI (7 layers)                 TCP/IP (4 layers)
7 Application  ┐
6 Presentation ├──────────────► Application
5 Session      ┘
4 Transport    ───────────────► Transport
3 Network      ───────────────► Internet
2 Data Link    ┐
1 Physical     ┴──────────────► Link (Network Access)
```

| TCP/IP layer | OSI layers | What it does | Examples |
|---|---|---|---|
| Application | 5–7 | User protocols and data formats | HTTP, DNS, TLS, SMTP |
| Transport | 4 | End-to-end delivery and ports | TCP, UDP |
| Internet | 3 | Addressing and routing between networks | IP, ICMP |
| Link | 1–2 | Local delivery on the physical link | Ethernet, Wi-Fi, ARP |

### Encapsulation

Encapsulation is how each layer adds its own header to the data it receives.

1. The application creates **data**.
2. The transport layer adds a TCP or UDP header, producing a **segment** (TCP)
   or **datagram** (UDP).
3. The internet layer adds an IP header, producing a **packet**.
4. The link layer adds a frame header and trailer, producing a **frame**.
5. The physical layer sends the frame as **bits**.

The receiver reverses the process, removing one header per layer
(**decapsulation**). This is why a packet capture can show Ethernet, IP, TCP,
and HTTP headers stacked inside one another.

### Bandwidth, latency, throughput, jitter, and packet loss

| Term | Meaning | Unit | Why it matters |
|---|---|---|---|
| Bandwidth | Maximum capacity of a link | Mbps or Gbps | The pipe size |
| Latency | Delay for one packet to travel | ms | Interactive feel; round-trip time (RTT) is there and back |
| Throughput | Actual data rate achieved | Mbps | What users experience; always at most the bandwidth |
| Jitter | Variation in latency | ms | Bad for voice and video |
| Packet loss | Packets that never arrive | % | Causes retransmission (TCP) or glitches (UDP) |

A link can have high bandwidth and still feel slow: a 1 Gbps link with 200 ms
RTT has a lot of capacity but a long wait per round trip. That is why "the
network is slow" should become a measurement: which metric, on which path, at
what time, and for which users?

## Part 2 — Topologies and Devices

### Physical vs logical topology

The **physical topology** is how devices and cables are arranged in a space:
which switch sits in which closet, which access point covers which floor. The
**logical topology** is how traffic actually flows: which subnets and VLANs
exist, where routing happens, and which paths are permitted by firewalls.

The two can differ. A modern office is usually a physical star, with every
device connected to a switch, but its logical topology may be several VLANs and
subnets joined by a router. When troubleshooting, ask both questions: where is
the device plugged in, and what path should its traffic take?

### Topologies

| Topology | One-line diagram | Strength | Failure mode |
|---|---|---|---|
| Bus | `node—node—node` on one backbone | Cheap and simple | A backbone break or heavy collisions take down the segment |
| Star | `node—switch—node` | Easy fault isolation; one link per device | The central switch is a single point of failure |
| Ring | `node→node→node→back` | Predictable path; dual rings can survive one break | A single break disrupts a simple ring |
| Full mesh | `every node ↔ every node` | Maximum redundancy | Expensive: n(n−1)/2 links |
| Partial mesh | `some nodes ↔ several nodes` | Redundancy where it matters | Design and troubleshooting complexity |
| Tree | `root → switches → leaves` | Scales as a hierarchy | Upper links and the root are single points of failure |
| Hybrid | `mix of star, mesh, and ring` | Fits real sites and legacy equipment | Harder to reason about and test |

Most enterprise LANs are **star or tree** at the access layer and **partial
mesh** in the core or WAN. Full mesh is reserved for small, critical groups
where the link cost is justified.

### Devices

| Device | Main layer | Job | QA note |
|---|---|---|---|
| Hub | 1 | Repeats incoming bits to every port | One collision domain; obsolete |
| Switch | 2 | Forwards frames by MAC address, learns a MAC table | Each port is its own collision domain; VLANs live here |
| Router | 3 | Forwards packets between IP networks | The default gateway; often does NAT |
| Access point | 2 | Bridges Wi-Fi clients onto the wired LAN | Coverage, roaming, and SSID issues look like "network" bugs |
| Modem | 1–2 | Converts the provider's signal to Ethernet | A link down here takes the whole site offline |
| Firewall | 3–4, sometimes 7 | Filters traffic by rules and connection state | A blocked port looks like a timeout, not a refusal |
| Proxy | 7 | Forwards requests on behalf of clients | Caching and filtering can change what the app sees |
| Load balancer | 4 or 7 | Distributes traffic across servers with health checks | Sessions may stick to one server; a bad node causes intermittent errors |

Devices can work at more than one layer; the table gives the layer each mainly
uses. For interviews, know the primary job and one failure symptom for each.

### Collision domains vs broadcast domains

A **collision domain** is the set of devices that can collide when they transmit
at the same time. Hubs extend one collision domain to every port; switches
break it into one domain per port, and full-duplex switch ports do not collide at
all.

A **broadcast domain** is the set of devices that receive a broadcast frame.
Switches forward broadcasts to every port in the same VLAN, so they extend the
broadcast domain; routers do not forward broadcasts, so they break it.

A **VLAN** is a logical switch partition that creates a separate broadcast
domain. Two devices in different VLANs cannot reach each other without routing
and, usually, a firewall rule. That is a common cause of "the server is up but
the test environment cannot reach it."

### What this means for QA

- Topology decides the blast radius: one access switch, one VLAN, or the whole
  site.
- Test across subnets and VLANs, not only between devices on the same LAN.
- A "network down" report may be one port, one VLAN, one route, or one firewall
  rule; the diagnostic ladder in Part 5 narrows it down.
- A diagram is a claim, not evidence. Verify the path with commands before
  writing the bug.

## Part 3 — Addressing and Subnetting

### IPv4 addresses

An IPv4 address is 32 bits, written as four decimal octets separated by dots:
`192.168.1.10`. Each octet is 0–255 because it holds 8 bits. The address has a
**network** part and a **host** part; the subnet mask decides where the split
falls.

Special ranges worth memorizing:

| Range | Name | What it means |
|---|---|---|
| `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` | Private | Not routable on the public internet; reused inside networks |
| `127.0.0.0/8` | Loopback | The local device; `127.0.0.1` is "this machine" |
| `169.254.0.0/16` | Link-local / APIPA | Self-assigned when DHCP fails; usually a symptom |
| `224.0.0.0/4` | Multicast | One sender, a group of receivers |
| `255.255.255.255` | Limited broadcast | Every device on the local network |

A **default gateway** is the router a device sends traffic to when the
destination is on a different subnet. If the gateway is wrong or missing, local
traffic may work while everything outside the subnet fails.

### Subnet masks and CIDR

A subnet mask is a run of 1s followed by a run of 0s. CIDR writes the number of
1s as a suffix: `/24` means 24 network bits and 8 host bits, or
`255.255.255.0`.

For a `/24`–`/28`, the last mask octet determines the **block size**:

`block size = 256 − last mask octet`

The **network address** has all host bits set to 0. The **broadcast address**
has all host bits set to 1. The usable range is everything between them:

`usable hosts = block size − 2`

| CIDR | Subnet mask | Block size | Networks in a /24 | Usable hosts |
|---|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 1 | 254 |
| /25 | 255.255.255.128 | 128 | 2 | 126 |
| /26 | 255.255.255.192 | 64 | 4 | 62 |
| /27 | 255.255.255.224 | 32 | 8 | 30 |
| /28 | 255.255.255.240 | 16 | 16 | 14 |

### Step-by-step subnetting

1. Write the prefix and the mask.
2. Find the block size: `256 − last mask octet`.
3. List the network addresses in multiples of the block size.
4. Place the given IP in the network whose block contains it.
5. First usable = network address + 1.
6. Broadcast = next network address − 1.
7. Last usable = broadcast − 1.
8. Usable hosts = block size − 2.

### A worked /26 example

Take `192.168.1.100/26`.

- Mask `/26` = `255.255.255.192`, because the last octet is
  `11000000` in binary, or 192.
- Block size = `256 − 192 = 64`. In binary, 64 is `01000000`, leaving 6 host
  bits, so `2^6 − 2 = 62` usable hosts.
- The networks in `192.168.1.0/24` are `.0`, `.64`, `.128`, and `.192`.
- `.100` falls in the `.64` network, so the network address is
  `192.168.1.64`.
- The broadcast is the next network minus one: `192.168.1.127`.
- The usable range is `192.168.1.65` through `192.168.1.126`.

| Subnet | Network | First usable | Last usable | Broadcast |
|---|---|---|---|---|
| 192.168.1.0/26 | 192.168.1.0 | 192.168.1.1 | 192.168.1.62 | 192.168.1.63 |
| 192.168.1.64/26 | 192.168.1.64 | 192.168.1.65 | 192.168.1.126 | 192.168.1.127 |
| 192.168.1.128/26 | 192.168.1.128 | 192.168.1.129 | 192.168.1.190 | 192.168.1.191 |
| 192.168.1.192/26 | 192.168.1.192 | 192.168.1.193 | 192.168.1.254 | 192.168.1.255 |
| 192.168.1.0/27 | 192.168.1.0 | 192.168.1.1 | 192.168.1.30 | 192.168.1.31 |
| 192.168.1.32/27 | 192.168.1.32 | 192.168.1.33 | 192.168.1.62 | 192.168.1.63 |
| 192.168.1.0/28 | 192.168.1.0 | 192.168.1.1 | 192.168.1.14 | 192.168.1.15 |
| 192.168.1.240/28 | 192.168.1.240 | 192.168.1.241 | 192.168.1.254 | 192.168.1.255 |

### Default gateway, routing, and NAT

If the destination is on the same subnet, the sender uses ARP to find the
destination's MAC address and sends the frame directly. If the destination is on
another subnet, the sender sends to the default gateway's MAC address and lets
the router forward the packet hop by hop.

**NAT** (network address translation) lets many private addresses share one
public address. It rewrites addresses and ports at the router, which is why an
outside client cannot start a connection to an inside server without a
port-forwarding or firewall rule.

For QA, this explains a common pattern: two machines can ping each other on the
same subnet but fail across subnets because a route or firewall rule is missing.
It also explains why a service can work from inside the network and time out
from outside.

### IPv6 basics

IPv6 addresses are 128 bits, written as eight groups of four hexadecimal digits:
`2001:0db8:0000:0000:0000:ff00:0042:8329`.

Two shortening rules apply:

1. Drop leading zeros in each group: `0db8` becomes `db8`.
2. Replace one run of all-zero groups with `::`, once per address:
   `2001:db8::ff00:42:8329`.

Common IPv6 addresses:

| Address | Meaning |
|---|---|
| `::1` | Loopback |
| `::` | Unspecified |
| `fe80::/10` | Link-local; every interface has one |
| `2000::/3` | Global unicast, the public address space |
| `ff00::/8` | Multicast |

IPv6 has no broadcast; it uses multicast instead. It was designed without NAT,
and hosts can configure themselves with SLAAC or use DHCPv6. For a new-grad
interview, know the format, the shortening rules, and the main address types;
advanced IPv6 subnetting is out of scope here.
