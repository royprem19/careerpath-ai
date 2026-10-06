import React from 'react';
import { CheckCircle2, AlertCircle, AlertTriangle, TrendingUp } from 'lucide-react';
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
    <div className="overflow-x-auto rounded-2xl border border-slate-200/80 bg-white/90 shadow-2xs">
      <table className="min-w-full divide-y divide-slate-100 text-sm">
        <thead className="bg-slate-50/80">
          <tr>
            <th scope="col" className="px-5 py-3.5 text-left text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              Skill
            </th>
            <th scope="col" className="px-5 py-3.5 text-left text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              Audit Status
            </th>
            <th scope="col" className="px-5 py-3.5 text-left text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              Priority Tier
            </th>
            <th scope="col" className="px-5 py-3.5 text-left text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              India Market Trend
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-slate-100/90">
          {allSkills.map((skill, idx) => {
            const vel = velMap[skill.name.toLowerCase()];
            const trendLabel = vel ? vel.trend : (skill.type === 'matched' ? 'Active in Profile' : 'Steady Industry Demand');
            const isHighGrowth = vel && (vel.velocity_score >= 80);

            return (
              <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                <td className="px-5 py-3.5 whitespace-nowrap">
                  <span className="font-bold text-slate-900 text-sm">{skill.name}</span>
                </td>
                <td className="px-5 py-3.5 whitespace-nowrap">
                  <div className="flex items-center text-xs font-bold">
                    {skill.type === 'matched' && (
                      <span className="flex items-center text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-xl border border-emerald-100">
                        <CheckCircle2 size={14} className="mr-1.5 text-emerald-600" /> Matched
                      </span>
                    )}
                    {skill.type === 'missing-essential' && (
                      <span className="flex items-center text-rose-700 bg-rose-50 px-2.5 py-1 rounded-xl border border-rose-100">
                        <AlertCircle size={14} className="mr-1.5 text-rose-600" /> Missing Essential
                      </span>
                    )}
                    {skill.type === 'missing-optional' && (
                      <span className="flex items-center text-amber-700 bg-amber-50 px-2.5 py-1 rounded-xl border border-amber-100">
                        <AlertTriangle size={14} className="mr-1.5 text-amber-600" /> Missing Optional
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
                  <span className={`inline-flex items-center gap-1.5 text-xs px-3 py-1 rounded-xl font-bold ${
                    isHighGrowth 
                      ? 'bg-rose-50 text-rose-700 border border-rose-200/80 shadow-2xs' 
                      : skill.type === 'matched'
                      ? 'bg-emerald-50 text-emerald-700 border border-emerald-100'
                      : 'bg-slate-100 text-slate-600 border border-slate-200/60'
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
