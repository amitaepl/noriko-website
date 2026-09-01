import { readFile } from "node:fs/promises";
import { join } from "node:path";

const RESEND_ENDPOINT = "https://api.resend.com/emails";
const CATALOGUE_NAME = "ASHOKASHA-HORECA-CATALOG-AUGUST-2026.pdf";
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function json(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }
  });
}

export default async (request) => {
  if (request.method !== "POST") return json(405, { error: "Method not allowed" });

  let payload;
  try {
    const contentType = request.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      payload = await request.json();
    } else {
      const form = await request.formData();
      payload = Object.fromEntries(form.entries());
    }
  } catch {
    return json(400, { error: "Invalid request" });
  }

  if (payload.website) return json(200, { ok: true });

  const email = String(payload.email || "").trim().toLowerCase();
  if (!EMAIL_PATTERN.test(email) || email.length > 254) {
    return json(400, { error: "Please enter a valid email address." });
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error("RESEND_API_KEY is not configured");
    return json(503, { error: "Catalogue delivery is temporarily unavailable." });
  }

  try {
    const pdf = await readFile(join(process.cwd(), "private", CATALOGUE_NAME));
    const resendResponse = await fetch(RESEND_ENDPOINT, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        from: "NORIKO India <info@aepl.biz>",
        to: [email],
        bcc: ["info@aepl.biz"],
        reply_to: "info@aepl.biz",
        subject: "Your ASHOKASHA HoReCa Catalogue",
        html: `
          <div style="font-family:Arial,sans-serif;max-width:620px;margin:auto;color:#111816;line-height:1.6">
            <div style="border-top:5px solid #ed1c24;padding:28px 4px 8px">
              <p style="margin:0 0 8px;color:#c8000c;font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase">NORIKO India</p>
              <h1 style="margin:0 0 18px;font-size:30px;line-height:1.15">Your HoReCa catalogue is attached.</h1>
              <p>Thank you for your interest in our professional Asian food range. The ASHOKASHA HoReCa Catalogue is attached to this email.</p>
              <p>For availability, pricing or product enquiries, reply to this email or call <strong>89282 27122</strong>.</p>
              <p style="margin-top:28px">NORIKO India<br>Thane West 400604, MH (INDIA)<br><a href="mailto:info@aepl.biz" style="color:#c8000c">info@aepl.biz</a></p>
            </div>
          </div>`,
        attachments: [{
          content: pdf.toString("base64"),
          filename: CATALOGUE_NAME
        }]
      })
    });

    if (!resendResponse.ok) {
      const detail = await resendResponse.text();
      console.error("Resend error", resendResponse.status, detail);
      return json(502, { error: "We could not send the catalogue. Please try again." });
    }

    return json(200, { ok: true });
  } catch (error) {
    console.error("Catalogue delivery error", error);
    return json(500, { error: "We could not send the catalogue. Please try again." });
  }
};

export const config = { path: "/api/send-catalogue" };
