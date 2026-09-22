import { send, requireAdmin, hasStorage } from "../../lib/http.js";
export default function handler(req, res) {
  if (req.method !== "POST") return send(res, 405, { error: "POST only" });
  if (!requireAdmin(req, res)) return;
  send(res, 200, { ok: true, storage: hasStorage() });
}
