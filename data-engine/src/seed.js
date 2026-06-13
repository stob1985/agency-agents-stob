import { db, nowIso } from "./db.js";

// Seed demo API keys (one per plan) so the API is usable immediately.
// In production these are minted at checkout (Stripe -> create key with plan).
const KEYS = [
  { key: "pk_demo_free", label: "Demo Free", plan: "free" },
  { key: "pk_demo_pro", label: "Demo Pro", plan: "pro" },
  { key: "pk_demo_ent", label: "Demo Enterprise", plan: "enterprise" }
];

const ins = db.prepare(
  `INSERT OR IGNORE INTO api_keys (key,label,plan,created_at) VALUES (?,?,?,?)`
);
for (const k of KEYS) ins.run(k.key, k.label, k.plan, nowIso());

console.log("seeded demo keys:");
for (const k of KEYS) console.log(`  ${k.plan.padEnd(10)} ${k.key}`);
