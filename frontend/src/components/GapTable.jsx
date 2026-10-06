import React from 'react';
import { CheckCircle, AlertCircle, AlertTriangle, TrendingUp } from 'lucide-react';
import SkillTag from './SkillTag';

const GapTable = ({ 
  matchedSkills = [], 
  missingEssential = [], 
  missingOptional = [], 
  surplusSkills = [],
  skillVelocities = [] 
}) => {
  const velMap = {};
  if (Array.isArray(skillVelocities)) {
    skillVelocities.forEach(v => {
      if (v && v.skill) {
        velMap[v.skill.toLowerCase()] = v;
      }
    });
  }

  const allSkills = [
    ...matchedSkills.map(s => ({ name: s, status: 'matched', type: 'matched' })),
    ...missingEssential.map(s => ({ name: s, status: 'missing', type: 'missing-essential' })),
    ...missingOptional.map(s => ({ name: s, status: 'missing', type: 'missing-optional' })),
  ];

  return (
    <div className="overflow-x-auto bg-white rounded-xl shadow-sm border border-gray-100">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-slate-50">
          <tr>
            <th scope="col" className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Skill
            </th>
            <th scope="col" className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Audit Status
            </th>
            <th scope="col" className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Priority
            </th>
            <th scope="col" className="px-5 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
              India Market Trend
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-100">
          {allSkills.map((skill, idx) => {
            const vel = velMap[skill.name.toLowerCase()];
            const trendLabel = vel ? vel.trend : (skill.type === 'matched' ? 'Active in Profile' : 'Steady Industry Demand');
            const isHighGrowth = vel && (vel.velocity_score >= 80);

            return (
              <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                <td className="px-5 py-3.5 whitespace-nowrap">
                  <span className="font-semibold text-gray-900">{skill.name}</span>
                </td>
                <td className="px-5 py-3.5 whitespace-nowrap">
                  <div className="flex items-center text-xs font-medium">
                    {skill.type === 'matched' && (
                      <span className="flex items-center text-emerald-600">
                        <CheckCircle size={15} className="mr-1.5" /> Matched
                      </span>
                    )}
                    {skill.type === 'missing-essential' && (
                      <span className="flex items-center text-rose-600 font-semibold">
                        <AlertCircle size={15} className="mr-1.5" /> Missing Essential
                      </span>
                    )}
                    {skill.type === 'missing-optional' && (
                      <span className="flex items-center text-amber-600">
                        <AlertTriangle size={15} className="mr-1.5" /> Missing Optional
                      </span>
                    )}
                  </div>
                </td>
                <td className="px-5 py-3.5 whitespace-nowrap">
                  <SkillTag 
                    name={skill.type === 'matched' ? 'Acquired' : skill.type === 'missing-essential' ? 'High Impact' : 'Nice-to-Have'} 
                    variant={skill.type} 
                  />
                </td>
                <td className="px-5 py-3.5 whitespace-nowrap">
                  <span className={`inline-flex items-center gap-1 text-xs px-2.5 py-1 rounded-full font-medium ${
                    isHighGrowth 
                      ? 'bg-rose-50 text-rose-700 border border-rose-200' 
                      : skill.type === 'matched'
                      ? 'bg-emerald-50 text-emerald-700'
                      : 'bg-slate-100 text-slate-600'
                  }`}>
                    <TrendingUp size={12} className={isHighGrowth ? 'text-rose-500' : 'text-slate-400'} />
                    {trendLabel}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default GapTable;
