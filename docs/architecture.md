# Architecture

## High-Level Flow

Target
↓
Scanner (ports / services)
↓
Fingerprint (headers, metadata)
↓
Risk Engine (scoring & interpretation)
↓
CLI Output / Report

## Modules

### scanner

Identifies reachable services with minimal assumptions.

### fingerprint

Collects observable, non-intrusive metadata from exposed services.

### risk_engine

Maps technical findings to risk levels and potential business impact.

### cli

User interface layer. No logic, no scanning.

## Design Rationale

This architecture ensures:

- Testability
- Extensibility
- Clear boundaries
- Safe execution

# Cost Model

This framework is designed to highlight issues that commonly lead to financial loss, such as:

## Indirect Costs

- Increased attack surface
- Easier reconnaissance for attackers
- Higher likelihood of successful exploitation

## Direct Costs

- Incident response
- Downtime
- Regulatory penalties
- Reputation damage

## Risk Scoring Philosophy

Risk scores do not represent exploitability.
They represent **probability × impact** from a business perspective.

This model is intentionally simple in v0 and will evolve based on:

- Real-world use
- Feedback
- Industry standards
