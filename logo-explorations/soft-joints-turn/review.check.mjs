// Trusted host-side test code: static review page, no controls.
import assert from 'node:assert/strict';
export async function review({ frame, checkImages, checkLayout }) {
  assert.equal(await frame.locator('section').count(), 7);
  assert.equal(await frame.locator('section img').count(), 49);
  await checkImages();
  await checkLayout?.();
}
