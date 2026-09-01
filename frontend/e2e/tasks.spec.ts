import { test, expect } from '@playwright/test';

test('tasks inbox loads and shows header', async ({ page }) => {
  await page.goto('http://localhost:3000/tasks');
  await expect(page.locator('text=Task Inbox')).toBeVisible();
});
