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
          margin={{ top: 5, right: 30, left: 10, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
          <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11, fill: '#64748b' }} unit="%" />
          <YAxis dataKey="role" type="category" width={130} tick={{ fontSize: 11, fill: '#334155', fontWeight: 600 }} />
          <Tooltip 
            cursor={{ fill: '#f8fafc', opacity: 0.7 }}
            formatter={(val) => [`${val}%`, 'Match Score']}
            contentStyle={{ backgroundColor: '#ffffff', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 4px 12px rgba(0,0,0,0.05)', fontSize: '12px' }}
          />
          <Bar dataKey="score" radius={[0, 8, 8, 0]} barSize={18}>
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={entry.score >= 80 ? '#10b981' : entry.score >= 60 ? '#6366f1' : entry.score >= 40 ? '#8b5cf6' : '#94a3b8'} 
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RoleBarChart;
