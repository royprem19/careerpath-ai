import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const CATEGORIES = [
  { name: 'Core Langs', keywords: ['python', 'javascript', 'typescript', 'java', 'c++', 'go', 'sql'] },
  { name: 'Frameworks', keywords: ['react', 'next.js', 'fastapi', 'node.js', 'express', 'django', 'html5', 'css3', 'tailwindcss'] },
  { name: 'Databases', keywords: ['postgresql', 'mongodb', 'mysql', 'redis', 'supabase', 'database', 'sql'] },
  { name: 'Cloud & Ops', keywords: ['docker', 'kubernetes', 'aws', 'azure', 'linux', 'ci/cd', 'terraform'] },
  { name: 'AI & Data', keywords: ['machine learning', 'deep learning', 'pandas', 'numpy', 'scikit-learn', 'pytorch', 'llm', 'rag', 'spark'] },
  { name: 'Tools & Eng', keywords: ['git & github', 'git', 'agile', 'rest apis', 'jest', 'testing', 'architecture'] },
];

const SkillRadarChart = ({ userSkills = [], roleEssential = [], roleOptional = [] }) => {
  const userLower = (userSkills || []).map(s => s.toLowerCase());
  const roleAll = [...(roleEssential || []), ...(roleOptional || [])].map(s => s.toLowerCase());

  const chartData = CATEGORIES.map(cat => {
    // Count how many keywords in this category are relevant to role
    const roleMatches = cat.keywords.filter(kw => roleAll.some(r => r.includes(kw) || kw.includes(r))).length;
    // Count how many user has in this category
    const userMatches = cat.keywords.filter(kw => userLower.some(u => u.includes(kw) || kw.includes(u))).length;

    const roleScore = roleMatches > 0 ? Math.min(100, Math.max(50, roleMatches * 35)) : 30;
    const userScore = roleMatches > 0 
      ? Math.min(100, Math.round((userMatches / Math.max(1, roleMatches)) * 100))
      : (userMatches > 0 ? 70 : 20);

    return {
      subject: cat.name,
      user: userScore,
      role: roleScore,
      fullMark: 100
    };
  });

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="68%" data={chartData}>
          <PolarGrid stroke="#e2e8f0" />
          <PolarAngleAxis dataKey="subject" tick={{ fill: '#475569', fontSize: 11, fontWeight: 500 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 9 }} />
          <Radar name="Your Profile" dataKey="user" stroke="#2563eb" fill="#3b82f6" fillOpacity={0.45} />
          <Radar name="Role Standard" dataKey="role" stroke="#7c3aed" fill="#8b5cf6" fillOpacity={0.25} />
          <Legend wrapperStyle={{ fontSize: 11, paddingTop: 6 }} />
          <Tooltip 
            formatter={(value) => [`${value}%`, 'Score']}
            contentStyle={{ backgroundColor: '#ffffff', borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SkillRadarChart;
