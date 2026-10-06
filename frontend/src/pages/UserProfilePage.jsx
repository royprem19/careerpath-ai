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
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 py-10">
      {/* Top Navigation Back Button */}
      <div className="mb-6 flex items-center justify-between">
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-gray-600 hover:text-gray-900 bg-white px-3 py-1.5 rounded-xl border border-gray-200 transition-colors"
        >
          <ArrowLeft size={14} /> Back
        </button>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold">
          <ShieldCheck size={14} /> Verified Student Account
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-8">
        
        {/* Left Column: Profile Card */}
        <div className="md:col-span-1 lg:col-span-1 space-y-6">
          <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100 text-center">
            <div className="w-20 h-20 rounded-full bg-gradient-to-tr from-primary-600 to-indigo-600 text-white font-extrabold text-2xl flex items-center justify-center mx-auto shadow-md mb-4">
              {currentUser.user_name ? currentUser.user_name.charAt(0).toUpperCase() : 'U'}
            </div>
            <h2 className="text-xl font-bold text-gray-900">{currentUser.user_name}</h2>
            <p className="text-xs text-gray-500 mt-0.5">{currentUser.email}</p>
            
            <div className="mt-4 pt-4 border-t border-gray-100 space-y-2 text-left text-xs">
              <div className="flex items-center justify-between text-gray-600">
                <span className="font-medium text-gray-500">Status</span>
                <span className="font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-md">Candidate</span>
              </div>
              <div className="flex items-center justify-between text-gray-600">
                <span className="font-medium text-gray-500">Cohort Year</span>
                <span className="font-semibold text-gray-800">{currentUser.graduation_year || 2026}</span>
              </div>
              <div className="flex flex-col gap-0.5 text-gray-600 pt-1">
                <span className="font-medium text-gray-500">Affiliation</span>
                <span className="font-semibold text-gray-800 truncate" title={currentUser.institution_name}>
                  {currentUser.institution_name || 'Institute of Technology'}
                </span>
              </div>
            </div>
          </div>

          {/* Quick Shortcuts */}
          <div className="bg-slate-100/70 rounded-3xl p-5 border border-slate-200/80 space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500">Quick Actions</h3>
            <Link
              to="/"
              className="w-full flex items-center gap-2 p-2.5 rounded-xl bg-white hover:bg-blue-50 text-gray-800 hover:text-primary-700 text-xs font-semibold shadow-2xs border border-gray-200/60 transition-colors"
            >
              <FileText size={15} className="text-primary-600" /> Upload / Update Resume
            </Link>
            <Link
              to="/roles"
              className="w-full flex items-center gap-2 p-2.5 rounded-xl bg-white hover:bg-blue-50 text-gray-800 hover:text-primary-700 text-xs font-semibold shadow-2xs border border-gray-200/60 transition-colors"
            >
              <Briefcase size={15} className="text-primary-600" /> Browse 81 Industry Roles
            </Link>
          </div>
        </div>

        {/* Right Column: Edit Form */}
        <div className="md:col-span-2 lg:col-span-3">
          <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-gray-100">
            <div className="mb-6">
              <h1 className="text-2xl font-bold text-gray-900">Manage Your Profile</h1>
              <p className="text-xs sm:text-sm text-gray-500 mt-1">
                Keep your academic details up to date for precise market calibration and salary benchmarking.
              </p>
            </div>

            {successMsg && (
              <div className="mb-6 p-4 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center gap-2.5 text-emerald-800 text-xs sm:text-sm">
                <CheckCircle2 size={18} className="shrink-0 text-emerald-600" />
                <span>{successMsg}</span>
              </div>
            )}

            {errorMsg && (
              <div className="mb-6 p-4 rounded-xl bg-red-50 border border-red-200 flex items-center gap-2.5 text-red-700 text-xs sm:text-sm">
                <AlertCircle size={18} className="shrink-0 text-red-600" />
                <span>{errorMsg}</span>
              </div>
            )}

            <form onSubmit={handleSaveProfile} className="space-y-5">
              
              {/* Full Name */}
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">Full Name</label>
                <div className="relative">
                  <User size={16} className="absolute left-3.5 top-3.5 text-gray-400" />
                  <input
                    type="text"
                    required
                    value={userName}
                    onChange={(e) => setUserName(e.target.value)}
                    placeholder="e.g. Rahul Sharma"
                    className="pl-10 w-full p-3 text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
                  />
                </div>
              </div>

              {/* Email (Read-Only) */}
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">Email Address</label>
                <div className="relative">
                  <Mail size={16} className="absolute left-3.5 top-3.5 text-gray-400" />
                  <input
                    type="email"
                    disabled
                    value={currentUser.email || ''}
                    className="pl-10 w-full p-3 text-sm border border-gray-200 rounded-xl bg-gray-50 text-gray-500 cursor-not-allowed outline-none"
                  />
                </div>
                <span className="text-[11px] text-gray-400 mt-1 block">Account email address cannot be changed</span>
              </div>

              {/* College / University Selection */}
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">College / University</label>
                <select
                  value={institution}
                  onChange={(e) => setInstitution(e.target.value)}
                  className="w-full p-3 text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white outline-none"
                >
                  {INDIAN_UNIVERSITIES.map(u => (
                    <option key={u} value={u}>{u}</option>
                  ))}
                </select>
              </div>

              {/* Conditional Custom College/University Field */}
              {institution === 'Other' && (
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1.5">
                    Enter College / University Name <span className="text-red-500">*</span>
                  </label>
                  <div className="relative">
                    <School size={16} className="absolute left-3.5 top-3.5 text-gray-400" />
                    <input
                      type="text"
                      required
                      value={customInstitution}
                      onChange={(e) => setCustomInstitution(e.target.value)}
                      placeholder="e.g. SRM Institute of Science & Technology, Chennai"
                      className="pl-10 w-full p-3 text-sm border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-blue-50/20 outline-none"
                    />
                  </div>
                </div>
              )}

              {/* Department & Grad Year */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1.5">Department</label>
                  <select
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    className="w-full p-3 text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white outline-none"
                  >
                    {DEPARTMENTS.map(d => (
                      <option key={d} value={d}>{d}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1.5">Expected Graduation Year</label>
                  <select
                    value={gradYear}
                    onChange={(e) => setGradYear(e.target.value)}
                    className="w-full p-3 text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white outline-none"
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
                  className="px-6 py-3 rounded-xl bg-primary-600 hover:bg-primary-700 text-white font-semibold text-sm shadow-sm transition-all flex items-center gap-2"
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
