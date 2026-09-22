/* Fallback catalogue: the Sept 2026 inventory. The live catalogue comes from the shop database. */
const SNAPSHOT=/*DATA*/;
const INVENTORY_DATE="4 Sep 2026";
const TRANSIT_DAYS=91; /* US → Kenya usually takes about 3 months */
/* Delivery zones — fill in fees (numbers, KSh) and times. */
let ZONES=[
  {id:"cbd",name:"Nairobi CBD & Upper Hill",how:"Rider",when:"[SAME DAY]",fee:null},
  {id:"nbo",name:"Rest of Nairobi",how:"Rider",when:"[SAME / NEXT DAY]",fee:null},
  {id:"env",name:"Nairobi environs — Kiambu, Ruiru, Thika Rd, Kitengela, Syokimau, Ngong, Rongai",how:"Rider",when:"[NEXT DAY]",fee:null},
  {id:"ctry",name:"Rest of Kenya",how:"Courier / parcel office [COURIER]",when:"[1–3 DAYS]",fee:null}
];
const CATS=["Body care","Shower","Hair","Deodorant","Fragrance"];
const SHAPES=[["pump","Pump bottle"],["pumpL","Large pump bottle (1 L)"],["flip","Flip-cap bottle"],["duo","Shampoo + conditioner duo"],["jar","Jar / tub"],["tube","Squeeze tube"],["oil","Body oil bottle"],["aerosol","Spray can"],["stick","Deodorant stick"],["mist","Fragrance mist"],["spray","Spray bottle"]];
const SHAPE_KEYS=SHAPES.map(s=>s[0]);
const FEATURED=["EOS|24H Moisture Body Lotion","EOS|Cashmere Body Wash","Fenty Hair|Moisture Repair Deep Conditioner","Bath & Body Works|Fine Fragrance Mist","EOS|Cashmere Whipped Oil Butter","Luseta|Shea Butter & Argan Oil Body Wash","Dove|Advanced Care Antiperspirant Deodorant Stick","EOS|Cashmere Body Oil"];

/* ---------- helpers ---------- */
const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const slug=s=>s.toLowerCase().replace(/&/g,"and").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
const HEX=/^#[0-9a-f]{6}$/i;
function mix(hex,amt){const n=parseInt(hex.slice(1),16);let r=n>>16,g=(n>>8)&255,b=n&255;const t=amt<0?0:255,p=Math.abs(amt);r=Math.round(r+(t-r)*p);g=Math.round(g+(t-g)*p);b=Math.round(b+(t-b)*p);return"#"+((1<<24)|(r<<16)|(g<<8)|b).toString(16).slice(1)}
function palette(body){return[body,mix(body,.6),"#FFFFFF",mix(body,-.45),mix(body,.78)]}
const today=()=>new Date().toISOString().slice(0,10);
function addDays(d,n){const x=new Date(d+"T00:00:00");x.setDate(x.getDate()+n);return x.toISOString().slice(0,10)}
const dLong=d=>d?new Date(d+"T00:00:00").toLocaleDateString("en-GB",{day:"numeric",month:"short",year:"numeric"}):"[DATE]";
const dShort=d=>d?new Date(d+"T00:00:00").toLocaleDateString("en-GB",{day:"numeric",month:"short"}):"[DATE]";
const fmt=n=>"KSh "+Math.round(n).toLocaleString("en-KE");

function norm(d){
  const i={};
  i.sku=String(d.sku||"");i.brand=String(d.brand||"");i.product=String(d.product||"");i.variant=String(d.variant||"");
  i.size=String(d.size||"");i.ml=String(d.ml||i.size.split("/").pop()||"").trim();
  i.qty=Math.max(0,Math.floor(Number(d.qty)||0));
  i.price=typeof d.price==="number"&&d.price>0?d.price:null;
  i.cat=CATS.includes(d.cat)?d.cat:"Body care";
  i.shape=SHAPE_KEYS.includes(d.shape)?d.shape:"pumpL";
  i.c=Array.isArray(d.c)&&d.c.length===5&&d.c.every(x=>HEX.test(x))?d.c:palette(HEX.test(d.color)?d.color:"#E9D3B4");
  i.notes=String(d.notes||"");i.cond=String(d.cond||"New");
  i.status=["in_stock","on_the_way","hidden"].includes(d.status)?d.status:"in_stock";
  i.eta=/^\d{4}-\d{2}-\d{2}$/.test(d.eta||"")?d.eta:null;
  i.shippedOn=/^\d{4}-\d{2}-\d{2}$/.test(d.shippedOn||"")?d.shippedOn:null;
  i.photo=/^https:\/\/[a-z0-9-]+\.public\.blob\.vercel-storage\.com\//.test(d.photo||"")?d.photo:null;
  i.createdAt=d.createdAt||"";
  return i;
}

/* ---------- catalogue ---------- */
let ITEMS=SNAPSHOT.map(norm),BY={},GROUPS=[],GBY={},GID={};
function rebuild(){
  BY={};ITEMS.forEach(i=>BY[i.sku]=i);
  GROUPS=[];GBY={};GID={};
  ITEMS.filter(i=>i.status!=="hidden"&&i.sku).forEach(i=>{
    const otw=i.status==="on_the_way",k=i.brand+"|"+i.product+(otw?"|otw":"");
    if(!GBY[k]){const g={id:slug(k)||i.sku.toLowerCase(),key:k,bp:i.brand+"|"+i.product,brand:i.brand,product:i.product,cat:i.cat,otw,skus:[]};GBY[k]=g;GROUPS.push(g);GID[g.id]=g}
    GBY[k].skus.push(i.sku);
  });
}
rebuild();
const inStockGroups=()=>GROUPS.filter(g=>!g.otw);
const stockOf=g=>g.skus.reduce((a,s)=>a+BY[s].qty,0);
const priceOf=sku=>BY[sku]?.price??null;
const priceText=sku=>{const p=priceOf(sku);return p==null?"KSh [PRICE]":fmt(p)};
function groupPrice(g){const ps=g.skus.map(priceOf);if(ps.some(p=>p==null))return "KSh [PRICE]";const mn=Math.min(...ps),mx=Math.max(...ps);return mn===mx?fmt(mn):fmt(mn)+" – "+fmt(mx)}
const groupEta=g=>g.skus.map(s=>BY[s].eta).filter(Boolean).sort()[0]||null;
function stockInfo(q,it){
  if(it&&it.status==="on_the_way")return q>0?["Arriving ~"+dShort(it.eta),"otw"]:["Pre-orders full","out"];
  if(q<=0)return["Sold out","out"];if(q===1)return["Last one","low"];if(q<=3)return["Only "+q+" left","low"];return[q+" in stock",""];
}
function defaultSku(g){return g.skus.slice().sort((a,b)=>BY[b].qty-BY[a].qty)[0]}

/* ---------- product renders (SVG) or real photos ---------- */
let uid=0;
function cyl(id,c,k=1){k*=.55;return `<linearGradient id="${id}" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="${mix(c,-.30*k)}"/><stop offset=".14" stop-color="${mix(c,-.06*k)}"/><stop offset=".34" stop-color="${mix(c,.32*k)}"/><stop offset=".52" stop-color="${c}"/><stop offset=".86" stop-color="${mix(c,-.12*k)}"/><stop offset="1" stop-color="${mix(c,-.34*k)}"/></linearGradient>`}
function labelBlock(x,y,w,h,id,acc,txt,sub){
  const cx=x+w/2;
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5" fill="url(#${id}l)"/><rect x="${x}" y="${y+10}" width="${w}" height="5" fill="${acc}" opacity=".85"/>`+
  `<circle cx="${cx}" cy="${y+h*0.42}" r="${Math.min(w,h)*0.13}" fill="none" stroke="${acc}" stroke-width="2.5"/><circle cx="${cx}" cy="${y+h*0.42}" r="${Math.min(w,h)*0.05}" fill="${acc}"/>`+
  (sub?`<text x="${cx}" y="${y+h-30}" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="8.5" font-weight="600" letter-spacing="1.2" fill="${acc}">${sub}</text>`:"")+
  `<rect x="${cx-w*0.3}" y="${y+h-24}" width="${w*0.6}" height="1.5" fill="${acc}" opacity=".5"/><text x="${cx}" y="${y+h-9}" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="${w<70?9.5:11}" font-weight="600" fill="${acc}">${txt}</text>`}
function hl(x,y,h,w=7,o=.38){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${w/2}" fill="#fff" opacity="${o}"/>`}
const SH={
 pump(id,c,t,big,sub){const top=big?112:132,hf=big?58:52,L=150-hf,R=150+hf;
  return `<path d="M${L} ${top+24}Q${L} ${top} ${L+24} ${top}L${R-24} ${top}Q${R} ${top} ${R} ${top+24}L${R} 304Q${R} 318 ${R-14} 318L${L+14} 318Q${L} 318 ${L} 304Z" fill="url(#${id}b)"/><rect x="128" y="${top-22}" width="44" height="26" rx="4" fill="url(#${id}c)"/><rect x="145" y="${top-46}" width="10" height="26" fill="${mix(c[1],-.15)}"/><rect x="124" y="${top-62}" width="44" height="18" rx="6" fill="url(#${id}c)"/><rect x="88" y="${top-58}" width="42" height="9" rx="4.5" fill="${mix(c[1],-.08)}"/>`+
  labelBlock(L+10,top+52,2*hf-20,318-top-92,id,c[3],t,sub)+hl(L+11,top+16,318-top-34)},
 flip(id,c,t){return `<path d="M112 318L188 318Q202 318 202 304L202 134Q202 98 170 94L130 94Q98 98 98 134L98 304Q98 318 112 318Z" fill="url(#${id}b)"/><rect x="114" y="54" width="72" height="44" rx="10" fill="url(#${id}c)"/><rect x="114" y="68" width="72" height="2" fill="${mix(c[1],-.25)}"/>`+labelBlock(108,158,84,124,id,c[3],t)+hl(108,112,190)},
 jar(id,c,t){return `<rect x="74" y="226" width="152" height="92" rx="16" fill="url(#${id}b)"/><rect x="64" y="182" width="172" height="48" rx="12" fill="url(#${id}c)"/>`+[196,206,216].map(y=>`<rect x="66" y="${y}" width="168" height="1.5" fill="${mix(c[1],-.18)}" opacity=".6"/>`).join("")+
  `<rect x="74" y="244" width="152" height="56" fill="url(#${id}l)"/><rect x="74" y="250" width="152" height="4" fill="${c[3]}" opacity=".85"/><text x="150" y="286" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="12" font-weight="600" fill="${c[3]}">${t}</text>`+hl(84,236,74,7,.35)},
 tube(id,c,t){return `<path d="M94 74L206 74Q198 200 180 282L120 282Q102 200 94 74Z" fill="url(#${id}b)"/><rect x="90" y="52" width="120" height="24" rx="3" fill="${mix(c[0],-.08)}"/>`+[58,64,70].map(y=>`<rect x="92" y="${y}" width="116" height="1.2" fill="${mix(c[0],-.25)}"/>`).join("")+`<rect x="114" y="278" width="72" height="40" rx="7" fill="url(#${id}c)"/>`+labelBlock(116,112,68,112,id,c[3],t)+hl(110,86,160)},
 oil(id,c,t){return `<path d="M120 150Q120 128 138 124L162 124Q180 128 180 150L180 304Q180 318 166 318L134 318Q120 318 120 304Z" fill="url(#${id}b)" opacity=".95"/><rect x="138" y="100" width="24" height="28" fill="${mix(c[1],-.1)}"/><rect x="130" y="58" width="40" height="46" rx="9" fill="url(#${id}c)"/>`+labelBlock(126,178,48,108,id,c[3],t)+hl(126,146,160,5)},
 aerosol(id,c,t){return `<rect x="108" y="108" width="84" height="210" rx="10" fill="url(#${id}b)"/><ellipse cx="150" cy="110" rx="42" ry="12" fill="${mix(c[0],-.2)}"/><rect x="114" y="52" width="72" height="60" rx="12" fill="url(#${id}c)" opacity=".92"/>`+labelBlock(108,164,84,118,id,c[3],t)+`<rect x="108" y="306" width="84" height="12" rx="4" fill="${mix(c[0],-.25)}"/>`+hl(118,120,184,6)},
 stick(id,c,t){return `<rect x="104" y="146" width="92" height="172" rx="26" fill="url(#${id}b)"/><rect x="104" y="92" width="92" height="66" rx="26" fill="url(#${id}c)"/><rect x="104" y="150" width="92" height="3" fill="${mix(c[1],-.25)}"/>`+labelBlock(114,178,72,106,id,c[3],t)+hl(114,104,200,6)},
 mist(id,c,t){return `<rect x="114" y="102" width="72" height="216" rx="12" fill="url(#${id}b)" opacity=".92"/><rect x="124" y="48" width="52" height="58" rx="16" fill="url(#${id}c)"/>`+labelBlock(120,166,60,116,id,c[3],t)+hl(122,112,196,6)},
 spray(id,c,t){return `<rect x="106" y="124" width="88" height="194" rx="18" fill="url(#${id}b)"/><rect x="136" y="104" width="28" height="24" fill="${mix(c[1],-.1)}"/><rect x="128" y="64" width="44" height="44" rx="10" fill="url(#${id}c)"/><rect x="164" y="76" width="14" height="7" rx="3" fill="${mix(c[1],-.2)}"/>`+labelBlock(114,168,72,116,id,c[3],t)+hl(114,136,168,6)}
};
function render(x,bare){
  const it=typeof x==="string"?BY[x]:x;if(!it)return"";
  const c=it.c,id="r"+(uid++);
  const ml=esc(it.ml.replace("2 × ","").replace(" fl oz","")).slice(0,14);
  const small=/^\d+ mL$/.test(it.ml)&&parseInt(it.ml)<350&&it.shape==="flip";
  let body;
  if(it.shape==="duo"){
    const bottle=(cx,sub,s)=>`<g transform="translate(${cx} 318) scale(.74) translate(-150 -318)">${SH.pump(id+s,s==="a"?c:[mix(c[0],.25),c[1],c[2],c[3]],ml,true,sub)}</g>`;
    body=bottle(104,"SHAMPOO","a")+bottle(198,"CONDITIONER","b");
  }else{
    const inner=SH[it.shape==="pumpL"?"pump":it.shape](id,c,ml,it.shape==="pumpL");
    body=small?`<g transform="translate(150 318) scale(.86) translate(-150 -318)">${inner}</g>`:inner;
  }
  const defs=["","a","b"].map(s=>{const b0=s==="b"?mix(c[0],.25):c[0];return cyl(id+s+"b",b0)+cyl(id+s+"c",c[1],.9)+cyl(id+s+"l",c[2],.35)}).join("");
  if(bare)return `<svg viewBox="${({pumpL:"84 46 128 274",pump:"84 66 122 254",flip:"94 50 112 270",mist:"110 44 80 276",tube:"86 48 128 272",stick:"100 88 100 232",aerosol:"104 48 92 272",spray:"102 60 96 260",oil:"116 54 68 266",jar:"60 178 180 142",duo:"20 40 260 280"})[it.shape]}" aria-hidden="true"><defs>${defs}</defs>${body}</svg>`;
  return `<svg viewBox="0 0 300 360" role="img" aria-label="${esc(it.brand+" "+it.product+" — "+it.variant+", "+it.size)} (illustration)"><defs>${defs}<radialGradient id="${id}s"><stop offset="0" stop-color="#000" stop-opacity=".28"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>`+
  `<rect width="300" height="360" fill="${c[4]}"/><circle cx="190" cy="150" r="118" fill="${mix(c[4],.5)}"/><rect y="318" width="300" height="42" fill="${mix(c[4],-.04)}"/><ellipse cx="150" cy="320" rx="${it.shape==="duo"?118:it.shape==="jar"?96:72}" ry="10" fill="url(#${id}s)"/>${body}</svg>`;
}
function visual(x,src){
  const it=typeof x==="string"?BY[x]:x;if(!it)return"";
  const url=src||it.photo;
  return url?`<img class="ph" src="${esc(url)}" alt="${esc(it.brand+" "+it.product+" — "+it.variant)}" loading="lazy" style="background:${it.c[4]}">`:render(it);
}

/* ---------- state ---------- */
let bag=[];try{bag=JSON.parse(localStorage.getItem("halisi-bag")||"[]")}catch(e){bag=[]}
const saveBag=()=>{try{localStorage.setItem("halisi-bag",JSON.stringify(bag))}catch(e){}};
let filt={cat:"All",brand:"All",q:"",sort:"feat"};
let cur=null,curSku=null,qty=1,toastT,view="home";
let isAdmin=false,dbLive=false,ORDERS=[],adminKey="";
try{adminKey=sessionStorage.getItem("halisi-admin")||""}catch(e){}
const API=location.protocol.startsWith("http");
async function api(path,opts={}){
  const h={"Content-Type":"application/json"};if(adminKey)h["x-admin-key"]=adminKey;
  const r=await fetch(path,{method:opts.body?"POST":"GET",headers:h,body:opts.body?JSON.stringify(opts.body):undefined,cache:"no-store"});
  let j={};try{j=await r.json()}catch(e){}
  if(!r.ok){const err=new Error(j.error||"Something went wrong — try again.");err.status=r.status;throw err}
  return j;
}
function setProducts(list){ITEMS=list.map(norm);afterData()}

/* ---------- home ---------- */
function facts(){
  const live=ITEMS.filter(i=>i.status==="in_stock");
  const units=live.reduce((a,i)=>a+i.qty,0),brands=new Set(live.map(i=>i.brand)).size;
  $("#facts").textContent=`${live.length} products · ${brands} US brands · ${units} units in Kenya right now`;
  let picks=["EOS-LOT-VC-473","BBW-FFM-OS-236","FEN-DC-RICH-340","DOV-ST-RP-74"].filter(s=>BY[s]&&BY[s].status==="in_stock");
  if(picks.length<4)picks=[...new Set([...picks,...live.slice().sort((a,b)=>b.qty-a.qty).map(i=>i.sku)])].slice(0,4);
  $("#manifestRow").innerHTML=picks.map(s=>{const i=BY[s],g=GBY[i.brand+"|"+i.product];return `<button data-product="${g.id}" data-sku="${esc(s)}" aria-label="${esc(i.brand+" "+i.product+" — "+i.variant)}">${render(i,true)}</button>`}).join("");
}
function card(g){
  const s=defaultSku(g),it=BY[s],q=stockOf(g),[st,cls]=stockInfo(q,it),n=g.skus.length;
  const dots=n>1?`<div class="dots">${g.skus.slice(0,7).map(k=>`<i style="background:${BY[k].c[0]}"></i>`).join("")}<em>${n} ${g.cat==="Hair"?"types":"scents"}</em></div>`:`<div class="dots"><em>${esc(it.variant)}</em></div>`;
  return `<button class="card" data-product="${g.id}"><div class="r">${visual(s)}<span class="badge ${cls}">${esc(st)}</span></div><div><div class="card-brand">${esc(g.brand)}</div><div class="card-name">${esc(g.product)}</div></div>${dots}<div class="card-meta"><b>${groupPrice(g)}</b><span class="muted">${esc(it.ml)}</span></div></button>`;
}
function renderCats(){
  const gs=inStockGroups(),cnt=c=>c==="All"?gs.length:gs.filter(g=>g.cat===c).length;
  $("#cats").innerHTML=["All",...CATS].map(c=>`<button data-cat="${c}" aria-pressed="${filt.cat===c}">${c}<span>${cnt(c)}</span></button>`).join("");
}
function matchQ(g,q){return !q||g.skus.some(s=>{const i=BY[s];return(i.brand+" "+i.product+" "+i.variant+" "+i.cat+" "+i.notes).toLowerCase().includes(q)})}
function renderGrid(){
  const q=filt.q.trim().toLowerCase();
  let gs=inStockGroups().filter(g=>(filt.cat==="All"||g.cat===filt.cat)&&(filt.brand==="All"||g.brand===filt.brand)&&matchQ(g,q));
  const fi=g=>{const k=FEATURED.indexOf(g.bp);return k<0?99:k};
  if(filt.sort==="feat")gs.sort((a,b)=>fi(a)-fi(b));
  if(filt.sort==="az")gs.sort((a,b)=>(a.brand+a.product).localeCompare(b.brand+b.product));
  if(filt.sort==="stock")gs.sort((a,b)=>stockOf(b)-stockOf(a));
  if(filt.sort==="low")gs.sort((a,b)=>stockOf(a)-stockOf(b));
  $("#grid").innerHTML=gs.length?gs.map(card).join(""):`<p class="empty" style="grid-column:1/-1">Nothing matches that yet. <button class="link" id="clearF">Clear filters</button> or request it below.</p>`;
  $("#resCount").textContent=gs.length+(gs.length===1?" product":" products");
}
function renderComing(){
  const gs=GROUPS.filter(g=>g.otw).sort((a,b)=>(groupEta(a)||"9").localeCompare(groupEta(b)||"9"));
  $("#coming").hidden=!gs.length;
  $("#comingGrid").innerHTML=gs.map(card).join("");
  const first=gs.length?groupEta(gs[0]):null;
  $("#comingLead").textContent=first?`Next box lands around ${dLong(first)}. Shipping from the US takes about 3 months — pre-order now and it’s yours as soon as it arrives.`:"";
}
function renderBrands(){
  const live=ITEMS.filter(i=>i.status==="in_stock"),bs=[...new Set(live.map(i=>i.brand))].sort((a,b)=>live.filter(i=>i.brand===b).length-live.filter(i=>i.brand===a).length);
  const sel=$("#brandSel").value||"All";
  $("#brandSel").innerHTML=`<option value="All">All brands</option>`+bs.map(b=>`<option>${esc(b)}</option>`).join("");
  $("#brandSel").value=bs.includes(sel)?sel:"All";
  $("#brandsEyebrow").textContent=bs.length+" US brands";
  $("#brandGrid").innerHTML=bs.map(b=>{const its=live.filter(i=>i.brand===b),u=its.reduce((a,i)=>a+i.qty,0);return `<button data-brand="${esc(b)}"><b>${esc(b)}</b><span>${its.length} product${its.length>1?"s":""} · ${u} in stock</span></button>`}).join("");
}
function renderZones(){
  $("#zonesBody").innerHTML=ZONES.map(z=>`<tr><td>${esc(z.name)}</td><td>${esc(z.how)}</td><td>${esc(z.when)}</td><td><b>${z.fee==null?"KSh [FEE]":fmt(z.fee)}</b></td></tr>`).join("");
  $("#coZone").innerHTML=`<option value="">Choose your area</option>`+ZONES.map(z=>`<option value="${z.id}">${esc(z.name)} — ${z.fee==null?"KSh [FEE]":fmt(z.fee)}</option>`).join("");
}
function renderHome(){facts();renderCats();renderBrands();renderGrid();renderComing()}

/* ---------- views ---------- */
function show(v,anchor){
  view=v;
  document.querySelectorAll("[data-view]").forEach(el=>el.hidden=el.dataset.view!==v);
  closeBag();
  if(v==="admin")renderAdmin();
  if(anchor){requestAnimationFrame(()=>{const el=document.getElementById(anchor);if(el)el.scrollIntoView({behavior:"smooth",block:"start"})});return}
  window.scrollTo({top:0});
}
function openProduct(gid,sku){
  const g=GID[gid];if(!g)return;
  cur=g;curSku=sku&&g.skus.includes(sku)?sku:defaultSku(g);qty=1;
  fillPdpFrame();renderPdp();show("product");
}
function fillPdpFrame(){
  $("#crumbCat").textContent=cur.otw?"Arriving soon":cur.cat;$("#crumbCat").dataset.anchor=cur.otw?"coming":"shop";
  $("#crumbName").textContent=cur.product;$("#pdpBrand").textContent=cur.brand;$("#pdpName").textContent=cur.product;
  $("#variantWrap").hidden=cur.skus.length<2;
  const others=GROUPS.filter(g=>g!==cur&&!g.otw&&(g.brand===cur.brand||g.cat===cur.cat)).sort((a,b)=>(b.brand===cur.brand)-(a.brand===cur.brand)).slice(0,4);
  $("#moreTitle").textContent="You might also like";$("#moreGrid").innerHTML=others.map(card).join("");
}
function inBag(sku){const l=bag.find(x=>x.sku===sku);return l?l.qty:0}
function renderPdp(){
  const it=BY[curSku],otw=it.status==="on_the_way",left=it.qty-inBag(curSku),[st,cls]=stockInfo(it.qty,it);
  $("#pdpImg").innerHTML=visual(curSku);
  $("#pdpPrice").textContent=priceText(curSku);
  const s=$("#pdpStock");s.textContent=otw?"On the way · arrives ~"+dLong(it.eta):st;s.className="stock "+cls;
  $("#pdpPre").hidden=!otw;
  $("#pdpPre").innerHTML=otw?`<b>Pre-order.</b> This is on its way from the US and should land around <b>${dLong(it.eta)}</b>. Order now and we deliver it as soon as it arrives. [PRE-ORDER PAYMENT RULE — e.g. full payment or 50% deposit by M-Pesa]`:"";
  $("#variantName").textContent=it.variant;
  $("#variants").innerHTML=cur.skus.map(k=>{const v=BY[k];return `<button class="variant${v.qty<=0?" sold":""}" data-sku="${esc(k)}" aria-pressed="${k===curSku}"><i style="background:${v.c[0]}"></i>${esc(v.variant)}</button>`}).join("");
  qty=Math.max(1,Math.min(qty,Math.max(left,1)));
  $("#qOut").textContent=qty;$("#qMinus").disabled=qty<=1;$("#qPlus").disabled=qty>=left;
  const b=$("#addBtn");b.disabled=it.qty>0&&left<=0;
  b.textContent=it.qty<=0?(otw?"Pre-orders full — request more":"Sold out — request it"):left<=0?"All in your bag":otw?"Pre-order":"Add to bag";
  const rows=[["Size",it.size],["Scent / type",it.variant],["Condition",it.cond+", sealed"],["Category",it.cat]];
  if(otw)rows.push(["Arrives","About "+dLong(it.eta)]);
  if(it.notes)rows.push(["About",it.notes]);
  rows.push(["SKU",it.sku]);
  $("#specs").innerHTML=rows.map(([k,v])=>`<dt>${k}</dt><dd>${esc(v)}</dd>`).join("");
  $("#photoNote").textContent=it.photo?"This is a photo of the actual item we have in stock.":"This is an illustration of the pack shape and scent colour. [REPLACE WITH A REAL PHOTO — add one in Manage shop.]";
}

/* ---------- bag ---------- */
function totals(zoneId){
  const sub=bag.length&&bag.every(l=>priceOf(l.sku)!=null)?bag.reduce((a,l)=>a+priceOf(l.sku)*l.qty,0):bag.length?null:0;
  const z=ZONES.find(z=>z.id===zoneId),fee=z?z.fee:undefined;
  return{sub,fee,z,total:sub!=null&&typeof fee==="number"?sub+fee:null};
}
const count=()=>bag.reduce((a,l)=>a+l.qty,0);
function lineItem(l,editable){
  const i=BY[l.sku],pre=i.status==="on_the_way";
  return `<div class="line-item"><div class="r">${visual(l.sku)}</div><div><b>${esc(i.brand)} ${esc(i.product)}</b><small>${esc(i.variant)} · ${esc(i.ml)}</small>${pre?`<small style="color:var(--transit);font-weight:600">Pre-order · arrives ~${dShort(i.eta)}</small>`:""}${editable?`<div class="qty"><button data-dec="${esc(l.sku)}" aria-label="Fewer" ${l.qty<=1?"disabled":""}>−</button><output>${l.qty}</output><button data-inc="${esc(l.sku)}" aria-label="More" ${l.qty>=i.qty?"disabled":""}>+</button></div>`:`<small>Qty ${l.qty}</small>`}</div><div class="price">${priceOf(l.sku)==null?"[PRICE]":fmt(priceOf(l.sku)*l.qty)}${editable?`<button data-remove="${esc(l.sku)}">Remove</button>`:""}</div></div>`;
}
function cleanBag(){bag=bag.filter(l=>BY[l.sku]&&BY[l.sku].status!=="hidden"&&BY[l.sku].qty>0).map(l=>({sku:l.sku,qty:Math.min(l.qty,BY[l.sku].qty)}))}
function renderBag(){
  cleanBag();
  $("#bagCount").textContent=count();
  $("#bagList").innerHTML=bag.length?bag.map(l=>lineItem(l,true)).join(""):`<p class="empty">Your bag is empty.<br><button class="link" data-go="home" data-anchor="shop">Start shopping</button></p>`;
  const t=totals();
  $("#bagTotals").innerHTML=`<div><span>Subtotal · ${count()} item${count()===1?"":"s"}</span><b>${t.sub==null?"KSh [SUBTOTAL]":fmt(t.sub)}</b></div><div class="muted"><span>Delivery</span><span>Added at checkout</span></div>`;
  $("#toCheckout").disabled=!bag.length;
  saveBag();
}
function openBag(){$("#drawer").hidden=false;$("#scrim").hidden=false;$("#closeBag").focus()}
function closeBag(){$("#drawer").hidden=true;$("#scrim").hidden=true}
function add(sku,n){const l=bag.find(x=>x.sku===sku),max=BY[sku].qty;if(l)l.qty=Math.min(max,l.qty+n);else bag.push({sku,qty:Math.min(max,n)});renderBag()}

/* ---------- checkout ---------- */
function renderCheckout(){
  const zone=$("#coZone").value,t=totals(zone);
  $("#coItems").innerHTML=bag.map(l=>lineItem(l,false)).join("");
  const feeTxt=!t.z?"Choose your area":t.fee==null?"KSh [FEE]":fmt(t.fee);
  const totTxt=t.total!=null?fmt(t.total):"KSh [TOTAL]";
  $("#coTotals").innerHTML=`<div><span>Subtotal</span><span>${t.sub==null?"KSh [SUBTOTAL]":fmt(t.sub)}</span></div><div><span>Delivery</span><span>${feeTxt}</span></div><div class="grand"><span>Total</span><span>${totTxt}</span></div>`;
  const pre=bag.filter(l=>BY[l.sku].status==="on_the_way");
  $("#coPre").hidden=!pre.length;
  if(pre.length){const last=pre.map(l=>BY[l.sku].eta).filter(Boolean).sort().pop();$("#coPre").innerHTML=`<b>${pre.length} pre-order item${pre.length>1?"s":""}</b> in this order. They’re still on the way from the US and arrive around ${dLong(last)}. We deliver everything together then, unless you ask us to split it. [PRE-ORDER PAYMENT RULE]`}
  $("#tillAmt").textContent=totTxt;
  const pay=document.querySelector("input[name=pay]:checked").value;
  $("#tillBox").hidden=pay!=="till";
  $("#payBtn").textContent=pay==="stk"?"Pay "+totTxt+" with M-Pesa":pay==="till"?"Confirm payment & place order":"Place order · pay on delivery";
  $("#locHint").textContent=zone==="ctry"?"· or your nearest courier office":"";
  return t;
}
function normPhone(v){const d=String(v).replace(/[\s-]/g,"");const m=d.match(/^(?:\+?254|0)([17]\d{8})$/);return m?"0"+m[1]:null}
function setErr(id,msg){const f=$("#"+id);if(!f)return;const e=f.querySelector(".err");f.classList.toggle("bad",!!msg);if(e){e.hidden=!msg;e.textContent=msg||""}}
function validate(){
  let ok=true;const chk=(id,msg)=>{setErr(id,msg);if(msg&&ok){ok=false;const i=$("#"+id+" input,#"+id+" select");i&&i.focus()}};
  chk("f-name",$("#coName").value.trim()?"":"Enter the name we should deliver to.");
  chk("f-phone",normPhone($("#coPhone").value)?"":"Enter a Safaricom number like 0712 345 678.");
  chk("f-zone",$("#coZone").value?"":"Choose your delivery area.");
  chk("f-loc",$("#coLoc").value.trim()?"":"Tell us where to deliver — estate, street or building.");
  const pay=document.querySelector("input[name=pay]:checked").value;
  if(pay==="pod"&&$("#coZone").value==="ctry")chk("f-zone","Pay on delivery is Nairobi only. Choose M-Pesa prompt or Till.");
  if(pay==="till")chk("f-code",/^[A-Z0-9]{10}$/i.test($("#coCode").value.trim())?"":"Enter the 10-character code from your M-Pesa SMS.");else setErr("f-code","");
  return ok;
}
function sheet(html){$("#sheet").innerHTML=html;$("#modal").hidden=false;const b=$("#sheet button");b&&b.focus()}
function closeSheet(){$("#modal").hidden=true}
let stkTimer;
function startStk(){
  const ph=normPhone($("#coPhone").value),t=renderCheckout(),amt=t.total!=null?fmt(t.total):"KSh [TOTAL]";
  sheet(`<div class="spinner" aria-hidden="true"></div><h2 id="sheetTitle">Sending M-Pesa prompt…</h2><p>To ${ph}</p><p class="tiny">Prototype — no real prompt is sent.</p>`);
  clearTimeout(stkTimer);
  stkTimer=setTimeout(()=>sheet(`<div class="phone" aria-hidden="true"><span class="pin">PIN ••••</span></div><h2 id="sheetTitle">Check your phone</h2><p>Enter your M-Pesa PIN to pay <b style="color:var(--ink)">${amt}</b> to <b style="color:var(--ink)">[M-PESA BUSINESS NAME]</b>.</p><div class="btns"><button class="btn btn-accent" data-sheet="paid">I’ve entered my PIN</button><button class="btn btn-line" data-sheet="till">No prompt? Pay to Till instead</button><button class="link" data-sheet="cancel" style="padding:8px">Cancel</button></div><p class="tiny">Prototype — tap “I’ve entered my PIN” to simulate a successful payment.</p>`),1300);
}
async function placeOrder(method){
  const t=renderCheckout(),ph=normPhone($("#coPhone").value),z=t.z,code=$("#coCode").value.trim().toUpperCase();
  const no="HB-"+today().slice(2).replace(/-/g,"")+"-"+String(Math.floor(1000+Math.random()*9000));
  const lines=bag.map(l=>{const i=BY[l.sku];return{sku:l.sku,qty:l.qty,price:priceOf(l.sku),label:`${i.brand} ${i.product} — ${i.variant} (${i.ml})`,preorder:i.status==="on_the_way"}});
  const order={no,createdAt:new Date().toISOString(),name:$("#coName").value.trim(),phone:ph,zone:z?z.name:"",loc:$("#coLoc").value.trim(),landmark:$("#coLandmark").value.trim(),when:$("#coWhen").value,notes:$("#coNotes").value.trim(),pay:method,code:method==="till"?code:"",items:lines,subtotal:t.sub,fee:typeof t.fee==="number"?t.fee:null,total:t.total,status:"new",stockTaken:false};
  let saved=false,no2=no;
  if(API){
    try{const r=await api("/api/orders",{body:{name:order.name,phone:ph,zoneId:z?z.id:"",loc:order.loc,landmark:order.landmark,when:order.when,notes:order.notes,pay:method,code:order.code,items:bag.map(l=>({sku:l.sku,qty:l.qty}))}});no2=r.order.no;saved=true}
    catch(e){closeSheet();toast(e.message);return}
  }
  const items=bag.map(l=>lineItem(l,false)).join("");
  const payTxt=method==="stk"?"Paid by M-Pesa prompt":method==="till"?"Paid to Till · code "+esc(code):"M-Pesa on delivery";
  $("#doneBody").innerHTML=`<div class="tick"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg></div>
   <div><div class="eyebrow">Order ${no2}</div><h1>Asante, ${esc(order.name.split(" ")[0])}! Your order is in.</h1></div>
   <p class="muted" style="font-size:17px">We’ll WhatsApp you on <b style="color:var(--ink)">${ph}</b> to confirm your delivery time${z?` (${esc(z.when)})`:""}.${method==="till"?" We’ll check your M-Pesa code first.":""}${lines.some(l=>l.preorder)?" Pre-order items come as soon as the shipment lands.":""}</p>
   <div class="receipt"><div class="kv"><span>Payment</span><b>${payTxt}</b></div><div class="kv"><span>Deliver to</span><span>${esc(order.loc)}${z?", "+esc(z.name.split(" — ")[0]):""}</span></div><div class="kv"><span>Best time</span><span>${esc(order.when)}</span></div>
   <div style="display:flex;flex-direction:column;gap:12px;border-top:1px dashed var(--line);padding-top:12px">${items}</div><div class="totals" style="border-top:1px dashed var(--line)"><div class="grand"><span>Total</span><span>${t.total!=null?fmt(t.total):"KSh [TOTAL]"}</span></div></div></div>
   <p class="tiny muted" style="font-size:13px">Prototype — no money moved.${saved?"":" (Offline preview — order not sent.)"}</p>
   <div class="ctas"><button class="btn btn-ink" data-go="home" data-anchor="shop">Keep shopping</button></div>`;
  bag=[];renderBag();closeSheet();show("done");
}

/* ---------- admin ---------- */
let editing=null,etaTouched=false,pFile=null,pFileUrl=null,adminTab="products";
const dirty=new Set();
function renderAdmin(){
  if(view!=="admin")return;
  $("#admMode").textContent=!API?"Offline preview — open the live site to save changes.":dbLive?"Changes save straight to the live shop. Customers see them on their next visit.":"Storage isn’t connected yet — add a Blob store in Vercel before saving.";
  const live=ITEMS.filter(i=>i.status==="in_stock"),otw=ITEMS.filter(i=>i.status==="on_the_way"),noPrice=ITEMS.filter(i=>i.status!=="hidden"&&i.price==null).length,newO=ORDERS.filter(o=>o.status==="new").length;
  $("#admStats").innerHTML=`<div class="stat"><b>${live.reduce((a,i)=>a+i.qty,0)}</b><span>units in stock · ${live.length} products</span></div><div class="stat"><b>${otw.reduce((a,i)=>a+i.qty,0)}</b><span>units on the way · ${otw.length} products</span></div><div class="stat ${noPrice?"warn":""}"><b>${noPrice}</b><span>products without a price</span></div><div class="stat"><b>${newO}</b><span>new orders</span></div>`;
  $("#nOtw").textContent=otw.length||"";$("#nOrders").textContent=newO||"";
  document.querySelectorAll("[data-tab]").forEach(b=>b.setAttribute("aria-selected",b.dataset.tab===adminTab));
  document.querySelectorAll("[data-tabpanel]").forEach(p=>p.hidden=p.dataset.tabpanel!==adminTab);
  renderAdminList();renderShipments();renderOrders();
  $("#brandList").innerHTML=[...new Set(ITEMS.map(i=>i.brand))].map(b=>`<option value="${esc(b)}">`).join("");
}
function statusOpts(v){return[["in_stock","In stock"],["on_the_way","On the way"],["hidden","Hidden"]].map(([k,l])=>`<option value="${k}" ${k===v?"selected":""}>${l}</option>`).join("")}
function renderAdminList(){
  const keep={};dirty.forEach(s=>{const r=document.querySelector(`[data-row="${CSS.escape(s)}"]`);if(r)keep[s]={status:r.querySelector("[data-f=status]").value,qty:r.querySelector("[data-f=qty]").value,price:r.querySelector("[data-f=price]").value}});
  const q=$("#aq").value.trim().toLowerCase(),sf=$("#aStatus").value,pf=$("#aPrice").value;
  const rows=ITEMS.filter(i=>(sf==="all"||i.status===sf)&&(pf==="all"||i.price==null)&&(!q||(i.brand+" "+i.product+" "+i.variant+" "+i.sku).toLowerCase().includes(q)))
    .sort((a,b)=>(a.status==="hidden")-(b.status==="hidden")||(a.brand+a.product+a.variant).localeCompare(b.brand+b.product+b.variant));
  $("#aList").innerHTML=rows.length?rows.map(i=>{const k=keep[i.sku],id=slug(i.sku);return `<div class="arow${i.status==="hidden"?" hid":""}${k?" dirty":""}" data-row="${esc(i.sku)}">
    <div class="thumb r">${visual(i)}</div>
    <div class="ainfo"><b>${esc(i.brand)} ${esc(i.product)}</b><small>${esc(i.variant)} · ${esc(i.size)}${i.status==="on_the_way"?` · <span style="color:var(--transit)">arrives ~${dShort(i.eta)}</span>`:""}</small><span class="mono muted">${esc(i.sku)}</span></div>
    <div class="aedit"><label class="afield"><span>Status</span><select id="a-${id}-st" data-f="status">${statusOpts(k?k.status:i.status)}</select></label><label class="afield"><span>Qty</span><input id="a-${id}-q" data-f="qty" type="number" min="0" step="1" inputmode="numeric" value="${esc(k?k.qty:i.qty)}"></label><label class="afield"><span>Price (KSh)</span><input id="a-${id}-p" data-f="price" type="number" min="0" step="10" inputmode="numeric" placeholder="Not set" value="${esc(k?k.price:(i.price??""))}"></label></div>
    <div class="aact"><button class="btn-sm" data-save="${esc(i.sku)}" ${k?"":"disabled"}>Save</button><button class="btn-sm line" data-edit="${esc(i.sku)}">Edit</button></div></div>`}).join(""):`<p class="empty">No products match.</p>`;
}
async function saveRow(sku){
  const r=document.querySelector(`[data-row="${CSS.escape(sku)}"]`),st=r.querySelector("[data-f=status]").value,qv=r.querySelector("[data-f=qty]").value,pv=r.querySelector("[data-f=price]").value;
  const q=Math.max(0,Math.floor(Number(qv)||0)),p=pv===""?null:Math.max(0,Math.round(Number(pv)));
  const btn=r.querySelector("[data-save]");btn.disabled=true;btn.textContent="Saving…";
  try{const res=await api("/api/admin/products",{body:{action:"patch",sku,patch:{status:st,qty:q,price:p&&p>0?p:null}}});dirty.delete(sku);setProducts(res.products);toast("Saved "+BY[sku].variant)}
  catch(e){btn.disabled=false;btn.textContent="Save";adminErr(e)}
}
function adminErr(e){if(e.status===401){logout();toast("Your session ended — enter the password again.")}else toast(e.message)}
/* product form */
function fillSelects(){
  $("#pCat").innerHTML=CATS.map(c=>`<option>${c}</option>`).join("");
  $("#pShape").innerHTML=SHAPES.map(([k,l])=>`<option value="${k}">${l}</option>`).join("");
}
function formItem(){
  const size=$("#pSize").value.trim(),st=document.querySelector("input[name=pStatus]:checked").value,base=editing?BY[editing]:null,color=$("#pColor").value;
  return norm({sku:editing||"NEW",brand:$("#pBrand").value.trim()||"Brand",product:$("#pProduct").value.trim()||"Product name",variant:$("#pVariant").value.trim()||"Scent",size:size||"Size",
    qty:$("#pQty").value,price:$("#pPrice").value?Number($("#pPrice").value):null,cat:$("#pCat").value,shape:$("#pShape").value,
    c:base&&base.c[0].toLowerCase()===color.toLowerCase()?base.c:palette(color),notes:$("#pNotes").value.trim(),status:st,eta:$("#pEta").value,shippedOn:$("#pShipped").value,
    photo:base&&!$("#pRmPhoto").checked?base.photo:null});
}
function renderPreview(){
  const it=formItem(),[st,cls]=stockInfo(it.qty,it);
  $("#otwFields").hidden=it.status!=="on_the_way";
  $("#pPreview").innerHTML=`<div class="r" style="border-radius:18px;overflow:hidden">${visual(it,pFileUrl)}<span class="badge ${cls}">${esc(st)}</span></div><div><div class="card-brand">${esc(it.brand)}</div><div class="card-name">${esc(it.product)}</div></div><div class="dots"><em>${esc(it.variant)}</em></div><div class="card-meta"><b>${it.price?fmt(it.price):"KSh [PRICE]"}</b><span class="muted">${esc(it.ml)}</span></div>`;
}
function resetForm(){
  editing=null;etaTouched=false;pFile=null;if(pFileUrl)URL.revokeObjectURL(pFileUrl);pFileUrl=null;
  $("#pForm").reset();$("#pQty").value=1;$("#pColor").value="#E9D3B4";$("#pShape").value="pumpL";
  $("#pShipped").value=today();$("#pEta").value=addDays(today(),TRANSIT_DAYS);
  $("#pFormTitle").textContent="Add a product";$("#pSave").textContent="Add to shop";$("#tabAddBtn").textContent="Add product";
  $("#pCancel").hidden=true;$("#pDelete").hidden=true;$("#rmPhotoWrap").hidden=true;
  ["f-pBrand","f-pProduct","f-pVariant","f-pSize","f-pQty","f-pEta"].forEach(i=>setErr(i,""));
  renderPreview();
}
function editProduct(sku){
  const i=BY[sku];if(!i)return;resetForm();editing=sku;
  $("#pBrand").value=i.brand;$("#pProduct").value=i.product;$("#pVariant").value=i.variant;$("#pSize").value=i.size;$("#pCat").value=i.cat;$("#pNotes").value=i.notes;
  $("#pQty").value=i.qty;$("#pPrice").value=i.price??"";$("#pShape").value=i.shape;$("#pColor").value=i.c[0];
  document.querySelector(`input[name=pStatus][value=${i.status==="hidden"?"in_stock":i.status}]`).checked=true;
  $("#pShipped").value=i.shippedOn||"";$("#pEta").value=i.eta||addDays(today(),TRANSIT_DAYS);etaTouched=!!i.eta;
  $("#pFormTitle").textContent="Edit product";$("#pSave").textContent="Save changes";$("#tabAddBtn").textContent="Edit product";
  $("#pCancel").hidden=false;$("#pDelete").hidden=false;$("#rmPhotoWrap").hidden=!i.photo;
  adminTab="add";renderAdmin();renderPreview();window.scrollTo({top:0});
}
function makeSku(b,p,v){
  const ini=s=>s.replace(/&/g," ").split(/[^A-Za-z0-9]+/).filter(Boolean).map(w=>w[0]).join("").toUpperCase().slice(0,4)||"X";
  const base=(b.replace(/[^A-Za-z0-9]/g,"").slice(0,3).toUpperCase()||"HB")+"-"+ini(p)+"-"+ini(v);
  let s=base,n=2;while(BY[s])s=base+"-"+(n++);return s;
}
function shrink(file){return new Promise((res,rej)=>{const img=new Image(),u=URL.createObjectURL(file);img.onload=()=>{const m=1400,k=Math.min(1,m/Math.max(img.width,img.height)),c=document.createElement("canvas");c.width=Math.round(img.width*k);c.height=Math.round(img.height*k);c.getContext("2d").drawImage(img,0,0,c.width,c.height);URL.revokeObjectURL(u);c.toBlob(b=>b?res(b):rej(new Error("encode")),"image/jpeg",.86)};img.onerror=()=>{URL.revokeObjectURL(u);rej(new Error("decode"))};img.src=u})}
async function saveProduct(){
  let ok=true;const need=(id,el,msg)=>{const bad=!$(el).value.trim();setErr(id,bad?msg:"");if(bad&&ok){ok=false;$(el).focus()}};
  need("f-pBrand","#pBrand","Enter the brand.");need("f-pProduct","#pProduct","Enter the product name.");need("f-pVariant","#pVariant","Enter the scent or type — or “Original”.");need("f-pSize","#pSize","Enter the size from the pack.");
  const q=Number($("#pQty").value);if(!(q>=0)){setErr("f-pQty","Enter how many you have (0 or more).");ok=false}else setErr("f-pQty","");
  const st=document.querySelector("input[name=pStatus]:checked").value;
  if(st==="on_the_way"&&!$("#pEta").value){setErr("f-pEta","Add the expected arrival date.");ok=false}else setErr("f-pEta","");
  if(!ok)return;
  if(!API){toast("Open the live site to save products.");return}
  const btn=$("#pSave"),label=btn.textContent;btn.disabled=true;btn.textContent="Saving…";
  try{
    const it=formItem(),base=editing?BY[editing]:null,sku=editing||makeSku(it.brand,it.product,it.variant);
    let photo=base&&!$("#pRmPhoto").checked?base.photo:null;
    if(pFile){
      let blob;try{blob=await shrink(pFile)}catch(e){toast("Couldn’t read that photo — try a JPG or PNG.");return}
      btn.textContent="Uploading photo…";
      const data=await new Promise((res,rej)=>{const fr=new FileReader();fr.onload=()=>res(String(fr.result).split(",")[1]);fr.onerror=rej;fr.readAsDataURL(blob)});
      photo=(await api("/api/admin/photo",{body:{type:"image/jpeg",data}})).url;
    }
    const doc={sku,brand:it.brand,product:it.product,variant:it.variant,size:it.size,ml:it.ml,qty:it.qty,price:it.price,cat:it.cat,shape:it.shape,c:it.c,notes:it.notes,
      status:base&&base.status==="hidden"&&st==="in_stock"?"hidden":st,
      eta:st==="on_the_way"?$("#pEta").value:(base?base.eta:null),shippedOn:st==="on_the_way"?($("#pShipped").value||null):(base?base.shippedOn:null),photo};
    const res=await api("/api/admin/products",{body:{action:"upsert",product:doc}});
    setProducts(res.products);
    toast(editing?"Saved changes":`Added ${doc.variant} to the shop`);
    resetForm();adminTab=st==="on_the_way"?"otw":"products";renderAdmin();window.scrollTo({top:0});
  }catch(e){adminErr(e)}
  finally{btn.disabled=false;if(btn.textContent.endsWith("…"))btn.textContent=label}
}
function askDelete(){
  const i=BY[editing];if(!i)return;
  sheet(`<h2 id="sheetTitle">Delete this product?</h2><p>${esc(i.brand)} ${esc(i.product)} — ${esc(i.variant)} will be removed for good${i.photo?", with its photo":""}. To just take it off the shop for now, set its status to Hidden instead.</p><div class="btns"><button class="btn btn-line" data-sheet="cancel">Keep it</button><button class="btn btn-accent" data-sheet="delete" style="background:var(--danger);color:#fff">Delete product</button></div>`);
}
async function doDelete(){
  const i=BY[editing];closeSheet();if(!i||!API)return;
  try{const res=await api("/api/admin/products",{body:{action:"delete",sku:i.sku}});setProducts(res.products);toast("Deleted");resetForm();adminTab="products";renderAdmin()}catch(e){adminErr(e)}
}
/* shipments */
function renderShipments(){
  const otw=ITEMS.filter(i=>i.status==="on_the_way"),by={};
  otw.forEach(i=>{(by[i.eta||"none"]=by[i.eta||"none"]||[]).push(i)});
  const keys=Object.keys(by).sort();
  $("#shipList").innerHTML=keys.length?keys.map(k=>{
    const its=by[k],shipped=its.map(i=>i.shippedOn).filter(Boolean).sort()[0],units=its.reduce((a,i)=>a+i.qty,0);
    const start=shipped?new Date(shipped+"T00:00"):null,end=k!=="none"?new Date(k+"T00:00"):null,now=new Date();
    const pct=start&&end&&end>start?Math.max(3,Math.min(100,(now-start)/(end-start)*100)):8,days=end?Math.ceil((end-now)/864e5):null;
    return `<div class="ship"><div class="ship-head"><div><div class="mono muted">Arriving around</div><h3>${k==="none"?"Date not set":dLong(k)}</h3></div><button class="btn-sm" data-arrived="${k}">Mark as arrived</button></div>
      <div class="bar" role="img" aria-label="${Math.round(pct)}% of the way"><i style="width:${pct}%"></i></div>
      <div class="mono muted">${shipped?"Shipped "+dLong(shipped)+" · ":""}${days==null?"":days>0?days+" days to go · ":"Due now · "}${units} units · ${its.length} products</div>
      <ul>${its.map(i=>`<li><span>${esc(i.brand)} ${esc(i.product)} — ${esc(i.variant)}</span><span><b>${i.qty}</b> · <button class="link" data-edit="${esc(i.sku)}">Edit</button></span></li>`).join("")}</ul></div>`}).join("")
    :`<div class="ship"><h3>Nothing on the way right now</h3><p class="muted">When you ship a box from the US, add each product with status <b>On the way</b> and the date it left. It shows to customers under “Arriving soon” so they can pre-order.</p><button class="btn-sm" data-tabgo="add" style="align-self:flex-start">Add a product on the way</button></div>`;
}
async function markArrived(k){
  if(!API){toast("Open the live site to save changes.");return}
  try{const res=await api("/api/admin/products",{body:{action:"arrive",eta:k}});setProducts(res.products);toast("Moved to In stock. Pre-orders are in the Orders tab.")}catch(e){adminErr(e)}
}
/* orders */
const ORDER_ST=[["new","New"],["confirmed","Confirmed"],["out","Out for delivery"],["delivered","Delivered"],["cancelled","Cancelled"]];
function renderOrders(){
  if(!API){$("#orderList").innerHTML=`<p class="empty">Orders appear here on the live site.</p>`;return}
  $("#orderList").innerHTML=ORDERS.length?ORDERS.map(o=>{o.id=o.no;const items=Array.isArray(o.items)?o.items:[];return `<div class="order">
    <div class="order-head"><b>${esc(o.no||o.id)}</b><span class="st ${esc(o.status)}">${esc((ORDER_ST.find(s=>s[0]===o.status)||["","New"])[1])}</span></div>
    <div class="kv"><span>Placed</span><span>${o.createdAt?new Date(o.createdAt).toLocaleString("en-GB",{day:"numeric",month:"short",hour:"2-digit",minute:"2-digit"}):""}</span><span>Customer</span><span>${esc(o.name)} · <a href="tel:${esc(o.phone)}">${esc(o.phone)}</a></span><span>Deliver to</span><span>${esc(o.loc)}${o.landmark?" ("+esc(o.landmark)+")":""} · ${esc(o.zone)}</span><span>When</span><span>${esc(o.when)}${o.notes?" · “"+esc(o.notes)+"”":""}</span><span>Payment</span><span>${o.pay==="stk"?"M-Pesa prompt":o.pay==="till"?"Till · code "+esc(o.code):"M-Pesa on delivery"} · ${typeof o.total==="number"?fmt(o.total):"total not set"}</span></div>
    <ul>${items.map(l=>`<li>${l.qty} × ${esc(l.label)}${l.preorder?' <span style="color:var(--transit);font-weight:600">· pre-order</span>':""}</li>`).join("")}</ul>
    <label class="afield" style="max-width:260px"><span>Order status</span><select data-order="${esc(o.id)}" id="o-${esc(o.id)}">${ORDER_ST.map(([k,l])=>`<option value="${k}" ${k===o.status?"selected":""}>${l}</option>`).join("")}</select></label></div>`}).join("")
    :`<p class="empty">No orders yet. They’ll show up here as soon as someone checks out.</p>`;
}
async function setOrderStatus(id,st){
  try{const r=await api("/api/admin/orders",{body:{no:id,status:st}});const i=ORDERS.findIndex(o=>o.no===id);if(i>=0)ORDERS[i]=r.order;if(r.products)setProducts(r.products);else renderAdmin();
    toast(st==="cancelled"&&r.products?"Cancelled — items back in stock":r.products?"Confirmed — stock updated":"Order updated")}
  catch(e){adminErr(e);renderAdmin()}
}
/* ---------- live data ---------- */
function afterData(){
  rebuild();cleanBag();renderHome();renderBag();
  if(view==="product"&&curSku){if(BY[curSku]&&BY[curSku].status!=="hidden"){const i=BY[curSku];cur=GBY[i.brand+"|"+i.product+(i.status==="on_the_way"?"|otw":"")];fillPdpFrame();renderPdp()}else show("home","shop")}
  if(view==="checkout")renderCheckout();
  renderAdmin();
}
async function loadProducts(){
  if(!API)return;
  try{const r=await api("/api/products");if(Array.isArray(r.zones)&&r.zones.length){ZONES=r.zones;renderZones()}dbLive=!!r.live;if(adminKey&&!r.admin){logout()}setProducts(r.products)}
  catch(e){console.warn("Using the built-in catalogue:",e.message)}
}
async function loadOrders(){
  if(!API||!isAdmin)return;
  try{ORDERS=(await api("/api/admin/orders")).orders;renderAdmin()}catch(e){if(e.status===401)logout();else console.warn(e.message)}
}
function setAdmin(on){
  isAdmin=on;document.querySelectorAll(".adm-link").forEach(b=>b.hidden=!on);
  $("#logoutBtn").hidden=!on;$("#ownerLogin").hidden=on;
}
function logout(){adminKey="";try{sessionStorage.removeItem("halisi-admin")}catch(e){}setAdmin(false);ORDERS=[];if(view==="admin")show("home")}
function askLogin(){
  if(!API){toast("Open the live site to manage the shop.");return}
  sheet(`<h2 id="sheetTitle">Shop owner login</h2><p>Enter the shop password to add products and see orders.</p><form id="loginForm" style="display:flex;flex-direction:column;gap:10px;width:100%" novalidate><div class="field" style="text-align:left"><label for="adminPw">Password</label><input id="adminPw" type="password" autocomplete="current-password"></div><p class="err" id="loginErr" hidden></p><div class="btns"><button class="btn btn-accent" type="submit">Log in</button><button class="link" type="button" data-sheet="cancel" style="padding:8px">Cancel</button></div></form>`);
  $("#adminPw").focus();
}
async function doLogin(pw){
  adminKey=pw;
  try{await api("/api/admin/login",{body:{}});try{sessionStorage.setItem("halisi-admin",pw)}catch(e){}closeSheet();setAdmin(true);await loadProducts();loadOrders();show("admin")}
  catch(e){adminKey="";const el=$("#loginErr");if(el){el.hidden=false;el.textContent=e.status===401?"That password isn’t right.":e.message}}
}
async function connect(){
  await loadProducts();
  if(adminKey){try{await api("/api/admin/login",{body:{}});setAdmin(true);await loadProducts();loadOrders()}catch(e){logout()}}
  if(location.hash==="#manage"&&!isAdmin)askLogin();
  setInterval(()=>{if(document.visibilityState!=="visible")return;if(isAdmin&&view==="admin")loadOrders();else if(view==="home")loadProducts()},60000);
}

/* ---------- events ---------- */
function toast(m){const t=$("#toast");t.textContent=m;t.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>t.hidden=true,3000)}
document.addEventListener("click",e=>{
  const t=e.target.closest("[data-go],[data-product],[data-toast],[data-cat],[data-brand],[data-sku],[data-inc],[data-dec],[data-remove],[data-sheet],[data-tab],[data-tabgo],[data-save],[data-edit],[data-arrived],#clearF");if(!t)return;
  if(t.id==="clearF"){filt={...filt,cat:"All",brand:"All",q:""};$("#q").value="";$("#brandSel").value="All";renderCats();renderGrid();return}
  if(t.dataset.product){openProduct(t.dataset.product,t.dataset.sku);return}
  if(t.dataset.sku&&t.classList.contains("variant")){curSku=t.dataset.sku;qty=1;renderPdp();return}
  if(t.dataset.go){show(t.dataset.go,t.dataset.anchor);return}
  if(t.dataset.toast){toast(t.dataset.toast);return}
  if(t.dataset.cat){filt.cat=t.dataset.cat;renderCats();renderGrid();return}
  if(t.dataset.brand){filt.brand=t.dataset.brand;filt.cat="All";$("#brandSel").value=filt.brand;renderCats();renderGrid();show("home","shop");return}
  if(t.dataset.inc){add(t.dataset.inc,1);return}
  if(t.dataset.dec){const l=bag.find(x=>x.sku===t.dataset.dec);if(l&&l.qty>1){l.qty--;renderBag()}return}
  if(t.dataset.remove){bag=bag.filter(x=>x.sku!==t.dataset.remove);renderBag();return}
  if(t.dataset.tab){adminTab=t.dataset.tab;if(adminTab==="orders")loadOrders();if(adminTab==="add"&&!editing)resetForm();renderAdmin();return}
  if(t.dataset.tabgo){adminTab=t.dataset.tabgo;resetForm();document.querySelector("input[name=pStatus][value=on_the_way]").checked=true;renderPreview();renderAdmin();return}
  if(t.dataset.save){saveRow(t.dataset.save);return}
  if(t.dataset.edit){editProduct(t.dataset.edit);return}
  if(t.dataset.arrived){markArrived(t.dataset.arrived);return}
  if(t.dataset.sheet){const a=t.dataset.sheet;
    if(a==="paid"){sheet(`<div class="spinner" aria-hidden="true"></div><h2 id="sheetTitle">Confirming payment…</h2>`);setTimeout(()=>placeOrder("stk"),1100)}
    if(a==="till"){closeSheet();document.querySelector("input[name=pay][value=till]").checked=true;renderCheckout();$("#coCode").focus()}
    if(a==="cancel"){clearTimeout(stkTimer);closeSheet();if(view==="checkout")toast("Payment cancelled. Your bag is still saved.")}
    if(a==="delete")doDelete();
  }
});
$("#q").addEventListener("input",e=>{filt.q=e.target.value;renderGrid()});
$("#brandSel").addEventListener("change",e=>{filt.brand=e.target.value;renderGrid()});
$("#sortSel").addEventListener("change",e=>{filt.sort=e.target.value;renderGrid()});
$("#searchJump").addEventListener("click",()=>{show("home","shop");setTimeout(()=>$("#q").focus({preventScroll:true}),400)});
$("#qMinus").addEventListener("click",()=>{qty--;renderPdp()});
$("#qPlus").addEventListener("click",()=>{qty++;renderPdp()});
$("#addBtn").addEventListener("click",()=>{const it=BY[curSku];if(it.qty<=0){show("home","faq");$("#reqWhat").value=it.brand+" "+it.product+" — "+it.variant;return}add(curSku,qty);toast(`${it.status==="on_the_way"?"Pre-ordered":"Added"} ${qty} × ${it.variant}`);qty=1;renderPdp()});
$("#bagBtn").addEventListener("click",openBag);
$("#closeBag").addEventListener("click",closeBag);
$("#scrim").addEventListener("click",closeBag);
$("#toCheckout").addEventListener("click",()=>{if(!bag.length)return;renderCheckout();show("checkout")});
document.addEventListener("keydown",e=>{if(e.key!=="Escape")return;if(!$("#modal").hidden){clearTimeout(stkTimer);closeSheet()}else closeBag()});
$("#coZone").addEventListener("change",()=>{setErr("f-zone","");renderCheckout()});
document.querySelectorAll("input[name=pay]").forEach(r=>r.addEventListener("change",renderCheckout));
["coName","coPhone","coLoc","coCode"].forEach(id=>$("#"+id).addEventListener("input",()=>{const f=$("#"+id).closest(".field");if(f.classList.contains("bad"))setErr(f.id,"")}));
$("#coForm").addEventListener("submit",e=>{e.preventDefault();if(!bag.length){toast("Your bag is empty.");return}if(!validate())return;const pay=document.querySelector("input[name=pay]:checked").value;if(pay==="stk")startStk();else placeOrder(pay)});
$("#reqForm").addEventListener("submit",e=>{e.preventDefault();const w=$("#reqWhat").value.trim();if(!w){toast("Tell us which product you want.");$("#reqWhat").focus();return}if(!normPhone($("#reqPhone").value)){toast("Add a WhatsApp number like 0712 345 678 so we can reply.");$("#reqPhone").focus();return}toast("Request noted — we’ll WhatsApp you. (Prototype: not sent.)");e.target.reset()});
/* admin inputs */
$("#aq").addEventListener("input",renderAdminList);$("#aStatus").addEventListener("change",renderAdminList);$("#aPrice").addEventListener("change",renderAdminList);
$("#aList").addEventListener("input",e=>{const r=e.target.closest("[data-row]");if(!r)return;dirty.add(r.dataset.row);r.classList.add("dirty");r.querySelector("[data-save]").disabled=false});
$("#orderList").addEventListener("change",e=>{const s=e.target.closest("[data-order]");if(s)setOrderStatus(s.dataset.order,s.value)});
$("#pForm").addEventListener("input",e=>{if(e.target.id==="pEta")etaTouched=true;if(e.target.id==="pShipped"&&!etaTouched&&e.target.value)$("#pEta").value=addDays(e.target.value,TRANSIT_DAYS);if(e.target.id!=="pPhoto")renderPreview()});
$("#pForm").addEventListener("change",e=>{if(e.target.name==="pStatus"||e.target.id==="pRmPhoto")renderPreview()});
$("#pPhoto").addEventListener("change",e=>{pFile=e.target.files[0]||null;if(pFileUrl)URL.revokeObjectURL(pFileUrl);pFileUrl=pFile?URL.createObjectURL(pFile):null;renderPreview()});
$("#pForm").addEventListener("submit",e=>{e.preventDefault();saveProduct()});
$("#pCancel").addEventListener("click",()=>{resetForm();adminTab="products";renderAdmin()});
$("#pDelete").addEventListener("click",askDelete);
document.addEventListener("submit",e=>{if(e.target.id==="loginForm"){e.preventDefault();doLogin($("#adminPw").value)}});
$("#ownerLogin").addEventListener("click",askLogin);
$("#logoutBtn").addEventListener("click",()=>{logout();toast("Logged out")});
$("#refreshOrders").addEventListener("click",()=>{loadOrders();toast("Orders refreshed")});

fillSelects();renderZones();renderHome();renderBag();resetForm();
connect();
