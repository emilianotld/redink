# Standards and References

This document describes the standards, frameworks, and best practices that support
the technical rules and economic impact ranges used by the **redink** Risk Engine.

The objective is to ensure transparency, traceability, and ethical use of the model.

---

## 1. General Methodological Approach

redink adopts a **risk assessment approach based on technical exposure**, aligned with
international qualitative and semi-quantitative risk management frameworks.

The tool does **not** perform:

- financial audits
- forensic analysis
- exact loss calculations

All economic figures represent **orders of magnitude**, not precise values.

---

## 2. OWASP – Open Web Application Security Project

### 2.1 OWASP Top 10

The following OWASP Top 10 categories directly support the rules implemented in the
risk engine:

- **A05:2021 – Security Misconfiguration**
  - Missing HTTP security headers
  - Default or insecure configurations
  - Server information disclosure

redink checks related to:

- `Content-Security-Policy`
- `X-Frame-Options`
- `Strict-Transport-Security`
- server version disclosure

are explicitly aligned with this category.

Reference:

- https://owasp.org/Top10/

---

### 2.2 OWASP ASVS (Application Security Verification Standard)

OWASP ASVS defines baseline security controls for web applications.

Relevant sections include:

- **V14 – Configuration**
- **V9 – Communications Security**
- **V7 – Error Handling and Logging**

The absence of these baseline controls increases the attack surface and justifies a
progressive increase in technical risk within redink.

Reference:

- https://owasp.org/www-project-application-security-verification-standard/

---

## 3. Exposed Ports and Services

The classification of certain ports as higher risk is based on:

- NIST SP 800-41 – Guidelines on Firewalls and Firewall Policy
- CIS Benchmarks
- Common industry operational practices

Ports such as:

- 21 (FTP)
- 23 (Telnet)
- 3306 (MySQL)
- 6379 (Redis)

are considered **high risk when publicly exposed**, even without confirmed exploitation.

---

## 4. ISO/IEC 27005 – Risk Management

ISO/IEC 27005 defines risk as:

redink does not calculate real statistical likelihood. Instead, it:

- evaluates **observable exposure**
- maps that exposure to **potential impact**

This approach is consistent with qualitative and semi-quantitative risk assessments
described by the standard.

Reference:

- https://www.iso.org/standard/80585.html

---

## 5. Economic Impact Models

The economic loss ranges used by redink are aligned with **order-of-magnitude impact**
reported by public industry studies, without using proprietary or organization-specific
data.

Conceptual sources include:

- IBM – Cost of a Data Breach Report
- Verizon – Data Breach Investigations Report (DBIR)
- ENISA – Threat Landscape

These reports consistently show that:

- minor incidents incur limited operational costs
- poorly managed exposures can escalate into significant financial impact

---

## 6. Justification of Economic Loss Ranges

The loss ranges defined by redink are:

| Risk level | Estimated loss range |
| ---------- | -------------------- |
| LOW        | USD 0 – 1,000        |
| MEDIUM     | USD 1,000 – 10,000   |
| HIGH       | USD 10,000 – 100,000 |
| CRITICAL   | USD 100,000+         |

These ranges are:

- conservative
- cumulative in nature
- suitable for prioritization without exaggeration

---

## 7. Explicit Model Limitations

The redink risk model does **not**:

- calculate regulatory fines
- assess legal impact by jurisdiction
- understand business-specific context
- assign real exploit probability

These limitations are a deliberate part of the **ethical design** of the tool.

---

## 8. Conclusion

The rules and economic impact ranges used by redink are grounded in internationally
recognized standards and widely accepted best practices.

The Risk Engine is designed to:

- raise awareness
- support prioritization
- enable informed decision-making

Not to create fear or present misleading financial claims.
