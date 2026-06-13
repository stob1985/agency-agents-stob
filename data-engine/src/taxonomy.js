// Controlled vocabularies. These are the schema the whole product sells against:
// every labeled record maps to a known token, a known narrative, and (optionally)
// a known event type. A stable taxonomy is what makes the time-series queryable
// and the dataset worth paying for.

// Token registry: ticker -> { name, aliases }. Used to (a) ground the rules-based
// extractor and (b) normalize/validate whatever the LLM returns so we never store
// a ticker we don't recognize.
export const TOKENS = {
  BTC: { name: "Bitcoin", aliases: ["bitcoin"] },
  ETH: { name: "Ethereum", aliases: ["ethereum", "ether"] },
  SOL: { name: "Solana", aliases: ["solana"] },
  XRP: { name: "XRP", aliases: ["ripple"] },
  BNB: { name: "BNB", aliases: ["binance coin"] },
  DOGE: { name: "Dogecoin", aliases: ["dogecoin"] },
  ADA: { name: "Cardano", aliases: ["cardano"] },
  AVAX: { name: "Avalanche", aliases: ["avalanche"] },
  LINK: { name: "Chainlink", aliases: ["chainlink"] },
  MATIC: { name: "Polygon", aliases: ["polygon", "matic"] },
  POL: { name: "Polygon", aliases: ["polygon ecosystem token"] },
  DOT: { name: "Polkadot", aliases: ["polkadot"] },
  ARB: { name: "Arbitrum", aliases: ["arbitrum"] },
  OP: { name: "Optimism", aliases: ["optimism"] },
  SUI: { name: "Sui", aliases: ["sui network"] },
  APT: { name: "Aptos", aliases: ["aptos"] },
  TIA: { name: "Celestia", aliases: ["celestia"] },
  SEI: { name: "Sei", aliases: ["sei network"] },
  INJ: { name: "Injective", aliases: ["injective"] },
  RNDR: { name: "Render", aliases: ["render network", "render token"] },
  FET: { name: "Artificial Superintelligence", aliases: ["fetch.ai", "fetch ai"] },
  TAO: { name: "Bittensor", aliases: ["bittensor"] },
  NEAR: { name: "NEAR Protocol", aliases: ["near protocol"] },
  ATOM: { name: "Cosmos", aliases: ["cosmos"] },
  LDO: { name: "Lido", aliases: ["lido dao", "lido"] },
  EIGEN: { name: "EigenLayer", aliases: ["eigenlayer", "eigen layer"] },
  PEPE: { name: "Pepe", aliases: ["pepe coin"] },
  WIF: { name: "dogwifhat", aliases: ["dogwifhat"] },
  SHIB: { name: "Shiba Inu", aliases: ["shiba inu"] },
  UNI: { name: "Uniswap", aliases: ["uniswap"] },
  AAVE: { name: "Aave", aliases: ["aave"] },
  ENA: { name: "Ethena", aliases: ["ethena"] },
  ONDO: { name: "Ondo", aliases: ["ondo finance"] },
  JTO: { name: "Jito", aliases: ["jito"] },
  JUP: { name: "Jupiter", aliases: ["jupiter exchange"] }
};

// Narrative tags — the "themes" a hype index is sliced by.
export const NARRATIVES = [
  "AI",
  "RWA",
  "DeFi",
  "ETF",
  "Memecoin",
  "L2",
  "Restaking",
  "Gaming",
  "DePIN",
  "Stablecoin",
  "Regulation",
  "Privacy",
  "Modular",
  "Bitcoin-ecosystem",
  "Staking",
  "Interoperability"
];

// Keyword hints for the rules-based narrative classifier (fallback path).
export const NARRATIVE_KEYWORDS = {
  AI: ["ai ", "artificial intelligence", "agent", "gpu", "compute", "inference", "machine learning"],
  RWA: ["real-world asset", "real world asset", "rwa", "tokeniz", "treasury", "treasuries", "bond"],
  DeFi: ["defi", "lending", "amm", "liquidity pool", "yield", "dex", "perpetual"],
  ETF: ["etf", "exchange-traded fund", "spot etf", "blackrock", "fidelity", "grayscale"],
  Memecoin: ["memecoin", "meme coin", "meme token", "dogwifhat", "pepe", "shiba"],
  L2: ["layer 2", "layer-2", "l2", "rollup", "optimistic", "zk-rollup", "arbitrum", "optimism", "base chain"],
  Restaking: ["restaking", "restake", "eigenlayer", "eigen layer", "avs", "actively validated"],
  Gaming: ["gamefi", "web3 game", "play-to-earn", "play to earn", "gaming token"],
  DePIN: ["depin", "decentralized physical", "physical infrastructure"],
  Stablecoin: ["stablecoin", "usdc", "usdt", "tether", "circle", "pegged"],
  Regulation: ["sec", "regulat", "lawsuit", "court", "congress", "mica", "compliance", "ban "],
  Privacy: ["privacy", "zero-knowledge", "zk-proof", "mixer", "anonymous"],
  Modular: ["modular", "data availability", "celestia", "rollup-as-a-service"],
  "Bitcoin-ecosystem": ["ordinals", "runes", "brc-20", "bitcoin l2", "stacks"],
  Staking: ["staking", "validator", "proof-of-stake", "stake "],
  Interoperability: ["interoperability", "cross-chain", "bridge", "ibc", "cosmos"]
};

// Concrete, schedulable/notable events the Token Event Feed sells.
export const EVENT_TYPES = [
  "listing",
  "delisting",
  "unlock",
  "mainnet",
  "upgrade",
  "partnership",
  "hack",
  "governance",
  "funding",
  "regulation",
  "etf"
];

export const EVENT_KEYWORDS = {
  listing: ["will list", "lists ", "listing", "now available on", "trading begins", "spot trading"],
  delisting: ["delist", "removes ", "will remove", "trading suspended"],
  unlock: ["token unlock", "unlock", "vesting", "cliff", "tokens released", "supply unlock"],
  mainnet: ["mainnet", "goes live", "launches mainnet", "network launch"],
  upgrade: ["upgrade", "hard fork", "hardfork", "fork", "testnet", "dencun", "pectra"],
  partnership: ["partner", "partnership", "integrat", "collaborat", "teams up"],
  hack: ["hack", "exploit", "drained", "breach", "stolen", "attack"],
  governance: ["governance", "proposal", "vote", "dao approves", "snapshot"],
  funding: ["raises", "raised", "funding round", "series a", "series b", "seed round", "valuation"],
  regulation: ["sec", "lawsuit", "court rules", "settlement", "fined", "approval", "rejected"],
  etf: ["etf", "spot etf", "etf approval", "etf filing", "s-1", "19b-4"]
};

// Positive / negative lexicon for the rules-based sentiment fallback.
export const POS_WORDS = [
  "surge", "soar", "rally", "gains", "bullish", "record", "all-time high", "ath", "approval",
  "approved", "partnership", "launch", "adoption", "upgrade", "breakout", "inflows", "milestone",
  "outperform", "boom", "jumps", "climbs", "wins", "success", "expands"
];
export const NEG_WORDS = [
  "plunge", "crash", "drop", "falls", "bearish", "selloff", "sell-off", "hack", "exploit", "lawsuit",
  "ban", "rejected", "delay", "outflows", "liquidat", "fear", "dump", "scam", "fraud", "warning",
  "collapse", "slump", "sinks", "tumbles", "loss", "concerns", "fud"
];

// Source tiers weight how much a mention counts toward the heat score.
// Tier-1 wire/research outlets move the index more than aggregators.
export const SOURCE_TIER = {
  "CoinDesk": 1.0,
  "Cointelegraph": 0.8,
  "The Defiant": 0.9,
  "Decrypt": 0.8,
  "Bitcoin Magazine": 0.7,
  "CryptoSlate": 0.7
};
