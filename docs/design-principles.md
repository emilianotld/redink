# Design Principles

## 1. Ethics First

The framework must never encourage or automate exploitation.
It focuses on observation, exposure analysis, and risk evaluation.

## 2. Read-Only by Design

All modules operate in a non-intrusive, read-only manner.
No payloads, no fuzzing, no brute force.

## 3. Separation of Responsibilities

- Scanner: detects reachable services
- Fingerprint: collects observable metadata
- Risk Engine: interprets risk
- CLI: presentation layer only

### 3.1 Error Handling

Redink uses **custom exceptions** and never relies on `print()` for critical errors.

Examples:

- `TargetResolutionError`
- `ModuleExecutionError`
- `InvalidConfigurationError`

This enables:

- Clear user-facing messages
- Detailed logs for debugging
- More predictable and testable code

### 3.2 Logging and User Feedback

All communication is handled through a centralized **logger**:

- `INFO` → normal informational messages
- `WARNING` → non-critical situations
- `ERROR` → recoverable failures
- `CRITICAL` → execution aborts

`print()` statements are never used outside of exceptional debugging scenarios.

### 3.3 Risk Levels (Risk Ranges)

Redink classifies findings using normalized risk ranges:

- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

This allows seamless integration with reports, pipelines, or future graphical interfaces.

## 4. Explainability Over Complexity

Risk scoring must be transparent and explainable.
No black-box decisions.

## 5. Minimal Dependencies

The framework should remain lightweight and auditable.

## 6. Cross-Platform

Development may occur on Windows, but execution must be viable on Linux environments.
