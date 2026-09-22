// Edit these and push — the site picks them up on the next deploy.
// fee: a number in KSh, or null while it's still being decided.
export const ZONES = [
  { id: "cbd",  name: "Nairobi CBD & Upper Hill", how: "Rider", when: "[SAME DAY]", fee: null },
  { id: "nbo",  name: "Rest of Nairobi", how: "Rider", when: "[SAME / NEXT DAY]", fee: null },
  { id: "env",  name: "Nairobi environs — Kiambu, Ruiru, Thika Rd, Kitengela, Syokimau, Ngong, Rongai", how: "Rider", when: "[NEXT DAY]", fee: null },
  { id: "ctry", name: "Rest of Kenya", how: "Courier / parcel office [COURIER]", when: "[1–3 DAYS]", fee: null }
];
export const CATS = ["Body care", "Shower", "Hair", "Deodorant", "Fragrance"];
export const SHAPES = ["pump", "pumpL", "flip", "duo", "jar", "tube", "oil", "aerosol", "stick", "mist", "spray"];
export const ORDER_STATUSES = ["new", "confirmed", "out", "delivered", "cancelled"];
