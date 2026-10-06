import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { verifyEmail, resendVerification } from '../services/api';
import { 
  CheckCircle2, AlertCircle, Mail, ArrowRight, 
  RotateCw, ShieldCheck, Sparkles, LogIn 
} from 'lucide-react';

const VerifyEmailPage = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const navigate = useNavigate();

  const [status, setStatus] = useState('loading'); // 'loading' | 'success' | 'already_verified' | 'error'
  const [message, setMessage] = useState('');
  const [verifiedEmail, setVerifiedEmail] = useState('');

  // Prevent duplicate execution in React StrictMode
  const hasRequestedRef = useRef(false);

  // Resend form states
  const [resendEmail, setResendEmail] = useState('');
  const [isResending, setIsResending] = useState(false);
  const [resendSuccess, setResendSuccess] = useState('');
  const [resendError, setResendError] = useState('');
  const [cooldown, setCooldown] = useState(0);

  useEffect(() => {
    let timer;
    if (cooldown > 0) {
      timer = setInterval(() => setCooldown(prev => prev - 1), 1000);
    }
    return () => clearInterval(timer);
  }, [cooldown]);

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setMessage('No verification token found in URL. Please click the full link provided in your email.');
      return;
    }

    if (hasRequestedRef.current) return;
    hasRequestedRef.current = true;

    const performVerification = async () => {
      try {
        const res = await verifyEmail(token);
        setStatus('success');
        setMessage(res.data.message || 'Email verified successfully! Your account is now active.');
        if (res.data.email) {
          setVerifiedEmail(res.data.email);
          setResendEmail(res.data.email);
        }
      } catch (err) {
        console.error('Email verification error:', err);
        const detail = err.response?.data?.detail || err.message || 'Verification link is invalid or has expired.';
        
        // If the token was already used, account is already verified
        if (detail.toLowerCase().includes('already been used') || detail.toLowerCase().includes('already verified')) {
          setStatus('already_verified');
          setMessage('Your email address has already been verified! Your account is active and you can sign in directly.');
        } else {
          setStatus('error');
          setMessage(detail);
        }
      }
    };

    performVerification();
  }, [token]);

  const handleResend = async (e) => {
    e.preventDefault();
    if (!resendEmail || cooldown > 0) return;

    setIsResending(true);
    setResendSuccess('');
    setResendError('');

    try {
      const res = await resendVerification(resendEmail.trim());
      setResendSuccess(res.data.message || 'A new verification link has been sent to your email.');
      setCooldown(60);
    } catch (err) {
      const detail = err.response?.data?.detail || err.message || 'Failed to resend verification email.';
      setResendError(detail);
    } finally {
      setIsResending(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full glass-card rounded-3xl shadow-2xl shadow-indigo-500/10 border border-white/90 overflow-hidden text-center">
        
        {/* Top Header */}
        <div className="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 p-8 text-white text-center relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-32 h-32 bg-indigo-500/20 rounded-full blur-xl pointer-events-none"></div>
          
          <div className="relative z-10">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 text-xs font-bold text-indigo-200 mb-3 backdrop-blur-xs border border-white/10 shadow-2xs">
              <Sparkles size={13} className="text-indigo-300" />
              <span>Security Gateway</span>
            </div>
            <h2 className="text-2xl font-black tracking-tight">Account Activation</h2>
            <p className="text-indigo-200/80 text-xs mt-1 font-medium">Proof of Email Ownership Verification</p>
          </div>
        </div>

        <div className="p-8 sm:p-9 space-y-6">

          {/* 1. Loading State */}
          {status === 'loading' && (
            <div className="py-8 space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
              <h3 className="text-lg font-black text-slate-900">Validating Verification Token...</h3>
              <p className="text-xs text-slate-500 font-medium">Checking cryptographic signature and expiration with the security gateway.</p>
            </div>
          )}

          {/* 2. Success State */}
          {status === 'success' && (
            <div className="space-y-5 py-4">
              <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto border border-emerald-200 shadow-2xs">
                <CheckCircle2 size={34} />
              </div>
              
              <div className="space-y-1.5">
                <h3 className="text-xl font-black text-slate-900">Email Verified!</h3>
                <p className="text-xs sm:text-sm text-slate-600 font-medium">{message}</p>
                {verifiedEmail && (
                  <p className="text-xs font-bold text-indigo-700 bg-indigo-50 py-1.5 px-3 rounded-xl inline-block mt-2 border border-indigo-200/70 shadow-2xs">
                    {verifiedEmail}
                  </p>
                )}
              </div>

              <div className="pt-4">
                <button
                  type="button"
                  onClick={() => navigate('/auth')}
                  className="w-full py-4 px-5 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm shadow-md shadow-slate-900/10 hover:shadow-xl hover:scale-[1.01] transition-all flex items-center justify-center gap-2"
                >
                  <LogIn size={16} /> Proceed to Sign In <ArrowRight size={16} />
                </button>
              </div>
            </div>
          )}

          {/* 2b. Already Verified State */}
          {status === 'already_verified' && (
            <div className="space-y-5 py-4">
              <div className="w-16 h-16 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center mx-auto border border-indigo-200 shadow-2xs">
                <ShieldCheck size={34} />
              </div>
              
              <div className="space-y-1.5">
                <h3 className="text-xl font-black text-slate-900">Account Already Verified!</h3>
                <p className="text-xs sm:text-sm text-slate-600 font-medium">{message}</p>
                <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-bold mt-2 shadow-2xs">
                  <CheckCircle2 size={14} className="text-emerald-600" />
                  Your account is active & ready
                </div>
              </div>

              <div className="pt-4">
                <button
                  type="button"
                  onClick={() => navigate('/auth')}
                  className="w-full py-4 px-5 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-sm shadow-md shadow-slate-900/10 hover:shadow-xl hover:scale-[1.01] transition-all flex items-center justify-center gap-2"
                >
                  <LogIn size={16} /> Sign In Now <ArrowRight size={16} />
                </button>
              </div>
            </div>
          )}

          {/* 3. Error State */}
          {status === 'error' && (
            <div className="space-y-5 py-2">
              <div className="w-16 h-16 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center mx-auto border border-rose-200 shadow-2xs">
                <AlertCircle size={34} />
              </div>

              <div className="space-y-1.5">
                <h3 className="text-xl font-black text-slate-900">Verification Failed</h3>
                <p className="text-xs sm:text-sm text-slate-600 font-medium">{message}</p>
              </div>

              {/* Resend Form */}
              <div className="pt-4 border-t border-slate-100 text-left">
                <p className="text-xs font-bold text-slate-700 mb-2">Need a new verification link?</p>
                
                {resendSuccess && (
                  <div className="mb-3 p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2 font-medium">
                    <CheckCircle2 size={15} className="shrink-0 text-emerald-600" />
                    <span>{resendSuccess}</span>
                  </div>
                )}

                {resendError && (
                  <div className="mb-3 p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2 font-medium">
                    <AlertCircle size={15} className="shrink-0 text-rose-600" />
                    <span>{resendError}</span>
                  </div>
                )}

                <form onSubmit={handleResend} className="space-y-3">
                  <div className="relative">
                    <Mail size={16} className="absolute left-3.5 top-3.5 text-slate-400" />
                    <input
                      type="email"
                      required
                      value={resendEmail}
                      onChange={(e) => setResendEmail(e.target.value)}
                      placeholder="Enter your registered email"
                      className="pl-10 w-full p-3 text-xs sm:text-sm bg-white/90 border border-slate-200/90 rounded-2xl focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none transition-all shadow-2xs text-slate-800 placeholder-slate-400"
                    />
                  </div>
                  
                  <button
                    type="submit"
                    disabled={isResending || cooldown > 0}
                    className={`w-full py-3 px-4 rounded-2xl font-bold text-xs flex items-center justify-center gap-1.5 transition-all ${
                      cooldown > 0
                        ? 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200'
                        : 'bg-slate-900 hover:bg-slate-800 text-white shadow-sm'
                    }`}
                  >
                    <RotateCw size={14} className={isResending ? 'animate-spin' : ''} />
                    {isResending 
                      ? 'Sending...' 
                      : cooldown > 0 
                      ? `Resend in ${cooldown}s` 
                      : 'Resend Verification Email'}
                  </button>
                </form>
              </div>

              <div className="pt-2">
                <Link
                  to="/auth"
                  className="text-xs font-bold text-indigo-600 hover:text-indigo-700 hover:underline"
                >
                  &larr; Back to Student Sign In
                </Link>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default VerifyEmailPage;
