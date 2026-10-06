import React, { useState, useEffect } from 'react';
import { AppContext } from './AppContext';

export const AppProvider = ({ children }) => {
  const [userProfile, setUserProfile] = useState({
    skills: [],
    education: [],
    experience: [],
  });
  
  // Auth state
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(null);

  // Core application state
  const [selectedRole, setSelectedRole] = useState(null);
  const [gapAnalysis, setGapAnalysis] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [roadmap, setRoadmap] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Restore session from localStorage on initial render
  useEffect(() => {
    const savedToken = localStorage.getItem('careerpath_token');
    const savedUser = localStorage.getItem('careerpath_user');
    if (savedToken && savedUser) {
      try {
        const parsed = JSON.parse(savedUser);
        if (parsed.skills) {
          delete parsed.skills;
          localStorage.setItem('careerpath_user', JSON.stringify(parsed));
        }
        setCurrentUser(parsed);
        setToken(savedToken);
      } catch (e) {
        console.warn('Failed to parse saved user:', e);
      }
    }

    // Always start with a clean empty profile on page refresh
    sessionStorage.removeItem('careerpath_active_skills');
    setUserProfile({
      skills: [],
      education: [],
      experience: {},
      certifications: []
    });
    setSelectedRole(null);
    setGapAnalysis(null);
  }, []);

  const login = (authToken, user) => {
    const cleanUser = { ...user };
    delete cleanUser.skills;
    setToken(authToken);
    setCurrentUser(cleanUser);
    localStorage.setItem('careerpath_token', authToken);
    localStorage.setItem('careerpath_user', JSON.stringify(cleanUser));

    // Fresh sign in always resets resume skills
    sessionStorage.removeItem('careerpath_active_skills');
    setUserProfile({
      skills: [],
      education: cleanUser.department ? [cleanUser.department] : [],
      experience: {},
      certifications: []
    });
    setSelectedRole(null);
    setGapAnalysis(null);
  };

  const clearProfile = () => {
    sessionStorage.removeItem('careerpath_active_skills');
    setUserProfile({
      skills: [],
      education: [],
      experience: {},
      certifications: []
    });
    setSelectedRole(null);
    setGapAnalysis(null);
    const savedUser = localStorage.getItem('careerpath_user');
    if (savedUser) {
      try {
        const u = JSON.parse(savedUser);
        delete u.skills;
        localStorage.setItem('careerpath_user', JSON.stringify(u));
      } catch (e) {}
    }
  };

  const logout = () => {
    setToken(null);
    setCurrentUser(null);
    localStorage.removeItem('careerpath_token');
    localStorage.removeItem('careerpath_user');
    sessionStorage.removeItem('careerpath_active_skills');
    clearProfile();
  };

  const updateUser = (updatedFields) => {
    setCurrentUser(prev => {
      const merged = { ...prev, ...updatedFields };
      localStorage.setItem('careerpath_user', JSON.stringify(merged));
      return merged;
    });
  };

  const value = {
    userProfile,
    setUserProfile,
    currentUser,
    setCurrentUser,
    updateUser,
    token,
    login,
    logout,
    clearProfile,
    selectedRole,
    setSelectedRole,
    gapAnalysis,
    setGapAnalysis,
    recommendations,
    setRecommendations,
    roadmap,
    setRoadmap,
    loading,
    setLoading,
    error,
    setError,
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

export default AppProvider;
