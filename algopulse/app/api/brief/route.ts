import { NextResponse } from "next/server";
import { getFearGreed, getMarkets } from "@/lib/coingecko";
import { computeSignals } from "@/lib/signals";
import { generateBrief } from "@/lib/brief";

export const revalidate = 900;

export async function GET() {
  try {
    const [coins, fearGreed] = await Promise.all([getMarkets(20), getFearGreed()]);
    const signals = computeSignals(coins);
    const brief = await generateBrief({ coins, signals, fearGreed });
    return NextResponse.json({
      generatedAt: new Date().toISOString(),
      engine: brief.engine,
      text: brief.text
    });
  } catch (e) {
    return NextResponse.json({ error: "data source unavailable" }, { status: 503 });
  }
}
