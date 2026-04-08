# Troubleshooting: "Not enough seats to create a new organization"

**Applies to:** GitHub Enterprise Cloud — onboarding a new organization at  
`https://github.com/enterprises/<your-enterprise>/onboarding/organizations/new`

---

## What does this error mean?

When you see:

> **"Not enough seats to create a new organization"**

GitHub is telling you that your enterprise account does not currently have enough available user licenses (seats) to proceed with creating the organization.

Under GitHub Enterprise Cloud, seat availability is checked when you create a new organization. If the billing/licensing system does not yet show any available seats — or if the seats have not yet become visible to the org-creation flow — the request is blocked.

---

## Possible cause: trial seat-propagation delay (reported behavior)

> **Note:** The following describes a behavior that has been reported by some users and **may occur**, but is not guaranteed to affect every account. GitHub does not publicly document this as a named bug.

Some enterprise admins have reported a scenario where:

1. A GitHub Enterprise trial is activated.
2. The enterprise **Licensing** page (`/enterprises/<slug>/settings/billing`) shows the expected number of seats (e.g., 50).
3. Attempting to create an organization immediately afterward returns the "Not enough seats" error.

This **may** happen because the seat allocation is provisioned at the enterprise level but has not yet propagated to the internal permission check used by the organization-creation flow. The mismatch is typically transient.

---

## Actionable troubleshooting steps

Work through these steps in order.

### 1. Wait and retry

If your enterprise trial was just activated or seats were just added, **wait 5–15 minutes** and try again. Transient propagation delays sometimes resolve on their own.

### 2. Verify your seat allocation

Confirm that seats are actually showing as available:

1. Go to your enterprise settings:  
   `https://github.com/enterprises/<your-enterprise>/settings/billing`
2. Under **Licensing** (or **GitHub Enterprise Cloud** depending on your plan), check the number of **total seats** vs. **used seats**.
3. If the counts look correct but org creation still fails, continue to the next step.

### 3. Confirm you have the correct permissions

Only an **enterprise owner** can create a new organization during onboarding. Billing managers and organization owners cannot.

To verify your role:

1. Go to `https://github.com/enterprises/<your-enterprise>/people`.
2. Look for your account under the **Owners** tab.
3. If you are not listed as an owner, ask an existing enterprise owner to grant you the **Owner** role or to create the organization on your behalf.

### 4. Try a browser workaround

If the above checks pass, these browser-level workarounds have helped some users:

- **Sign out of GitHub and sign back in**, then retry.
- **Use a different browser or an incognito/private window**, then retry.
- **Clear cookies and cached data** for `github.com`, then retry.

### 5. Contact GitHub Support (fastest resolution)

If none of the above resolves the issue, opening a GitHub Support ticket is the fastest path to resolution. GitHub support engineers can inspect your enterprise's seat allocation and fix any provisioning inconsistency on the back end.

---

## Ready-to-copy support ticket

Use the template below. Replace `<your-enterprise>` and `<your-enterprise-name>` with your actual values.

---

**Subject:**

```
Enterprise shows available seats but "Not enough seats to create a new organization" — <your-enterprise-name>
```

**Body:**

```
Hello GitHub Support,

I am an enterprise owner for the following GitHub Enterprise Cloud account:

  Enterprise name: <your-enterprise-name>
  Enterprise URL:  https://github.com/enterprises/<your-enterprise>

Issue:
When I navigate to:
  https://github.com/enterprises/<your-enterprise>/onboarding/organizations/new

I receive the error:
  "Not enough seats to create a new organization"

However, the Licensing page at:
  https://github.com/enterprises/<your-enterprise>/settings/billing

shows [NUMBER] seats available (e.g., 50 total, 0 used).

Additional context:
- The enterprise trial / seat allocation was activated on [DATE].
- I have confirmed I am listed as an enterprise owner.
- I have tried signing out and back in, and retrying in a different browser.

Could you please investigate whether there is a provisioning or propagation
issue preventing the org-creation flow from recognizing the available seats,
and fix the seat allocation so I can create an organization?

Thank you.
```

---

## When to escalate

If GitHub Support confirms that seats are correctly provisioned but the error persists, ask them to:

- Manually trigger a seat-allocation refresh for your enterprise.
- Create the initial organization on your behalf as a workaround while they investigate.

---

## Related resources

- [GitHub Docs — Creating a new organization from scratch](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/creating-a-new-organization-from-scratch)
- [GitHub Docs — About billing for your enterprise](https://docs.github.com/en/billing/managing-billing-for-your-github-account/about-billing-for-your-enterprise)
- [GitHub Docs — Roles in an enterprise](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-accounts-and-repositories/managing-users-in-your-enterprise/roles-in-an-enterprise)
- [GitHub Support](https://support.github.com)
