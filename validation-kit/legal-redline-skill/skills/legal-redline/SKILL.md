# Legal Redline

**Command:** `/legal redline <contract-file>`

**Purpose:** Generate a professional Word `.docx` redline of a contract — the kind a lawyer would send to the other party as a negotiation document. Contains real Word tracked changes (`w:ins`/`w:del`) + real margin comments (`w:comment`), plus visual fallback formatting (red strikethrough + green underline) so it renders correctly even with revisions hidden.

## Inputs

- A contract file (`.md`, `.txt`, `.pdf`, `.docx`) — path supplied by the user
- The contract's language (Hungarian, English, or any other) — auto-detect from content

## What this skill produces

`REDLINED-<contract-name>.docx` containing:

1. **Cover page** — title, current score / score after redline, severity counts, verdict.
2. **Per-change blocks** — for each problematic clause:
   - Severity badge (🔴 HIGH / 🟡 MEDIUM / 🟢 LOW)
   - Original text shown as tracked deletion (real `w:del` + red strikethrough)
   - Proposed replacement shown as tracked insertion (real `w:ins` + green underline)
   - Margin comment with: why it's a problem / legal basis / what's at risk / what the change protects / negotiation tip
   - Inline yellow callout card with the same info (so it's readable even when revisions are hidden)
3. **Overview table** — section, severity, title, risk for every change.

## Process

1. **Run a full review of the contract.** Use the structure from `legal-review` or `legal-risks` skills: identify every red flag, classify severity, propose a concrete replacement clause.
2. **Run negotiate.** For every red flag, draft a realistic counter-proposal (not just "delete" — actual replacement text the user can ship to the other side).
3. **Compose a JSON input** matching the structure expected by `generate_redline_docx.py` (see schema below).
4. **Invoke the script:**
   ```bash
   python3 ~/.claude/scripts/generate_redline_docx.py /tmp/redline_input.json REDLINED-<contract>.docx
   ```
5. **Report back to the user:** the path to the generated `.docx`, the counts (high/medium/low changes), and a one-sentence summary.

## JSON input schema

```json
{
  "contract_title": "string — short name shown on cover",
  "language": "hu | en",
  "score": {
    "current": "int 0-100 — current contract score",
    "after_redline": "int 0-100 — projected score after applying all changes",
    "max": 100,
    "grade": "A | B | C | D | F"
  },
  "summary": {
    "high": "int — count of high-severity changes",
    "medium": "int",
    "low": "int",
    "verdict": "string — one-sentence overall recommendation"
  },
  "changes": [
    {
      "section": "string — section number from the contract (e.g. '3.1')",
      "title": "string — short name for the problem",
      "severity": "high | medium | low",
      "original": "string — exact text from the contract being redlined out",
      "proposed": "string — concrete replacement text (NOT just 'delete this')",
      "why": "string — 1-2 sentence explanation of the problem",
      "legal_basis": "string — specific statute / case law (Ptk. 6:152. §, GDPR Art. 28, NY GOL § 7-108, etc.)",
      "risk": "string — concrete monetary or business consequence",
      "protects": "string — what the proposed change preserves for the client",
      "tip": "string — optional negotiation tip"
    }
  ]
}
```

## Language handling

**Match the contract's language for all output:**
- Hungarian contract → Hungarian comments, citing Ptk., Mt., Szjt., Lt., GDPR (magyarul), NAIH
- English contract → English comments, citing UCC, FTC, GDPR, state-specific statutes (NY GOL, CA Labor Code)
- Other languages → comments in that language with jurisdiction-appropriate citations

## Quality requirements

- **Every `proposed` MUST be real replacement text**, not "delete" or "negotiate." The user is going to send this `.docx` to the other party — vague stubs make us look amateur.
- **Every `legal_basis` MUST cite specific statutes** with section numbers (Ptk. 6:152. §, not "Hungarian civil code").
- **Every `risk` MUST be concrete** — monetary amounts, time frames, specific consequences.
- **Tone:** professional, neutral, lawyerly. Not alarmist, but clear about what's at stake.

## Examples

See `examples/vallalkozoi_hu_redline_input.json` for a Hungarian freelance/contractor contract, and the generated `REDLINED-Vallalkozoi-HU.docx`.

## Failure modes to avoid

- ❌ Don't redline cosmetic issues (typos, formatting) — only legal/business risks
- ❌ Don't propose unrealistic asks (e.g., "remove all indemnification") — propose what the other side might actually accept
- ❌ Don't redline more than ~15 sections in one pass — pick the top issues. A 50-change redline is unusable as a negotiation document
- ❌ Don't cite generic "case law" — only specific statutes you can stand behind
