# ContractMD Validációs Kit

> **Cél:** 30-60 perc alatt eldönteni, hogy az `ai-legal-claude` engine kimenete eladható minőségű-e — MIELŐTT bármilyen SaaS-frontendet építenénk köré.
>
> **Filozófia (Pat Walls):** *"Validate before you build."*

## Tartalom

```
validation-kit/
├── README.md                      ← itt vagy
├── 01_SETUP_HU.md                 ← Claude Code + ai-legal-claude install
├── 02_TEST_PROTOCOL_HU.md         ← teszt-menet (eredetileg 3 szerződésre)
├── EREDMENYEK_HU.md               ← értékelő űrlap (6 szerződésre frissítve)
├── contracts-en/
│   ├── freelancer_contract.md     ← 7 piros zászló (IP, non-compete, poison pill cap)
│   ├── apartment_lease.md         ← 10 piros zászló (NYC: 3-havi kaució = illegális!)
│   └── saas_msa.md                ← 12 piros zászló (AI training klauzula, GDPR explicit kizárás)
└── contracts-hu/
    ├── vallalkozoi_szerzodes.md   ← 10 piros zászló (színlelt szerződés, Mt./Ptk./Szjt.)
    ├── alberleti_szerzodes.md     ← 12 piros zászló (bejelentkezés tiltása, NAV-elhallgatás)
    └── saas_szerzodes.md          ← 13 piros zászló (GDPR 28., 72h notice, EU-n kívüli transzfer)
```

## Letöltés a saját gépedre

```bash
git clone -b claude/validate-core-engine-5AyzT https://github.com/stob1985/agency-agents-stob.git
cd agency-agents-stob/validation-kit
```

vagy csak ezt a mappát:

```bash
git archive --remote=https://github.com/stob1985/agency-agents-stob.git claude/validate-core-engine-5AyzT validation-kit | tar -x
```

## Gyors start (futtatás saját gépen, NEM itt!)

1. **Setup** → `01_SETUP_HU.md` (Claude Code + ai-legal-claude install + API key)
2. **Protokoll** → `02_TEST_PROTOCOL_HU.md` (6 futtatás, PDF generation)
3. **Értékelés** → `EREDMENYEK_HU.md` (pontozás, döntés)

## Fontos

- Ez a remote container **ephemeral**, itt nem fut Claude Code+API key.
- A teszteket a **saját gépeden** futtatod (Mac/Linux/WSL).
- A `EREDMENYEK_HU.md`-ban minden szerződéshez van megoldó kulcs (`<details>` blokkokban). **Ne nyisd ki** futtatás előtt — különben az értékelés torzít!

## Sikerkritérium röviden

| Pontszám / 150 | Találat % | Döntés |
|---|---|---|
| 120+ | 75%+ | 🟢 GO — építünk SaaS frontendet |
| 90-119 | 50-75% | 🟡 TUNE — playbook írás |
| 60-89 | 30-50% | 🟠 REBUILD — saját prompt logika |
| <60 | <30% | 🔴 PIVOT — más ötlet/alap |
