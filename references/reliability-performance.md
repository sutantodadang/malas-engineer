# Reliability and performance guide

Read this before changing a hot path, a queue consumer, a scheduled job, or a capacity-sensitive service.

## Define reliability before measuring it

An SLI is a ratio of good events to valid events. A latency number alone is not an SLI. "Percent of requests completed under 300 ms" is an SLI.

An SLO is a target for an SLI over a window. "99.9 percent of requests succeed under 300 ms over 30 days."

The error budget is the allowed violation. If the SLO is 99.9 percent over 30 days, about 43 minutes of full failure is the budget. Spend it deliberately.

Practical defaults:

| Service type | SLI | Starting SLO |
|---|---|---|
| User-facing API | Successful requests under a latency threshold | 99.9 percent over 30 days |
| Internal API | Successful requests | 99.5 percent over 30 days |
| Batch pipeline | Events processed within a window | 99 percent within the window |
| Queue consumer | Messages processed without dead-letter | 99.9 percent |

These are starting points. Set them from user expectations and measured baseline, not from ambition.

## Measure correctly

- Report p50, p95, and p99. An average hides the tail.
- Measure at the boundary the user experiences, not only inside the service.
- Beware coordinated omission: a load generator that waits for a response understates latency during overload.
- Separate client-side and server-side latency when both matter.
- Record the sample size and the window. A percentile from 20 requests is noise.

## Latency budgets

Split the end-to-end budget across hops before optimizing one hop.

```text
Client 300 ms budget
  gateway        20 ms
  auth           10 ms
  service A      80 ms
  service B     120 ms
  database       50 ms
  serialization  20 ms
```

A hop that exceeds its budget is the target. Do not optimize a hop that is inside budget while the tail is elsewhere.

## Change-level checklist

- [ ] Every network call has a timeout.
- [ ] Retries apply only to idempotent operations, with jitter and a cap.
- [ ] Retry budgets prevent retry storms.
- [ ] Queues and pools are bounded.
- [ ] Backpressure exists. Producers slow down or shed load.
- [ ] Background jobs are idempotent and safe to replay.
- [ ] Scheduled jobs cannot overlap into duplicate work without a lock or idempotency key.
- [ ] Pagination is enforced on user-controlled collections.
- [ ] N+1 queries are absent on the changed path.
- [ ] Work that does not need a transaction is outside it.
- [ ] Large payloads are streamed, not loaded whole.
- [ ] Caches have a size bound, a TTL, and an invalidation story.
- [ ] Circuit breakers or bulkheads protect shared dependencies where the blast radius justifies them.
- [ ] Graceful shutdown drains in-flight work.

## Database performance

- Index for the query patterns you actually run. Verify with the query plan.
- Avoid functions on indexed columns in predicates.
- Select only needed columns.
- Use keyset pagination for deep pages, not large offsets.
- Watch for lock contention on hot rows.
- Keep migrations online when the table is large: add nullable, backfill in batches, then constrain.
- Measure before adding an index. Measure after to confirm it is used.

## Load and resilience testing

- Use realistic scenarios and data volumes.
- Assert on percentiles, not averages.
- Run a baseline, a target load, and an overload test.
- Test dependency failure: timeout, error rate, slow response.
- Test recovery: does the system return to baseline without a restart?
- Chaos experiments start in staging with a hypothesis and a rollback.

Common tools: k6, Gatling, Locust, Vegeta.

## Observability

- Log actionable events with a correlation identifier.
- Emit metrics at boundaries: request rate, error rate, duration, saturation.
- Trace across service boundaries where the system is distributed.
- Alert on symptoms users feel, not on every internal metric.
- Keep cardinality under control. Do not put user identifiers in metric labels.
- Dashboards should answer: is it broken, where, and since when?

## Release safety

- Canary or progressive rollout when the blast radius is real.
- Feature flags for behavior that may need a fast rollback.
- Rollback plan for schema and data changes. A code rollback that cannot read the new schema is not a rollback.
- Post-deploy smoke test on the critical path.

## Incident response

1. Stop the bleeding. Roll back or disable the feature.
2. Communicate status and impact.
3. Preserve evidence: logs, metrics, traces, deploy history.
4. Write a blameless postmortem with a timeline and contributing factors.
5. Track corrective actions to completion.

## Anti-patterns

- Adding a cache before measuring the bottleneck.
- Adding a queue to hide a slow synchronous call.
- Retrying a non-idempotent write.
- Unbounded goroutines, threads, or promise chains over user data.
- Alerting on CPU instead of user-visible symptoms.
- A dashboard with 40 panels and no answer.
- Claiming a speedup without a before-and-after measurement.

## References

- Google SRE Workbook, Implementing SLOs: https://sre.google/workbook/implementing-slos/
- Google SRE Book, Monitoring Distributed Systems: https://sre.google/sre-book/monitoring-distributed-systems/
- DORA metrics: https://dora.dev/guides/dora-metrics-four-keys/
