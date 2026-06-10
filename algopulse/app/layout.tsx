import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "AlgoPulse — AI-Powered Crypto Intelligence",
  description:
    "Systematic signals, live market data and AI research briefs for crypto investors. Built on an MCP-powered agent stack."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="container">
          <nav className="nav">
            <Link href="/" className="logo">
              <span className="logo-mark">Λ</span> AlgoPulse
            </Link>
            <div className="nav-links">
              <Link href="/#features">Features</Link>
              <Link href="/#pricing">Pricing</Link>
              <Link href="/dashboard">Dashboard</Link>
              <Link href="/dashboard" className="btn btn-primary">
                Launch app
              </Link>
            </div>
          </nav>
        </header>
        {children}
        <footer className="footer">
          <div className="container disclaimer">
            <p>
              © {new Date().getFullYear()} AlgoPulse. Market data by CoinGecko. Sentiment by alternative.me.
            </p>
            <p>
              AlgoPulse provides systematic research and analytics for informational purposes only. Nothing on
              this platform constitutes investment advice, a recommendation or an offer to buy or sell any
              digital asset. Crypto-assets are highly volatile; you can lose your entire investment. Past
              signal performance does not guarantee future results.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
