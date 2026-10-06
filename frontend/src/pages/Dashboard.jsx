import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import FitScoreGauge from '../components/FitScoreGauge';
import SkillRadarChart from '../components/SkillRadarChart';
import RoleBarChart from '../components/RoleBarChart';
import GapTable from '../components/GapTable';
import RoadmapTimeline from '../components/RoadmapTimeline';
import { 
  Download, RefreshCw, ArrowLeft, Target, Info, CheckCircle2, 
  AlertCircle, Sparkles, BookOpen, ExternalLink, Award, IndianRupee,
  UploadCloud, FileText, Briefcase
} from 'lucide-react';
import { analyzeGap, getRecommendations, getRoadmap, downloadReport, getRoles } from '../services/api';

const Dashboard = () => {
  const { userProfile, selectedRole, setSelectedRole, clearProfile } = useAppContext();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [isDownloading, setIsDownloading] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [roadmap, setRoadmap] = useState([]);
  const [errorMsg, setErrorMsg] = useState('');
  const [resolvedRole, setResolvedRole] = useState(selectedRole);

  const hasProfile = Boolean(userProfile?.skills && userProfile.skills.length > 0);
  const effectiveSkills = userProfile?.skills || [];

  useEffect(() => {
    let isMounted = true;

    if (!hasProfile || !selectedRole) {
      setLoading(false);
      return;
    }

    const performAnalysis = async () => {
      try {
        setLoading(true);
        setErrorMsg('');

        if (isMounted) setResolvedRole(selectedRole);
        const roleId = selectedRole.id || '1';

        // 1. Run Real Gap Analysis API
        const gapResp = await analyzeGap(effectiveSkills, roleId);
        const gap = gapResp.data;

        // 2. Run Real Recommendations API
        let recs = [];
        try {
          const recResp = await getRecommendations(
            effectiveSkills, 
            userProfile?.education || [], 
            userProfile?.experience || {}
          );
          recs = recResp.data || [];
        } catch (recErr) {
          console.warn('Recommendation API fallback:', recErr);
        }

        // 3. Run Real Roadmap API
        const missingAll = [...(gap.missing_essential || []), ...(gap.missing_optional || [])];
        let roadmapData = [];
        try {
          const roadResp = await getRoadmap(missingAll);
          roadmapData = roadResp.data?.entries || [];
        } catch (roadErr) {
          console.warn('Roadmap API fallback:', roadErr);
        }

        if (isMounted) {
          setAnalysisData(gap);
          setRecommendations(recs);
          setRoadmap(roadmapData);
          setLoading(false);
        }
      } catch (err) {
        console.error('Analysis error:', err);
        if (isMounted) {
          setErrorMsg('Failed to run analysis against backend. Please ensure FastAPI server is running on port 8000.');
          setLoading(false);
        }
      }
    };

    performAnalysis();

    return () => {
      isMounted = false;
    };
  }, [selectedRole, userProfile, hasProfile]);

  const currentRole = resolvedRole || selectedRole || {
    id: '1',
    title: 'Full Stack Developer',
    description: 'Architects and builds complete web applications.',
    essential_skills: [],
    optional_skills: []
  };

  const handleDownloadPDF = async () => {
    if (!analysisData) return;
    try {
      setIsDownloading(true);
      const payload = {
        user_profile: {
          skills: effectiveSkills,
          education: userProfile?.education || [],
          experience: userProfile?.experience || {}
        },
        gap_analysis: analysisData,
        recommendations: recommendations,
        roadmap: roadmap
      };
      const response = await downloadReport(payload);
      
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `CareerPath_Analysis_${currentRole.title.replace(/\s+/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('PDF generation error:', err);
      alert('Could not generate PDF report. Check backend report endpoint.');
    } finally {
      setIsDownloading(false);
    }
  };

  // 1. Empty State: User has not uploaded a resume or selected a target role
  if (!hasProfile || !selectedRole) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <div className="bg-white rounded-3xl p-10 md:p-14 shadow-sm border border-gray-100 max-w-2xl mx-auto">
          <div className="w-20 h-20 bg-blue-50 text-primary-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xs border border-blue-100">
            <UploadCloud size={38} />
          </div>
          <span className="inline-block text-xs font-semibold px-3 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200 mb-3">
            {!hasProfile ? 'Profile Needed' : 'Target Role Needed'}
          </span>
          <h2 className="text-2xl md:text-3xl font-extrabold text-gray-900 mb-3">
            {!hasProfile ? 'No Resume or Skills Added Yet' : 'Please Select a Target Role'}
          </h2>
          <p className="text-gray-600 text-sm md:text-base leading-relaxed mb-8 max-w-lg mx-auto">
            {!hasProfile 
              ? 'Upload your resume (PDF/DOCX) or paste your technical skills on the home page. Our AI engine will extract your competencies and benchmark them against real Indian industry roles.'
              : 'Please choose an industry occupation benchmark from the Roles page to calculate your skill fit score and generate your learning roadmap.'}
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={() => navigate('/')}
              className="w-full sm:w-auto px-6 py-3 rounded-xl bg-primary-600 hover:bg-primary-700 text-white font-semibold text-sm shadow-sm transition-all flex items-center justify-center gap-2"
            >
              <UploadCloud size={18} />
              Upload Resume or Enter Skills
            </button>
            <button
              onClick={() => navigate('/roles')}
              className="w-full sm:w-auto px-6 py-3 rounded-xl bg-gray-50 hover:bg-gray-100 text-gray-700 font-semibold text-sm border border-gray-200 transition-all flex items-center justify-center gap-2"
            >
              <Briefcase size={18} />
              Browse 81 Real Industry Roles
            </button>
          </div>
        </div>
      </div>
    );
  }

  // 2. Loading State during active real analysis
  if (loading) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center p-4">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-600 mb-6"></div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">Analyzing Competencies & Industry Demand...</h3>
        <p className="text-sm text-gray-500 max-w-md text-center">
          Matching your skill vector against real industry benchmarks, calculating essential coverage, and tailoring course pathways.
        </p>
      </div>
    );
  }

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 py-8 space-y-8">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
        <div className="flex items-center space-x-4">
          <button 
            onClick={() => navigate('/roles')} 
            className="p-2.5 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-colors border border-gray-200"
            title="Choose different role"
          >
            <ArrowLeft size={20} />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-700">
                Target Role
              </span>
              <span className="text-xs text-gray-400">•</span>
              <span className="text-xs text-gray-500">{currentRole.category || 'Technology'}</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mt-0.5">
              {currentRole.title}
            </h1>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <button 
            onClick={() => {
              clearProfile();
              navigate('/');
            }} 
            className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors"
          >
            <RefreshCw size={15} className="mr-1.5 text-gray-500" /> New Profile
          </button>
          <button 
            onClick={handleDownloadPDF}
            disabled={isDownloading}
            className="flex items-center px-5 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-xl shadow-sm transition-all"
          >
            {isDownloading ? (
              <span className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Generating PDF...
              </span>
            ) : (
              <>
                <Download size={16} className="mr-1.5" /> Download Report
              </>
            )}
          </button>
        </div>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-center gap-3 text-amber-800 text-sm">
          <AlertCircle size={20} className="shrink-0 text-amber-600" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Metrics & Visualizations */}
        <div className="lg:col-span-1 space-y-6">
          
          {/* Match Overview Card */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-base font-bold text-gray-900 mb-4 flex items-center justify-between">
              <span className="flex items-center">
                <Target className="mr-2 text-primary-500" size={18} /> Role Fit Score
              </span>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                70/30 Essential Weighted
              </span>
            </h2>

            <FitScoreGauge score={analysisData?.fit_score || 0} />
            
            <div className="mt-6 space-y-4 pt-4 border-t border-gray-100">
              <div>
                <div className="flex justify-between text-xs font-medium mb-1.5">
                  <span className="text-gray-600">Essential Skill Coverage</span>
                  <span className="font-bold text-emerald-600">{analysisData?.essential_coverage || 0}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                  <div 
                    className="bg-emerald-500 h-2 rounded-full transition-all duration-700" 
                    style={{ width: `${Math.min(100, analysisData?.essential_coverage || 0)}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-medium mb-1.5">
                  <span className="text-gray-600">Optional Skill Coverage</span>
                  <span className="font-bold text-blue-600">{analysisData?.optional_coverage || 0}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all duration-700" 
                    style={{ width: `${Math.min(100, analysisData?.optional_coverage || 0)}%` }}
                  ></div>
                </div>
              </div>
            </div>
            
            <div className="mt-6 pt-4 border-t border-gray-100 grid grid-cols-3 text-center gap-2">
              <div className="bg-slate-50 p-2.5 rounded-xl">
                <p className="text-xl font-extrabold text-emerald-600">{analysisData?.matched_count || 0}</p>
                <p className="text-[11px] font-semibold text-gray-500 uppercase tracking-wider">Matched</p>
              </div>
              <div className="bg-slate-50 p-2.5 rounded-xl">
                <p className="text-xl font-extrabold text-red-500">{analysisData?.missing_essential?.length || 0}</p>
                <p className="text-[11px] font-semibold text-gray-500 uppercase tracking-wider">Missing</p>
              </div>
              <div className="bg-slate-50 p-2.5 rounded-xl">
                <p className="text-xl font-extrabold text-blue-600">{analysisData?.surplus_skills?.length || 0}</p>
                <p className="text-[11px] font-semibold text-gray-500 uppercase tracking-wider">Surplus</p>
              </div>
            </div>

            {analysisData?.predicted_salary && (
              <div className="mt-4 p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-center justify-between">
                <span className="font-semibold flex items-center gap-1.5">
                  <IndianRupee size={14} className="text-emerald-600" /> ML Predicted CTC:
                </span>
                <span className="font-bold text-xs text-emerald-900 bg-white px-2.5 py-1 rounded-lg border border-emerald-200 shadow-xs">
                  {analysisData.predicted_salary}
                </span>
              </div>
            )}
          </div>

          {/* Skill Radar Chart */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-base font-bold text-gray-900 mb-1">Competency Radar</h2>
            <p className="text-xs text-gray-500 mb-4">Domain overlap against role requirements</p>
            <SkillRadarChart 
              userSkills={effectiveSkills}
              roleEssential={currentRole.essential_skills || []}
              roleOptional={currentRole.optional_skills || []}
            />
          </div>

          {/* Top Recommendations Bar Chart */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-base font-bold text-gray-900 mb-1">Market Role Rankings</h2>
            <p className="text-xs text-gray-500 mb-4">Alternative careers matching your current profile</p>
            <RoleBarChart 
              recommendations={recommendations.map(r => ({
                role: r.role_title,
                score: r.score,
                role_id: r.role_id
              }))} 
            />
          </div>
        </div>

        {/* Right Column: Deep Analysis, Gap Breakdown & Learning Path */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Explainability Panel */}
          <div className="bg-gradient-to-br from-blue-50/80 via-white to-purple-50/50 p-6 rounded-2xl shadow-sm border border-blue-100">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-xl bg-blue-600 text-white shadow-sm mt-0.5">
                <Sparkles size={20} />
              </div>
              <div className="space-y-2">
                <h2 className="text-lg font-bold text-gray-900">Explainable AI Insights</h2>
                <p className="text-sm text-gray-700 leading-relaxed">
                  {analysisData?.why_this_role || "Our intelligence engine compared your skills with real Indian industry demand standards."}
                </p>
                <div className="flex flex-wrap items-center gap-4 pt-2 text-xs text-gray-500">
                  <span className="flex items-center gap-1 font-medium text-emerald-700">
                    <CheckCircle2 size={14} className="text-emerald-500" />
                    Verified vs ESCO & Naukri 2025 data
                  </span>
                  <span className="flex items-center gap-1 font-medium text-blue-700">
                    <Award size={14} className="text-blue-500" />
                    NPTEL & Industry Credential Pathways
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Gap Breakdown Table */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-bold text-gray-900 mb-1">Detailed Skill Audit</h2>
            <p className="text-xs text-gray-500 mb-5">
              Comprehensive breakdown of essential criteria, optional bonus skills, and transferable surplus
            </p>
            <GapTable 
              matchedSkills={analysisData?.matched_skills || []}
              missingEssential={analysisData?.missing_essential || []}
              missingOptional={analysisData?.missing_optional || []}
              surplusSkills={analysisData?.surplus_skills || []}
              skillVelocities={analysisData?.skill_velocities || []}
            />
          </div>

          {/* Week-by-Week Learning Roadmap */}
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                  <BookOpen size={20} className="text-primary-600" />
                  Personalized Learning Roadmap
                </h2>
                <p className="text-xs text-gray-500 mt-1">
                  Week-by-week curriculum mapped to verified courses & real hands-on projects
                </p>
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                {roadmap.length} Milestone Modules
              </span>
            </div>

            <RoadmapTimeline roadmap={roadmap} />
          </div>

        </div>
      </div>
    </div>
  );
};

export default Dashboard;
