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
