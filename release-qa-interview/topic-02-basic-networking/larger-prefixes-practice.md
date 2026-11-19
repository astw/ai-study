# Larger Prefixes Practice — /8, /16, /24

Focused drills for larger IPv4 networks. Read the "Larger prefixes" section of
`networking-basics.md` first, then answer without revealing the answer.

## Contents

- [Questions and answers](#questions-and-answers)
- [Multiple-choice questions](#multiple-choice-questions)

## Questions and answers

#### Q1. How many host bits are in /8, /16, and /24?

<details>
<summary>Show answer</summary>

Host bits are 32 minus the prefix. /8 has 24 host bits, /16 has 16, and /24 has 8.

</details>

#### Q2. How many usable hosts do /8, /16, and /24 provide?

<details>
<summary>Show answer</summary>

Usable hosts are 2^host bits − 2. /8 provides 16,777,214, /16 provides 65,534, and /24 provides 254.

</details>

#### Q3. For 10.20.30.40/8, what are the network and broadcast addresses?

<details>
<summary>Show answer</summary>

A /8 fixes the first octet as the network, so the network is 10.0.0.0 and the broadcast is 10.255.255.255. The usable range is 10.0.0.1 through 10.255.255.254.

</details>

#### Q4. A host at 172.16.5.9 uses a /16 mask. Which network and broadcast addresses should the engineer expect?

<details>
<summary>Show answer</summary>

A /16 fixes the first two octets, so the network is 172.16.0.0 and the broadcast is 172.16.255.255. The usable range is 172.16.0.1 through 172.16.255.254.

</details>

#### Q5. How many /24 networks fit in a /16?

<details>
<summary>Show answer</summary>

Each /24 is 8 bits longer than a /16, so 2^8 = 256 /24 networks fit. The /24s range from 172.16.0.0/24 to 172.16.255.0/24 inside 172.16.0.0/16.

</details>

#### Q6. How many /16 networks fit in a /8?

<details>
<summary>Show answer</summary>

A /16 is 8 bits longer than a /8, so 2^8 = 256 /16 networks fit. For example, 10.0.0.0/8 contains 10.0.0.0/16 through 10.255.0.0/16.

</details>

#### Q7. How many /24 networks fit in a /8?

<details>
<summary>Show answer</summary>

A /24 is 16 bits longer than a /8, so 2^16 = 65,536 /24 networks fit. That is 256 /16 networks, each containing 256 /24 networks.

</details>

#### Q8. Which prefix is the smallest that provides at least 60,000 usable hosts?

<details>
<summary>Show answer</summary>

A /16 provides 65,534 usable hosts, while a /17 provides only 32,766. So /16 is the smallest prefix that meets the requirement; a /8 would provide far more than needed.

</details>

#### Q9. Why does the "256 − last mask octet" shortcut not work for /16?

<details>
<summary>Show answer</summary>

For /16, the last mask octet is 0, and the interesting octet is the third. Use the general formula 2^(32 − prefix) for addresses per subnet, or apply 256 minus the mask octet where the mask stops being 255.

</details>

#### Q10. What block size applies at the interesting octet for /8, /16, and /24?

<details>
<summary>Show answer</summary>

The interesting octet is the second for /8, the third for /16, and the fourth for /24. In each case the block size is 256, and the total addresses per subnet come from the remaining host bits: 2^24, 2^16, and 2^8.

</details>

## Multiple-choice questions

#### MCQ 1. How many usable hosts does a /8 provide?

A. 16,777,214
B. 65,534
C. 254
D. 16,777,216

<details>
<summary>Show answer</summary>

**Correct answer: A.** A /8 has 24 host bits, so 2^24 − 2 = 16,777,214 usable hosts.

</details>

#### MCQ 2. How many usable hosts does a /16 provide?

A. 65,536
B. 65,534
C. 254
D. 16,777,214

<details>
<summary>Show answer</summary>

**Correct answer: B.** A /16 has 16 host bits, so 2^16 − 2 = 65,534 usable hosts.

</details>

#### MCQ 3. How many usable hosts does a /24 provide?

A. 254
B. 256
C. 65,534
D. 16,777,214

<details>
<summary>Show answer</summary>

**Correct answer: A.** A /24 has 8 host bits, so 2^8 − 2 = 254 usable hosts.

</details>

#### MCQ 4. What is the network address of 10.20.30.40/8?

A. 10.20.0.0
B. 10.0.0.0
C. 10.20.30.0
D. 10.20.30.40

<details>
<summary>Show answer</summary>

**Correct answer: B.** A /8 fixes only the first octet, so the network is 10.0.0.0.

</details>

#### MCQ 5. What is the broadcast address of 10.20.30.40/8?

A. 10.20.255.255
B. 10.20.30.255
C. 10.255.255.255
D. 10.0.0.0

<details>
<summary>Show answer</summary>

**Correct answer: C.** A /8 leaves the last three octets as host bits, so the broadcast sets them all to 1: 10.255.255.255.

</details>

#### MCQ 6. A host at 172.16.5.9/16 needs its network address for a configuration file. Which address is correct?

A. 172.0.0.0
B. 172.16.5.0
C. 172.16.5.9
D. 172.16.0.0

<details>
<summary>Show answer</summary>

**Correct answer: D.** A /16 fixes the first two octets, so the network is 172.16.0.0.

</details>

#### MCQ 7. What is the broadcast address of 172.16.5.9/16?

A. 172.16.255.255
B. 172.255.255.255
C. 172.16.5.255
D. 172.16.0.0

<details>
<summary>Show answer</summary>

**Correct answer: A.** A /16 leaves the last two octets as host bits, so the broadcast is 172.16.255.255.

</details>

#### MCQ 8. A /16 is split into /24 networks for departments. How many /24 networks are available?

A. 128
B. 256
C. 512
D. 65,536

<details>
<summary>Show answer</summary>

**Correct answer: B.** The prefix difference is 8 bits, so 2^8 = 256 /24 networks fit.

</details>

#### MCQ 9. A /8 is split into /16 networks for regional sites. How many /16 networks are available?

A. 128
B. 512
C. 256
D. 65,536

<details>
<summary>Show answer</summary>

**Correct answer: C.** The prefix difference is 8 bits, so 2^8 = 256 /16 networks fit.

</details>

#### MCQ 10. A team needs about 60,000 usable addresses for a new campus. Which prefix is the smallest that fits?

A. /17
B. /24
C. /8
D. /16

<details>
<summary>Show answer</summary>

**Correct answer: D.** /17 provides 32,766 usable hosts, which is too few; /16 provides 65,534, which is enough.

</details>
