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
        
        // If the token was already used, that means the account is already verified!
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
      <div className="max-w-md w-full bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden text-center">
        
        {/* Top Header */}
        <div className="bg-gradient-to-r from-blue-700 via-primary-600 to-indigo-700 p-8 text-white text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-xs font-semibold text-blue-100 mb-2 backdrop-blur-xs">
            <Sparkles size={14} className="text-yellow-300" />
            Security Gateway
          </div>
          <h2 className="text-2xl font-extrabold tracking-tight">Account Activation</h2>
          <p className="text-blue-100 text-xs mt-1">Proof of Email Ownership Verification</p>
        </div>

        <div className="p-8 space-y-6">

          {/* 1. Loading State */}
          {status === 'loading' && (
            <div className="py-8 space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
              <h3 className="text-lg font-bold text-gray-900">Validating Verification Token...</h3>
              <p className="text-xs text-gray-500">Checking signature and expiration with the security gateway.</p>
            </div>
          )}

          {/* 2. Success State */}
          {status === 'success' && (
            <div className="space-y-5 py-4">
              <div className="w-16 h-16 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto border-2 border-emerald-200">
                <CheckCircle2 size={36} />
              </div>
              
              <div className="space-y-1.5">
                <h3 className="text-xl font-extrabold text-gray-900">Email Verified!</h3>
                <p className="text-xs sm:text-sm text-gray-600">{message}</p>
                {verifiedEmail && (
                  <p className="text-xs font-semibold text-primary-600 bg-primary-50 py-1.5 px-3 rounded-lg inline-block mt-2">
                    {verifiedEmail}
                  </p>
                )}
              </div>

              <div className="pt-4">
                <button
                  type="button"
                  onClick={() => navigate('/auth')}
                  className="w-full py-3.5 px-4 rounded-xl bg-primary-600 hover:bg-primary-700 text-white font-bold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2"
                >
                  <LogIn size={16} /> Proceed to Sign In <ArrowRight size={16} />
                </button>
              </div>
            </div>
          )}

          {/* 2b. Already Verified State */}
          {status === 'already_verified' && (
            <div className="space-y-5 py-4">
              <div className="w-16 h-16 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mx-auto border-2 border-blue-200">
                <ShieldCheck size={36} />
              </div>
              
              <div className="space-y-1.5">
                <h3 className="text-xl font-extrabold text-gray-900">Account Already Verified!</h3>
                <p className="text-xs sm:text-sm text-gray-600">{message}</p>
                <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-semibold mt-2">
                  <CheckCircle2 size={14} className="text-emerald-600" />
                  Your account is active & ready
                </div>
              </div>

              <div className="pt-4">
                <button
                  type="button"
                  onClick={() => navigate('/auth')}
                  className="w-full py-3.5 px-4 rounded-xl bg-primary-600 hover:bg-primary-700 text-white font-bold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2"
                >
                  <LogIn size={16} /> Sign In Now <ArrowRight size={16} />
                </button>
              </div>
            </div>
          )}

          {/* 3. Error State */}
          {status === 'error' && (
            <div className="space-y-5 py-2">
              <div className="w-16 h-16 rounded-full bg-rose-50 text-rose-600 flex items-center justify-center mx-auto border-2 border-rose-200">
                <AlertCircle size={36} />
              </div>

              <div className="space-y-1.5">
                <h3 className="text-xl font-extrabold text-gray-900">Verification Failed</h3>
                <p className="text-xs sm:text-sm text-gray-600">{message}</p>
              </div>

              {/* Resend Form */}
              <div className="pt-2 border-t border-gray-100 text-left">
                <p className="text-xs font-bold text-gray-700 mb-2">Need a new verification link?</p>
                
                {resendSuccess && (
                  <div className="mb-3 p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2">
                    <CheckCircle2 size={15} className="shrink-0 text-emerald-600" />
                    <span>{resendSuccess}</span>
                  </div>
                )}

                {resendError && (
                  <div className="mb-3 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
                    <AlertCircle size={15} className="shrink-0 text-rose-600" />
                    <span>{resendError}</span>
                  </div>
                )}

                <form onSubmit={handleResend} className="space-y-3">
                  <div className="relative">
                    <Mail size={16} className="absolute left-3.5 top-3.5 text-gray-400" />
                    <input
                      type="email"
                      required
                      value={resendEmail}
                      onChange={(e) => setResendEmail(e.target.value)}
                      placeholder="Enter your registered email"
                      className="pl-10 w-full p-2.5 text-xs sm:text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
                    />
                  </div>
                  
                  <button
                    type="submit"
                    disabled={isResending || cooldown > 0}
                    className={`w-full py-2.5 px-4 rounded-xl font-bold text-xs flex items-center justify-center gap-1.5 transition-all ${
                      cooldown > 0
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        : 'bg-slate-800 hover:bg-slate-900 text-white shadow-xs'
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
                  className="text-xs font-semibold text-primary-600 hover:text-primary-700"
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
