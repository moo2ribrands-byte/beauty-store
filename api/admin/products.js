import { getProducts, saveProducts, cleanProduct, deletePhoto } from "../../lib/store.js";
import { send, body, requireAdmin, storageReady } from "../../lib/http.js";

const today = () => new Date().toISOString().slice(0, 10);
const addDays = (d, n) => { const x = new Date(d + "T00:00:00Z"); x.setUTCDate(x.getUTCDate() + n); return x.toISOString().slice(0, 10); };

export default async function handler(req, res) {
  if (req.method !== "POST") return send(res, 405, { error: "POST only" });
  if (!requireAdmin(req, res) || !storageReady(res)) return;
  const b = body(req), now = new Date().toISOString();
  let products;
  try { products = await getProducts(); } catch (e) { console.error(e); return send(res, 502, { error: "Couldn't load products." }); }
  const idx = (sku) => products.findIndex((p) => p.sku === sku);
  const dropPhotos = [];

  if (b.action === "upsert") {
    const p = cleanProduct({ ...b.product, updatedAt: now });
    if (!p.sku || !p.brand || !p.product || !p.variant || !p.size) return send(res, 400, { error: "Brand, product, scent and size are required." });
    const i = idx(p.sku);
    if (i >= 0) { if (products[i].photo && products[i].photo !== p.photo) dropPhotos.push(products[i].photo); p.createdAt = products[i].createdAt || now; products[i] = p; }
    else { p.createdAt = now; products.push(p); }
  } else if (b.action === "patch") {
    const i = idx(b.sku); if (i < 0) return send(res, 404, { error: "Product not found." });
    const allowed = {};
    for (const k of ["status", "qty", "price", "eta", "shippedOn"]) if (k in (b.patch || {})) allowed[k] = b.patch[k];
    const p = cleanProduct({ ...products[i], ...allowed, updatedAt: now });
    if (p.status === "on_the_way" && !p.eta) p.eta = addDays(today(), 91);
    products[i] = p;
  } else if (b.action === "delete") {
    const i = idx(b.sku); if (i < 0) return send(res, 404, { error: "Product not found." });
    if (products[i].photo) dropPhotos.push(products[i].photo);
    products.splice(i, 1);
  } else if (b.action === "arrive") {
    let n = 0;
    for (const p of products) if (p.status === "on_the_way" && (p.eta || "none") === b.eta) { p.status = "in_stock"; p.updatedAt = now; n++; }
    if (!n) return send(res, 404, { error: "Nothing on the way for that date." });
  } else return send(res, 400, { error: "Unknown action." });

  try { await saveProducts(products); } catch (e) { console.error(e); return send(res, 502, { error: "Couldn't save — try again." }); }
  await Promise.all(dropPhotos.map(deletePhoto));
  send(res, 200, { products });
}
