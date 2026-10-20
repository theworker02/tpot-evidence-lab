# Data card

## Summary

T-Pot Evidence Lab v3.0.0 is a static public derivative of a local T-Pot collection. It has 741 structured events across 126 opaque source groups and 675 instruction examples. The capture interval is 2026-10-20T12:13:15Z through 2026-10-20T23:01:18Z.

## Labels

`qualifies` is a deterministic weak label. It is true only when an evidence window meets one of these fixed thresholds: five failed authentications in 180 seconds; five recognized web/Redis probes; five explicit decoy-shell commands/uploads; or five distinct honeypot TCP ports. It is not a judgment about intent, identity, ownership, compromise, or provider responsibility.

## Splits

Train, validation, and test splits are disjoint by opaque source group. The split process stratifies groups by whether they include a qualifying window. The evaluation reference answers are supplied for reproducible local grading; do not train on them when reporting held-out metrics.

## Privacy and safety

The public release omits literal IPs, hostnames, provider contacts, target addresses, credentials, raw payloads, captured commands, uploaded objects, secrets, and source-group mappings. It retains event timing and behavior summaries. Review your own policy before combining this dataset with other data.

## Limitations

It is a small, single-environment, short-duration dataset with weak deterministic labels. Distribution, timing, coverage, and labels should not be generalized to the internet. This is unsuitable as the only dataset for a security model or automated enforcement system.

