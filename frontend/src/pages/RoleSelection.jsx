import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { Search, ChevronRight, Briefcase, IndianRupee, Clock, AlertCircle } from 'lucide-react';
import { getRoles } from '../services/api';

const RoleSelection = () => {
  const [roles, setRoles] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const { userProfile, setSelectedRole } = useAppContext();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRoles = async () => {
      try {
        setLoading(true);
        const res = await getRoles();
        if (Array.isArray(res.data) && res.data.length > 0) {
          setRoles(res.data);
        } else {
          setErrorMsg('No roles found in the database.');
        }
      } catch (err) {
        console.error('Failed to fetch roles:', err);
        setErrorMsg('Could not connect to the API server. Please check if the backend is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchRoles();
  }, []);

  const filteredRoles = roles.filter(role => 
    (role.title && role.title.toLowerCase().includes(searchTerm.toLowerCase())) || 
    (role.description && role.description.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (role.category && role.category.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const handleSelectRole = (role) => {
    setSelectedRole(role);
    if (!userProfile?.skills || userProfile.skills.length === 0) {
      navigate('/');
    } else {
      navigate('/dashboard');
    }
  };

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 py-10">
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-200 text-blue-700 text-xs font-semibold mb-2">
            Target Occupation Benchmark
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Select Target Role</h1>
          <p className="text-gray-600">Choose an industry role to benchmark your skills, quantify the gap, and generate a customized roadmap.</p>
        </div>
        <button
          onClick={() => {
            if (roles.length > 0) {
              setSelectedRole(roles[0]);
            }
            if (!userProfile?.skills || userProfile.skills.length === 0) {
              navigate('/');
            } else {
              navigate('/dashboard');
            }
          }}
          className="py-2.5 px-6 rounded-xl text-primary-700 bg-primary-50 border border-primary-200 hover:bg-primary-100 font-semibold transition-colors whitespace-nowrap text-sm"
        >
          Compare All Roles
        </button>
      </div>

      {errorMsg && (
        <div className="mb-6 p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-center gap-3 text-amber-800 text-sm">
          <AlertCircle size={18} className="shrink-0 text-amber-600" />
          <span>{errorMsg}</span>
        </div>
      )}

      <div className="relative mb-8 max-w-4xl">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
          <Search size={20} className="text-gray-400" />
        </div>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search by title, category, or skill (e.g. Data Scientist, Cloud, DevOps)..."
          className="pl-11 block w-full border-gray-200 rounded-xl border focus:ring-2 focus:ring-primary-500 focus:border-primary-500 p-3.5 shadow-sm text-base bg-white"
        />
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-24 space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="text-gray-500 text-sm font-medium">Fetching real industry roles from Supabase...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredRoles.map((role) => {
            const skillCount = (role.essential_skills?.length || 0) + (role.optional_skills?.length || 0);
            return (
              <div 
                key={role.id}
                onClick={() => handleSelectRole(role)}
                className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm hover:shadow-md hover:border-primary-300 cursor-pointer transition-all flex flex-col justify-between group"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-primary-50 w-11 h-11 rounded-xl flex items-center justify-center text-primary-600 group-hover:bg-primary-600 group-hover:text-white transition-colors">
                      <Briefcase size={22} />
                    </div>
                    {role.category && (
                      <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 bg-slate-100 px-2.5 py-1 rounded-full">
                        {role.category}
                      </span>
                    )}
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
                    {role.title}
                  </h3>
                  <p className="text-gray-600 mb-4 text-sm line-clamp-2">
                    {role.description}
                  </p>
                </div>

                <div className="space-y-3 pt-4 border-t border-gray-50">
                  <div className="flex items-center justify-between text-xs text-gray-500 font-medium">
                    <span className="flex items-center gap-1">
                      <IndianRupee size={13} className="text-emerald-600" />
                      {role.avg_salary || 'Competitive'}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock size={13} />
                      {role.experience_range || '0-2 yrs'}
                    </span>
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <span className="text-xs font-semibold text-primary-700 bg-primary-50 px-2 py-0.5 rounded-md">
                      {skillCount} Skills Defined
                    </span>
                    <span className="flex items-center text-xs font-semibold text-primary-600 group-hover:translate-x-1 transition-transform">
                      Analyze Fit <ChevronRight size={16} />
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
          {filteredRoles.length === 0 && (
            <div className="col-span-full text-center py-16 bg-white rounded-2xl border border-gray-100 p-8">
              <p className="text-gray-500 text-base mb-2">No roles found matching "{searchTerm}".</p>
              <button 
                onClick={() => setSearchTerm('')}
                className="text-primary-600 font-semibold text-sm hover:underline"
              >
                Clear Search Filter
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RoleSelection;
