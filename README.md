# Halisi Beauty

Delivery-only shop for genuine US beauty brands in Kenya, with M-Pesa checkout (simulated for now).

- `index.html` is the whole storefront plus the **Manage shop** page. There's no build step.
- `api/` holds small Vercel functions: products, orders, owner login and photo upload.
- `lib/` has the shared code:
  - `config.js`: delivery zones and fees. Edit this file to set them.
  - `store.js`: storage on Vercel Blob.
  - `seed.js`: the starting catalogue from the 4 Sep 2026 inventory. It has no buying costs, and buying costs are never stored.
- `scripts/` holds the page's source parts. Run `python3 scripts/build.py` to rebuild `index.html` after editing them.

## Deploy on Vercel (one time, about 5 minutes)

1. **Import the repo:** on vercel.com, go to **Add New → Project** and pick this GitHub repo. Leave every setting as it is (Framework: *Other*, no build command) and press **Deploy**.
2. **Add storage:** in the project, go to **Storage → Create → Blob** and create a store with **public** access. Connect it to the project. This adds `BLOB_STORE_ID` (or `BLOB_READ_WRITE_TOKEN` on older stores) automatically.
3. **Set the owner password:** in **Settings → Environment Variables**, add `ADMIN_PASSWORD` with 8 or more characters, for Production and Preview.
4. **Redeploy:** go to **Deployments**, open the latest one, choose **⋯ → Redeploy**. The redeploy picks up the new variables.

After that, every push to `main` goes live automatically.

## Using it

- **Customers:** open the site, shop, and check out.
- **Owner:** tap **Shop owner login** at the bottom of the page, or go to `/#manage`, and enter the password. From there she can:
  - add products and upload photos
  - set prices and stock
  - mark shipments as on the way or arrived
  - confirm or cancel orders. Confirming takes the items out of stock, and cancelling puts them back.

Until storage is connected, the site shows the starting catalogue and saving is switched off.

## Still to do before real customers

- A real M-Pesa connection (Daraja STK Push), which needs her Till or Paybill and Safaricom API keys. Payments are simulated right now.
- The details still in [BRACKETS] on the page: prices, delivery fees, Till number, WhatsApp, returns policy, and so on.
- Keep in mind that orders, which include customer names and phone numbers, are stored as unlisted files in the Blob store. That's fine for a pilot. Move them to a database before scaling up.
