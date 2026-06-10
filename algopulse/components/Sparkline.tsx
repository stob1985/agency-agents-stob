export default function Sparkline({
  data,
  width = 110,
  height = 32
}: {
  data: number[];
  width?: number;
  height?: number;
}) {
  if (!data || data.length < 2) return null;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const step = width / (data.length - 1);
  const points = data
    .map((v, i) => `${(i * step).toFixed(1)},${(height - 2 - ((v - min) / range) * (height - 4)).toFixed(1)}`)
    .join(" ");
  const up = data[data.length - 1] >= data[0];
  const color = up ? "#21c77d" : "#f4536e";
  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} aria-hidden>
      <polyline fill="none" stroke={color} strokeWidth="1.6" points={points} strokeLinejoin="round" />
    </svg>
  );
}
