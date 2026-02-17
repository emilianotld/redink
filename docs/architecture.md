# Architecture

## High-Level Flow

```
Target
   ↓
Scanner (port & service discovery)
   ↓
Fingerprint Engine (metadata & context extraction)
   ↓
Risk Engine (correlation, scoring & interpretation)
   ↓
CLI Interface / Structured Report
```

### Flow Philosophy

Redink separates **observation** from **interpretation**:

- The Scanner and Fingerprint layers gather observable data.
- The Risk Engine is solely responsible for contextual analysis and scoring.
- The CLI layer only presents results.

This strict separation prevents risk inflation caused by raw detection noise and improves maintainability.

---

## Modules

### scanner

Responsible for identifying reachable network services with minimal assumptions.

**Design principles:**

- Non-intrusive discovery
- Deterministic behavior
- Configurable timeouts and concurrency
- Conservative default strategy

The scanner does not evaluate risk.

---

### fingerprint

Extracts observable and non-intrusive metadata from exposed services, such as:

- Service banners
- Protocol headers
- Response patterns
- Version hints (when available)

This module increases context without performing exploitation or intrusive probing.

The fingerprint layer enriches data — it does not score it.

---

### engine

Core abstraction layer.

**Responsibilities:**

- Normalize detection output
- Correlate services with exposure patterns
- Apply weighted scoring logic
- Integrate confidence levels to reduce false positives
- Map technical findings to business-oriented risk tiers

The scoring model follows:

```
Risk ≈ Probability × Impact × Confidence
```

Where:

- Probability reflects exposure patterns and service type.
- Impact reflects typical business consequences.
- Confidence reflects detection reliability.

Risk scores are intentionally conservative in v0 to avoid artificial inflation.

---

### cli

User interface layer.

**Responsibilities:**

- Parse arguments
- Orchestrate module execution
- Render structured output (human-readable or JSON)

No scanning logic.  
No scoring logic.  
Pure presentation and coordination.

---

## Design Rationale

This architecture ensures:

- Clear boundaries between detection and interpretation
- High testability (modules can be unit-tested independently)
- Extensibility (future scoring models can be swapped without modifying scanner logic)
- Predictable behavior
- Safe execution model
- Reduced false-positive amplification

The separation between raw detection and risk abstraction is deliberate and foundational to the tool.

---

# Cost Model

Redink focuses on exposure patterns that historically correlate with financial impact.

The objective is not vulnerability enumeration, but **economic risk signaling**.

---

## Indirect Costs

These represent structural weaknesses that increase organizational exposure:

- Expanded attack surface
- Lower reconnaissance friction
- Increased probability of lateral movement
- Higher exploitation feasibility

These factors compound over time and increase breach likelihood.

---

## Direct Costs

These represent measurable financial consequences:

- Incident response operations
- Downtime and service disruption
- Regulatory penalties and compliance violations
- Reputational damage and customer churn

The model aims to translate technical exposure into potential financial impact signals.

---

## Risk Scoring Philosophy

Redink risk scores:

- Do **not** represent exploitability.
- Do **not** replace CVSS.
- Do **not** claim vulnerability confirmation.

They represent a simplified, business-oriented abstraction of:

```
Exposure × Likely Impact
```

The v0 model is intentionally simple.

It is designed to evolve through:

- Empirical validation
- Community feedback
- Real-world datasets
- Alignment with industry standards

The long-term vision is to refine scoring without sacrificing interpretability.
