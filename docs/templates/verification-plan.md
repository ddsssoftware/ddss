# Verification Plan: [feature or release]

| Field | Value |
| --- | --- |
| Specification | [link] |
| Version | [spec version] |
| Owner | [person or team] |
| Environment | [environment and version] |

## Coverage matrix

| Requirement | Scenario | Check type | Expected evidence | Status |
| --- | --- | --- | --- | --- |
| `REQ-001` | `SCN-001` | Automated | [test output] | Pending |

## Test cases

### VFY-001: [case name]

- **Requirement:** `REQ-###`
- **Setup:** [data, permissions, feature flags]
- **Steps:** [numbered actions]
- **Expected:** [observable result]
- **Failure signal:** [what means the check failed]
- **Evidence:** [link, output, screenshot, or log reference]

## Non-functional checks

- [ ] Security and authorization
- [ ] Privacy and sensitive-data handling
- [ ] Accessibility and keyboard navigation
- [ ] Performance against stated thresholds
- [ ] Compatibility and migration
- [ ] Error handling and recovery
- [ ] Observability and auditability

## Exit criteria

- Every in-scope requirement has a passing check or an explicitly approved waiver.
- Failures include reproduction steps and an owner.
- No critical or high-risk issue is unresolved.
- Evidence is reproducible from the recorded commit and environment.
- Known limitations are documented and communicated.

