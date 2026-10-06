import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Sparkles, Target, Compass, Award, ShieldCheck, 
  Cpu, Users, BookOpen, ArrowRight, CheckCircle2, 
  IndianRupee, GraduationCap, Code2, LineChart 
} from 'lucide-react';

const AboutPage = () => {
  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-8 py-10 space-y-16">
      
      {/* Hero Section */}
      <div className="text-center max-w-4xl mx-auto pt-4">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-50 border border-indigo-200/80 text-indigo-700 text-xs font-bold uppercase tracking-wider mb-5 shadow-2xs">
          <Sparkles size={14} className="text-indigo-600" />
          <span>Built for Bharat • Career Intelligence</span>
        </div>
        
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-tight mb-5">
          Democratizing Career Pathways for{' '}
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600">
            India's Next Generation
          </span>
        </h1>
        
        <p className="text-base sm:text-lg text-slate-600 leading-relaxed font-normal max-w-2xl mx-auto mb-8">
          CareerPath AI is an empirical competency intelligence platform built to bridge the divide between university curricula and modern tech industry demands across Bharat.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4">
          <Link
            to="/"
            className="px-6 py-3.5 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm shadow-md shadow-slate-900/10 hover:shadow-xl hover:scale-[1.01] transition-all flex items-center gap-2"
          >
            Benchmark Your Skills <ArrowRight size={16} />
          </Link>
          <Link
            to="/roles"
            className="px-6 py-3.5 rounded-2xl border-2 border-indigo-300 hover:border-indigo-400 text-indigo-700 bg-white hover:bg-indigo-50/60 font-bold text-sm shadow-2xs transition-all"
          >
            Browse 81 Industry Roles
          </Link>
        </div>
      </div>

      {/* Key Impact Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
        <div className="glass-card rounded-3xl p-6 text-center border border-white/90 shadow-xl shadow-indigo-500/5">
          <p className="text-3xl sm:text-4xl font-black text-indigo-600">1.5M+</p>
          <p className="text-xs sm:text-sm font-bold text-slate-800 mt-1">Graduates Annually</p>
          <p className="text-[11px] text-slate-400 mt-0.5 font-medium">Entering Indian workforce</p>
        </div>

        <div className="glass-card rounded-3xl p-6 text-center border border-white/90 shadow-xl shadow-indigo-500/5">
          <p className="text-3xl sm:text-4xl font-black text-purple-600">80+</p>
          <p className="text-xs sm:text-sm font-bold text-slate-800 mt-1">Industry Roles</p>
          <p className="text-[11px] text-slate-400 mt-0.5 font-medium">Empirically benchmarked</p>
        </div>

        <div className="glass-card rounded-3xl p-6 text-center border border-white/90 shadow-xl shadow-indigo-500/5">
          <p className="text-3xl sm:text-4xl font-black text-emerald-600">300+</p>
          <p className="text-xs sm:text-sm font-bold text-slate-800 mt-1">Tech Taxonomies</p>
          <p className="text-[11px] text-slate-400 mt-0.5 font-medium">Normalized via RapidFuzz</p>
        </div>

        <div className="glass-card rounded-3xl p-6 text-center border border-white/90 shadow-xl shadow-indigo-500/5">
          <p className="text-3xl sm:text-4xl font-black text-blue-600">0%</p>
          <p className="text-xs sm:text-sm font-bold text-slate-800 mt-1">Pedigree Bias</p>
          <p className="text-[11px] text-slate-400 mt-0.5 font-medium">100% skill-first evaluation</p>
        </div>
      </div>

      {/* The Problem vs Our Solution */}
      <div className="grid md:grid-cols-2 gap-8">
        
        {/* Problem Card */}
        <div className="glass-card rounded-3xl p-7 sm:p-9 border border-rose-100 bg-rose-50/20 shadow-xl shadow-indigo-500/5 flex flex-col justify-between">
          <div>
            <div className="w-12 h-12 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center border border-rose-200 shadow-2xs mb-5">
              <Target size={24} />
            </div>
            <h2 className="text-2xl font-black text-slate-900 mb-3">The Employability Challenge</h2>
            <p className="text-slate-600 text-sm leading-relaxed mb-6 font-medium">
              Over 80% of Indian engineering graduates encounter difficulty securing specialized core technical roles due to:
            </p>
            <ul className="space-y-3.5 text-xs sm:text-sm text-slate-700 font-medium">
              <li className="flex items-start gap-2.5">
                <span className="text-rose-500 font-bold shrink-0 mt-0.5">✕</span>
                <span><strong>Curriculum Disconnect:</strong> College syllabi frequently lag 3–5 years behind cloud, DevOps, and modern AI industry practices.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-rose-500 font-bold shrink-0 mt-0.5">✕</span>
                <span><strong>College Brand Bias:</strong> Non-metro and Tier-2/Tier-3 students are often filtered out by pedigree rather than evaluated on verified skills.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <span className="text-rose-500 font-bold shrink-0 mt-0.5">✕</span>
                <span><strong>Unclear Upskilling Paths:</strong> Job postings ask for vague lists of 20+ requirements with no clear prioritization between essential and optional skills.</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Solution Card */}
        <div className="glass-card rounded-3xl p-7 sm:p-9 border border-indigo-100 bg-indigo-50/20 shadow-xl shadow-indigo-500/5 flex flex-col justify-between">
          <div>
            <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-200 shadow-2xs mb-5">
              <Compass size={24} />
            </div>
            <h2 className="text-2xl font-black text-slate-900 mb-3">Our Intelligent Solution</h2>
            <p className="text-slate-600 text-sm leading-relaxed mb-6 font-medium">
              CareerPath AI replaces guesswork with empirical data and personalized mentorship:
            </p>
            <ul className="space-y-3.5 text-xs sm:text-sm text-slate-700 font-medium">
              <li className="flex items-start gap-2.5">
                <CheckCircle2 size={16} className="text-emerald-600 shrink-0 mt-0.5" />
                <span><strong>Exact Gap Audit:</strong> Quantifies essential vs. optional skill coverage percentages for any specific occupation.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <CheckCircle2 size={16} className="text-emerald-600 shrink-0 mt-0.5" />
                <span><strong>Predictive Compensation:</strong> Trained ML Ridge Regressor estimates realistic median salary CTC (₹ LPA) based on actual proficiencies.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <CheckCircle2 size={16} className="text-emerald-600 shrink-0 mt-0.5" />
                <span><strong>Public Infrastructure Alignment:</strong> Direct integration with accredited Indian government programs (NPTEL, SWAYAM, FutureSkills Prime).</span>
              </li>
            </ul>
          </div>
        </div>

      </div>

      {/* Core Ethical & Architectural Pillars */}
      <div className="space-y-6">
        <div className="text-center max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-bold uppercase tracking-wider mb-3">
            Core Principles
          </div>
          <h2 className="text-3xl font-black text-slate-900 tracking-tight">
            How We Guarantee Ethical & Transparent AI
          </h2>
          <p className="text-sm text-slate-500 mt-2 font-medium">
            Designed from day one to eliminate systemic hiring biases and empower learners regardless of geography.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
          
          <div className="glass-card glass-card-hover rounded-3xl p-7 border border-white/90 shadow-xl shadow-indigo-500/5">
            <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center border border-indigo-100 shadow-2xs mb-5">
              <GraduationCap size={22} />
            </div>
            <h3 className="text-lg font-black text-slate-900 mb-2">Skill-First Meritocracy</h3>
            <p className="text-xs sm:text-sm text-slate-500 leading-relaxed font-normal">
              Candidates are evaluated purely on demonstrable competencies and practical capabilities. No penalties are assessed for non-traditional degrees (BCA, polytechnic, bootcamps, or Tier-3 colleges).
            </p>
          </div>

          <div className="glass-card glass-card-hover rounded-3xl p-7 border border-white/90 shadow-xl shadow-indigo-500/5">
            <div className="w-12 h-12 rounded-2xl bg-purple-50 text-purple-600 flex items-center justify-center border border-purple-100 shadow-2xs mb-5">
              <Award size={22} />
            </div>
            <h3 className="text-lg font-black text-slate-900 mb-2">NEP 2020 & SWAYAM Integration</h3>
            <p className="text-xs sm:text-sm text-slate-500 leading-relaxed font-normal">
              Our learning roadmaps prioritize high-quality, free courses from IITs, IISc, and NPTEL that qualify for university elective credits under national AICTE/NEP guidelines.
            </p>
          </div>

          <div className="glass-card glass-card-hover rounded-3xl p-7 border border-white/90 shadow-xl shadow-indigo-500/5">
            <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-100 shadow-2xs mb-5">
              <ShieldCheck size={22} />
            </div>
            <h3 className="text-lg font-black text-slate-900 mb-2">Explainable AI (No Black Boxes)</h3>
            <p className="text-xs sm:text-sm text-slate-500 leading-relaxed font-normal">
              Every score comes with transparent reasoning. We break down exactly which essential skills were matched, which are missing, and the empirical market velocity of each skill.
            </p>
          </div>

        </div>
      </div>

      {/* Technical Architecture */}
      <div className="glass-card rounded-3xl p-8 sm:p-10 border border-white/90 shadow-xl shadow-indigo-500/5">
        <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight mb-2">
          Under the Hood: Technical Architecture
        </h2>
        <p className="text-sm text-slate-500 mb-8 font-medium">
          Engineered for high performance, accuracy, and enterprise-grade resilience.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80">
            <div className="flex items-center gap-2 mb-3">
              <Code2 size={18} className="text-indigo-600" />
              <h4 className="font-bold text-sm text-slate-900">NLP Ingestion</h4>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed font-normal">
              PyMuPDF & python-docx extract text from multi-page resumes with fallback detection for scanned image density.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80">
            <div className="flex items-center gap-2 mb-3">
              <Cpu size={18} className="text-purple-600" />
              <h4 className="font-bold text-sm text-slate-900">Taxonomic Normalization</h4>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed font-normal">
              RapidFuzz Levenshtein matching maps shorthand aliases against 300+ canonical technical skill standards.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80">
            <div className="flex items-center gap-2 mb-3">
              <LineChart size={18} className="text-emerald-600" />
              <h4 className="font-bold text-sm text-slate-900">Ridge ML Regression</h4>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed font-normal">
              Scikit-Learn Ridge model calibrated on Indian compensation bands with TF-IDF cosine similarity for role discovery.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50/80 border border-slate-200/80">
            <div className="flex items-center gap-2 mb-3">
              <BookOpen size={18} className="text-blue-600" />
              <h4 className="font-bold text-sm text-slate-900">ReportLab PDF Engine</h4>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed font-normal">
              Generates multi-page vector PDF career audits containing radar charts, audit tables, and personalized roadmaps.
            </p>
          </div>
        </div>
      </div>

      {/* Call to Action Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-blue-950 text-white rounded-3xl p-8 sm:p-12 shadow-2xl relative overflow-hidden text-center">
        <div className="relative z-10 max-w-2xl mx-auto space-y-4">
          <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
            Ready to Take Control of Your Career?
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 font-medium leading-relaxed">
            Upload your resume now to receive instant competency benchmarks, predicted compensation, and a week-by-week learning roadmap.
          </p>
          <div className="pt-2">
            <Link
              to="/"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-2xl bg-white text-slate-950 hover:bg-slate-100 font-bold text-sm shadow-lg hover:scale-105 transition-all"
            >
              Analyze Your Resume for Free <ArrowRight size={16} />
            </Link>
          </div>
        </div>
      </div>

    </div>
  );
};

export default AboutPage;
