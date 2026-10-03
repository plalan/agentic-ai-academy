# Ransomware response runbook (sample)

A generic, vendor-neutral runbook for the first hours of a suspected ransomware incident. Adapt it to your organisation, your legal duties and your regulators.

## 1. Detect and confirm

Signs include files renamed with an unfamiliar extension, ransom notes in shared folders, a sudden spike in file changes, backup anomaly alerts and endpoint detection alerts for mass encryption. Confirm quickly, but do not wait for certainty before containing.

## 2. Contain

Isolate affected machines from the network. Prefer network isolation through your endpoint tool over powering machines off, because memory can hold evidence and sometimes encryption keys. Disable compromised accounts and revoke their active sessions. Block known malicious domains and IP addresses at the firewall.

## 3. Protect the backups

Attackers target backups first. Confirm that immutable and offline copies are intact and locked. Suspend any scheduled job that could overwrite good backups with encrypted data. Change backup administrator credentials from a clean device.

## 4. Assess and report

Identify which systems and data are affected, and whether data was stolen as well as encrypted. Involve legal counsel early. Some regulators require notification within hours: for example, India's CERT-In directions set a 6-hour reporting window for specified incidents, and GDPR requires reporting qualifying personal data breaches within 72 hours.

## 5. Recover

Restore in an agreed order of business priority, from backups verified to be clean. Rebuild compromised systems rather than cleaning them. Reset credentials, patch the entry point, and monitor closely for re-infection.

## 6. Learn

Hold a review within two weeks. Record the entry point, the time to detect, the time to contain and the time to recover, then fix the gaps that slowed you down.
