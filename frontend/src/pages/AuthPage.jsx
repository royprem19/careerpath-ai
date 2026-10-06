import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { loginUser, registerUser } from '../services/api';
import { 
  Lock, Mail, User, School, Sparkles, ArrowRight, 
  CheckCircle2, AlertCircle 
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

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  
  // Form fields
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userName, setUserName] = useState('');
  const [institution, setInstitution] = useState('IIT Madras');
  const [customInstitution, setCustomInstitution] = useState('');
  const [department, setDepartment] = useState('Computer Science & Engineering');
  const [gradYear, setGradYear] = useState('2026');

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const { login } = useAppContext();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setLoading(true);

    try {
      if (isLogin) {
        const resp = await loginUser({ email, password });
        const { access_token, user } = resp.data;
        login(access_token, user);
        navigate('/');
      } else {
        const finalInstitution = institution === 'Other'
          ? (customInstitution.trim() || 'Other Institute')
          : institution;

        const payload = {
          email,
          password,
          user_name: userName,
          role: 'candidate',
          institution_name: finalInstitution,
          department,
          graduation_year: parseInt(gradYear, 10),
          skills: [] // Strictly empty on registration
        };
        const resp = await registerUser(payload);
        const { access_token, user } = resp.data;
        login(access_token, user);
        navigate('/');
      }
    } catch (err) {
      console.error('Auth error:', err);
      const detail = err.response?.data?.detail || err.message || 'Authentication failed. Please check your credentials.';
      setErrorMsg(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4 py-12">
      <div className="max-w-xl w-full bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
        
        {/* Header Banner */}
        <div className="bg-gradient-to-r from-blue-700 via-primary-600 to-indigo-700 p-8 text-white text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-xs font-semibold text-blue-100 mb-3 backdrop-blur-xs">
            <Sparkles size={14} className="text-yellow-300" />
            Career Intelligence Gateway
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            {isLogin ? 'Student Sign In' : 'Create Your Student Account'}
          </h2>
          <p className="text-blue-100 text-xs sm:text-sm mt-1.5 max-w-sm mx-auto">
            {isLogin 
              ? 'Access personalized skill gap benchmarks and predictive career roadmaps' 
              : 'Join the intelligent workforce ecosystem connecting engineering students to industry careers'}
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex border-b border-gray-100 bg-gray-50/50">
          <button
            type="button"
            onClick={() => { setIsLogin(true); setErrorMsg(''); }}
            className={`flex-1 py-3.5 text-sm font-bold text-center transition-all ${
              isLogin 
                ? 'bg-white text-primary-600 border-b-2 border-primary-600 shadow-xs' 
                : 'text-gray-500 hover:text-gray-800'
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => { setIsLogin(false); setErrorMsg(''); }}
            className={`flex-1 py-3.5 text-sm font-bold text-center transition-all ${
              !isLogin 
                ? 'bg-white text-primary-600 border-b-2 border-primary-600 shadow-xs' 
                : 'text-gray-500 hover:text-gray-800'
            }`}
          >
            Create Account
          </button>
        </div>

        <div className="p-6 sm:p-8 space-y-6">

          {errorMsg && (
            <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 flex items-center gap-2.5 text-red-700 text-xs sm:text-sm">
              <AlertCircle size={17} className="shrink-0 text-red-600" />
              <span>{errorMsg}</span>
            </div>
          )}

          {successMsg && (
            <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center gap-2.5 text-emerald-800 text-xs sm:text-sm">
              <CheckCircle2 size={17} className="shrink-0 text-emerald-600" />
              <span>{successMsg}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            
            {!isLogin && (
              <>
                {/* Full Name */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Full Name</label>
                  <div className="relative">
                    <User size={16} className="absolute left-3.5 top-3 text-gray-400" />
                    <input
                      type="text"
                      required
                      value={userName}
                      onChange={(e) => setUserName(e.target.value)}
                      placeholder="e.g. Rahul Sharma"
                      className="pl-10 w-full p-2.5 text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                  </div>
                </div>

                {/* University Selection */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">College / University</label>
                    <select
                      value={institution}
                      onChange={(e) => setInstitution(e.target.value)}
                      className="w-full p-2.5 text-xs sm:text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white"
                    >
                      {INDIAN_UNIVERSITIES.map(u => (
                        <option key={u} value={u}>{u}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">Department</label>
                    <select
                      value={department}
                      onChange={(e) => setDepartment(e.target.value)}
                      className="w-full p-2.5 text-xs sm:text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white"
                    >
                      {DEPARTMENTS.map(d => (
                        <option key={d} value={d}>{d}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Conditional Custom College/University Field */}
                {institution === 'Other' && (
                  <div>
                    <label className="block text-xs font-semibold text-gray-700 mb-1">
                      Enter College / University Name <span className="text-red-500">*</span>
                    </label>
                    <div className="relative">
                      <School size={16} className="absolute left-3.5 top-3 text-gray-400" />
                      <input
                        type="text"
                        required
                        value={customInstitution}
                        onChange={(e) => setCustomInstitution(e.target.value)}
                        placeholder="e.g. SRM Institute of Science & Technology, Chennai"
                        className="pl-10 w-full p-2.5 text-sm border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-blue-50/20"
                      />
                    </div>
                  </div>
                )}

                {/* Graduation Year */}
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Expected Graduation Year</label>
                  <select
                    value={gradYear}
                    onChange={(e) => setGradYear(e.target.value)}
                    className="w-full p-2.5 text-xs sm:text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white"
                  >
                    {['2024', '2025', '2026', '2027', '2028'].map(yr => (
                      <option key={yr} value={yr}>{yr}</option>
                    ))}
                  </select>
                </div>
              </>
            )}

            {/* Email Address */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">Email Address</label>
              <div className="relative">
                <Mail size={16} className="absolute left-3.5 top-3 text-gray-400" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="student@example.edu or rahul@mail.com"
                  className="pl-10 w-full p-2.5 text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">Password</label>
              <div className="relative">
                <Lock size={16} className="absolute left-3.5 top-3 text-gray-400" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="pl-10 w-full p-2.5 text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 rounded-xl bg-primary-600 hover:bg-primary-700 text-white font-semibold text-sm shadow-sm transition-all flex items-center justify-center gap-2 mt-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Processing...
                </>
              ) : (
                <>
                  {isLogin ? 'Sign In to Student Account' : 'Register & Access Career Intelligence'}
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>

        </div>
      </div>
    </div>
  );
};

export default AuthPage;
