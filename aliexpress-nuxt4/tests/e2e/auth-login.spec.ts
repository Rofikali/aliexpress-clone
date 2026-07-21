import { expect, test } from '@playwright/test'

const unauthenticatedSession = {
  success: false,
  code: 401,
  message: 'Authentication required',
  data: null,
}

test.beforeEach(async ({ page }) => {
  await page.route('**/api/auth/session', (route) => route.fulfill({
    status: 401,
    contentType: 'application/json',
    body: JSON.stringify(unauthenticatedSession),
  }))
})

test('signs in through the BFF without exposing tokens to the page', async ({ page }) => {
  await page.route('**/api/auth/login', async (route) => {
    const request = route.request()
    expect(request.method()).toBe('POST')
    expect(request.postDataJSON()).toEqual({ email: 'buyer@example.com', password: 'StrongPassword123!' })

    await route.fulfill({
      contentType: 'application/json',
      body: JSON.stringify({
        success: true,
        code: 200,
        message: 'Logged in successfully',
        data: { profile: { id: 'buyer-1', email: 'buyer@example.com' } },
      }),
    })
  })

  await page.goto('/auth/login')
  await page.getByTestId('login-email').fill('buyer@example.com')
  await page.getByTestId('login-password').fill('StrongPassword123!')
  await page.getByTestId('login-submit').click()

  await expect(page).toHaveURL('/auth/profile')
  await expect(page.getByText('Profile')).toBeVisible()
  await expect(page.locator('body')).not.toContainText('access-token')
  await expect(page.locator('body')).not.toContainText('refresh-token')
})

test('shows a safe error when the BFF rejects credentials', async ({ page }) => {
  await page.route('**/api/auth/login', (route) => route.fulfill({
    status: 401,
    contentType: 'application/json',
    body: JSON.stringify({ success: false, code: 401, message: 'Invalid credentials', data: null }),
  }))

  await page.goto('/auth/login')
  await page.getByTestId('login-email').fill('buyer@example.com')
  await page.getByTestId('login-password').fill('wrong-password')
  await page.getByTestId('login-submit').click()

  await expect(page.getByRole('alert')).toHaveText('Invalid credentials')
  await expect(page).toHaveURL('/auth/login')
})
