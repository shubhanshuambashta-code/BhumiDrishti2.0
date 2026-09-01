import { test, expect } from '@playwright/test';

test('project page comments and attachments UI present', async ({ page }) => {
  // Navigate to a sample project page. Adjust ID if your seeded data differs.
  await page.goto('http://localhost:3000/projects/1');
  await expect(page.locator('text=Tasks')).toBeVisible();
  await expect(page.locator('text=Comments').first()).toBeVisible();
  await expect(page.locator('text=Attachments').first()).toBeVisible();
});
