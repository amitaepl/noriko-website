# NORIKO catalogue auto-emailer setup

The website code and Netlify function are ready. Complete these one-time steps before testing.

1. Create a Resend account at https://resend.com.
2. In Resend, add and verify the sending domain `aepl.biz`.
3. Add the SPF and DKIM records supplied by Resend wherever DNS for `aepl.biz` is managed. Do not change unrelated MX records.
4. In Resend, create an API key with sending permission.
5. In Netlify, open **Project configuration > Environment variables** and add:
   - Key: `RESEND_API_KEY`
   - Value: the Resend API key
   - Scope: Functions, or all scopes
6. Trigger a new Netlify deploy after saving the variable.
7. Submit one catalogue request using an email address you can check.

Expected result:

- The visitor receives an email from `NORIKO India <info@aepl.biz>` with the PDF attached.
- `info@aepl.biz` receives a BCC copy and can identify the requesting address in the To field.
- The website confirms successful delivery without exposing a public catalogue download button.

If Resend reports that the sender is not verified, confirm the SPF and DKIM records for `aepl.biz` and wait for DNS propagation before testing again.
