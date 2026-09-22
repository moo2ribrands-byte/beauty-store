import { getOrders, getOrder, saveOrder, getProducts, saveProducts, ORDER_STATUSES } from "../../lib/store.js";
import { send, body, requireAdmin, storageReady } from "../../lib/http.js";

export default async function handler(req, res) {
  if (!requireAdmin(req, res) || !storageReady(res)) return;
  if (req.method === "GET") {
    try { return send(res, 200, { orders: await getOrders() }); }
    catch (e) { console.error(e); return send(res, 502, { error: "Couldn't load orders." }); }
  }
  if (req.method !== "POST") return send(res, 405, { error: "GET or POST only" });
  const b = body(req);
  if (!/^HB-\d{6}-\d{4}$/.test(String(b.no)) || !ORDER_STATUSES.includes(b.status)) return send(res, 400, { error: "Bad order or status." });
  try {
    const o = await getOrder(b.no);
    if (!o) return send(res, 404, { error: "Order not found." });
    const take = ["confirmed", "out", "delivered"].includes(b.status) && !o.stockTaken;
    const give = b.status === "cancelled" && o.stockTaken;
    let products;
    if (take || give) {
      products = await getProducts();
      const by = Object.fromEntries(products.map((p) => [p.sku, p]));
      for (const l of o.items || []) { const p = by[l.sku]; if (p) p.qty = take ? Math.max(0, p.qty - l.qty) : p.qty + l.qty; }
      await saveProducts(products);
      o.stockTaken = take;
    }
    o.status = b.status; o.updatedAt = new Date().toISOString();
    await saveOrder(o);
    send(res, 200, { order: o, products: products || null });
  } catch (e) { console.error(e); send(res, 502, { error: "Couldn't update the order — try again." }); }
}
