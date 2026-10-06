import React from 'react';

const FitScoreGauge = ({ score = 0 }) => {
  // Determine color based on score
  let colorClass = 'text-green-500';
  let strokeClass = 'stroke-green-500';
  if (score < 40) {
    colorClass = 'text-red-500';
    strokeClass = 'stroke-red-500';
  } else if (score < 70) {
    colorClass = 'text-yellow-500';
    strokeClass = 'stroke-yellow-500';
  }

  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative w-40 h-40">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 140 140">
          <circle
            className="text-gray-200 stroke-current"
            strokeWidth="12"
            cx="70"
            cy="70"
            r={radius}
            fill="transparent"
          />
          <circle
            className={`${strokeClass} transition-all duration-1000 ease-in-out`}
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            cx="70"
            cy="70"
            r={radius}
            fill="transparent"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-4xl font-bold ${colorClass}`}>{score}%</span>
          <span className="text-xs text-gray-500 font-medium mt-1">FIT SCORE</span>
        </div>
      </div>
    </div>
  );
};

export default FitScoreGauge;
