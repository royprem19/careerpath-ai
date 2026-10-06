import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import FileUpload from '../components/FileUpload';
import { 
  Sparkles, ArrowRight, AlertCircle, Lock, LogIn, 
  CheckCircle2, FileText, Cpu, BarChart3, Compass, 
  Target, TrendingUp, GraduationCap, ShieldCheck, 
  Check, Layers, BookOpen, Download
} from 'lucide-react';
import { uploadResume, normalizeSkills, loginUser } from '../services/api';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [manualSkills, setManualSkills] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const { currentUser, token, login, setUserProfile, setError } = useAppContext();
  const navigate = useNavigate();

  // Smooth scroll support for #how-it-works link
  useEffect(() => {
    if (window.location.hash === '#how-it-works') {
      const el = document.getElementById('how-it-works');
      if (el) {
        setTimeout(() => el.scrollIntoView({ behavior: 'smooth' }), 100);
      }
    }
  }, []);

  const isAuthenticated = Boolean(currentUser && token);

  const requireAuthRedirect = () => {
    navigate('/auth');
  };

  const handleResumeAnalysis = async () => {
    if (!isAuthenticated) {
      requireAuthRedirect();
      return;
    }
    if (!file) return;
    setIsProcessing(true);
    setErrorMessage('');
    setError(null);

    try {
      const response = await uploadResume(file);
      const data = response.data;
      
      setUserProfile({
        skills: data.skills || [],
        education: data.education || [],
        experience: data.experience || {},
        certifications: data.certifications || [],
        raw_text: data.raw_text || ''
      });
      sessionStorage.setItem('careerpath_active_skills', JSON.stringify(data.skills || []));
      
      setIsProcessing(false);
      navigate('/profile');
    } catch (err) {
      console.error('Resume upload error:', err);
      if (err.response?.status === 401) {
        setErrorMessage('Authentication session expired. Please sign in again.');
        navigate('/auth');
      } else {
        const detail = err.response?.data?.detail || 'Failed to analyze resume. Please check the backend connection or enter skills manually.';
        setErrorMessage(detail);
        setError(detail);
      }
      setIsProcessing(false);
    }
  };

  const handleManualSkillsAnalysis = async () => {
    if (!isAuthenticated) {
      requireAuthRedirect();
      return;
    }
    if (!manualSkills.trim()) return;
    setIsProcessing(true);
    setErrorMessage('');
    setError(null);

    try {
      const rawSkillsList = manualSkills
        .split(/[,\n]/)
        .map(s => s.trim())
        .filter(Boolean);

      // Call normalization API
      let finalSkills = rawSkillsList;
      try {
        const normResp = await normalizeSkills(rawSkillsList);
        if (normResp.data?.normalized_skills?.length > 0) {
          finalSkills = normResp.data.normalized_skills;
        }
      } catch (normErr) {
        console.warn('Normalization fallback:', normErr);
      }

      setUserProfile({
        skills: finalSkills,
        education: [],
        experience: {},
        certifications: []
      });
      sessionStorage.setItem('careerpath_active_skills', JSON.stringify(finalSkills));
      
      setIsProcessing(false);
      navigate('/profile');
    } catch (err) {
      console.error('Manual skills error:', err);
      setErrorMessage('Failed to process skills. Please try again.');
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 pt-8 pb-20">
      <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16">
        
        {/* Hero Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-100/80 border border-blue-200 text-blue-800 text-xs font-semibold uppercase tracking-wider mb-4">
            <Sparkles size={14} className="text-primary-600" />
            <span>Intelligent Career & Talent Ecosystem</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-black text-gray-900 mb-4 tracking-tight">
            AI-Powered <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary-600 via-indigo-600 to-accent-600">Career Intelligence</span>
          </h1>
          <p className="text-base sm:text-lg text-gray-600 max-w-2xl mx-auto">
            Bridge the industry skill gap with real-world Indian job demand data, quantified role fit analysis, and tailored learning roadmaps.
          </p>
        </div>

        {/* Authentication Gate Banner (When User Is Not Signed In) */}
        {!isAuthenticated && (
          <div className="mb-8 p-6 rounded-3xl bg-gradient-to-r from-amber-50 via-white to-blue-50 border border-amber-200/90 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div className="flex items-start gap-3.5">
                <div className="p-2.5 rounded-2xl bg-amber-500 text-white shadow-xs shrink-0 mt-0.5">
                  <Lock size={20} />
                </div>
                <div>
                  <h3 className="text-base font-bold text-gray-900">
                    Authentication Required to Upload & Analyze Resume
                  </h3>
                  <p className="text-xs sm:text-sm text-gray-600 mt-1 max-w-xl">
                    Please sign in or create an account to securely parse your resume, save your verified competency vector, and unlock customized roadmap analytics.
                  </p>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-2 shrink-0">
                <button
                  type="button"
                  onClick={requireAuthRedirect}
                  className="px-4 py-2 text-xs font-bold rounded-xl bg-primary-600 hover:bg-primary-700 text-white shadow-xs transition-colors flex items-center gap-1.5"
                >
                  <LogIn size={14} /> Sign In / Register
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Logged in Welcome Badge */}
        {isAuthenticated && (
          <div className="mb-6 p-4 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-between">
            <div className="flex items-center gap-2.5 text-emerald-800 text-xs sm:text-sm font-semibold">
              <CheckCircle2 size={18} className="text-emerald-600" />
              <span>Signed in as <span className="font-bold">{currentUser?.user_name}</span> ({currentUser?.email})</span>
            </div>
            <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
              Candidate Active
            </span>
          </div>
        )}

        {errorMessage && (
          <div className="mb-6 p-4 rounded-xl bg-red-50 border border-red-200 flex items-start gap-3 text-red-700 text-sm">
            <AlertCircle size={20} className="shrink-0 mt-0.5 text-red-500" />
            <div>
              <p className="font-semibold">Notice</p>
              <p>{errorMessage}</p>
            </div>
          </div>
        )}

        {/* Main Action Cards Grid */}
        <div className="grid md:grid-cols-2 gap-8">
          
          {/* Card 1: Resume Upload */}
          <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-8 hover:shadow-md transition-shadow flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-xl sm:text-2xl font-bold text-gray-900 flex items-center">
                  <Sparkles className="text-primary-500 mr-2" size={22} />
                  Upload Resume
                </h2>
                {!isAuthenticated && (
                  <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200 flex items-center gap-1">
                    <Lock size={10} /> Locked
                  </span>
                )}
              </div>
              <p className="text-gray-500 mb-6 text-xs sm:text-sm">
                Supported formats: PDF, DOCX. Our NLP parser will extract technical skills, experience, and education.
              </p>
              
              <div className="mb-6">
                <FileUpload 
                  onFileSelect={setFile} 
                  selectedFile={file} 
                  onClear={() => setFile(null)} 
                  disabled={!isAuthenticated}
                  onDisabledClick={requireAuthRedirect}
                />
              </div>
            </div>
            
            <button
              type="button"
              onClick={handleResumeAnalysis}
              disabled={isAuthenticated && (!file || isProcessing)}
              className={`w-full py-3.5 px-4 rounded-xl flex items-center justify-center font-bold text-sm transition-all ${
                !isAuthenticated
                  ? 'bg-primary-600 hover:bg-primary-700 text-white shadow-sm'
                  : (!file || isProcessing)
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-primary-600 hover:bg-primary-700 text-white shadow-md hover:shadow-lg'
              }`}
            >
              {!isAuthenticated ? (
                <>
                  <Lock size={15} className="mr-1.5" /> Sign In to Analyze Resume
                </>
              ) : isProcessing ? (
                <div className="flex items-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Parsing & Extracting Skills...</span>
                </div>
              ) : (
                <>
                  Analyze Resume <ArrowRight className="ml-2" size={17} />
                </>
              )}
            </button>
          </div>

          {/* Card 2: Manual Skills */}
          <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-8 hover:shadow-md transition-shadow flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-xl sm:text-2xl font-bold text-gray-900">
                  Enter Skills Manually
                </h2>
                {!isAuthenticated && (
                  <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200 flex items-center gap-1">
                    <Lock size={10} /> Locked
                  </span>
                )}
              </div>
              <p className="text-gray-500 mb-6 text-xs sm:text-sm">
                Don't have a resume document handy? Paste your technical skills separated by commas or line breaks.
              </p>
              <div className="mb-6 relative">
                <textarea
                  value={manualSkills}
                  disabled={!isAuthenticated}
                  onChange={(e) => setManualSkills(e.target.value)}
                  onClick={() => { if (!isAuthenticated) requireAuthRedirect(); }}
                  placeholder={isAuthenticated ? "e.g. Python, SQL, React, FastAPI, Machine Learning, Docker, Pandas..." : "Sign in to enter skills manually..."}
                  className={`w-full h-44 p-4 border rounded-2xl focus:ring-2 focus:ring-primary-500 outline-none resize-none text-sm ${
                    !isAuthenticated 
                      ? 'bg-gray-50/80 border-gray-200 text-gray-400 cursor-not-allowed' 
                      : 'border-gray-200 text-gray-800'
                  }`}
                />
              </div>
            </div>

            <button
              type="button"
              onClick={handleManualSkillsAnalysis}
              disabled={isAuthenticated && (!manualSkills.trim() || isProcessing)}
              className={`w-full py-3.5 px-4 rounded-xl flex items-center justify-center font-bold text-sm transition-all ${
                !isAuthenticated
                  ? 'border border-primary-200 bg-primary-50 text-primary-700 hover:bg-primary-100'
                  : (!manualSkills.trim() || isProcessing)
                  ? 'border border-gray-200 text-gray-400 cursor-not-allowed'
                  : 'border border-primary-300 bg-primary-50 text-primary-700 hover:bg-primary-100'
              }`}
            >
              {!isAuthenticated ? (
                <>
                  <Lock size={15} className="mr-1.5" /> Sign In to Submit Skills
                </>
              ) : isProcessing ? (
                <div className="flex items-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
                  <span>Normalizing Skills...</span>
                </div>
              ) : (
                <>
                  Analyze Skills <ArrowRight className="ml-2" size={17} />
                </>
              )}
            </button>
          </div>

        </div>

        {/* ==============================================================================
            HOW IT WORKS SECTION
        ============================================================================== */}
        <div id="how-it-works" className="pt-16 pb-8 border-t border-gray-200/80 scroll-mt-20">
          
          {/* Section Header */}
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-primary-50 border border-primary-200/60 text-primary-700 text-xs font-bold tracking-wide uppercase mb-4 shadow-2xs">
              <Sparkles size={14} className="text-primary-600 animate-pulse" />
              Intelligence Pipeline & Methodology
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
              How CareerPath AI Works
            </h2>
            <p className="mt-3.5 text-base sm:text-lg text-gray-600 leading-relaxed">
              Transform unstructured technical resumes or skill lists into empirical role alignments, machine-learned salary valuations, and actionable learning roadmaps in 4 automated stages.
            </p>
          </div>

          {/* 4 Interactive Steps Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 relative">
            
            {/* Step 1 */}
            <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs hover:shadow-md transition-all group flex flex-col justify-between relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-blue-500 to-blue-600" />
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[11px] font-extrabold tracking-wider px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-100">
                    STEP 01
                  </span>
                  <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <FileText size={20} />
                  </div>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">Ingest & Extract</h3>
                <p className="text-xs sm:text-sm text-gray-500 leading-relaxed mb-4">
                  Upload your PDF/DOCX resume or enter skills manually. Our multi-format parsing engine isolates technical competencies, degrees, and work history.
                </p>
              </div>
              <div className="pt-3 border-t border-gray-50 flex flex-wrap gap-1.5">
                <span className="text-[10px] font-semibold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">PyMuPDF</span>
                <span className="text-[10px] font-semibold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">DOCX Parsing</span>
                <span className="text-[10px] font-semibold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-md">NLP Filter</span>
              </div>
            </div>

            {/* Step 2 */}
            <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs hover:shadow-md transition-all group flex flex-col justify-between relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-indigo-500 to-indigo-600" />
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[11px] font-extrabold tracking-wider px-2.5 py-1 rounded-md bg-indigo-50 text-indigo-700 border border-indigo-100">
                    STEP 02
                  </span>
                  <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Cpu size={20} />
                  </div>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">AI Normalization</h3>
                <p className="text-xs sm:text-sm text-gray-500 leading-relaxed mb-4">
                  Non-standard acronyms and shorthand skills (<code className="text-indigo-600 font-mono text-[11px]">k8s</code>, <code className="text-indigo-600 font-mono text-[11px]">ML</code>, <code className="text-indigo-600 font-mono text-[11px]">Postgres</code>) are normalized against 300+ standard tech taxonomies using RapidFuzz.
                </p>
              </div>
              <div className="pt-3 border-t border-gray-50 flex flex-wrap gap-1.5">
                <span className="text-[10px] font-semibold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">RapidFuzz</span>
                <span className="text-[10px] font-semibold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">Synonym Taxonomy</span>
                <span className="text-[10px] font-semibold bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-md">Deduplication</span>
              </div>
            </div>

            {/* Step 3 */}
            <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs hover:shadow-md transition-all group flex flex-col justify-between relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-purple-500 to-purple-600" />
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[11px] font-extrabold tracking-wider px-2.5 py-1 rounded-md bg-purple-50 text-purple-700 border border-purple-100">
                    STEP 03
                  </span>
                  <div className="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <BarChart3 size={20} />
                  </div>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">Gap & Salary AI</h3>
                <p className="text-xs sm:text-sm text-gray-500 leading-relaxed mb-4">
                  Your profile is evaluated against 80+ Indian engineering roles. Essential vs optional skills are quantified, and CTC compensation is predicted using our trained Ridge ML regressor.
                </p>
              </div>
              <div className="pt-3 border-t border-gray-50 flex flex-wrap gap-1.5">
                <span className="text-[10px] font-semibold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">Fit Score %</span>
                <span className="text-[10px] font-semibold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">Ridge ML (R²=0.72)</span>
                <span className="text-[10px] font-semibold bg-purple-50 text-purple-700 px-2 py-0.5 rounded-md">Indian CTC Bands</span>
              </div>
            </div>

            {/* Step 4 */}
            <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs hover:shadow-md transition-all group flex flex-col justify-between relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-emerald-500 to-emerald-600" />
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-[11px] font-extrabold tracking-wider px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-100">
                    STEP 04
                  </span>
                  <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Compass size={20} />
                  </div>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">Targeted Roadmap</h3>
                <p className="text-xs sm:text-sm text-gray-500 leading-relaxed mb-4">
                  Receive a structured week-by-week upskilling pathway bridging missing essential skills first. Every module pairs free verified courses (NPTEL, freeCodeCamp) with hands-on projects.
                </p>
              </div>
              <div className="pt-3 border-t border-gray-50 flex flex-wrap gap-1.5">
                <span className="text-[10px] font-semibold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">NPTEL / Coursera</span>
                <span className="text-[10px] font-semibold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">Weekly Timeline</span>
                <span className="text-[10px] font-semibold bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded-md">PDF Export</span>
              </div>
            </div>

          </div>

          {/* Deep-Dive Architecture Callout Banner */}
          <div className="mt-12 bg-gradient-to-r from-slate-900 via-indigo-950 to-blue-950 text-white rounded-3xl p-8 sm:p-10 shadow-xl border border-indigo-900/40 relative overflow-hidden">
            <div className="absolute -right-20 -bottom-20 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />
            <div className="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-8">
              
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center text-blue-300 shrink-0 border border-white/10">
                  <Target size={24} />
                </div>
                <div>
                  <h4 className="text-base font-bold text-white mb-1">Empirical Role Calibration</h4>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    Trained on real hiring criteria across top Indian tech hubs (Bengaluru, Hyderabad, Pune, NCR) spanning 80+ engineering specializations.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center text-yellow-300 shrink-0 border border-white/10">
                  <TrendingUp size={24} />
                </div>
                <div>
                  <h4 className="text-base font-bold text-white mb-1">Quantified Skill Velocities</h4>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    Identifies high-impact skills that produce the greatest boost to market fit and compensation when acquired.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center text-emerald-300 shrink-0 border border-white/10">
                  <ShieldCheck size={24} />
                </div>
                <div>
                  <h4 className="text-base font-bold text-white mb-1">Enterprise-Grade Security</h4>
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                    Protected with single-use cryptographic token verification, Bcrypt password hashing, and real-time DNS & SQL injection defense.
                  </p>
                </div>
              </div>

            </div>
          </div>

        </div>

      </div>
    </div>
  );
};

export default UploadPage;
