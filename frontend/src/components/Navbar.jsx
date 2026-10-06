import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { LogIn, LogOut, User, GraduationCap } from 'lucide-react';

const Navbar = () => {
  const { currentUser, logout } = useAppContext();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16">
        <div className="flex justify-between h-16 items-center">
          
          {/* Brand Logo */}
          <div className="flex items-center space-x-3">
            <Link to="/" className="flex items-center space-x-2">
              <span className="text-2xl font-black bg-clip-text text-transparent bg-gradient-to-r from-primary-600 via-indigo-600 to-accent-600">
                CareerPath AI
              </span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center space-x-5 sm:space-x-8">
            <Link to="/" className="text-gray-700 hover:text-primary-600 text-sm font-semibold transition-colors">
              Home
            </Link>
            <Link to="/roles" className="text-gray-700 hover:text-primary-600 text-sm font-semibold transition-colors">
              Roles
            </Link>
            <Link to="/dashboard" className="text-gray-700 hover:text-primary-600 text-sm font-semibold transition-colors">
              Dashboard
            </Link>

            {/* Auth State Button */}
            {currentUser ? (
              <div className="flex items-center space-x-3 pl-3 border-l border-gray-200">
                <Link
                  to="/my-profile"
                  className="flex items-center gap-2 group px-2 py-1 rounded-xl hover:bg-gray-50 transition-colors"
                  title="View and Edit Profile"
                >
                  <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary-600 to-indigo-600 text-white font-bold text-xs flex items-center justify-center shadow-2xs">
                    {currentUser.user_name ? currentUser.user_name.charAt(0).toUpperCase() : 'U'}
                  </div>
                  <div className="hidden md:flex flex-col text-left">
                    <span className="text-xs font-bold text-gray-800 group-hover:text-primary-600 leading-tight">
                      {currentUser.user_name}
                    </span>
                    <span className="text-[10px] text-gray-400 font-medium">
                      My Profile
                    </span>
                  </div>
                </Link>

                <button
                  onClick={handleLogout}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-gray-700 hover:text-red-600 bg-gray-50 hover:bg-red-50 rounded-xl border border-gray-200 transition-colors"
                  title="Sign out of account"
                >
                  <LogOut size={13} />
                  <span className="hidden sm:inline">Sign Out</span>
                </button>
              </div>
            ) : (
              <div className="pl-3 border-l border-gray-200">
                <Link
                  to="/auth"
                  className="flex items-center gap-1.5 px-4 py-2 text-xs font-bold text-white bg-primary-600 hover:bg-primary-700 rounded-xl shadow-xs transition-all"
                >
                  <LogIn size={13} />
                  <span>Sign In</span>
                </Link>
              </div>
            )}

          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
