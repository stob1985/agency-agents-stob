"use client";

import { useEffect, useState } from "react";

const KEY = "algopulse_watchlist";

function load(): string[] {
  try {
    return JSON.parse(localStorage.getItem(KEY) || "[]");
  } catch {
    return [];
  }
}

export default function WatchButton({ coinId }: { coinId: string }) {
  const [on, setOn] = useState(false);

  useEffect(() => {
    setOn(load().includes(coinId));
  }, [coinId]);

  function toggle() {
    const list = load();
    const next = list.includes(coinId) ? list.filter((x) => x !== coinId) : [...list, coinId];
    localStorage.setItem(KEY, JSON.stringify(next));
    setOn(next.includes(coinId));
  }

  return (
    <button
      className={`watch-btn ${on ? "on" : ""}`}
      onClick={toggle}
      title={on ? "Remove from watchlist" : "Add to watchlist"}
      aria-label="Toggle watchlist"
    >
      {on ? "★" : "☆"}
    </button>
  );
}
