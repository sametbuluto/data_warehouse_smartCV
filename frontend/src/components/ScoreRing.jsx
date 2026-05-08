export default function ScoreRing({ score, size = 72 }) {
  const radius = (size - 8) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getColor = (s) => {
    if (s >= 80) return 'var(--accent-green)';
    if (s >= 60) return 'var(--accent-blue)';
    if (s >= 40) return 'var(--accent-amber)';
    return 'var(--accent-red)';
  };

  const color = getColor(score);

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size/2} cy={size/2} r={radius} fill="none"
                stroke="var(--border)" strokeWidth="4" />
        <circle cx={size/2} cy={size/2} r={radius} fill="none"
                stroke={color} strokeWidth="4" strokeLinecap="round"
                strokeDasharray={circumference} strokeDashoffset={offset}
                style={{ transition: 'stroke-dashoffset 1s ease' }} />
      </svg>
      <span className="absolute text-sm font-bold" style={{ color }}>
        {Math.round(score)}
      </span>
    </div>
  );
}
