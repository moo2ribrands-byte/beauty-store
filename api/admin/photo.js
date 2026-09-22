import { savePhoto } from "../../lib/store.js";
import { send, body, requireAdmin, storageReady } from "../../lib/http.js";

export default async function handler(req, res) {
  if (req.method !== "POST") return send(res, 405, { error: "POST only" });
  if (!requireAdmin(req, res) || !storageReady(res)) return;
  const b = body(req);
  const type = ["image/jpeg", "image/png", "image/webp"].includes(b.type) ? b.type : null;
  if (!type || typeof b.data !== "string") return send(res, 400, { error: "Send a JPG, PNG or WebP photo." });
  const buf = Buffer.from(b.data, "base64");
  if (!buf.length || buf.length > 3.2e6) return send(res, 413, { error: "That photo is too big — try a smaller one." });
  try { send(res, 201, { url: await savePhoto(buf, type) }); }
  catch (e) { console.error(e); send(res, 502, { error: "Couldn't upload the photo — try again." }); }
}
