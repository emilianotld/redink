# CLI Contract

The CLI is the primary interface for users and must remain stable.

## Core Command´

```bash
redink <target>
```

## Expected Behavior

- Clear startup banner
- Deterministic output
- Human-readable by default
- Scriptable when JSON output is enabled

## Planned Flags

-h, --help              show this help message and exit
--ports PORTS           Ports to scan (e.g. 80,443 or 1-1024)
--timeout TIMEOUT       HTTP request timeout in seconds (default: 5)
--concurrency           CONCURRENCY Maximum concurrent connections
--json                  Output results in JSON format (machine-readable)
--risk-only             Display only risk assessment results
--no-banner             Disable startup ASCII banner
--verify-tls            Enable TLS certificate verification (disabled by default)
--version               show program's version number and exit
-o, --output {normal,json,quiet}  Output format: normal (default), json, quiet
-v, --verbose           Increase verbosity (-v, -vv, -vvv)
--silent                Suppress all non-essential output

## Output Responsibility

The CLI is the only component allowed to:

- Print to stdout
- Format results
- Display warnings or disclaimers
