---
status: current
created: 2026-08-04
updated: 2026-11-11
tags: [knowledge, network-rail, stomp, trains]
---

# Network Rail Live Data Integration

## STOMP Feed details
The application connects to Network Rail's STOMP feed to receive live train metadata, specifically Train Movements (TRUST).

- **Host:** `publicdatafeeds.networkrail.co.uk`
- **Port:** `61618`
- **Topic:** `/topic/TRAIN_MVT_ALL_TOC` (for TRUST train movements across all Train Operating Companies)

## Message Processing
The feed emits JSON messages. Train movement messages are identified by `msg_type: "0003"`.
When a "0003" message is received, the application parses the `body` for `loc_stanox` (STANOX code) or `tpl` (TIPLOC code) to identify the train's location.

To follow trains at particular places, filter on the STANOX codes of those locations, for example Birmingham New Street, London Euston or Edinburgh. Look each code up in Network Rail's CORPUS reference data rather than hard-coding one from memory.

For a level crossing Proof of Concept (PoC):
- Ideally, monitor the STANOX locations either side of the crossing.
- A first version can trigger crossing events from general feed activity, to demonstrate the UI responding to live data.

## Notes on UK Rail Reliability
> [!NOTE]
> It is an accepted reality that the UK rail network is less than ideal on more occasions than one would hope. Live data feeds will faithfully report these delays and cancellations, so the frontend UI must be designed to handle and display gracefully when train schedules go awry or data is missing.
