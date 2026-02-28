### 📁 examples/advanced_scan/README.md

---

# Advanced Scan Example

This example demonstrates a customized REDINK execution using advanced CLI options.

## Purpose

Run a detailed scan with:

- Custom port range
- Increased concurrency
- Custom timeout
- Optional TLS verification
- Verbosity control

## Usage

```bash
redink example.com \
  --ports 1-1024 \
  --timeout 10 \
  --concurrency 50 \
  --verify-tls \
  -vv
```
