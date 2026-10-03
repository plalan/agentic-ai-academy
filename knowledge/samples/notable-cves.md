# Notable CVEs (reference notes)

Short notes on well-known vulnerabilities, useful for practising exact-identifier search. Always check the vendor advisory for current affected versions and fixes.

## CVE-2021-44228 (Log4Shell)

A remote code execution flaw in Apache Log4j 2. Logging a crafted string triggered a JNDI lookup that could load attacker-controlled code. Rated CVSS 10.0. It affected a huge range of Java applications because Log4j is embedded so widely.

## CVE-2023-4966 (Citrix Bleed)

A sensitive information disclosure flaw in Citrix NetScaler ADC and NetScaler Gateway. Attackers could read memory containing session tokens and hijack authenticated sessions, bypassing multi-factor authentication. Rated CVSS 9.4. Patching was not enough on its own; active sessions also had to be terminated.

## CVE-2024-3400

A command injection flaw in the GlobalProtect feature of Palo Alto Networks PAN-OS, exploitable without authentication. Rated CVSS 10.0. It affected PAN-OS 10.2, 11.0 and 11.1 with GlobalProtect configured, and was fixed in hotfix releases.

## CVE-2024-6387 (regreSSHion)

A signal-handler race condition in the OpenSSH server (sshd) on glibc-based Linux systems that can allow unauthenticated remote code execution as root. Rated CVSS 8.1. Exploitation is difficult and slow in practice, but the impact is severe.
