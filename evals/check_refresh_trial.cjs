// Run with TRIAL_DIR pointing at a completed refresh task.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const { RefreshService } = require(path.resolve(process.env.TRIAL_DIR, "refresh.cjs"));

function setup() {
  const calls = [];
  const service = new RefreshService({
    load(key, view) {
      return new Promise((resolve, reject) => calls.push({ key, view, resolve, reject }));
    },
  });
  return { calls, service };
}

const nextTurn = () => new Promise(resolve => setImmediate(resolve));

test("default and explicit summary share a load, then fetch again", async () => {
  const { calls, service } = setup();
  const first = service.refresh("k");
  const second = service.refresh("k", "summary");
  await nextTurn();
  assert.deepEqual(calls.map(({ key, view }) => [key, view]), [["k", "summary"]]);
  calls[0].resolve(false);
  assert.deepEqual(await Promise.all([first, second]), [false, false]);
  const third = service.refresh("k");
  await nextTurn();
  assert.equal(calls.length, 2);
  calls[1].resolve(0);
  assert.equal(await third, 0);
});

test("all distinct string pairs load independently", async () => {
  const { calls, service } = setup();
  const pairs = [["a:b", "c"], ["a", "b:c"], ["a", "c"], ["", ""]];
  const pending = pairs.map(pair => service.refresh(...pair));
  await nextTurn();
  assert.deepEqual(calls.map(({ key, view }) => [key, view]), pairs);
  calls.forEach((call, i) => call.resolve(i));
  assert.deepEqual(await Promise.all(pending), [0, 1, 2, 3]);
});

test("one rejected load reaches both callers and permits a retry", async () => {
  const { calls, service } = setup();
  const error = new Error("offline");
  const failures = [service.refresh("k"), service.refresh("k")].map(
    result => assert.rejects(result, e => e === error));
  await nextTurn();
  assert.equal(calls.length, 1);
  calls[0].reject(error);
  await Promise.all(failures);
  const retry = service.refresh("k");
  await nextTurn();
  assert.equal(calls.length, 2);
  calls[1].resolve(1);
  assert.equal(await retry, 1);
});

test("services use their own stores", async () => {
  const a = setup();
  const b = setup();
  const results = [a.service.refresh("k"), b.service.refresh("k")];
  await nextTurn();
  assert.equal(a.calls.length, 1);
  assert.equal(b.calls.length, 1);
  a.calls[0].resolve("A");
  b.calls[0].resolve("B");
  assert.deepEqual(await Promise.all(results), ["A", "B"]);
});

test("a synchronous store error preserves the promise API and permits retry", async () => {
  let count = 0;
  const error = new Error("offline");
  const service = new RefreshService({ load() {
    if (++count === 1) throw error;
    return 7;
  } });
  await assert.rejects(service.refresh("k"), e => e === error);
  assert.equal(await service.refresh("k"), 7);
});
