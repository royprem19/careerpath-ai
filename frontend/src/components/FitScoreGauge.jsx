import React from 'react';

const FitScoreGauge = ({ score = 0 }) => {
  const radius = 56;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (Math.min(Math.max(score, 0), 100) / 100) * circumference;

  let gradientId = "gaugeGradientHigh";
  let textColor = "text-emerald-600";
  let labelText = "High Match";

  if (score < 40) {
    gradientId = "gaugeGradientLow";
    textColor = "text-rose-600";
    labelText = "Foundational";
  } else if (score < 70) {
    gradientId = "gaugeGradientMid";
    textColor = "text-amber-600";
    labelText = "Moderate Fit";
  }

  return (
    <div className="flex flex-col items-center justify-center py-2">
      <div className="relative w-44 h-44 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 140 140">
          <defs>
            <linearGradient id="gaugeGradientHigh" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#059669" />
            </linearGradient>
            <linearGradient id="gaugeGradientMid" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#f59e0b" />
              <stop offset="100%" stopColor="#d97706" />
            </linearGradient>
            <linearGradient id="gaugeGradientLow" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#f43f5e" />
              <stop offset="100%" stopColor="#e11d48" />
            </linearGradient>
          </defs>

          {/* Background circle track */}
          <circle
            className="text-slate-100/90 stroke-current"
            strokeWidth="11"
            cx="70"
            cy="70"
            r={radius}
            fill="transparent"
          />

          {/* Value stroke */}
          <circle
            stroke={`url(#${gradientId})`}
            className="transition-all duration-1000 ease-out"
            strokeWidth="11"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            cx="70"
            cy="70"
            r={radius}
            fill="transparent"
          />
        </svg>

        {/* Center label */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-4xl font-black tracking-tight ${textColor}`}>
            {score}%
          </span>
          <span className="text-[10px] font-extrabold uppercase tracking-widest text-slate-400 mt-1">
            {labelText}
          </span>
        </div>
      </div>
    </div>
  );
};

export default FitScoreGauge;
