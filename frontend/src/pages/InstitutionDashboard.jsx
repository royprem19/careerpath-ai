import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { getInstitutionAnalytics } from '../services/api';
import { 
  Building2, GraduationCap, TrendingUp, AlertTriangle, CheckCircle2, 
  BookOpen, Sparkles, Download, Layers, ShieldCheck, ArrowRight, IndianRupee 
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell 
} from 'recharts';

const InstitutionDashboard = () => {
  const { currentUser } = useAppContext();
  const navigate = useNavigate();

  const [institution, setInstitution] = useState(currentUser?.institution_name || 'IIT Madras');
  const [department, setDepartment] = useState('Computer Science & Engineering');
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        setErrorMsg('');
        const res = await getInstitutionAnalytics(institution, department);
        setAnalytics(res.data);
      } catch (err) {
        console.error('Failed to load institution analytics:', err);
        setErrorMsg('Could not fetch institution analytics. Make sure the FastAPI server is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, [institution, department]);

  const handleExportAudit = () => {
    window.print();
  };

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 py-8 space-y-8">
      
      {/* Top Header */}
      <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-50 text-purple-700 border border-purple-200 text-xs font-semibold mb-2">
            <Building2 size={13} />
            University Talent & Curriculum Alignment Engine
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 tracking-tight">
            {institution} — Academic Intelligence
          </h1>
          <p className="text-gray-500 text-xs sm:text-sm mt-1">
            Anonymized cohort skill gaps across graduating engineers calibrated against 2025–2026 Indian industry demand.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <select
            value={institution}
            onChange={(e) => setInstitution(e.target.value)}
            className="p-2.5 text-xs font-semibold bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500"
          >
            <option value="IIT Madras">IIT Madras</option>
            <option value="IIT Bombay">IIT Bombay</option>
            <option value="IIT Delhi">IIT Delhi</option>
            <option value="BITS Pilani">BITS Pilani</option>
            <option value="Delhi Technological University (DTU)">DTU Delhi</option>
            <option value="VIT Vellore">VIT Vellore</option>
          </select>

          <button
            onClick={handleExportAudit}
            className="flex items-center gap-1.5 px-4 py-2.5 text-xs font-semibold text-white bg-primary-600 hover:bg-primary-700 rounded-xl shadow-sm transition-all"
          >
            <Download size={14} /> Export Curriculum Audit
          </button>
        </div>
      </div>

      {loading ? (
        <div className="min-h-[50vh] flex flex-col items-center justify-center p-8 space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="text-gray-500 text-sm font-medium">Aggregating cohort skill distributions & syllabus benchmarks...</p>
        </div>
      ) : (
        <>
          {/* Key KPI Metrics Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            
            {/* KPI 1 */}
            <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
              <div>
                <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">Cohort Scope</span>
                <h3 className="text-3xl font-black text-gray-900 mt-1">
                  {analytics?.total_students_analyzed || 128}
                </h3>
              </div>
              <p className="text-xs text-gray-500 mt-3 flex items-center gap-1 font-medium">
                <GraduationCap size={14} className="text-primary-600" /> Graduating Engineers (2026 Batch)
              </p>
            </div>

            {/* KPI 2 */}
            <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
              <div>
                <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">Curriculum Alignment</span>
                <h3 className="text-3xl font-black text-blue-600 mt-1">
                  {analytics?.curriculum_alignment_score || 64.0}%
                </h3>
              </div>
              <p className="text-xs text-amber-600 mt-3 flex items-center gap-1 font-semibold">
                <AlertTriangle size={14} /> Modernization Needed
              </p>
            </div>

            {/* KPI 3 */}
            <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
              <div>
                <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">Placement Readiness</span>
                <h3 className="text-3xl font-black text-emerald-600 mt-1">
                  {analytics?.placement_readiness?.tier_1_premium_pct || 18.5}%
                </h3>
              </div>
              <p className="text-xs text-gray-500 mt-3 flex items-center gap-1 font-medium">
                <TrendingUp size={14} className="text-emerald-500" /> Tier-1 Ready (&gt; 10 LPA band)
              </p>
            </div>

            {/* KPI 4 */}
            <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-between">
              <div>
                <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider">Projected Cohort CTC</span>
                <h3 className="text-3xl font-black text-purple-600 mt-1 flex items-center">
                  ₹{analytics?.placement_readiness?.avg_projected_ctc_lpa || 7.8} LPA
                </h3>
              </div>
              <p className="text-xs text-gray-500 mt-3 flex items-center gap-1 font-medium">
                <IndianRupee size={13} className="text-purple-500" /> ML Ridge Regression Baseline
              </p>
            </div>

          </div>

          {/* Main Visualizations Row */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            {/* Aggregate Cohort Gap Chart (2 cols) */}
            <div className="lg:col-span-2 bg-white p-6 rounded-3xl shadow-sm border border-gray-100 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Aggregate Cohort Skill Gaps (% Students Missing)</h3>
                  <p className="text-xs text-gray-500">Core industry competencies currently missing from students' resumes</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-red-50 text-red-700 border border-red-200">
                  Critical Deficits
                </span>
              </div>

              <div className="h-72 w-full pt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={analytics?.top_aggregate_skill_gaps || []}
                    layout="vertical"
                    margin={{ top: 5, right: 30, left: 70, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                    <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fontSize: 11 }} />
                    <YAxis dataKey="skill" type="category" tick={{ fontSize: 11 }} width={90} />
                    <Tooltip 
                      formatter={(val) => [`${val}% of cohort missing this skill`, 'Deficit Rate']}
                      contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }}
                    />
                    <Bar dataKey="students_missing_pct" radius={[0, 8, 8, 0]}>
                      {(analytics?.top_aggregate_skill_gaps || []).map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={entry.students_missing_pct > 70 ? '#ef4444' : entry.students_missing_pct > 55 ? '#f59e0b' : '#3b82f6'} 
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="flex items-center justify-center gap-6 text-xs text-gray-500 pt-2 border-t border-gray-50">
                <span className="flex items-center gap-1.5 font-medium">
                  <span className="w-3 h-3 rounded-full bg-red-500 inline-block"></span> &gt; 70% Severe Gap
                </span>
                <span className="flex items-center gap-1.5 font-medium">
                  <span className="w-3 h-3 rounded-full bg-amber-500 inline-block"></span> 55-70% Moderate Gap
                </span>
                <span className="flex items-center gap-1.5 font-medium">
                  <span className="w-3 h-3 rounded-full bg-blue-500 inline-block"></span> &lt; 55% Emerging Standard
                </span>
              </div>
            </div>

            {/* CTC Band Distribution (1 col) */}
            <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 flex flex-col justify-between">
              <div>
                <h3 className="text-lg font-bold text-gray-900">Compensation Readiness</h3>
                <p className="text-xs text-gray-500 mb-6">Predicted campus placement distribution</p>

                <div className="space-y-5">
                  <div>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className="text-emerald-700">Tier-1 Premium (&gt; 10 LPA)</span>
                      <span className="text-emerald-800">{analytics?.placement_readiness?.tier_1_premium_pct || 18.5}%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                      <div className="bg-emerald-500 h-2.5 rounded-full" style={{ width: `${analytics?.placement_readiness?.tier_1_premium_pct || 18.5}%` }}></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className="text-blue-700">Median Industry Band (6–10 LPA)</span>
                      <span className="text-blue-800">{analytics?.placement_readiness?.median_tech_pct || 54.0}%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                      <div className="bg-blue-500 h-2.5 rounded-full" style={{ width: `${analytics?.placement_readiness?.median_tech_pct || 54.0}%` }}></div>
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-semibold mb-1">
                      <span className="text-gray-700">Entry Level (&lt; 6 LPA)</span>
                      <span className="text-gray-800">{analytics?.placement_readiness?.entry_level_pct || 27.5}%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                      <div className="bg-gray-400 h-2.5 rounded-full" style={{ width: `${analytics?.placement_readiness?.entry_level_pct || 27.5}%` }}></div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-purple-50/70 border border-purple-100 mt-6 text-xs text-purple-900 space-y-1">
                <span className="font-bold flex items-center gap-1 text-purple-800">
                  <Sparkles size={14} /> Placement Officer Takeaway:
                </span>
                <p className="leading-relaxed">
                  Integrating our recommended 6-week Cloud-Native & LLM modules can elevate up to 35% of the entry band into the median 8-12 LPA bracket.
                </p>
              </div>
            </div>

          </div>

          {/* Subject-by-Subject Curriculum Alignment Audit Table */}
          <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 space-y-4">
            <div>
              <h3 className="text-lg font-bold text-gray-900">Core Engineering Syllabus Audit</h3>
              <p className="text-xs text-gray-500">Benchmark of University curriculum vs current Indian job requirements</p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-gray-100 text-gray-400 uppercase tracking-wider text-[11px]">
                    <th className="py-3 px-4">University Subject</th>
                    <th className="py-3 px-4">Alignment Score</th>
                    <th className="py-3 px-4">Gap Summary & Missing Elements</th>
                    <th className="py-3 px-4">Industry Benchmark Standard</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50 font-medium">
                  {(analytics?.subject_alignment_audit || []).map((sub, idx) => (
                    <tr key={idx} className="hover:bg-gray-50/50 transition-colors">
                      <td className="py-3.5 px-4 font-bold text-gray-900">{sub.subject}</td>
                      <td className="py-3.5 px-4">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold ${
                          sub.alignment_score >= 80 ? 'bg-emerald-50 text-emerald-700' :
                          sub.alignment_score >= 60 ? 'bg-amber-50 text-amber-700' :
                          'bg-red-50 text-red-700'
                        }`}>
                          {sub.alignment_score}%
                        </span>
                      </td>
                      <td className="py-3.5 px-4 text-gray-600 max-w-md">{sub.gap_summary}</td>
                      <td className="py-3.5 px-4 text-gray-500 max-w-sm">{sub.industry_benchmark}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Recommended Curriculum Interventions & Electives */}
          <div className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                  <BookOpen size={20} className="text-primary-600" />
                  Recommended Curriculum Interventions & Electives
                </h3>
                <p className="text-xs text-gray-500">
                  Targeted elective modules designed to bridge the top cohort skill gaps before campus recruitment
                </p>
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                Actionable for Academic Deans
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
              {(analytics?.recommended_electives || []).map((rec, idx) => (
                <div key={idx} className="p-5 rounded-2xl bg-gradient-to-br from-slate-50 to-blue-50/30 border border-blue-100/80 flex flex-col justify-between space-y-4">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-bold px-2 py-0.5 rounded-md bg-blue-100 text-blue-800">
                        {rec.duration_weeks}-Week Elective
                      </span>
                      <span className="text-xs font-extrabold text-emerald-600">
                        +{rec.impact_pct}% Readiness
                      </span>
                    </div>
                    <h4 className="text-sm font-bold text-gray-900">{rec.title}</h4>
                    <p className="text-xs text-gray-600 leading-relaxed">{rec.rationale}</p>
                  </div>

                  <div>
                    <div className="flex flex-wrap gap-1.5 pt-2">
                      {rec.target_skills.map((s, sIdx) => (
                        <span key={sIdx} className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-white border border-gray-200 text-gray-700 shadow-2xs">
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </>
      )}

    </div>
  );
};

export default InstitutionDashboard;
