import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import SkillTag from '../components/SkillTag';
import { GraduationCap, Briefcase, Plus, ArrowRight, LayoutDashboard, AlertCircle } from 'lucide-react';

const ProfileReview = () => {
  const { userProfile, setUserProfile } = useAppContext();
  const navigate = useNavigate();
  const [newSkill, setNewSkill] = useState('');

  const handleRemoveSkill = (skillToRemove) => {
    setUserProfile({
      ...userProfile,
      skills: userProfile.skills.filter(s => s !== skillToRemove)
    });
  };

  const handleAddSkill = (e) => {
    if (e.key === 'Enter' && newSkill.trim()) {
      e.preventDefault();
      if (!userProfile.skills.includes(newSkill.trim())) {
        setUserProfile({
          ...userProfile,
          skills: [...(userProfile.skills || []), newSkill.trim()]
        });
      }
      setNewSkill('');
    }
  };

  const hasFewSkills = (userProfile?.skills?.length || 0) < 3;
  const isZeroSkills = (userProfile?.skills?.length || 0) === 0;

  return (
    <div className="w-full px-4 sm:px-8 lg:px-12 xl:px-16 py-10">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Review Your Profile</h1>
      <p className="text-gray-600 mb-6">We've extracted the following information. You can add or remove skills to ensure accuracy.</p>

      {/* Uncertainty & Low-Confidence Guardrail Banner */}
      {(userProfile?.warning_message || hasFewSkills) && (
        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 flex items-start gap-3.5 text-amber-900 mb-6 shadow-xs">
          <AlertCircle size={22} className="shrink-0 text-amber-600 mt-0.5" />
          <div className="space-y-1.5 w-full">
            <div className="flex items-center justify-between">
              <p className="font-bold text-sm text-amber-900">
                {userProfile?.is_scanned_or_low_text 
                  ? "Scanned or Low-Text Document Detected" 
                  : "Low Confidence Skill Extraction"}
              </p>
              <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-200 text-amber-800">
                Action Recommended
              </span>
            </div>
            <p className="text-xs text-amber-800 leading-relaxed">
              {userProfile?.warning_message || "We detected very few skills from your document. To prevent inaccurate role recommendations, please confirm or add your core skills below."}
            </p>
            <div className="pt-2 flex flex-wrap items-center gap-1.5">
              <span className="text-[11px] font-semibold text-amber-800 mr-1">Quick Add Starters:</span>
              {['Python', 'JavaScript', 'SQL', 'HTML5', 'CSS3', 'React', 'Git & GitHub', 'Figma'].map((starter) => (
                !userProfile?.skills?.includes(starter) && (
                  <button
                    key={starter}
                    type="button"
                    onClick={() => {
                      setUserProfile({
                        ...userProfile,
                        skills: [...(userProfile?.skills || []), starter]
                      });
                    }}
                    className="text-[11px] font-medium px-2.5 py-1 rounded-full bg-white hover:bg-amber-100 border border-amber-300 text-amber-800 transition-colors shadow-2xs"
                  >
                    + {starter}
                  </button>
                )
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="space-y-6">
        {/* Skills Section */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            Your Skills
            <span className="ml-2 bg-primary-100 text-primary-800 text-sm py-0.5 px-2 rounded-full">
              {userProfile.skills?.length || 0}
            </span>
          </h2>
          
          <div className="flex flex-wrap gap-2 mb-6">
            {userProfile.skills?.map((skill, idx) => (
              <SkillTag 
                key={idx} 
                name={skill} 
                removable 
                onRemove={handleRemoveSkill} 
                variant="default"
              />
            ))}
          </div>
          
          <div className="relative max-w-md">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Plus size={18} className="text-gray-400" />
            </div>
            <input
              type="text"
              value={newSkill}
              onChange={(e) => setNewSkill(e.target.value)}
              onKeyDown={handleAddSkill}
              placeholder="Type a skill and press Enter to add..."
              className="pl-10 block w-full sm:text-sm border-gray-300 rounded-lg border focus:ring-primary-500 focus:border-primary-500 p-2.5"
            />
          </div>
        </div>

        {/* Education & Experience */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <GraduationCap className="mr-2 text-primary-500" size={20} />
              Education
            </h2>
            {userProfile.education?.length > 0 ? (
              <ul className="space-y-3">
                {userProfile.education.map((edu, idx) => (
                  <li key={idx} className="border-l-2 border-primary-200 pl-3">
                    <p className="font-semibold text-gray-900">{edu.degree}</p>
                    <p className="text-gray-600">{edu.institution}</p>
                    <p className="text-sm text-gray-500">{edu.year}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 italic">No education details found.</p>
            )}
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <Briefcase className="mr-2 text-primary-500" size={20} />
              Experience
            </h2>
            {userProfile.experience?.length > 0 ? (
              <ul className="space-y-3">
                {userProfile.experience.map((exp, idx) => (
                  <li key={idx} className="border-l-2 border-primary-200 pl-3">
                    <p className="font-semibold text-gray-900">{exp.role}</p>
                    <p className="text-gray-600">{exp.company}</p>
                    <p className="text-sm text-gray-500">{exp.duration}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 italic">No experience details found.</p>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 pt-6">
          <button
            onClick={() => {
              if (isZeroSkills) {
                alert('Please add or select at least 1-2 skills so we can calculate meaningful career matches.');
                return;
              }
              navigate('/roles');
            }}
            disabled={isZeroSkills}
            className={`flex-1 py-3 px-6 rounded-xl flex items-center justify-center font-semibold transition-all shadow-md ${
              isZeroSkills 
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed shadow-none' 
                : 'text-white bg-primary-600 hover:bg-primary-700 hover:shadow-lg'
            }`}
          >
            Continue to Role Selection <ArrowRight className="ml-2" size={20} />
          </button>
          <button
            onClick={() => {
              if (isZeroSkills) {
                alert('Please add or select at least 1-2 skills so we can evaluate role alignments.');
                return;
              }
              navigate('/dashboard');
            }}
            disabled={isZeroSkills}
            className={`flex-1 py-3 px-6 rounded-xl flex items-center justify-center font-semibold transition-all ${
              isZeroSkills
                ? 'bg-gray-100 text-gray-400 border-2 border-gray-200 cursor-not-allowed'
                : 'text-primary-700 bg-white border-2 border-primary-200 hover:bg-primary-50'
            }`}
          >
            <LayoutDashboard className="mr-2" size={20} /> Analyze All Roles
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfileReview;
