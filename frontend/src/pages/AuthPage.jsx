import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { loginUser, registerUser, resendVerification } from '../services/api';
import { 
  Lock, Mail, User, School, Sparkles, ArrowRight, 
  CheckCircle2, AlertCircle, MailCheck, RotateCw, LogIn 
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

const KNOWN_EMAIL_TYPOS = {
  "gmai.com": "gmail.com",
  "gamil.com": "gmail.com",
  "gmial.com": "gmail.com",
  "gmaill.com": "gmail.com",
  "gmaii.com": "gmail.com",
  "gma.com": "gmail.com",
  "gmeil.com": "gmail.com",
  "gmail.co": "gmail.com",
  "gmail.cm": "gmail.com",
  "gmal.com": "gmail.com",
  "gemail.com": "gmail.com",
  "yaho.com": "yahoo.com",
  "yahooo.com": "yahoo.com",
  "yaho.co": "yahoo.com",
  "yhaoo.com": "yahoo.com",
  "hotmial.com": "hotmail.com",
  "hotmai.com": "hotmail.com",
  "hotamil.com": "hotmail.com",
  "outlok.com": "outlook.com",
  "outloo.com": "outlook.com",
  "ootlook.com": "outlook.com",
  "icoud.com": "icloud.com",
  "iclod.com": "icloud.com"
};

const checkEmailDomainTypo = (emailStr) => {
  if (!emailStr || !emailStr.includes('@')) return null;
  const parts = emailStr.trim().split('@');
  if (parts.length !== 2) return null;
  const domain = parts[1].toLowerCase().trim();
  if (KNOWN_EMAIL_TYPOS[domain]) {
    return {
      invalidDomain: domain,
      suggestedEmail: `${parts[0]}@${KNOWN_EMAIL_TYPOS[domain]}`
    };
  }
  return null;
};

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

  // UI & Flow states
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  // Email verification states
  const [verificationSent, setVerificationSent] = useState(false);
  const [registeredEmail, setRegisteredEmail] = useState('');
  const [unverifiedLoginEmail, setUnverifiedLoginEmail] = useState('');
  const [isResending, setIsResending] = useState(false);
  const [resendMsg, setResendMsg] = useState('');
  const [cooldown, setCooldown] = useState(0);

  const { login } = useAppContext();
  const navigate = useNavigate();

  const domainSuggestion = checkEmailDomainTypo(email);

  // Cooldown countdown timer
  useEffect(() => {
    let timer;
    if (cooldown > 0) {
      timer = setInterval(() => setCooldown(prev => prev - 1), 1000);
    }
    return () => clearInterval(timer);
  }, [cooldown]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setUnverifiedLoginEmail('');

    if (!isLogin && domainSuggestion) {
      setErrorMsg(`Invalid email domain '${domainSuggestion.invalidDomain}'. Did you mean '${domainSuggestion.suggestedEmail}'?`);
      return;
    }

    setLoading(true);

    try {
      if (isLogin) {
        const resp = await loginUser({ email: email.trim(), password });
        const { access_token, user } = resp.data;
        login(access_token, user);
        navigate('/');
      } else {
        const finalInstitution = institution === 'Other'
          ? (customInstitution.trim() || 'Other Institute')
          : institution;

        const payload = {
          email: email.trim(),
          password,
          user_name: userName.trim(),
          role: 'candidate',
          institution_name: finalInstitution,
          department,
          graduation_year: parseInt(gradYear, 10),
          skills: [] // Strictly empty on registration
        };

        const resp = await registerUser(payload);
        
        // Account created with emailVerified = false. DO NOT issue JWT.
        setRegisteredEmail(email.trim());
        setVerificationSent(true);
        setSuccessMsg(resp.data.message || 'Account created! Please verify your email.');
      }
    } catch (err) {
      console.error('Auth error:', err);
      const detail = err.response?.data?.detail || err.message || 'Authentication failed. Please check your credentials.';
      
      // Check for unverified email login rejection
      if (err.response?.status === 403 || detail.toLowerCase().includes('verify your email')) {
        setUnverifiedLoginEmail(email.trim());
      }
      
      setErrorMsg(detail);
    } finally {
      setLoading(false);
    }
  };

  const handleResendVerification = async (targetEmail) => {
    const toEmail = targetEmail || registeredEmail || email;
    if (!toEmail || cooldown > 0) return;

    setIsResending(true);
    setResendMsg('');

    try {
      const res = await resendVerification(toEmail.trim());
      setResendMsg(res.data.message || 'Verification link re-sent successfully!');
      setCooldown(60);
    } catch (err) {
      const detail = err.response?.data?.detail || err.message || 'Failed to resend verification email.';
      setResendMsg(`Notice: ${detail}`);
    } finally {
      setIsResending(false);
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
            {verificationSent 
              ? 'Verify Your Email Address' 
              : isLogin 
              ? 'Student Sign In' 
              : 'Create Your Student Account'}
          </h2>
          <p className="text-blue-100 text-xs sm:text-sm mt-1.5 max-w-sm mx-auto">
            {verificationSent
              ? 'Account created! Please check your email and click the verification link to activate your account.'
              : isLogin 
              ? 'Access personalized skill gap benchmarks and predictive career roadmaps' 
              : 'Join the intelligent workforce ecosystem connecting engineering students to industry careers'}
          </p>
        </div>

        {/* ==============================================================================
            SCREEN 1: EMAIL VERIFICATION REQUIRED NOTICE
        ============================================================================== */}
        {verificationSent ? (
          <div className="p-6 sm:p-8 space-y-6 text-center">
            <div className="w-16 h-16 rounded-full bg-blue-50 text-primary-600 flex items-center justify-center mx-auto border-2 border-primary-200">
              <MailCheck size={36} />
            </div>

            <div className="space-y-2">
              <h3 className="text-xl font-extrabold text-gray-900">Check Your Inbox</h3>
              <p className="text-xs sm:text-sm text-gray-600 max-w-md mx-auto">
                Account created! We've sent a secure, time-limited verification link to:
              </p>
              <div className="bg-slate-50 border border-slate-200 p-3 rounded-xl inline-block max-w-full">
                <span className="font-mono text-sm font-bold text-primary-700">{registeredEmail}</span>
              </div>
              <p className="text-xs text-gray-500 pt-2">
                Click the verification link in the email to activate your account. You will not be able to log in or access career benchmarks until your email is verified.
              </p>
              <p className="text-[11px] text-rose-500 font-semibold">
                ⏱️ Link expires in 30 minutes.
              </p>
            </div>

            {resendMsg && (
              <div className="p-3.5 rounded-xl bg-blue-50 border border-blue-200 text-blue-800 text-xs sm:text-sm">
                {resendMsg}
              </div>
            )}

            <div className="pt-2 space-y-3">
              <button
                type="button"
                onClick={() => handleResendVerification(registeredEmail)}
                disabled={isResending || cooldown > 0}
                className={`w-full py-3 px-4 rounded-xl font-bold text-xs sm:text-sm flex items-center justify-center gap-2 transition-all ${
                  cooldown > 0
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
                    : 'bg-white hover:bg-gray-50 text-gray-800 border border-gray-300 shadow-2xs'
                }`}
              >
                <RotateCw size={15} className={isResending ? 'animate-spin' : ''} />
                {isResending 
                  ? 'Sending verification email...' 
                  : cooldown > 0 
                  ? `Resend available in ${cooldown}s` 
                  : 'Resend Verification Email'}
              </button>

              <button
                type="button"
                onClick={() => {
                  setVerificationSent(false);
                  setIsLogin(true);
                  setErrorMsg('');
                  setSuccessMsg('');
                }}
                className="w-full py-3 px-4 rounded-xl bg-primary-600 hover:bg-primary-700 text-white font-bold text-xs sm:text-sm shadow-md transition-all flex items-center justify-center gap-1.5"
              >
                <LogIn size={15} /> Back to Sign In
              </button>
            </div>
          </div>
        ) : (
          /* ==============================================================================
             SCREEN 2: NORMAL SIGN IN & REGISTRATION TABS
          ============================================================================== */
          <>
            {/* Tab Switcher */}
            <div className="flex border-b border-gray-100 bg-gray-50/50">
              <button
                type="button"
                onClick={() => { setIsLogin(true); setErrorMsg(''); setUnverifiedLoginEmail(''); }}
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
                onClick={() => { setIsLogin(false); setErrorMsg(''); setUnverifiedLoginEmail(''); }}
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
                <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs sm:text-sm space-y-2">
                  <div className="flex items-center gap-2.5">
                    <AlertCircle size={17} className="shrink-0 text-red-600" />
                    <span className="font-medium">{errorMsg}</span>
                  </div>

                  {/* Quick Resend button for unverified accounts trying to log in */}
                  {unverifiedLoginEmail && (
                    <div className="pt-2 border-t border-red-200/60 flex items-center justify-between">
                      <span className="text-[11px] text-red-600">Need a fresh activation link?</span>
                      <button
                        type="button"
                        onClick={() => handleResendVerification(unverifiedLoginEmail)}
                        disabled={isResending || cooldown > 0}
                        className="text-xs font-bold text-primary-700 hover:underline flex items-center gap-1"
                      >
                        <RotateCw size={12} className={isResending ? 'animate-spin' : ''} />
                        {cooldown > 0 ? `Resend (${cooldown}s)` : 'Resend Verification Link'}
                      </button>
                    </div>
                  )}
                </div>
              )}

              {resendMsg && (
                <div className="p-3.5 rounded-xl bg-blue-50 border border-blue-200 text-blue-800 text-xs sm:text-sm flex items-center gap-2">
                  <CheckCircle2 size={16} className="shrink-0 text-blue-600" />
                  <span>{resendMsg}</span>
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
                  <div className="flex items-center justify-between mb-1">
                    <label className="block text-xs font-semibold text-gray-700">Email Address</label>
                    {domainSuggestion && (
                      <span className="text-[11px] text-amber-600 font-medium animate-pulse">Typo detected</span>
                    )}
                  </div>
                  <div className="relative">
                    <Mail size={16} className="absolute left-3.5 top-3 text-gray-400" />
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => {
                        setEmail(e.target.value);
                        setErrorMsg('');
                      }}
                      placeholder="student@college.edu.in"
                      className={`pl-10 w-full p-2.5 text-sm border rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                        domainSuggestion ? 'border-amber-400 bg-amber-50/20' : 'border-gray-200'
                      }`}
                    />
                  </div>

                  {/* Inline Domain Typo Suggestion Pill */}
                  {domainSuggestion && (
                    <div className="mt-2 p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex items-center justify-between shadow-xs">
                      <div className="flex items-center gap-1.5 overflow-hidden">
                        <AlertCircle size={14} className="shrink-0 text-amber-600" />
                        <span className="truncate">
                          Did you mean <strong className="text-amber-950 font-mono">{domainSuggestion.suggestedEmail}</strong>?
                        </span>
                      </div>
                      <button
                        type="button"
                        onClick={() => {
                          setEmail(domainSuggestion.suggestedEmail);
                          setErrorMsg('');
                        }}
                        className="ml-2 shrink-0 px-2.5 py-1 bg-amber-600 hover:bg-amber-700 text-white font-semibold rounded-lg text-[11px] transition shadow-xs"
                      >
                        Fix to {KNOWN_EMAIL_TYPOS[domainSuggestion.invalidDomain]}
                      </button>
                    </div>
                  )}
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
                  className="w-full py-3 px-4 rounded-xl bg-primary-600 hover:bg-primary-700 text-white font-bold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center"
                >
                  {loading ? (
                    <div className="flex items-center gap-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>{isLogin ? 'Authenticating...' : 'Creating Account...'}</span>
                    </div>
                  ) : (
                    <>
                      {isLogin ? 'Sign In' : 'Create Student Account'}
                      <ArrowRight size={16} className="ml-2" />
                    </>
                  )}
                </button>
              </form>

              {!isLogin && (
                <p className="text-[11px] text-gray-500 text-center">
                  By creating an account, a verification link will be sent to your email to prove ownership before activation.
                </p>
              )}
            </div>
          </>
        )}

      </div>
    </div>
  );
};

export default AuthPage;
