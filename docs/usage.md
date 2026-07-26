(usage)=

# Usage

Assuming that you've followed the {ref}`installations steps <installation>`, you're now ready to use this package.

Start by importing it:

```python
import bluetooth_data_tools
```

TODO: Document usage

## Parsed results are cached and shared

`parse_advertisement_data`, `parse_advertisement_data_bytes` and
`parse_advertisement_data_tuple` are all memoized. Two callers parsing the same
payload receive the _same_ `service_uuids` list, `service_data` dict and
`manufacturer_data` dict — not copies. Advertisements that carry none of a given
AD type get a shared module-level empty container, so the aliasing also spans
unrelated payloads.

**Treat every parsed result as read-only.** Mutating one corrupts the cache for
every subsequent caller in the process:

```python
uuids = parse_advertisement_data_bytes(flags_only_ad)[1]
uuids.append("dead")                       # don't
parse_advertisement_data_bytes(other_ad)[1]
# ['dead'] — an unrelated advertisement now reports a UUID it never sent
```

Copy before you modify:

```python
uuids = list(parse_advertisement_data_bytes(ad)[1])
```
