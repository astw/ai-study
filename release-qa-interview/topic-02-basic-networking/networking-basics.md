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
