import { timingSafeEqual } from "node:crypto";

export function send(res, status, body) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.end(JSON.stringify(body));
}
export function isAdmin(req) {
  const want = process.env.ADMIN_PASSWORD || "";
  const got = String(req.headers["x-admin-key"] || "");
  if (want.length < 8 || !got) return false;
  const a = Buffer.from(want), b = Buffer.from(got);
  return a.length === b.length && timingSafeEqual(a, b);
}
export function requireAdmin(req, res) {
  if (!process.env.ADMIN_PASSWORD) { send(res, 500, { error: "ADMIN_PASSWORD is not set in Vercel." }); return false; }
  if (!isAdmin(req)) { send(res, 401, { error: "Wrong password." }); return false; }
  return true;
}
export function body(req) {
  if (req.body && typeof req.body === "object") return req.body;
  try { return JSON.parse(req.body || "{}"); } catch { return {}; }
}
// Vercel now connects Blob stores with BLOB_STORE_ID (plus an automatic OIDC token);
// older stores use BLOB_READ_WRITE_TOKEN. Either one works.
export const hasStorage = () => !!(process.env.BLOB_STORE_ID || process.env.BLOB_READ_WRITE_TOKEN);
export function storageReady(res) {
  if (!hasStorage()) {
    send(res, 503, { error: "Storage isn't connected yet — add a Blob store to this Vercel project." });
    return false;
  }
  return true;
}
