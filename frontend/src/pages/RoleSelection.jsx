import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import { Search, ChevronRight, Briefcase, IndianRupee, Clock, AlertCircle, Sparkles, Filter } from 'lucide-react';
import { getRoles } from '../services/api';

const RoleSelection = () => {
  const [roles, setRoles] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
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

  const categories = ['All', ...new Set(roles.map(r => r.category).filter(Boolean))];

  const filteredRoles = roles.filter(role => {
    const matchesCategory = selectedCategory === 'All' || role.category === selectedCategory;
    const matchesSearch = 
      (role.title && role.title.toLowerCase().includes(searchTerm.toLowerCase())) || 
      (role.description && role.description.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (role.category && role.category.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const handleSelectRole = (role) => {
    setSelectedRole(role);
    if (!userProfile?.skills || userProfile.skills.length === 0) {
      navigate('/');
    } else {
      navigate('/dashboard');
    }
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-8 py-10">
      
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-50 border border-indigo-200/80 text-indigo-700 text-xs font-bold uppercase tracking-wider mb-3 shadow-2xs">
            <Sparkles size={13} className="text-indigo-600" />
            <span>Target Occupation Benchmark</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight mb-2">
            Select Target Role
          </h1>
          <p className="text-slate-500 font-medium text-sm sm:text-base max-w-2xl">
            Choose an industry role to benchmark your skills, quantify the gap, and generate a customized roadmap.
          </p>
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
          className="py-3 px-6 rounded-2xl border-2 border-indigo-300 hover:border-indigo-400 text-indigo-700 bg-white hover:bg-indigo-50/60 font-bold transition-all shadow-2xs whitespace-nowrap text-xs sm:text-sm self-start md:self-auto"
        >
          Compare All Roles
        </button>
      </div>

      {errorMsg && (
        <div className="mb-6 p-4 rounded-2xl bg-amber-50 border border-amber-200 flex items-center gap-3 text-amber-900 text-sm shadow-xs font-medium">
          <AlertCircle size={20} className="shrink-0 text-amber-600" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Search and Filters */}
      <div className="space-y-4 mb-8">
        <div className="relative max-w-4xl">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
            <Search size={20} />
          </div>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by title, category, or skills (e.g. Data Scientist, Cloud, DevOps)..."
            className="pl-12 pr-4 py-3.5 block w-full rounded-2xl border border-slate-200/90 bg-white/90 focus:ring-2 focus:ring-indigo-400 focus:border-transparent outline-none shadow-sm text-sm sm:text-base text-slate-800 placeholder-slate-400 transition-all"
          />
        </div>

        {/* Category Pills */}
        {categories.length > 1 && (
          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
            <Filter size={15} className="text-slate-400 shrink-0 ml-1 mr-1" />
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`text-xs font-bold px-3.5 py-1.5 rounded-xl whitespace-nowrap transition-all shadow-2xs ${
                  selectedCategory === cat
                    ? 'bg-slate-900 text-white shadow-xs'
                    : 'bg-white/80 text-slate-600 hover:bg-white border border-slate-200/80 hover:text-slate-900'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        )}
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-24 space-y-4 glass-card rounded-3xl border border-white/90">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          <p className="text-slate-500 text-sm font-semibold">Fetching real industry roles from Supabase...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredRoles.map((role) => {
            const skillCount = (role.essential_skills?.length || 0) + (role.optional_skills?.length || 0);
            return (
              <div 
                key={role.id}
                onClick={() => handleSelectRole(role)}
                className="glass-card glass-card-hover rounded-3xl p-6 sm:p-7 border border-white/90 shadow-xl shadow-indigo-500/5 cursor-pointer transition-all duration-300 flex flex-col justify-between group"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 rounded-2xl bg-indigo-50/90 text-indigo-600 flex items-center justify-center border border-indigo-100 group-hover:bg-slate-900 group-hover:text-white transition-all shadow-2xs">
                      <Briefcase size={22} />
                    </div>
                    {role.category && (
                      <span className="text-[10px] font-extrabold uppercase tracking-wider text-indigo-700 bg-indigo-50/90 border border-indigo-200/70 px-2.5 py-1 rounded-full shadow-2xs">
                        {role.category}
                      </span>
                    )}
                  </div>
                  <h3 className="text-lg font-black text-slate-900 mb-2 group-hover:text-indigo-600 transition-colors">
                    {role.title}
                  </h3>
                  <p className="text-slate-500 mb-5 text-xs sm:text-sm line-clamp-2 leading-relaxed font-normal">
                    {role.description}
                  </p>
                </div>

                <div className="space-y-3 pt-4 border-t border-slate-100/90">
                  <div className="flex items-center justify-between text-xs font-semibold text-slate-600">
                    <span className="flex items-center gap-1 text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded-lg border border-emerald-100">
                      <IndianRupee size={12} />
                      {role.avg_salary || 'Competitive'}
                    </span>
                    <span className="flex items-center gap-1 text-slate-500 bg-slate-50 px-2 py-0.5 rounded-lg border border-slate-200/60">
                      <Clock size={12} />
                      {role.experience_range || '0-2 yrs'}
                    </span>
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <span className="text-xs font-bold text-indigo-700 bg-indigo-50/90 px-2.5 py-1 rounded-xl border border-indigo-200/60 shadow-2xs">
                      {skillCount} Skills Defined
                    </span>
                    <span className="flex items-center text-xs font-black text-slate-900 group-hover:text-indigo-600 group-hover:translate-x-1 transition-all">
                      Analyze Fit <ChevronRight size={15} />
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
          {filteredRoles.length === 0 && (
            <div className="col-span-full text-center py-16 glass-card rounded-3xl border border-white/90 p-8">
              <p className="text-slate-500 text-base mb-3 font-semibold">No roles found matching "{searchTerm}".</p>
              <button 
                onClick={() => { setSearchTerm(''); setSelectedCategory('All'); }}
                className="text-indigo-600 font-bold text-sm hover:underline"
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
