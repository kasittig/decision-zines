# AI-Assisted Development Policy

AI tools are welcome as collaborators, but they are not authorities for editorial claims, provenance, safety interpretation, or publication policy.

## Appropriate uses

- Drafting implementation code and tests from approved contracts.
- Producing synthetic fixtures.
- Finding inconsistencies between schemas, fixtures, and documentation.
- Generating candidate layouts for human review.
- Automating mechanical validation and visual comparison.

## Human review is required for

- Historical and teaching claims.
- Provenance assignments.
- Privacy and de-identification decisions.
- Changes to semantic grammar or validation severity.
- Approval of printed layout, booklet orientation, and visual baselines.

## Disclosure

Material AI-assisted contributions should be disclosed in the pull request. State the tool or model when known, what it helped produce, and how a person verified the result. A disclosure is not a substitute for review.

Suggested pull-request language:

> AI assistance was used to draft the schema and fixture updates. I reviewed the contract changes, ran the validation suite, and inspected the rendered pages.

## Data handling

Do not submit confidential source documents, personal information, unpublished participant recollections, credentials, or private URLs to an AI service without authorization. Prefer de-identified, synthetic fixtures. Follow the source organization's retention, privacy, and security policies.

## Accountability

The human contributor remains responsible for the submitted change. AI-generated output must pass the same tests and review as human-authored output. If the output cannot be explained or verified, it should not be merged.

