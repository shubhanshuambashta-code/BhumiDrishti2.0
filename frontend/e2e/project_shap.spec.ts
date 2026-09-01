import { test, expect } from '@playwright/test';

test('project page shows explanation SHAP panel', async ({ page }) => {
  await page.goto('http://localhost:3000/projects/1');
  // Wait for explanation image to appear
  await expect(page.locator('img[alt="SHAP chart"]')).toBeVisible({ timeout: 5000 });
  // also check positive/negative lists visible
  await expect(page.locator('text=Top Contributors').first()).toBeVisible();
});
