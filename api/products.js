import { getProducts } from "../lib/store.js";
import { SEED } from "../lib/seed.js";
import { cleanProduct } from "../lib/store.js";
import { ZONES } from "../lib/config.js";
import { send, isAdmin } from "../lib/http.js";

export default async function handler(req, res) {
  if (req.method !== "GET") return send(res, 405, { error: "GET only" });
  const admin = isAdmin(req);
  let products, live = true;
  try {
    products = process.env.BLOB_READ_WRITE_TOKEN ? await getProducts() : SEED.map(cleanProduct);
    live = !!process.env.BLOB_READ_WRITE_TOKEN;
  } catch (e) {
    console.error(e);
    return send(res, 502, { error: "Couldn't load products." });
  }
  if (!admin) products = products.filter((p) => p.status !== "hidden");
  send(res, 200, { products, zones: ZONES, live, admin });
}
