# SessionCommit Default Concurrency 50 Implementation Plan

**Goal:** Raise the OpenViking `SessionCommit` queue's default worker concurrency from 4 to 50 while preserving the `queue_workers.session_commit.max_concurrent` override introduced by PR #3636.

**Architecture:** Use `QueueWorkersConfig` as the server configuration source, pass the configured value through `OpenVikingService` into `QueueManager`, and keep `QueueManager`'s direct-construction default consistent. Other queue defaults remain unchanged.

## Required changes

- Change the `session_commit`-specific configuration default to 50.
- Keep explicit `queue_workers.session_commit.max_concurrent` values working.
- Change the `QueueManager` and storage-initialization fallback defaults to 50.
- Update the example configuration and English/Chinese server configuration references.
- Do not change any other queue concurrency limit or restart a running service.

## Verification

1. Add behavior tests proving that an empty configuration selects 50 for `session_commit`, while explicit per-queue values are preserved.
2. Add a focused `QueueManager` test proving that direct construction selects 50 for `SessionCommit`.
3. Run the focused tests and confirm they fail with the old value of 4.
4. Implement the configuration and runtime defaults.
5. Re-run focused tests, Ruff checks, and `git diff --check`.
