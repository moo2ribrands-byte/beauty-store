// Storage on Vercel Blob. Every save writes a NEW file (never overwrites), and reads take the
// newest one, so there is no stale-cache problem. Old versions are pruned.
import { put, list, del } from "@vercel/blob";
import { SEED } from "./seed.js";
import { CATS, SHAPES, ORDER_STATUSES } from "./config.js";

const KEEP_VERSIONS = 15;
const stamp = () => String(Date.now()).padStart(15, "0");

async function listAll(prefix) {
  const out = [];
  let cursor;
  do {
    const r = await list({ prefix, cursor, limit: 1000 });
    out.push(...r.blobs);
    cursor = r.hasMore ? r.cursor : undefined;
  } while (cursor);
  return out;
}
async function readJson(url) {
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error("Blob read failed: " + r.status);
  return r.json();
}
const newestFirst = (a, b) => (a.pathname < b.pathname ? 1 : a.pathname > b.pathname ? -1 : 0);

/* ---------------- products ---------------- */
const HEX = /^#[0-9a-f]{6}$/i;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const str = (v, n = 200) => String(v ?? "").trim().slice(0, n);
export const isBlobUrl = (u) => typeof u === "string" && /^https:\/\/[a-z0-9-]+\.public\.blob\.vercel-storage\.com\/photos\/[A-Za-z0-9._\/-]+$/.test(u);

export function cleanProduct(d) {
  const p = {
    sku: str(d.sku, 60).toUpperCase().replace(/[^A-Z0-9-]/g, ""),
    brand: str(d.brand, 60), product: str(d.product, 120), variant: str(d.variant, 80),
    size: str(d.size, 60), notes: str(d.notes, 300), cond: "New",
    qty: Math.max(0, Math.min(99999, Math.floor(Number(d.qty) || 0))),
    price: Number(d.price) > 0 ? Math.round(Number(d.price)) : null,
    cat: CATS.includes(d.cat) ? d.cat : "Body care",
    shape: SHAPES.includes(d.shape) ? d.shape : "pumpL",
    c: Array.isArray(d.c) && d.c.length === 5 && d.c.every((x) => HEX.test(x)) ? d.c : null,
    status: ["in_stock", "on_the_way", "hidden"].includes(d.status) ? d.status : "in_stock",
    eta: DATE.test(d.eta || "") ? d.eta : null,
    shippedOn: DATE.test(d.shippedOn || "") ? d.shippedOn : null,
    photo: isBlobUrl(d.photo) ? d.photo : null,
    createdAt: str(d.createdAt, 40), updatedAt: str(d.updatedAt, 40),
  };
  p.ml = str(d.ml, 40) || str(p.size.split("/").pop(), 40);
  return p;
}

export async function getProducts() {
  const blobs = (await listAll("state/products-")).sort(newestFirst);
  if (!blobs.length) return SEED.map(cleanProduct);
  const doc = await readJson(blobs[0].url);
  return (doc.products || []).map(cleanProduct);
}
export async function saveProducts(products) {
  await put(`state/products-${stamp()}.json`, JSON.stringify({ products, savedAt: new Date().toISOString() }), {
    access: "public", addRandomSuffix: true, contentType: "application/json",
  });
  const old = (await listAll("state/products-")).sort(newestFirst).slice(KEEP_VERSIONS);
  if (old.length) await del(old.map((b) => b.url)).catch(() => {});
}

/* ---------------- photos ---------------- */
export async function savePhoto(buffer, contentType) {
  const ext = contentType === "image/png" ? "png" : contentType === "image/webp" ? "webp" : "jpg";
  const r = await put(`photos/p-${stamp()}.${ext}`, buffer, { access: "public", addRandomSuffix: true, contentType });
  return r.url;
}
export async function deletePhoto(url) {
  if (isBlobUrl(url)) await del(url).catch(() => {});
}

/* ---------------- orders ---------------- */
// Each order save is a new file under orders/<order no>/ ; the newest one is the current state.
export async function getOrders() {
  const blobs = await listAll("orders/");
  const latest = {};
  for (const b of blobs) {
    const no = b.pathname.split("/")[1];
    if (!latest[no] || newestFirst(b, latest[no]) < 0) latest[no] = b;
  }
  const orders = await Promise.all(Object.values(latest).map((b) => readJson(b.url).catch(() => null)));
  return orders.filter(Boolean).sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1));
}
export async function getOrder(no) {
  const blobs = (await listAll(`orders/${no}/`)).sort(newestFirst);
  return blobs.length ? readJson(blobs[0].url) : null;
}
export async function saveOrder(order) {
  await put(`orders/${order.no}/${stamp()}.json`, JSON.stringify(order), {
    access: "public", addRandomSuffix: true, contentType: "application/json",
  });
  const old = (await listAll(`orders/${order.no}/`)).sort(newestFirst).slice(5);
  if (old.length) await del(old.map((b) => b.url)).catch(() => {});
}
export { ORDER_STATUSES };
