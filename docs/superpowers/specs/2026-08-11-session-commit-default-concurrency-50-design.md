# SessionCommit Default Concurrency 50

## Goal

Raise the OpenViking `SessionCommit` queue's default worker concurrency from 4 to 50 so bulk imports such as LoCoMo do not spend most of their wall time waiting behind a four-worker server queue.

## Design

Change only `DEFAULT_MAX_CONCURRENT_SESSION_COMMIT` in `openviking/storage/queuefs/queue_manager.py` from 4 to 50. `QueueManager._max_concurrent_for_queue()` remains the single consumer of this default, and all other queue limits remain unchanged.

This intentionally changes the global default rather than adding a new configuration surface or a LoCoMo-only override. A running OpenViking process keeps its current worker pool; the new default takes effect after the service is restarted.

## Error Handling and Operational Impact

No new error path is introduced. The existing queue worker loop continues to bound active `SessionCommit` work with an `asyncio.Semaphore`; the bound is simply raised to 50. Deployments must therefore provision model quota, network capacity, and memory for up to 50 concurrent commits.

## Testing

Update the focused `QueueManager` concurrency-selection test so the real `_max_concurrent_for_queue(SESSION_COMMIT)` behavior is expected to return 50. Run that test first against the old implementation to confirm it fails with 4, then change the production constant and rerun the focused storage tests.
