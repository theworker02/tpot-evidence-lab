# Data card

Version 3.1.0 has 133,137 combined observations: 741 original local events and 132,396 MIT-licensed observations derived from the Multi-Regional Cloud Honeynet Dataset. There are 14 sensor types. See [source attribution](../THIRD_PARTY_NOTICES.md) and [field definitions](observations.md).

The original 675 instruction examples and 601 evaluation tasks remain unchanged. Only the original subset has deterministic collector-rule labels. Imported observations are unlabelled and do not expand the supervised task. Negative weak labels do not prove benignness; positive weak labels do not prove intent or compromise.

Source groups are split-disjoint within each corpus, with no guarantee of independence across corpora. The imported collection is dominated by three sensors and the two captures differ in location, time, and instrumentation. Protocol/port records do not establish compromise or botnet membership. No model is trained or included.

Literal addresses, geolocation, organizations, hostnames, credentials, commands, and raw payloads are excluded. Timing and behavior remain linkable to the public upstream source; full anonymization is not claimed. Re-identification and automated enforcement are inappropriate uses.
