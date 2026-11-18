# TCP/IP for QA

### A Practical Networking Primer for People Who Have Never Worked with Networks

**Version 1.0 · November 2026**

> You do not need to become a network engineer. You need to know enough to tell whether a failure is in the application, the network, or the environment — and to describe it so someone can fix it.

---

## Contents

- [Part 1: The big picture](#part-1-the-big-picture)
- [Part 2: Addresses, ports, and paths](#part-2-addresses-ports-and-paths)
- [Part 3: The protocols you will meet](#part-3-the-protocols-you-will-meet)
- [Part 4: DNS, DHCP, and VPN](#part-4-dns-dhcp-and-vpn)
- [Part 5: What QA needs to test](#part-5-what-qa-needs-to-test)
- [Part 6: Troubleshooting like a QA engineer](#part-6-troubleshooting-like-a-qa-engineer)
- [Part 7: Labs](#part-7-labs)
- [Appendices](#appendices)
  - [A: Cheat sheet](#appendix-a-cheat-sheet)
  - [B: Glossary](#appendix-b-glossary)
  - [C: Quiz](#appendix-c-quiz)
  - [D: Bug report template](#appendix-d-bug-report-template)
  - [E: Running a knowledge-sharing session](#appendix-e-running-a-knowledge-sharing-session)
  - [F: Resources and what to learn next](#appendix-f-resources-and-what-to-learn-next)

---

## What this guide will do for you

By the end, you will be able to:

- Explain what happens between typing a URL and seeing a page.
- Read an IP address, subnet mask, default gateway, port, and DNS server.
- Explain TCP, UDP, DNS, DHCP, NAT, HTTP, TLS, VPN, proxies, and firewalls in plain English.
- Use the basic tools — `ping`, `traceroute`, `nslookup`/`dig`, `curl`, DevTools, `netstat`, Wireshark — without fear.
- Design network-aware test cases instead of only "happy path on office Wi-Fi."
- Write a bug report that says which layer failed and includes evidence someone can act on.
- Know when a problem is yours to test and when to escalate.

## Who this is for

People starting in QA, manual testers moving into more technical work, career changers, and anyone who has used the internet every day but never looked underneath it.

No programming is required. Some comfort with a command line helps; Part 6 and the labs teach the commands you need.

## Three rules before you start

**1. Find the layer, not just the symptom.** "It doesn't work" is not a diagnosis. "DNS resolves, TCP connects, TLS fails with an expired certificate" is.

**2. Change one variable at a time.** If you turn on a VPN, switch browsers, and clear cookies at once, you learn nothing. Compare one condition against a baseline.

**3. Protect data and get permission.** Capturing traffic, scanning ports, and testing corporate networks can expose other people's data or break rules. Work only on systems you are authorized to test, use test accounts, and never paste production secrets, tokens, or personal data into tickets or tools.

---

# Part 1: The Big Picture

## 1.1 What "the network" actually is

A network is a set of agreements for moving bytes between programs on different machines. Those agreements are called **protocols**. The internet works because millions of devices follow the same ones.

A useful analogy is the postal system:

| Postal idea | Network equivalent |
|---|---|
| Your street address | IP address |
| Apartment or office number | Port |
| Phone book | DNS |
| Front desk assigning a room | DHCP |
| Tracked delivery with signature | TCP |
| Postcard, no tracking | UDP |
| Private courier tunnel | VPN |
| Mailroom that forwards packages | Proxy |
| Building security that checks who may enter | Firewall |

The analogy is not perfect, but it gives you the right instincts: addresses get things to the right building, ports get them to the right desk, and different delivery services make different promises.

## 1.2 What happens when you open a web page

You type `https://example.com/login` and press Enter. A simplified sequence:

1. **The browser checks its cache.** It may already have the page, a DNS answer, or an open connection.
2. **DNS resolves the name.** `example.com` becomes one or more IP addresses.
3. **The client chooses a path.** It may try IPv6 and IPv4 in parallel ("Happy Eyeballs").
4. **A transport connection opens.** For HTTPS over HTTP/1.1 or HTTP/2, this is a TCP three-way handshake. For HTTP/3, it is a QUIC connection over UDP.
5. **TLS negotiates.** For HTTPS, client and server agree on encryption, verify certificates, and derive keys.
6. **The HTTP request is sent.** `GET /login` plus headers and cookies travel through your local network, router, NAT, possibly a VPN, proxy, firewall, load balancer, and CDN.
7. **The server responds.** Status code, headers, and body come back. The browser may fetch dozens of additional resources.
8. **The browser renders.** JavaScript may make more API calls; each one repeats part of this journey.

```
   You
    │
    ▼
 [Browser] ── DNS lookup ──► [Resolver] ──► root / TLD / authoritative servers
    │
    ▼
 [TCP or QUIC connection]
    │
    ▼
 [TLS handshake]              ← HTTPS only
    │
    ▼
 [HTTP request]
    │
    ▼
 [Wi-Fi / router / NAT] ──► [VPN?] ──► [Proxy?] ──► [Firewall] ──► [Load balancer] ──► [Server]
```

Every arrow is a place a bug can live. "The page is slow" could mean slow DNS, a slow TCP handshake, a slow TLS handshake, a slow server, or a slow download. Part 6 shows how to tell them apart.

> **QA takeaway:** A single user action crosses many layers. Test and report at the layer where the failure occurs, not only at the UI.

## 1.3 The TCP/IP model in plain English

Networking models divide the job into layers. The **TCP/IP model** has four practical layers:

| Layer | What it does | Examples | QA question |
|---|---|---|---|
| **Application** | The conversation the user cares about | HTTP, DNS, DHCP, SSH, TLS | Is the request correct and is the response valid? |
| **Transport** | Process-to-process delivery | TCP, UDP, QUIC | Did a connection open? Is data reliable? |
| **Internet** | Addressing and routing between networks | IP, ICMP | Can packets reach the destination network? |
| **Link** | Local network delivery | Ethernet, Wi-Fi, ARP | Is the device connected to its local network? |

You will also hear about the **OSI seven-layer model**. It is a teaching model, not something you configure. The rough mapping:

| OSI | TCP/IP | Examples |
|---|---|---|
| 7 Application | Application | HTTP, DNS |
| 6 Presentation | Application | TLS encryption, encoding |
| 5 Session | Application | Session management, TLS |
| 4 Transport | Transport | TCP, UDP |
| 3 Network | Internet | IP, ICMP |
| 2 Data link | Link | Ethernet, Wi-Fi, ARP |
| 1 Physical | Link | Cables, radio, ports |

TLS sits between the transport and application layers in practice. Do not lose sleep over exact OSI placement; use the model to ask "which layer is failing?"

### Encapsulation

Each layer wraps the data from the layer above it:

```
[ Ethernet header ][ IP header ][ TCP header ][ HTTP request ][ Ethernet trailer ]
        link            internet     transport      application
```

The receiving side unwraps the same layers in reverse. The maximum size of a link-layer payload is the **MTU** (Maximum Transmission Unit), typically 1500 bytes on Ethernet. Large messages are split across packets. A VPN adds its own headers and can reduce the usable MTU, which is why some sites hang over VPN but work without it.

## 1.4 Packets, latency, and why "it's slow" is not a bug report

Data is sent as **packets**. Packets can take different routes, arrive out of order, be delayed, duplicated, or dropped. TCP hides most of this from the application; UDP does not.

Four terms you will use constantly:

- **Latency** — how long one round trip takes (milliseconds). Distance, Wi-Fi, VPNs, and congestion increase it.
- **Bandwidth** — the maximum data rate of a link (Mbps/Gbps).
- **Throughput** — the data rate you actually achieve, usually less than or equal to bandwidth.
- **Packet loss and jitter** — packets dropped or arriving with uneven delays. Voice and video hate both.

A 100 Mbps link with 400 ms latency feels worse for interactive work than a 10 Mbps link with 20 ms latency. Bandwidth is not speed in the way users mean it.

> **QA takeaway:** Timing bugs need conditions and numbers. Record the network type, latency, loss, and the phase that was slow. "Took 12 seconds on 3G with 400 ms latency" is testable; "slow" is not.

## 1.5 The boxes in the path

You will hear these device names in bug reports and network diagrams:

| Device | Main job | Works with |
|---|---|---|
| **Modem** | Converts the ISP's signal into Ethernet or another local connection | ISP line, physical media |
| **Router** | Connects different networks, chooses the next hop, often does NAT and DHCP | IP addresses |
| **Switch** | Connects devices inside one local network and forwards frames to the right port | MAC addresses |
| **Access point (AP)** | Bridges Wi-Fi devices onto the wired local network | Wi-Fi, Ethernet |
| **Firewall** | Allows or blocks traffic by rule | IPs, ports, protocols, application |
| **Load balancer** | Distributes requests across servers and checks their health | HTTP/TCP, server pools |
| **Proxy** | Forwards traffic on behalf of a client or server | HTTP, HTTPS, other protocols |

A home "router" is usually several of these in one box: modem, router, switch, access point, and firewall. In an office or cloud environment they are often separate, which is why a request may cross many devices that each have their own logs.

> **QA takeaway:** "The router is broken" is rarely a useful report. Say which device and function you suspect — DHCP, DNS forwarding, NAT, Wi-Fi association, firewall, or routing — and what evidence points there.

---

# Part 2: Addresses, Ports, and Paths

## 2.1 IP addresses

An **IP address** identifies a network interface so packets can be routed to it. There are two versions in use.

### IPv4

IPv4 is a 32-bit number written as four decimal octets:

```
192.168.1.42
```

Each octet is 0–255. The address has a **network portion** and a **host portion**. A **subnet mask** or CIDR suffix tells you where the split is:

```
192.168.1.42/24
```

`/24` means the first 24 bits identify the network; the last 8 bits identify the host. This network has 256 addresses, of which 254 are normally usable (one is the network address, one is broadcast).

| CIDR | Subnet mask | Total addresses | Typical use |
|---|---|---|---|
| `/24` | 255.255.255.0 | 256 | Small office or home LAN |
| `/25` | 255.255.255.128 | 128 | Two `/25` subnets in one `/24` |
| `/26` | 255.255.255.192 | 64 | Smaller segments |
| `/16` | 255.255.0.0 | 65,536 | Large private network |
| `/8` | 255.0.0.0 | 16,777,216 | Very large private network |

You do not need to do subnet math in your head for most QA work. You do need to recognize when two addresses are on the same local network and when traffic must go through a router.

**Private IPv4 ranges** are not routable on the public internet:

| Range | CIDR | Common place |
|---|---|---|
| `10.0.0.0` – `10.255.255.255` | `10.0.0.0/8` | Corporate networks, cloud VPCs |
| `172.16.0.0` – `172.31.255.255` | `172.16.0.0/12` | Corporate networks, Docker |
| `192.168.0.0` – `192.168.255.255` | `192.168.0.0/16` | Home and small-office routers |

Other special addresses:

| Address | Meaning |
|---|---|
| `127.0.0.1` | Loopback — this machine |
| `0.0.0.0` | "Any address" when listening; "this network" in some contexts |
| `169.254.x.x` | Link-local / APIPA — often means DHCP failed |
| `224.0.0.0/4` | IPv4 multicast |
| `255.255.255.255` | Local broadcast |

### IPv6

IPv6 is 128 bits, written as eight groups of hexadecimal digits:

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

Rules for shortening:

- Leading zeros in a group can be dropped: `0db8` → `db8`.
- One run of all-zero groups can be replaced by `::` (only once): `2001:db8:85a3::8a2e:370:7334`.

Important IPv6 addresses:

| Address | Meaning |
|---|---|
| `::1` | Loopback |
| `fe80::/10` | Link-local — local network only |
| `2000::/3` | Global unicast — routable on the internet |
| `fc00::/7` | Unique local — roughly the private-address equivalent |
| `ff00::/8` | Multicast; IPv6 has no broadcast |

Most modern networks run **dual stack**: IPv4 and IPv6 at the same time. Applications choose with algorithms such as Happy Eyeballs, racing both and preferring the one that connects first.

> **QA takeaway:** Test IPv4 and IPv6 separately when the product supports both. A bug that only appears on an IPv6-only network is invisible on a dual-stack office Wi-Fi where IPv4 quietly succeeds.

### Default gateway and routing

If the destination is on the same subnet, the device sends directly using **ARP** (IPv4) or **neighbor discovery** (IPv6), which map IP addresses to local hardware (MAC) addresses.

If the destination is on a different subnet, the device sends the packet to its **default gateway** — usually the router. The router consults a **routing table** and forwards the packet to the next hop. This repeats until the packet reaches the destination network.

For example, `192.168.1.10/24` and `192.168.1.20/24` are on the same subnet and talk directly. `192.168.1.10/24` and `192.168.2.20/24` are on different subnets, so the first host sends through its gateway.

`traceroute` (Windows: `tracert`) shows the hops. High latency at one hop does not always mean that hop is at fault; routers may deprioritize replies to diagnostic packets.

## 2.2 Ports and sockets

An IP address gets data to a machine. A **port** gets it to the right program on that machine. Ports are 16-bit numbers, 0–65535.

| Range | Name | Notes |
|---|---|---|
| 0–1023 | Well-known | Assigned to standard services; binding often needs admin rights |
| 1024–49151 | Registered | Common application services |
| 49152–65535 | Ephemeral / dynamic | Temporary client-side ports chosen by the OS |

A **socket** is an IP address plus a port. A TCP connection is identified by a four-tuple:

```
source IP : source port  ↔  destination IP : destination port
```

That is why many browser tabs can talk to the same server on port 443 at once: each connection has a different client port.

Common ports worth recognizing:

| Port | Protocol | Service |
|---|---|---|
| 22 | TCP | SSH |
| 25 | TCP | SMTP (mail transfer) |
| 53 | UDP/TCP | DNS |
| 67/68 | UDP | DHCP server/client |
| 80 | TCP | HTTP |
| 123 | UDP | NTP (time sync) |
| 443 | TCP/UDP | HTTPS; HTTP/3 uses UDP 443 |
| 500/4500 | UDP | IPsec IKE / NAT traversal |
| 853 | TCP/UDP | DNS over TLS |
| 1194 | UDP/TCP | OpenVPN default |
| 3306 | TCP | MySQL |
| 5432 | TCP | PostgreSQL |
| 6379 | TCP | Redis |
| 8080 | TCP | Alternative HTTP / proxy |
| 51820 | UDP | WireGuard default |

Server applications usually **listen** on a port. Clients connect from an ephemeral port. `0.0.0.0:8080` means "listen on every IPv4 interface"; `127.0.0.1:8080` means "only local connections." That difference explains many "works on my machine but not from another machine" bugs.

> **QA takeaway:** "Connection refused" usually means the machine is reachable but nothing is listening on that port (or a firewall actively rejected it). "Connection timed out" usually means packets were dropped — wrong route, firewall, or VPN. They point to different investigations.

## 2.3 NAT, routing, and the path

**NAT** (Network Address Translation) lets many private devices share one public IP. The router rewrites source addresses and tracks which internal device owns each connection. The common form with ports is **PAT** or **NAPT** — many private `IP:port` pairs map to one public IP with different ports.

Consequences:

- Inbound connections need **port forwarding** or a reverse proxy; you cannot normally reach a home device from the internet just because it has a private IP.
- External services see the public IP, not the internal one. Features based on IP address — rate limits, geolocation, allowlists, fraud checks — may behave differently behind NAT or a VPN.
- **CGNAT** (carrier-grade NAT) puts many subscribers behind one carrier IP. Port forwarding is usually impossible, and IP-based blocking can affect unrelated users.

**MTU and fragmentation:** If a packet is larger than the path can carry, IPv4 may fragment it; IPv6 relies on the sender discovering the path MTU. Firewalls that drop the necessary ICMP messages create an **MTU black hole** — small requests work, large uploads or pages hang. VPNs reduce the usable MTU because of encapsulation.

> **QA takeaway:** Test large payloads and file uploads over VPN, not just small API calls. "Homepage loads, upload spinner never finishes" is a classic MTU symptom.

---

# Part 3: The Protocols You Will Meet

## 3.1 TCP: reliable delivery

**TCP** (Transmission Control Protocol) provides a reliable, ordered byte stream between two programs. It handles retransmission, ordering, flow control, and congestion control.

### The three-way handshake

Before data flows, TCP establishes a connection:

```
Client                          Server
  │ ────── SYN ────────────────► │   "I want to connect; my sequence starts here"
  │ ◄───── SYN + ACK ─────────── │   "OK; my sequence starts here"
  │ ────── ACK ────────────────► │   "Acknowledged"
  │ ────── data ───────────────► │
```

Key TCP flags:

| Flag | Meaning |
|---|---|
| SYN | Start a connection |
| ACK | Acknowledge received data |
| FIN | Gracefully close one direction |
| RST | Reset — abort the connection |
| PSH | Push data to the application promptly |
| URG | Urgent pointer (rarely used today) |

**How reliability works:** every byte has a sequence number. The receiver acknowledges what it got. Missing data is retransmitted after a timeout or fast-retransmit trigger. Duplicates are discarded, and data is delivered to the application in order.

**Flow and congestion control:** the receiver advertises a window (how much it can buffer), and TCP adjusts sending rate based on loss and round-trip time. This is why a lossy link can slow down dramatically even when bandwidth looks fine.

**Closing:** normally a four-step FIN/ACK exchange. Either side can also send a RST to abort immediately.

### What failures look like

| Symptom | Likely meaning |
|---|---|
| SYN gets no reply, connection times out | Packet dropped: firewall, wrong route, VPN, server down |
| SYN gets RST | Host reachable, port closed or actively refused |
| Handshake succeeds, then RST | Application or middlebox killed the connection; timeout or policy |
| Handshake slow, response fast | Network latency, distance, Wi-Fi, VPN |
| Handshake fast, response slow | Server processing or downstream dependency |
| Retransmissions and long stalls | Packet loss, congested link, bad Wi-Fi |
| Connection works, then hangs mid-transfer | MTU black hole, idle timeout, proxy, server stall |

> **QA takeaway:** Measure the phases separately. DNS time, TCP connect time, TLS time, time to first byte, and download time are different bugs with different owners.

## 3.2 UDP: fast and forgetful

**UDP** (User Datagram Protocol) is connectionless. It sends datagrams with no handshake, no acknowledgment, no ordering guarantee, and no automatic retransmission.

That sounds bad, but it is exactly right for:

- DNS queries (small, retry at the application level)
- DHCP
- Voice and video (a late packet is useless; waiting for it makes things worse)
- Online games
- QUIC / HTTP/3 (reliability is built into QUIC itself)
- VPN protocols such as WireGuard (IPsec uses ESP, an IP-layer protocol, plus UDP for IKE/NAT traversal)

UDP has a small header and low overhead. The application must handle loss, duplication, ordering, and congestion if it cares about them.

## 3.3 TCP vs UDP

| Property | TCP | UDP |
|---|---|---|
| Connection | Three-way handshake | None |
| Reliability | Retransmits lost data | No guarantee |
| Ordering | Preserves order | No guarantee |
| Overhead | Higher | Lower |
| Latency | Higher setup cost | Lower |
| Congestion control | Built in | Application's job |
| Typical uses | Web (HTTP/1.1, HTTP/2), SSH, email, file transfer | DNS, DHCP, VoIP, games, HTTP/3 (QUIC), VPNs |

## 3.4 HTTP and HTTPS in one page

**HTTP** is the request/response protocol of the web. A request has a method, a path, headers, and optionally a body. A response has a status code, headers, and a body.

### Reading a URL

```
https://app.example.com:8443/login?next=/home#top
  scheme  host           port  path  query     fragment
```

- **Scheme** — `http`, `https`, `ws`, or `wss`.
- **Host** — a DNS name or an IP address.
- **Port** — optional; defaults to 80 for HTTP and 443 for HTTPS.
- **Path** — the resource on the server.
- **Query** — `?key=value` parameters sent to the server.
- **Fragment** — `#top` is handled by the client and is normally not sent to the server.

For QA: a wrong port, a missing path prefix, an unencoded space, or a query parameter the server ignores are common reasons a request works in one tool but fails in another.

Methods you will see: `GET` (read), `POST` (create/submit), `PUT`/`PATCH` (update), `DELETE` (remove), `HEAD` (headers only), `OPTIONS` (capabilities/CORS preflight).

Status code families:

| Code | Meaning | QA use |
|---|---|---|
| 1xx | Informational | Rare in app tests |
| 2xx | Success | `200 OK`, `201 Created`, `204 No Content` |
| 3xx | Redirect | `301` permanent, `302` temporary, `304` not modified |
| 4xx | Client-side problem | `400` bad request, `401` unauthenticated, `403` forbidden, `404` not found, `409` conflict, `429` rate limited |
| 5xx | Server-side problem | `500` internal error, `502` bad gateway, `503` unavailable, `504` gateway timeout |

Headers worth knowing:

| Header | Direction | Why QA cares |
|---|---|---|
| `Host` | Request | Virtual hosting; the wrong host can route to the wrong site |
| `Content-Type` | Both | Body format; a wrong type often causes `400` or `415` |
| `Authorization` | Request | Auth scheme; missing or expired tokens |
| `Cookie` / `Set-Cookie` | Both | Sessions, `Secure`, `HttpOnly`, `SameSite` |
| `Location` | Response | Where a redirect sends the client |
| `Cache-Control` | Both | Caching and stale-content behavior |
| `Access-Control-Allow-Origin` | Response | CORS policy for browser clients |

**HTTPS** is HTTP carried inside **TLS**. The TLS handshake:

1. Client sends a ClientHello with supported versions, cipher suites, and **SNI** (the hostname it wants).
2. Server selects parameters, sends its certificate chain.
3. Client verifies the chain against trusted roots, checks the hostname and validity dates.
4. Both sides derive session keys; encrypted HTTP flows.

Things that break in QA:

- Expired or not-yet-valid certificate (check the system clock too).
- Wrong hostname in the certificate.
- Missing intermediate certificate in the chain.
- Corporate proxy or VPN intercepting TLS; the client must trust the proxy's CA.
- Old TLS version disabled by the server.
- HSTS forcing HTTPS and blocking a test HTTP endpoint.
- Mixed content: an HTTPS page loading HTTP resources.
- SNI-based routing: the same IP serves different certificates/sites depending on hostname.
- Mutual TLS (mTLS): the client must present a valid certificate; missing or expired client certs fail before HTTP.
- Certificate pinning: the app trusts only specific certificates or keys, so a proxy or certificate rotation can break it.

**HTTP versions:**

- **HTTP/1.1** — one request at a time per connection (pipelining is rarely used); browsers open several connections.
- **HTTP/2** — multiplexed streams over one TCP connection; still suffers TCP-level head-of-line blocking when packets are lost.
- **HTTP/3** — runs over QUIC/UDP; independent streams, faster setup, better loss recovery. Some networks block UDP 443, so fallback matters.

**WebSocket** (`ws://` or `wss://`) starts as an HTTP upgrade and then becomes a persistent, bidirectional connection. Proxies, load balancers, and firewalls must allow the upgrade and not time out idle connections; test reconnect and message ordering after a drop.

> **QA takeaway:** Test HTTPS failure modes deliberately: expired certificate, wrong host, untrusted CA, TLS version, and captive portal. `expired.badssl.com`, `wrong.host.badssl.com`, and `self-signed.badssl.com` are safe public examples.

## 3.5 ICMP and diagnostic tools

**ICMP** carries diagnostic and error messages. `ping` uses ICMP Echo Request/Reply; `traceroute` uses ICMP or UDP with increasing TTL values.

A failed `ping` does **not** prove the application is broken. Many networks block ICMP while allowing TCP 443. Conversely, a successful `ping` only proves the host is reachable; it says nothing about the web server or application.

---

# Part 4: DNS, DHCP, and VPN

## 4.1 DNS: the internet's phone book

**DNS** (Domain Name System) translates human-friendly names into IP addresses and stores other records.

### The hierarchy

```
Root (.)
  └── Top-level domain (com, org, net, uk, io)
        └── Authoritative name server for example.com
              └── Records: www.example.com → 203.0.113.10
```

A **recursive resolver** (your ISP, corporate DNS, or a public resolver) does the walking and caches answers. Your device asks the resolver; the resolver asks root, TLD, and authoritative servers as needed.

### Caching and TTL

Every DNS record has a **TTL** (time to live) in seconds. Resolvers cache the answer for that long. A short TTL allows quick changes; a long TTL reduces lookup load but makes changes propagate slowly. There are caches at multiple levels:

- Browser DNS cache
- Operating-system cache
- Recursive resolver cache
- Authoritative server (source of truth)

"DNS is not updating" often means a cache still holds an old TTL. Test from a fresh resolver or wait out the TTL; do not assume the server is wrong.

### Record types

| Record | Meaning | Example |
|---|---|---|
| `A` | Name → IPv4 address | `www.example.com → 203.0.113.10` |
| `AAAA` | Name → IPv6 address | `www.example.com → 2606:2800:...` |
| `CNAME` | Alias to another name | `shop.example.com → store.example.net` |
| `MX` | Mail server for a domain | `example.com → mail.example.com` |
| `TXT` | Arbitrary text; SPF, DKIM, verification | `v=spf1 include:...` |
| `NS` | Authoritative name servers | `ns1.example.com` |
| `PTR` | Reverse lookup: IP → name | `34.216.184.93.in-addr.arpa` |
| `SOA` | Start of authority; zone metadata | Serial, refresh, retry, TTL |
| `SRV` | Service location | `_sip._tcp.example.com` |

### How a query works

```
Application
   │  "www.example.com?"
   ▼
OS resolver ──► recursive resolver ──► root server ──► .com TLD ──► authoritative server
   ▲                    │
   └──── cached answer ─┘
```

DNS normally uses UDP port 53. Large responses or zone transfers use TCP 53. **DNS over TLS (DoT)** uses port 853; **DNS over HTTPS (DoH)** uses HTTPS (443) and hides queries inside normal web traffic. Both encrypt the path to the resolver; they do not make the destination anonymous.

### Common DNS failures

| Symptom | Likely cause |
|---|---|
| `NXDOMAIN` | Name does not exist (typo, wrong domain, deleted record) |
| `SERVFAIL` | Resolver or authoritative server failure, DNSSEC problem |
| Query timeout | DNS server unreachable, UDP 53 blocked, VPN DNS issue |
| Wrong IP | Stale cache, split-horizon DNS, wrong record, hosts file |
| Works on office Wi-Fi, fails on VPN | Internal DNS only reachable through VPN; split DNS misconfigured |
| Works in browser, fails in app | App uses a different resolver, proxy, or connection path |
| Intermittent failure | Multiple A/AAAA records, one bad backend, resolver rotation |

**Split-horizon DNS** returns different answers depending on where you ask — internal users get private IPs, external users get public ones. Corporate VPNs and internal tools rely on this. It is a common source of "works at the office, fails at home" and vice versa.

**Other name-resolution paths:** Windows may use LLMNR, NetBIOS, or DNS search suffixes; macOS and Linux have their own resolver stacks. The `hosts` file overrides DNS locally and is a frequent cause of mysterious test-machine behavior.

### Commands

```bash
# Cross-platform-ish
nslookup example.com
nslookup example.com 1.1.1.1        # ask a specific resolver
dig example.com +short              # macOS/Linux, if installed
dig example.com AAAA +short
dig example.com @8.8.8.8

# Windows PowerShell
Resolve-DnsName example.com

# Linux with systemd-resolved
resolvectl query example.com
```

Flush caches:

```powershell
# Windows
ipconfig /flushdns
```

```bash
# macOS
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# Linux (systemd-resolved)
sudo resolvectl flush-caches
```

> **QA takeaway:** Test DNS separately from connectivity. If a hostname fails but its IP works, you have a DNS or proxy problem, not a server problem. If both fail, continue down the diagnostic ladder.

## 4.2 DHCP: getting an address automatically

**DHCP** (Dynamic Host Configuration Protocol) gives devices an IP address, subnet mask, default gateway, DNS servers, and sometimes other options, without manual configuration.

### The DORA exchange

```
Client                          DHCP server
  │ ── DHCP Discover ──────────► │   "Is there a DHCP server?"
  │ ◄─ DHCP Offer ────────────── │   "You can have 192.168.1.42"
  │ ── DHCP Request ───────────► │   "I'll take it"
  │ ◄─ DHCP ACK ──────────────── │   "Confirmed; lease is yours"
```

The four steps are **D**iscover, **O**ffer, **R**equest, **A**cknowledge — **DORA**.

- The address is leased for a period. The client renews before expiry (typically at 50% of the lease, then rebinds at 87.5%).
- A **reservation** ties a specific address to a device's MAC address.
- **Static** configuration means no DHCP; the device has a fixed address.
- **DHCPv6** exists, but IPv6 also supports **SLAAC** (Stateless Address Autoconfiguration), where the device builds its own address from a network prefix advertised by the router.

### When DHCP fails

Windows and some other systems assign a **link-local/APIPA** address in `169.254.0.0/16`. That address lets the device talk only on the local link. If you see `169.254.x.x`, the device probably did not get a DHCP lease.

Common causes: no DHCP server, DHCP scope exhausted, VLAN mismatch, Wi-Fi association problem, captive portal blocking DHCP, or a rogue DHCP server.

### Commands

```powershell
# Windows
ipconfig /all
ipconfig /release
ipconfig /renew
```

```bash
# Linux
ip addr
ip route
# or older
ifconfig
route -n
```

```bash
# macOS
ifconfig
netstat -rn
ipconfig getpacket en0
```

Release/renew can disconnect you. Use it only on a test machine or with permission.

> **QA takeaway:** Network changes are test cases. Test DHCP success, lease renewal, address conflict, wrong gateway, wrong DNS, and the APIPA state. A UI that hangs forever when it has no IP is a resilience bug.

## 4.3 VPN: a private tunnel

A **VPN** (Virtual Private Network) creates an encrypted tunnel between your device and a VPN gateway. Traffic inside the tunnel is protected from the local network and the ISP. The gateway then forwards it to the destination.

A VPN is not anonymity software. The destination and the VPN provider can still see your traffic metadata, and the VPN does not protect a compromised device.

### Remote access vs site-to-site

| Type | What it connects | Example |
|---|---|---|
| Remote access | One user/device to a private network | Employee working from home |
| Site-to-site | Two networks | Branch office to data center |

### Full tunnel vs split tunnel

- **Full tunnel** — all traffic goes through the VPN. Internal and external sites see the VPN's public IP. More consistent policy, more latency.
- **Split tunnel** — only selected traffic (usually internal subnets) goes through the VPN; the rest goes directly. Better performance, but different DNS and security behavior.

### Common VPN technologies

| Technology | Notes |
|---|---|
| IPsec | Network-layer encryption; IKE for key exchange; ESP for data. Common in corporate and site-to-site VPNs. |
| TLS-based VPN (OpenVPN, many "SSL VPNs") | Uses TLS; often UDP 1194 by default; can traverse proxies over TCP 443. |
| WireGuard | Modern, lightweight UDP protocol using Noise; default UDP 51820, configurable. |
| Vendor clients | May combine IPsec, TLS, and proprietary features; behavior depends on the client. |

### What VPNs break in testing

- **DNS:** internal names resolve only through VPN DNS; full tunnel may send all DNS to corporate; split DNS may route only some domains. Check for DNS leaks and split-horizon differences.
- **MTU:** encapsulation adds overhead; large packets may be dropped. Symptoms include uploads hanging, pages stalling after the first part, or TLS handshakes succeeding but bodies failing.
- **Latency and throughput:** extra hops and encryption reduce speed. Timeout values that work on the LAN may be too short.
- **Reconnects:** VPN drops mid-request can produce connection resets, partial uploads, stale sessions, or duplicate submissions on retry.
- **Proxies and certificates:** corporate VPNs may force a proxy or TLS inspection; the client must trust the inspection CA.
- **IPv6:** some VPNs tunnel IPv4 only, causing IPv6 traffic to bypass the tunnel or fail.
- **Authentication:** MFA, session expiry, device posture checks, and certificate renewal can fail independently of the app.

> **QA takeaway:** "VPN on/off" is not one test case. Test connect, disconnect mid-request, reconnect, split tunnel, full tunnel, internal vs external DNS, large uploads, and session expiry. Record which VPN client and profile you used.

## 4.4 Proxies and firewalls

A **proxy** sits between client and server and forwards requests.

| Type | Where it sits | What it does |
|---|---|---|
| Forward proxy | In front of clients | Controls/filters outgoing traffic; caches; logs; may inspect TLS |
| Reverse proxy | In front of servers | Load balancing, TLS termination, routing, caching, protection |
| Transparent proxy | Inline, no client config | Intercepts traffic without the client knowing |
| Explicit proxy | Client configured | Client sends requests to the proxy (often port 8080/3128) |

Proxies may use **PAC** (Proxy Auto-Config) files or environment variables such as `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`. A common QA bug is that the browser uses the system proxy but a command-line tool or test runner does not.

A **firewall** filters traffic by rules — source, destination, port, protocol, application, or state. A stateful firewall remembers established connections and allows return traffic. Security groups in cloud environments are distributed firewalls.

**TLS interception:** Some corporate proxies decrypt and re-encrypt traffic to inspect it. The client must trust the proxy's certificate authority. If it does not, you get certificate errors that look like server bugs but are actually trust-store problems.

**Load balancers and CDNs** are not firewalls, but they sit in the same path:

- A **load balancer** spreads requests across backends. Health checks decide which backends are used; sticky sessions keep a user on one backend.
- A **CDN** caches content at edge locations. Cache hits, cache misses, and stale content can explain differences between regions.
- Because different requests may hit different backends, intermittent bugs can look random. Correlate with response headers such as `X-Request-Id`, `Via`, `Server`, or `X-Cache`.

> **QA takeaway:** Test with and without proxy, with the PAC file, with CLI tools, and with TLS inspection enabled. "Works in Chrome, fails in curl" often means different proxy or certificate settings, not a server bug.

---

# Part 5: What QA Needs to Test

## 5.1 The network test matrix

A single "it works on my Wi-Fi" pass is not network testing. Use a matrix and record which condition each test covers.

| Condition | How to simulate safely | What to assert |
|---|---|---|
| Normal network | Baseline Wi-Fi or Ethernet | Correct data, acceptable timing |
| High latency | DevTools throttling, network link conditioner, lab `tc` | Timeouts, spinners, retries, user feedback |
| Low bandwidth | DevTools "Slow 3G", proxy throttling | Progressive loading, no broken states |
| Packet loss / jitter | Lab network emulator; Wi-Fi far from AP | Retries, recovery, no duplicate side effects |
| Offline | DevTools offline; disable test device Wi-Fi | Clear error, queued actions, safe retry |
| DNS failure | `curl --resolve` to a black-hole IP; lab DNS block | Error message, no infinite spinner, no crash |
| Wrong/stale DNS | Test resolver, hosts file, short TTL | Fallback behavior, correct error, no data leak |
| Captive portal | Public Wi-Fi or lab portal | Detection, redirect handling, certificate behavior |
| IPv6-only | Lab network; `curl -6`; disable IPv4 with care | App works without IPv4; AAAA handling |
| Dual stack | Normal modern network | Correct family chosen; fallback works |
| VPN on | Authorized test profile | Internal names resolve, uploads complete, no leak |
| VPN off | Same test off VPN | Expected differences documented |
| Split tunnel | Authorized VPN profile | Only intended traffic uses tunnel |
| VPN drop mid-request | Disconnect during upload/download | Graceful recovery, no corruption or duplicate |
| Proxy on/off | Browser/system proxy; `curl -x` | Proxy-aware clients work; errors are clear |
| Firewall/blocked port | Lab firewall rule | Timeouts handled, no misleading success |
| MTU black hole | Lab VPN/MTU setting; large uploads | Large payloads complete; no hang |
| Expired/wrong TLS cert | `badssl.com` test endpoints | Clear warning; no silent bypass |
| Clock skew | Change test VM clock (authorized) | Certificate and token errors handled |
| Server 5xx | Mock server or feature flag | Error state, retry policy, no data loss |
| Rate limiting (429) | Load or mock `429` | Backoff, messaging, no retry storm |
| Connection drop | Kill connection via proxy/lab | Timeout, recovery, idempotency |
| Reconnect/resume | Toggle network mid-operation | Resume or safe restart |

## 5.2 Functional, resilience, and compatibility testing

**Functional network tests** answer: does the app use the right endpoint, port, protocol, and headers; does it handle the response correctly?

**Resilience tests** answer: what happens when the network is slow, lossy, interrupted, or lying? Look for:

- Timeouts at the right layer (connect, read, total).
- Retries with backoff and a cap.
- Idempotency: a retried `POST` must not create duplicate orders or charges.
- User messaging: "Check your connection" only when that is true.
- Recovery: does the app return to a good state when the network returns?
- Cancellation: does navigating away cancel unnecessary requests?

**Compatibility tests** cover OS, browser, device, Wi-Fi/cellular, VPN, proxy, IPv4/IPv6, and TLS versions.

**Security-adjacent tests** (not penetration testing) include:

- Certificate validation is not disabled.
- No tokens, passwords, or personal data in URLs, logs, or error messages.
- HTTPS is enforced where required.
- Proxy/VPN trust settings do not silently accept invalid certificates.
- Sensitive data is not sent over cleartext protocols.

## 5.3 Timing and performance checks

Open the browser DevTools **Network** panel and read the timing breakdown:

| Phase | What it measures | If it is large |
|---|---|---|
| Queueing / Stalled | Waiting for a connection slot or proxy | Too many parallel requests, connection limits |
| DNS Lookup | Name resolution | DNS slow, resolver issue, first visit |
| Initial Connection | TCP handshake | Latency, distance, VPN, packet loss |
| SSL/TLS | TLS handshake | Certificate chain, CPU, proxy, TLS version |
| Request Sent | Uploading the request | Large request body, slow uplink |
| Waiting (TTFB) | Server processing until first byte | Server or downstream dependency |
| Content Download | Transferring the response | Bandwidth, large payload, compression |

Rules for useful timing tests:

- Compare **cold** and **warm** cache. First visits include DNS and connection setup.
- Report **p50/p95/p99**, not just averages. Averages hide the slow tail users feel.
- Record the network condition. "Slow" on office Wi-Fi means nothing.
- Separate client, network, and server time where possible. A high TTFB with a fast connection points at the server, not the network.
- Test from more than one location if the product is global; CDN and routing differ.

## 5.4 What is not a network bug

Before you file a network bug, rule out:

- Wrong credentials, expired session, or missing permission.
- Application logic errors and validation rules.
- Server 5xx caused by a backend bug or bad deployment.
- Test data or environment configuration.
- Feature flags and A/B tests.
- Browser extensions, ad blockers, or corporate policy.
- Cached old frontend assets after a deployment.

A network bug should have evidence that the failure is in name resolution, connectivity, transport, TLS, proxy/VPN, or routing — not just a generic "network error" shown by the UI.

## 5.5 A checklist for any feature

Before testing a feature, write down:

- Which URLs, hosts, ports, and protocols does it use?
- Which DNS names must resolve, both internally and externally?
- Does it require a VPN, proxy, or specific certificate trust?
- What are its connect, read, and total timeouts?
- What should happen offline, under high latency, and with packet loss?
- Which operations retry, and are they idempotent?
- What is cached, for how long, and how is stale content invalidated?
- What does it log, and is sensitive data excluded from those logs?
- Which network conditions are in scope for this release, and which are out?

That list becomes your test matrix and the evidence checklist in the bug report.

---

# Part 6: Troubleshooting Like a QA Engineer

## 6.1 The diagnostic ladder

Work in order from scope down to the application. Stop when a step fails; that is your layer.

```
0. Scope        Is it one user, one network, one region, or everyone?
1. Link         Is the device connected? Can it reach the gateway?
2. IP           Does it have a valid address, mask, gateway, DNS?
3. DNS          Does the name resolve? Does the IP work?
4. Route        Can packets reach the destination network? VPN? Proxy?
5. Port         Is the destination port open and accepting connections?
6. TLS          Is the certificate valid and trusted? Is the handshake completing?
7. HTTP         What status, headers, redirects, and body came back?
8. Application  Logs, correlation IDs, server-side behavior.
```

| Step | Command examples | What it tells you |
|---|---|---|
| Scope | Ask users, check status page, try another device | Whether the problem is local or widespread |
| Link | `ping <gateway>`, check Wi-Fi/Ethernet | Local connectivity |
| IP | `ipconfig /all`, `ip addr`, `ip route` | Address, DHCP, gateway, DNS servers |
| DNS | `nslookup`, `dig`, `Resolve-DnsName` | Whether the name resolves and to what |
| Route | `tracert`, `traceroute`, `mtr` | Where packets stop or slow down |
| Port | `Test-NetConnection host -Port 443`, `nc -vz host 443` | Whether TCP can connect |
| TLS | `curl -v`, `openssl s_client` | Certificate chain, protocol, handshake errors |
| HTTP | `curl -v`, DevTools Network | Status, headers, redirects, body |
| App | Logs, request IDs, server traces | Business logic and backend errors |

## 6.2 Command toolkit

### Windows PowerShell

```powershell
ipconfig /all
ipconfig /flushdns
ping example.com
tracert example.com
nslookup example.com
Resolve-DnsName example.com
Test-NetConnection example.com -Port 443
curl.exe -v https://example.com
netstat -ano
route print
```

Use `curl.exe`, not bare `curl`, in Windows PowerShell: `curl` is an alias for `Invoke-WebRequest` in older PowerShell versions and its flags differ.

### macOS and Linux

```bash
ip addr                    # Linux
ifconfig                   # macOS / older Linux
ip route                   # Linux
netstat -rn                # macOS
ping example.com
traceroute example.com
dig example.com +short
nslookup example.com
nc -vz example.com 443
curl -v https://example.com
ss -tulpn                  # Linux sockets
lsof -i :443               # macOS / Linux
openssl s_client -connect example.com:443 -servername example.com
```

### Browser DevTools

- **Network** — requests, status, headers, payloads, timing, throttling, offline mode.
- **Console** — CORS, mixed content, certificate, and JavaScript errors.
- **Security** — certificate details and TLS version.
- **Application** — cookies, local storage, service workers, cache.

## 6.3 Reading `curl -v` output

`curl -v` is the fastest way to see which layer failed. A successful request looks roughly like:

```
* Host example.com:443 was resolved.
* IPv6: 2606:2800:...
* IPv4: 203.0.113.10
*   Trying 203.0.113.10:443...
* Connected to example.com (203.0.113.10) port 443
* TLS 1.3 connection using TLS_AES_128_GCM_SHA256
* Server certificate:
*  subject: CN=example.com
*  start date: ...
*  expire date: ...
> GET / HTTP/1.1
> Host: example.com
> User-Agent: curl/...
>
< HTTP/1.1 200 OK
< content-type: text/html
<
```

How to read failures:

| Message | Layer | Meaning |
|---|---|---|
| `Could not resolve host` | DNS | Name resolution failed |
| `Failed to connect ... timed out` | Network/port | Packets dropped or no route |
| `Connection refused` | Port | Host reachable, nothing listening or actively rejected |
| `SSL certificate problem` | TLS | Invalid, expired, self-signed, or untrusted certificate |
| `SSL: wrong version number` | TLS | Speaking TLS to a non-TLS port, or proxy interference |
| `HTTP/1.1 403` / `404` / `500` | HTTP | Connected fine; server or application responded |
| `Empty reply from server` | HTTP/server | Connection closed without a response |

## 6.4 Packet capture without fear

Wireshark (or `tshark`) shows the actual packets. It is useful when logs and curl disagree, or when a failure is intermittent.

Start with simple display filters:

```
dns
tcp.flags.syn == 1
tcp.analysis.retransmission
tcp.flags.reset == 1
tls.alert_message
ip.addr == 192.0.2.10
tcp.port == 443
```

What to look for:

- Does the SYN get a SYN-ACK? If not, the port is blocked or the host is unreachable.
- Are there retransmissions or duplicate ACKs? Packet loss or congestion.
- Is there a RST? Something actively closed the connection.
- Does DNS return an answer? Is it the expected address?
- Does the TLS handshake complete? Is there a TLS alert?
- Does the HTTP request go out, and what comes back?

Use capture filters to limit volume — for example, capture only traffic to one host. Capturing everything can be huge and may contain other people's data. Get authorization, capture only your own test traffic, and sanitize before attaching to a ticket.

## 6.5 Writing a bug report that gets fixed

A network bug report must answer: **what network path, what layer, what evidence, how reproducible, and what impact.**

Use this template:

```markdown
## Summary
Login fails with "Network error" only when the corporate VPN is connected.

## Environment
- Build/version: Web app 2.4.1, API 3.8.0
- OS/browser: Windows 11, Chrome 131
- Network: Office Wi-Fi, full-tunnel VPN, PAC proxy enabled
- IPv4/IPv6: IPv4 only
- VPN/proxy: CorpVPN 5.2, profile "Full Tunnel"; proxy auto-config

## Preconditions
Valid test account; same account works with VPN disconnected.

## Steps to reproduce
1. Connect the corporate VPN.
2. Open https://app.example.test/login.
3. Enter valid test credentials and submit.
4. Wait 30 seconds.

## Expected
Dashboard loads.

## Actual
Spinner then "Network error". DevTools: POST /api/login fails with
net::ERR_CONNECTION_TIMED_OUT after 30 seconds.

## Evidence
- Timestamp: 2026-11-12 10:14 IST (UTC+05:30)
- HAR file: login-vpn-fail.har
- curl -v: connection to api.example.test:443 timed out
- nslookup: resolves to 10.20.30.40 (internal) on VPN; public IP off VPN
- tracert: stops after VPN gateway
- Screenshot/recording: login-vpn-fail.mp4

## Reproduction
5/5 with VPN on; 0/5 with VPN off.

## Impact
All VPN users cannot log in. Work is blocked for remote staff.

## Suspected layer
Routing/firewall or VPN split-tunnel configuration, not the login form.
```

Why this report works:

- It isolates one variable (VPN).
- It includes timestamps with a timezone.
- It shows evidence at multiple layers.
- It distinguishes "connection timed out" from "server returned an error."
- It states impact and reproducibility.

## 6.6 When to escalate

Escalate when the evidence points outside your control:

- DNS answers are wrong or missing from the authoritative source.
- A network path is down for everyone or a region.
- A firewall, load balancer, or proxy is dropping traffic.
- Certificates are expired or misconfigured on the server.
- VPN infrastructure or corporate policy is blocking the app.
- The server returns 5xx with no application-level explanation.

Hand over: timestamps, source and destination IPs, ports, URLs, command outputs, HAR or capture files, reproduction steps, and what you already ruled out.

---

# Part 7: Labs

These labs are safe on your own machine or an authorized test network. Do not run scans or captures on networks you do not own.

## Lab 1 — Map your own connection (15 min)

**Goal:** Read your address, gateway, DNS, and routes.

```powershell
# Windows
ipconfig /all
route print
netstat -ano | findstr :443
```

```bash
# Linux
ip addr
ip route
ss -tulpn
```

```bash
# macOS
ifconfig
netstat -rn
lsof -iTCP -sTCP:LISTEN
```

**Observe:** IPv4 and IPv6 addresses, default gateway, DNS servers, subnet mask/prefix, listening ports.

**QA takeaway:** Most "cannot connect" tickets start with a wrong gateway, no address, or a VPN-provided DNS server.

## Lab 2 — DNS detective (20 min)

**Goal:** Compare name resolution with direct IP access.

```bash
nslookup example.com
dig example.com +short
dig example.com AAAA +short
curl -v https://example.com
```

Force a connection to a specific IP without changing DNS. Resolve the current address first, then reuse it:

```bash
# macOS/Linux
ip=$(dig +short example.com | head -1)
curl -v --resolve example.com:443:"$ip" https://example.com
```

```powershell
# Windows PowerShell
$ip = (Resolve-DnsName example.com -Type A | Select-Object -First 1).IPAddress
curl.exe -v --resolve "example.com:443:$ip" https://example.com
```

**Observe:** Which resolver answered, whether A and AAAA records exist, whether the site works when DNS is bypassed.

**QA takeaway:** Hostname fails + IP works = DNS, proxy, or SNI problem. Both fail = continue down the ladder.

## Lab 3 — Read a real request (20 min)

**Goal:** See DNS, TCP, TLS, and HTTP as separate phases.

1. Open DevTools → Network.
2. Visit a site with cache disabled.
3. Click the main document request.
4. Read the Timing tab.

```bash
curl -v https://example.com -o /dev/null
```

**Observe:** DNS lookup, initial connection, TLS, TTFB, download. Which phase dominates?

**QA takeaway:** "Slow page" is not one bug. Report the phase and the numbers.

## Lab 4 — Trace the path (15 min)

**Goal:** See the hops between you and a destination.

```powershell
tracert example.com
```

```bash
traceroute example.com
# or, if installed:
mtr example.com
```

**Observe:** Where latency jumps, where replies stop, whether a VPN adds hops.

**QA takeaway:** A timeout at an intermediate hop is not always a failure; routers may ignore probes. What matters is whether the final destination is reached.

## Lab 5 — Test a port (10 min)

**Goal:** Distinguish host reachability from service availability.

```powershell
Test-NetConnection example.com -Port 443
Test-NetConnection example.com -Port 80
```

```bash
nc -vz example.com 443
nc -vz example.com 80
```

**Observe:** `TcpTestSucceeded` or "succeeded" means a TCP connection opened. "Refused" or "timed out" means different things.

**QA takeaway:** A reachable host can still have a closed port. Test the exact port the app uses.

## Lab 6 — Break DNS safely (15 min)

**Goal:** See how the app behaves when a name resolves to the wrong place.

```bash
curl -v --resolve app.example.test:443:203.0.113.1 https://app.example.test
```

`203.0.113.0/24` is reserved for documentation; the connection should fail. Observe the timeout and any retry or user-facing error.

**QA takeaway:** DNS failure should produce a clear error, not an infinite spinner or a crash.

## Lab 7 — Throttle and go offline (15 min)

**Goal:** Test resilience without touching the network.

1. Open DevTools → Network → Throttling.
2. Choose "Slow 3G" or add a custom profile with high latency.
3. Load the app and perform a key workflow.
4. Switch to "Offline" mid-request.

**Observe:** Spinners, timeouts, retry behavior, duplicate submissions, error messages, recovery when back online.

**QA takeaway:** Most users are on worse networks than your office. Test the unhappy path deliberately.

## Lab 8 — Inspect a certificate (15 min)

**Goal:** Read a TLS certificate and recognize common failures.

```bash
openssl s_client -connect example.com:443 -servername example.com
```

Or open the site in a browser and view the certificate details.

Then try safe public test endpoints:

- `https://expired.badssl.com`
- `https://wrong.host.badssl.com`
- `https://self-signed.badssl.com`

**Observe:** Issuer, subject, validity dates, chain, protocol version, and the browser error for each bad endpoint.

**QA takeaway:** Certificate errors are not all the same. Record the exact error and the certificate details.

## Lab 9 — VPN comparison (20 min, authorized)

**Goal:** See how a VPN changes DNS, path, and latency.

With permission on a test VPN profile:

1. Record your public IP and DNS servers without VPN.
2. Connect the VPN and repeat.
3. Resolve an internal and an external name.
4. Run `tracert` to an external host.
5. Upload a large test file.

**Observe:** DNS answers, route changes, latency, MTU/upload behavior.

**QA takeaway:** VPN testing is more than "does the page load." Check DNS, large transfers, reconnects, and split tunneling.

## Lab 10 — Your first packet capture (20 min)

**Goal:** See a TCP handshake and DNS query.

1. Install Wireshark.
2. Start capture on your active interface with a filter for one host.
3. Run `nslookup example.com` and open `https://example.com`.
4. Stop the capture.
5. Apply display filters: `dns`, `tcp.flags.syn == 1`, `tcp.port == 443`.

**Observe:** DNS query/response, SYN, SYN-ACK, ACK, TLS handshake.

**QA takeaway:** Captures resolve arguments. "The server never responded" is provable when the SYN has no reply.

---

# Appendices

## Appendix A: Cheat sheet

### Layers

```
Application  HTTP, DNS, DHCP, SSH, TLS
Transport    TCP, UDP, QUIC
Internet     IP, ICMP
Link         Ethernet, Wi-Fi, ARP
```

### Private IPv4 ranges

```
10.0.0.0/8        10.0.0.0    – 10.255.255.255
172.16.0.0/12     172.16.0.0  – 172.31.255.255
192.168.0.0/16    192.168.0.0 – 192.168.255.255
169.254.0.0/16    link-local / APIPA
127.0.0.0/8       loopback
```

### Common ports

```
22    SSH
25    SMTP
53    DNS
67/68 DHCP
80    HTTP
123   NTP
443   HTTPS / HTTP/3 (UDP)
500   IPsec IKE
4500  IPsec NAT-T
853   DNS over TLS
1194  OpenVPN default
3306  MySQL
5432  PostgreSQL
6379  Redis
8080  Alternate HTTP / proxy
51820 WireGuard default
```

### DNS records

```
A      IPv4 address
AAAA   IPv6 address
CNAME  Alias
MX     Mail server
TXT    Text / SPF / verification
NS     Authoritative name server
PTR    Reverse lookup
SOA    Zone authority
SRV    Service location
```

### TCP flags

```
SYN  start connection
ACK  acknowledge
FIN  graceful close
RST  reset / abort
PSH  push data
URG  urgent (rare)
```

### Status codes

```
2xx success      200 201 204
3xx redirect     301 302 304
4xx client       400 401 403 404 409 429
5xx server       500 502 503 504
```

### Diagnostic ladder

```
Scope → Link → IP → DNS → Route → Port → TLS → HTTP → App
```

### Commands

```powershell
ipconfig /all
ipconfig /flushdns
ping example.com
tracert example.com
nslookup example.com
Resolve-DnsName example.com
Test-NetConnection example.com -Port 443
curl.exe -v https://example.com
netstat -ano
route print
```

```bash
ip addr
ip route
ping example.com
traceroute example.com
dig example.com +short
nc -vz example.com 443
curl -v https://example.com
ss -tulpn
openssl s_client -connect example.com:443 -servername example.com
```

### VPN checks

```
DNS: internal names resolve? any leak?
Route: full tunnel or split tunnel?
MTU: do large uploads complete?
Reconnect: does a dropped tunnel recover?
IPv6: does traffic bypass the tunnel?
Certificates: is TLS inspection trusted?
```

## Appendix B: Glossary

| Term | Definition |
|---|---|
| **APIPA** | Automatic Private IP Addressing; `169.254.x.x` assigned when DHCP fails |
| **ARP** | Address Resolution Protocol; maps an IPv4 address to a MAC address on a local network |
| **Bandwidth** | Maximum data rate of a link |
| **CIDR** | Classless Inter-Domain Routing; notation such as `/24` describing the network prefix length |
| **CGNAT** | Carrier-grade NAT; many subscribers share one public IP |
| **DHCP** | Dynamic Host Configuration Protocol; assigns IP configuration automatically |
| **DNS** | Domain Name System; maps names to addresses and other records |
| **DORA** | DHCP Discover, Offer, Request, Acknowledge |
| **Default gateway** | The router a device sends off-subnet traffic to |
| **Ephemeral port** | Temporary client-side port chosen by the OS |
| **Firewall** | Device or software that filters traffic by rule |
| **FQDN** | Fully qualified domain name, e.g. `www.example.com.` |
| **HSTS** | HTTP Strict Transport Security; forces HTTPS for a site |
| **ICMP** | Internet Control Message Protocol; used by ping and traceroute |
| **IP address** | Logical address used to route packets |
| **IPsec** | A suite of protocols for encrypting IP traffic |
| **Jitter** | Variation in packet delay |
| **Latency** | Time for a packet to travel to a destination and back |
| **Lease** | Temporary assignment of an IP address by DHCP |
| **MAC address** | Hardware address of a network interface on the local link |
| **MTU** | Maximum Transmission Unit; largest payload a link can carry |
| **NAT** | Network Address Translation; rewrites addresses between networks |
| **NTP** | Network Time Protocol; synchronizes clocks |
| **PAC** | Proxy Auto-Config; a script that tells clients which proxy to use |
| **Packet** | A unit of data carrying IP headers and payload |
| **PAT/NAPT** | NAT that also translates ports so many clients share one IP |
| **Port** | Number identifying a service or connection endpoint on a host |
| **Proxy** | Intermediary that forwards traffic |
| **QUIC** | UDP-based transport used by HTTP/3 |
| **Recursive resolver** | DNS server that looks up answers on your behalf and caches them |
| **RST** | TCP reset; aborts a connection |
| **SLAAC** | Stateless Address Autoconfiguration for IPv6 |
| **SNI** | Server Name Indication; hostname sent in the TLS ClientHello |
| **Socket** | IP address plus port |
| **Split tunneling** | VPN mode where only selected traffic uses the tunnel |
| **Subnet mask** | Bitmask separating network and host portions of an IPv4 address |
| **TCP** | Transmission Control Protocol; reliable, ordered, connection-oriented |
| **TLS** | Transport Layer Security; encrypts and authenticates connections |
| **TTL** | Time to live; DNS cache lifetime or IP hop limit, depending on context |
| **UDP** | User Datagram Protocol; connectionless, unreliable, low overhead |
| **VPN** | Virtual Private Network; encrypted tunnel between networks or devices |
| **Wireshark** | Packet capture and analysis tool |

## Appendix C: Quiz

Answer these without looking. The answers follow.

1. What does DNS do?
2. What is the difference between TCP and UDP?
3. What is a port, and why does it matter?
4. Name the three private IPv4 ranges.
5. What is a default gateway?
6. What are the four DHCP steps?
7. What does a `169.254.x.x` address usually mean?
8. What does NAT do?
9. What is the difference between a full tunnel and split tunnel VPN?
10. What is the difference between DNS TTL and IP TTL?
11. What does HTTP 502 mean?
12. What does "connection refused" usually mean?
13. What does "connection timed out" usually mean?
14. What is MTU, and why does it matter over VPN?
15. Where does TLS sit in the TCP/IP model?
16. What is SNI?
17. What is a TCP four-tuple?
18. What does `traceroute` show?
19. Why can `ping` fail while HTTPS works?
20. What should a network bug report include?

### Answers

1. Translates names into IP addresses and other records, using a hierarchy of servers and caches.
2. TCP is connection-oriented, reliable, and ordered; UDP is connectionless, unreliable, and unordered, with lower overhead.
3. A number (0–65535) that identifies a service or connection endpoint on a host; it lets multiple programs share one IP.
4. `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
5. The router a device sends traffic to when the destination is outside its local subnet.
6. Discover, Offer, Request, Acknowledge.
7. DHCP failed or no DHCP server was reachable; the device assigned itself a link-local address.
8. Rewrites private addresses/ports to a public address so many devices can share one public IP.
9. Full tunnel sends all traffic through the VPN; split tunnel sends only selected traffic.
10. DNS TTL is a cache lifetime in seconds; IP TTL is a hop limit that prevents packets looping forever.
11. Bad gateway: a proxy or load balancer received an invalid response from an upstream server.
12. The host is reachable but nothing is listening on that port, or a firewall actively rejected it.
13. Packets were dropped or no route exists; the connection never completed.
14. The largest payload a link can carry. VPN encapsulation reduces it; oversized packets may be dropped, causing hangs.
15. Between the transport and application layers in practice, even though OSI models often place it in the presentation/session area.
16. Server Name Indication: the hostname the client wants, sent in the TLS ClientHello so one IP can serve multiple sites.
17. Source IP, source port, destination IP, destination port.
18. The router hops between you and the destination, with round-trip times.
19. ICMP may be blocked while TCP 443 is allowed.
20. Environment, network path, VPN/proxy status, steps, expected/actual, timestamps with timezone, evidence (HAR, curl, DNS, traceroute, capture), reproduction rate, and impact.

## Appendix D: Bug report template

```markdown
## Summary
[One sentence: what fails, under which network condition.]

## Environment
- Build/version:
- OS/browser/device:
- Network type: Wi-Fi / Ethernet / cellular / lab
- IPv4 / IPv6 / dual stack:
- VPN: client, profile, full or split tunnel
- Proxy: none / PAC / explicit; TLS inspection?
- DNS resolver:

## Preconditions
[Test account, data, feature flags, permissions.]

## Steps to reproduce
1.
2.
3.

## Expected

## Actual

## Evidence
- Timestamp with timezone:
- URL/endpoint and method:
- HTTP status:
- DevTools timing / HAR:
- curl -v output:
- nslookup / dig output:
- ping / traceroute output:
- Port test result:
- Certificate details:
- Packet capture (filtered, sanitized):
- Screenshot/recording:

## Reproduction rate
X/Y attempts; works/does not work under which conditions.

## Impact
Who is affected, how often, and what work is blocked.

## Suspected layer
DNS / routing / TCP / TLS / HTTP / proxy / VPN / application.
```

## Appendix E: Running a knowledge-sharing session

A 60–90 minute session for beginners. Adjust as needed.

| Time | Topic | Activity |
|---|---|---|
| 5 min | Why networking matters in QA | One bug story: "works in office, fails on VPN" |
| 10 min | The journey of a request | Draw the browser → DNS → TCP → TLS → HTTP path |
| 10 min | IP addresses, ports, NAT | Read a real `ipconfig /all` output together |
| 10 min | TCP vs UDP | Compare a handshake with a UDP DNS query |
| 10 min | DNS | Live `nslookup` / `dig`, show a stale-cache example |
| 10 min | DHCP and VPN | DORA diagram; VPN on/off demo |
| 10 min | QA test matrix | Pick a feature and list network conditions |
| 10 min | Troubleshooting demo | `curl -v`, DevTools timing, `tracert` |
| 5 min | Bug report exercise | Improve a vague "network error" ticket |
| 5 min | Q&A and take-home labs | Assign Labs 1–3 |

**Demo checklist:**

- A terminal with `curl`, `ping`, `nslookup`/`dig`, `tracert`/`traceroute`.
- A browser with DevTools open.
- A safe TLS test endpoint such as `expired.badssl.com`.
- A test VPN profile, if available and authorized.
- A sample HAR file and a packet capture, pre-recorded so the demo cannot fail.

**Discussion prompts:**

- "The page spins forever. What are the first three things you check?"
- "Login works at the office but not at home. What differs?"
- "The API returns 200 but the UI shows a network error. Where do you look?"
- "A user says the internet is down. How do you prove whether the app or the network is at fault?"

## Appendix F: Resources and what to learn next

**Beginner-friendly references**

- Cloudflare Learning Center — networking, DNS, TLS, VPN, DDoS: https://www.cloudflare.com/learning/
- MDN Web Docs — HTTP, headers, status codes, CORS: https://developer.mozilla.org/
- Wireshark User's Guide: https://www.wireshark.org/docs/
- IANA Service Name and Transport Protocol Port Number Registry: https://www.iana.org/assignments/service-names-port-numbers/
- RFC 791 (IPv4), RFC 793 (TCP), RFC 1034/1035 (DNS), RFC 2131 (DHCP): https://www.rfc-editor.org/

**What to learn next**

- Subnetting and CIDR math — enough to read a network diagram.
- TLS in more depth — certificate chains, SNI, mutual TLS.
- HTTP/2 and HTTP/3 — multiplexing, QUIC, fallback behavior.
- Performance testing — latency, throughput, percentiles, load generation.
- Cloud networking — VPCs, security groups, load balancers, private DNS.
- Packet analysis — Wireshark filters and TCP stream graphs.
- Browser automation — see the companion guide `playwright-for-qa.md`.
- Security testing — authorization, TLS configuration, and safe handling of captured data.

---

## A final word

Networking feels large because it is layered. You do not need to hold all of it in your head. You need a reliable order of questions:

> Is the device connected? Does it have an address? Does the name resolve? Can it reach the network? Is the port open? Is TLS valid? What did HTTP say? What do the logs say?

Ask those in order, change one variable at a time, and write down what you observed. That is most of what network-aware QA looks like — and it is enough to turn a vague "network error" into a bug someone can fix.
