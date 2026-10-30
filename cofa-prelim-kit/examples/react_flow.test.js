import { expect, test } from 'vitest';
import { addEdge, applyNodeChanges } from '@xyflow/react';

test('React Flow changes a real node position without changing node identity', () => {
  const nodes = [{ id: 'a', position: { x: 0, y: 0 }, data: { label: 'A' } }];
  const changed = applyNodeChanges([{ id: 'a', type: 'position', position: { x: 3, y: 5 } }], nodes);
  expect(changed[0].position).toEqual({ x: 3, y: 5 });
  expect(changed[0].id).toBe('a');
  expect(nodes[0].position).toEqual({ x: 0, y: 0 });
});

test('React Flow addEdge avoids adding the same connection twice', () => {
  const first = addEdge({ source: 'a', target: 'b' }, []);
  expect(first).toHaveLength(1);
  expect(addEdge({ source: 'a', target: 'b' }, first)).toHaveLength(1);
});
