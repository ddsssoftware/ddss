# Spec-Driven Development

Spec-driven development makes the intended behavior explicit before implementation
begins. The specification is the shared contract between people, agents, code, and
verification.

## The delivery loop

1. **Discover** — establish the user, problem, context, constraints, and non-goals.
2. **Specify** — describe observable behavior with examples and acceptance criteria.
3. **Plan** — decompose the work into small, ordered tasks with clear ownership.
4. **Implement** — change only what the approved specification requires.
5. **Verify** — test the acceptance criteria, including failure and boundary cases.
6. **Review** — inspect the implementation, evidence, risks, and unresolved questions.
7. **Record** — update the specification and decision records when behavior changes.

Do not treat a plan as approval or a passing unit test as proof that the whole
specification is satisfied.

## What a good specification contains

- **Problem and outcome:** who needs what and why it matters.
- **Scope:** what is included, explicitly excluded, and deferred.
- **Terms:** definitions for domain language and ambiguous concepts.
- **Inputs and outputs:** shapes, types, defaults, limits, and error behavior.
- **Behavior:** rules written as observable scenarios.
- **Quality attributes:** security, privacy, accessibility, performance, reliability,
  and compatibility requirements.
- **Acceptance criteria:** objective conditions that can be checked.
- **Open decisions:** unresolved questions with an owner and due date.

Prefer precise language:

- “The system **must** …” for a requirement.
- “The system **should** …” for a strong preference.
- “The system **may** …” for an optional behavior.
- Avoid “fast”, “simple”, or “user-friendly” without a measurable threshold.

## Scenario format

Use a consistent structure for behavior:

```text
Given [initial context]
When [action or event]
Then [observable result]
And [additional result]
```

Include at least one happy path, one invalid-input case, one boundary case, and one
recovery or permission case where relevant.

## Agent operating rules

An implementation agent should:

1. Restate the goal, constraints, and non-goals.
2. Identify missing information and risky assumptions.
3. Propose a bounded plan before editing.
4. Use the smallest suitable tools and least privilege.
5. Keep changes traceable to a requirement.
6. Surface errors; never invent success or silently discard failures.
7. Run the relevant checks and report exact evidence.
8. Stop and ask when a decision changes scope, safety, data handling, or public behavior.

An approval is required before an agent performs destructive actions, changes a public
interface, handles sensitive data, or expands the agreed scope.

## Traceability

Give each requirement a stable identifier, such as `REQ-001`. Reference those IDs in
tasks, tests, pull requests, and release notes:

```text
REQ-001 → TASK-003 → TEST-007 → implementation
```

When a requirement cannot be verified, mark it as blocked rather than claiming
completion.

## Change control

For every proposed change, state:

- Which requirement changes.
- Why the existing behavior is insufficient.
- The compatibility and migration impact.
- Which tests and documentation need updating.
- Whether the specification needs a new version or decision record.

Keep completed specifications immutable where practical. Record later changes as new
decisions or revisions instead of rewriting history without explanation.

## Definition of ready

- The problem and user outcome are clear.
- Scope and non-goals are explicit.
- Inputs, outputs, constraints, and failure behavior are defined.
- Acceptance criteria are testable.
- Dependencies, risks, and open decisions have owners.
- The implementation boundary and approval gate are known.

## Definition of done

- Every acceptance criterion has evidence.
- Relevant automated and manual checks pass.
- Security, privacy, accessibility, and performance impacts were considered.
- The diff contains no unrelated changes or debug artifacts.
- Documentation and decision records match the shipped behavior.
- Known limitations and follow-up work are recorded.

