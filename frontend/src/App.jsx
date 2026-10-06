import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AppProvider } from './context/AppProvider';
import Navbar from './components/Navbar';
import UploadPage from './pages/UploadPage';
import ProfileReview from './pages/ProfileReview';
import RoleSelection from './pages/RoleSelection';
import Dashboard from './pages/Dashboard';
import AuthPage from './pages/AuthPage';
import UserProfilePage from './pages/UserProfilePage';
import VerifyEmailPage from './pages/VerifyEmailPage';

function App() {
  return (
    <AppProvider>
      <Router>
        <div className="min-h-screen flex flex-col font-sans text-slate-900 bg-slate-50">
          <Navbar />
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<UploadPage />} />
              <Route path="/profile" element={<ProfileReview />} />
              <Route path="/roles" element={<RoleSelection />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/auth" element={<AuthPage />} />
              <Route path="/my-profile" element={<UserProfilePage />} />
              <Route path="/verify-email" element={<VerifyEmailPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AppProvider>
  );
}

export default App;
