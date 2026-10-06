import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const RoleBarChart = ({ recommendations }) => {
  const data = recommendations || [
    { role: 'Frontend Dev', score: 85 },
    { role: 'Full Stack Dev', score: 72 },
    { role: 'Backend Dev', score: 65 },
    { role: 'DevOps Eng', score: 40 },
    { role: 'Data Scientist', score: 30 },
  ];

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          layout="vertical"
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" domain={[0, 100]} />
          <YAxis dataKey="role" type="category" width={120} tick={{ fontSize: 12 }} />
          <Tooltip cursor={{ fill: 'transparent' }} />
          <Bar dataKey="score" radius={[0, 4, 4, 0]}>
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={entry.score >= 80 ? '#10b981' : entry.score >= 60 ? '#3b82f6' : '#8b5cf6'} 
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RoleBarChart;
