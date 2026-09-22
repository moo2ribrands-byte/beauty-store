// Customers place orders here. Prices and totals are worked out on the server from the live
// catalogue — never trusted from the browser. Stock is taken when the shop confirms the order.
import { getProducts, saveOrder } from "../lib/store.js";
import { ZONES } from "../lib/config.js";
import { send, body, storageReady } from "../lib/http.js";
import { randomInt } from "node:crypto";

const phone = (v) => { const m = String(v || "").replace(/[\s-]/g, "").match(/^(?:\+?254|0)([17]\d{8})$/); return m ? "0" + m[1] : null; };
const s = (v, n) => String(v ?? "").trim().slice(0, n);

export default async function handler(req, res) {
  if (req.method !== "POST") return send(res, 405, { error: "POST only" });
  if (!storageReady(res)) return;
  const b = body(req);
  const name = s(b.name, 80), ph = phone(b.phone), loc = s(b.loc, 200);
  const zone = ZONES.find((z) => z.id === b.zoneId);
  const pay = ["stk", "till", "pod"].includes(b.pay) ? b.pay : null;
  const code = s(b.code, 12).toUpperCase();
  if (!name || !ph || !loc || !zone || !pay) return send(res, 400, { error: "Missing name, phone, area, location or payment method." });
  if (pay === "till" && !/^[A-Z0-9]{10}$/.test(code)) return send(res, 400, { error: "Enter the 10-character M-Pesa code." });
  if (pay === "pod" && zone.id === "ctry") return send(res, 400, { error: "Pay on delivery is Nairobi only." });
  const want = Array.isArray(b.items) ? b.items.slice(0, 30) : [];
  if (!want.length) return send(res, 400, { error: "Your bag is empty." });

  let products;
  try { products = await getProducts(); } catch (e) { console.error(e); return send(res, 502, { error: "Couldn't check stock — try again." }); }
  const by = Object.fromEntries(products.map((p) => [p.sku, p]));
  const items = [];
  for (const w of want) {
    const p = by[String(w.sku)], q = Math.floor(Number(w.qty) || 0);
    if (!p || p.status === "hidden" || q < 1) return send(res, 409, { error: "Something in your bag is no longer available." });
    if (q > p.qty) return send(res, 409, { error: `Only ${p.qty} left of ${p.brand} ${p.product} — ${p.variant}.` });
    items.push({ sku: p.sku, qty: q, price: p.price, label: `${p.brand} ${p.product} — ${p.variant} (${p.ml})`, preorder: p.status === "on_the_way", eta: p.eta });
  }
  const subtotal = items.every((i) => i.price != null) ? items.reduce((a, i) => a + i.price * i.qty, 0) : null;
  const fee = typeof zone.fee === "number" ? zone.fee : null;
  const d = new Date(Date.now() + 3 * 3600e3).toISOString(); // Nairobi date for the order number
  const order = {
    no: `HB-${d.slice(2, 10).replace(/-/g, "")}-${randomInt(1000, 9999)}`,
    createdAt: new Date().toISOString(), status: "new", stockTaken: false,
    name, phone: ph, zoneId: zone.id, zone: zone.name, when: s(b.when, 40), loc, landmark: s(b.landmark, 120), notes: s(b.notes, 300),
    pay, code: pay === "till" ? code : "", items, subtotal, fee, total: subtotal != null && fee != null ? subtotal + fee : null,
  };
  try { await saveOrder(order); } catch (e) { console.error(e); return send(res, 502, { error: "Couldn't save your order — try again." }); }
  send(res, 201, { order: { no: order.no, total: order.total, zone: zone.name, when: zone.when } });
}
