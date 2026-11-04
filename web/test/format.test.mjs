import { test } from 'node:test';
import assert from 'node:assert/strict';

import { statusLabel, summarize } from '../src/format.mjs';

test('statusLabel names known statuses', () => {
  assert.equal(statusLabel('in_progress'), 'In progress');
  assert.equal(statusLabel('unknown'), 'unknown');
});

test('summarize counts tasks by status', () => {
  const counts = summarize([{ status: 'todo' }, { status: 'done' }, { status: 'done' }]);
  assert.deepEqual(counts, { todo: 1, in_progress: 0, done: 2 });
});
