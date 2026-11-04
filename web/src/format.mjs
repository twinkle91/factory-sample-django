// Formatting helpers shared by the build script and the page.

const STATUS_LABELS = { todo: 'To do', in_progress: 'In progress', done: 'Done' };

export function statusLabel(status) {
  return STATUS_LABELS[status] ?? status;
}

export function summarize(tasks) {
  const counts = { todo: 0, in_progress: 0, done: 0 };
  for (const task of tasks) {
    if (task.status in counts) counts[task.status] += 1;
  }
  return counts;
}
