# Security policy

> **MedXAI is a research and educational tool. It is not a medical device, has not been clinically validated, and must not be used to make health decisions.**

## Scope

MedXAI processes user-uploaded medical images and de-identified tabular
features for **demonstration only**. It does not store user data, does not
train on user data, and is **not** appropriate for handling protected
health information (PHI / PII / personal identifiers).

If you find:

- A way to exfiltrate uploads or other users' data from the live demo,
- A path traversal, RCE, SSRF, or similar in the FastAPI backend,
- A dependency advisory that affects this project's runtime,

please report it privately rather than opening a public issue.

## How to report

Email **sonikrish2248@gmail.com** with:

1. A description of the issue and its impact.
2. Steps to reproduce (a minimal proof of concept is ideal).
3. Any disclosure timeline you would like to follow.

You should receive an acknowledgement within seven days. Coordinated
disclosure of fixed issues will be credited in `CHANGELOG.md` and on the
relevant GitHub release notes.

## Out of scope

- Reports about model accuracy, fairness, or clinical correctness — please
  open a regular GitHub issue with the `quality` label instead.
- Issues in third-party datasets we redistribute pointers to (those should
  be reported to the dataset host).
- Issues already covered by published advisories with no novel exploit
  path against MedXAI specifically.
