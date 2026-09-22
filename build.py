import json,re,os
HERE=os.path.dirname(os.path.abspath(__file__))
t=open(HERE+'/template_v1.html').read()
def rep(a,b,count=1):
    global t
    assert t.count(a)>=1, a
    t=t.replace(a,b,count)
rep('</style>',open(HERE+'/admin.css').read()+open(HERE+'/theme.css').read()+'</style>')
rep('<button data-go="home" data-anchor="faq">FAQ</button>\n      </nav>','<button data-go="home" data-anchor="faq">FAQ</button>\n        <button class="adm-link" data-go="admin" hidden>Manage shop</button>\n      </nav>')
rep('<button data-go="home" data-anchor="faq">FAQ</button>\n    </div>','<button data-go="home" data-anchor="faq">FAQ</button>\n      <button class="adm-link" data-go="admin" hidden>Manage shop</button>\n    </div>')
rep('<section class="wrap block" id="brands" style="padding-top:0">','''<section class="wrap block" id="coming" hidden style="padding-top:0">
    <div class="sec-head"><div><div class="eyebrow" style="color:var(--transit)">On the way from the US</div><h2>Arriving soon</h2></div><p class="muted" style="max-width:32em" id="comingLead"></p></div>
    <div class="grid" id="comingGrid"></div>
  </section>

  <section class="wrap block" id="brands" style="padding-top:0">''')
rep('<div class="eyebrow">10 US brands</div>','<div class="eyebrow" id="brandsEyebrow">US brands</div>')
rep('<details><summary>Why is stock so limited?</summary>','<details><summary>What does pre-order mean?</summary><p>Products under “Arriving soon” are already bought and on their way from the US — shipping takes about 3 months. Pre-order to reserve yours and we deliver it as soon as the box lands. [PRE-ORDER PAYMENT RULE]</p></details>\n          <details><summary>Why is stock so limited?</summary>')
rep('<span class="stock" id="pdpStock"></span></div>','<span class="stock" id="pdpStock"></span></div>\n        <p class="pre-note" id="pdpPre" hidden></p>')
rep('<details><summary>Photos</summary><p>These are illustrated renders of the pack shape and scent colour. [REPLACE WITH REAL PHOTOS of the actual item, ideally showing the batch code.]</p></details>','<details><summary>Photos</summary><p id="photoNote"></p></details>')
rep('<div class="totals" id="coTotals"></div>','<p class="pre-note" id="coPre" hidden></p>\n        <div class="totals" id="coTotals"></div>')
rep('</main>',open(HERE+'/admin_html.html').read()+'</main>')
rep('<div class="foot-base"><span>© 2026 Halisi Beauty [WORKING NAME] · Kenya</span>','<div class="foot-base"><span>© 2026 Halisi Beauty [WORKING NAME] · Kenya · <button class="link" id="ownerLogin" style="font-weight:500;color:inherit">Shop owner login</button><button class="link" id="logoutBtn" hidden style="font-weight:500;color:inherit">Log out</button></span>')
t=re.sub(r'<script>.*</script>','<script>\n'+open(HERE+'/app.src.js').read().replace('\\','\\\\')+'</script>',t,flags=re.S)
t=t.replace('\\\\','\\')
items=json.load(open(HERE+'/seed.json'))
t=t.replace('/*DATA*/',json.dumps(items,ensure_ascii=False,separators=(',',':')))
head='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="description" content="Genuine US body care, hair care and fragrance, delivered across Kenya. Pay with M-Pesa.">\n<meta name="theme-color" content="#26131F">\n<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Crect width=%2232%22 height=%2232%22 rx=%228%22 fill=%22%2326131F%22/%3E%3Ctext x=%2216%22 y=%2223%22 text-anchor=%22middle%22 font-family=%22Arial Black,sans-serif%22 font-size=%2219%22 fill=%22%23F07CA3%22%3Eh%3C/text%3E%3C/svg%3E">\n'
i=t.index('<div class="proto">')
t=head+t[:i]+'</head>\n<body>\n'+t[i:]+'\n</body>\n</html>\n'
t=t.replace('<style>','<style>\n[hidden]{display:none!important}\nhtml{-webkit-text-size-adjust:100%}\nbody{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}',1)
open(HERE+'/../index.html','w').write(t)
print(len(t))
