import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { updateUserProfile } from '../services/api';
import { 
  User, Mail, School, GraduationCap, Building2, CheckCircle2, 
  AlertCircle, Save, ArrowLeft, ShieldCheck, Sparkles, FileText, Briefcase
} from 'lucide-react';

const INDIAN_UNIVERSITIES = [
  "IIT Madras",
  "IIT Bombay",
  "IIT Delhi",
  "BITS Pilani",
  "Delhi Technological University (DTU)",
  "VIT Vellore",
  "NIT Trichy",
  "IIIT Hyderabad",
  "Anna University",
  "Jadavpur University",
  "Other"
];

const DEPARTMENTS = [
  "Computer Science & Engineering",
  "Data Science & Artificial Intelligence",
  "Information Technology",
  "Electronics & Communication Engineering",
  "Electrical & Computer Engineering",
  "Mechanical / Multi-Disciplinary"
];

const UserProfilePage = () => {
  const { currentUser, updateUser } = useAppContext();
  const navigate = useNavigate();

  const [userName, setUserName] = useState('');
  const [institution, setInstitution] = useState('IIT Madras');
  const [customInstitution, setCustomInstitution] = useState('');
  const [department, setDepartment] = useState('Computer Science & Engineering');
  const [gradYear, setGradYear] = useState('2026');

  const [isSaving, setIsSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (!currentUser) {
      navigate('/auth');
      return;
    }

    setUserName(currentUser.user_name || '');
    setDepartment(currentUser.department || 'Computer Science & Engineering');
    setGradYear(String(currentUser.graduation_year || 2026));

    const currInst = currentUser.institution_name || 'IIT Madras';
    if (INDIAN_UNIVERSITIES.includes(currInst) && currInst !== 'Other') {
      setInstitution(currInst);
      setCustomInstitution('');
    } else {
      setInstitution('Other');
      setCustomInstitution(currInst === 'Other' ? '' : currInst);
    }
  }, [currentUser, navigate]);

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSuccessMsg('');
    setErrorMsg('');
    setIsSaving(true);

    try {
      const finalInstitution = institution === 'Other'
        ? (customInstitution.trim() || 'Other Institute')
        : institution;

      const payload = {
        user_name: userName.trim(),
        institution_name: finalInstitution,
        department: department,
        graduation_year: parseInt(gradYear, 10)
      };

      const res = await updateUserProfile(payload);
      const updatedData = res.data;

      // Update global context & localStorage
      updateUser({
        user_name: updatedData.user_name,
        institution_name: updatedData.institution_name,
        department: updatedData.department,
        graduation_year: updatedData.graduation_year
      });

      setSuccessMsg('Profile details successfully updated!');
      setTimeout(() => setSuccessMsg(''), 4000);
    } catch (err) {
      console.error('Update profile error:', err);
      const detail = err.response?.data?.detail || err.message || 'Failed to update profile. Please try again.';
      setErrorMsg(detail);
    } finally {
      setIsSaving(false);
    }
  };

  if (!currentUser) return null;

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-8 py-10">
      
      {/* Top Navigation Back Button */}
      <div className="mb-8 flex items-center justify-between">
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-2 text-xs font-bold text-slate-600 hover:text-slate-900 bg-white/90 px-4 py-2 rounded-2xl border border-slate-200/90 shadow-2xs hover:bg-slate-50 transition-all"
        >
          <ArrowLeft size={14} /> Back
        </button>
        <div className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-indigo-50 border border-indigo-200/80 text-indigo-700 text-xs font-bold shadow-2xs">
          <ShieldCheck size={14} /> Verified Student Account
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-8">
        
        {/* Left Column: Profile Summary Card */}
        <div className="md:col-span-1 lg:col-span-1 space-y-6">
          <div className="glass-card rounded-3xl p-7 border border-white/90 shadow-xl shadow-indigo-500/5 text-center">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-slate-900 via-indigo-950 to-slate-900 text-white font-black text-2xl flex items-center justify-center mx-auto shadow-md mb-4 border border-indigo-400/20">
              {currentUser.user_name ? currentUser.user_name.charAt(0).toUpperCase() : 'U'}
            </div>
            <h2 className="text-xl font-black text-slate-900">{currentUser.user_name}</h2>
            <p className="text-xs text-slate-500 font-medium mt-0.5 truncate">{currentUser.email}</p>
            
            <div className="mt-5 pt-5 border-t border-slate-100 space-y-3 text-left text-xs">
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-400">Status</span>
                <span className="font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-lg border border-emerald-100">Active Candidate</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-400">Cohort Year</span>
                <span className="font-bold text-slate-800">{currentUser.graduation_year || 2026}</span>
              </div>
              <div className="flex flex-col gap-1 pt-1">
                <span className="font-bold text-slate-400">Affiliation</span>
                <span className="font-semibold text-slate-800 truncate" title={currentUser.institution_name}>
                  {currentUser.institution_name || 'Institute of Technology'}
                </span>
              </div>
            </div>
          </div>

          {/* Quick Shortcuts */}
          <div className="glass-card rounded-3xl p-6 border border-white/90 shadow-xl shadow-indigo-500/5 space-y-3">
            <h3 className="text-xs font-black uppercase tracking-wider text-slate-400">Quick Actions</h3>
            <Link
              to="/"
              className="w-full flex items-center gap-2.5 p-3 rounded-2xl bg-white/90 hover:bg-indigo-50 text-slate-800 hover:text-indigo-700 text-xs font-bold shadow-2xs border border-slate-200/80 transition-colors"
            >
              <FileText size={16} className="text-indigo-600" /> Upload / Update Resume
            </Link>
            <Link
              to="/roles"
              className="w-full flex items-center gap-2.5 p-3 rounded-2xl bg-white/90 hover:bg-indigo-50 text-slate-800 hover:text-indigo-700 text-xs font-bold shadow-2xs border border-slate-200/80 transition-colors"
            >
              <Briefcase size={16} className="text-indigo-600" /> Browse 81 Industry Roles
            </Link>
          </div>
        </div>

        {/* Right Column: Edit Form */}
        <div className="md:col-span-2 lg:col-span-3">
          <div className="glass-card rounded-3xl p-7 sm:p-9 border border-white/90 shadow-xl shadow-indigo-500/5">
            <div className="mb-6">
              <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">Manage Your Profile</h1>
              <p className="text-xs sm:text-sm text-slate-500 mt-1 font-medium">
                Keep your academic details up to date for precise market calibration and salary benchmarking.
              </p>
            </div>

            {successMsg && (
              <div className="mb-6 p-4 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center gap-2.5 text-emerald-800 text-xs sm:text-sm font-semibold">
                <CheckCircle2 size={18} className="shrink-0 text-emerald-600" />
                <span>{successMsg}</span>
              </div>
            )}

            {errorMsg && (
              <div className="mb-6 p-4 rounded-2xl bg-rose-50 border border-rose-200 flex items-center gap-2.5 text-rose-800 text-xs sm:text-sm font-semibold">
                <AlertCircle size={18} className="shrink-0 text-rose-600" />
                <span>{errorMsg}</span>
              </div>
            )}

            <form onSubmit={handleSaveProfile} className="space-y-5">
              
              {/* Full Name */}
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">Full Name</label>
                <div className="relative">
                  <User size={16} className="absolute left-3.5 top-3.5 text-slate-400" />
                  <input
                    type="text"
                    required
                    value={userName}
                    onChange={(e) => setUserName(e.target.value)}
                    placeholder="e.g. Rahul Sharma"
                    className="pl-10 w-full p-3 text-sm bg-white/90 border border-slate-200/90 rounded-2xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none transition-all shadow-2xs text-slate-800 placeholder-slate-400"
                  />
                </div>
              </div>

              {/* Email (Read-Only) */}
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">Email Address</label>
                <div className="relative">
                  <Mail size={16} className="absolute left-3.5 top-3.5 text-slate-400" />
                  <input
                    type="email"
                    disabled
                    value={currentUser.email || ''}
                    className="pl-10 w-full p-3 text-sm border border-slate-200/90 rounded-2xl bg-slate-50 text-slate-400 cursor-not-allowed outline-none font-medium"
                  />
                </div>
                <span className="text-[11px] text-slate-400 mt-1 block font-medium">Account email address cannot be changed</span>
              </div>

              {/* College / University Selection */}
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1.5">College / University</label>
                <select
                  value={institution}
                  onChange={(e) => setInstitution(e.target.value)}
                  className="w-full p-3 text-xs sm:text-sm bg-white/90 border border-slate-200/90 rounded-2xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none transition-all shadow-2xs text-slate-800 font-medium"
                >
                  {INDIAN_UNIVERSITIES.map(u => (
                    <option key={u} value={u}>{u}</option>
                  ))}
                </select>
              </div>

              {/* Conditional Custom College/University Field */}
              {institution === 'Other' && (
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1.5">
                    Enter College / University Name <span className="text-rose-500">*</span>
                  </label>
                  <div className="relative">
                    <School size={16} className="absolute left-3.5 top-3.5 text-slate-400" />
                    <input
                      type="text"
                      required
                      value={customInstitution}
                      onChange={(e) => setCustomInstitution(e.target.value)}
                      placeholder="e.g. SRM Institute of Science & Technology, Chennai"
                      className="pl-10 w-full p-3 text-sm border border-indigo-300 rounded-2xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent bg-indigo-50/30 outline-none text-slate-800"
                    />
                  </div>
                </div>
              )}

              {/* Department & Grad Year */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1.5">Department</label>
                  <select
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    className="w-full p-3 text-xs sm:text-sm bg-white/90 border border-slate-200/90 rounded-2xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none transition-all shadow-2xs text-slate-800 font-medium"
                  >
                    {DEPARTMENTS.map(d => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1.5">Expected Graduation Year</label>
                  <select
                    value={gradYear}
                    onChange={(e) => setGradYear(e.target.value)}
                    className="w-full p-3 text-xs sm:text-sm bg-white/90 border border-slate-200/90 rounded-2xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none transition-all shadow-2xs text-slate-800 font-medium"
                  >
                    {['2024', '2025', '2026', '2027', '2028', '2029'].map(yr => (
                      <option key={yr} value={yr}>{yr}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 flex items-center justify-end gap-3">
                <button
                  type="submit"
                  disabled={isSaving}
                  className="px-7 py-3.5 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm shadow-md shadow-slate-900/10 hover:shadow-xl hover:scale-[1.01] transition-all flex items-center gap-2"
                >
                  {isSaving ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      Saving Changes...
                    </>
                  ) : (
                    <>
                      <Save size={16} /> Save Profile Changes
                    </>
                  )}
                </button>
              </div>

            </form>
          </div>
        </div>

      </div>
    </div>
  );
};

export default UserProfilePage;
