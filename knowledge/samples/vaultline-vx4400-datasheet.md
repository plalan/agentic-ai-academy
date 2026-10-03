# VaultLine VX-4400 Immutable Backup Appliance (fictional datasheet)

This is a fictional product, written for the Academy's retrieval labs. It exists to show how keyword search rescues exact product names and model numbers that embeddings tend to blur.

## Overview

The VaultLine VX-4400 is a 2U backup appliance that stores an immutable copy of protected data. Once a backup snapshot is written, it is locked for the retention period and cannot be modified, encrypted or deleted, including by administrators.

## Key capabilities

WORM retention lock: each snapshot is written once and locked for a retention period between 7 and 3,650 days. The lock is enforced by the storage layer, not by user permissions.

Quorum approval: destructive operations such as shortening retention, deleting a policy or factory reset need approval from two separate administrators. A single compromised admin account cannot destroy backups.

VaultLink air gap: a scheduled, outbound-only replication link copies locked snapshots to an isolated VaultLine vault. The link is closed outside the replication window.

Anomaly alerts: the VX-4400 compares daily change rates and file entropy against a baseline and raises an alert when a backup looks like mass encryption, a common sign of ransomware.

Instant recovery: virtual machines can boot directly from a snapshot on the appliance while data is restored in the background.

## Specifications

Usable capacity: 96 TB, expandable to 384 TB with VX-EXP shelves.
Ingest rate: up to 18 TB per hour.
Network: 4 × 25 GbE.
Encryption: AES-256 at rest, TLS 1.3 in transit.
Supported workloads: VMware vSphere, Microsoft Hyper-V, Microsoft 365, NAS file shares, PostgreSQL and Microsoft SQL Server.

## Model line-up

VX-2200: entry model, 24 TB usable, for branch offices.
VX-4400: mid-range model, 96 TB usable, for data centres.
VX-8800: high-end model, 384 TB usable, with dual controllers.
