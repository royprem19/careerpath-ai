import React from 'react';
import { X } from 'lucide-react';

const SkillTag = ({ name, removable = false, onRemove, variant = 'default' }) => {
  const getColors = () => {
    switch (variant) {
      case 'matched':
        return 'bg-emerald-50/90 text-emerald-800 border-emerald-200/90 shadow-xs';
      case 'missing-essential':
        return 'bg-rose-50/90 text-rose-800 border-rose-200/90 shadow-xs';
      case 'missing-optional':
        return 'bg-amber-50/90 text-amber-800 border-amber-200/90 shadow-xs';
      case 'surplus':
        return 'bg-indigo-50/90 text-indigo-800 border-indigo-200/90 shadow-xs';
      default:
        return 'bg-white/90 text-slate-800 border-slate-200/90 hover:border-indigo-300 shadow-2xs';
    }
  };

  return (
    <div className={`inline-flex items-center px-3 py-1.5 rounded-xl text-xs sm:text-sm font-semibold border backdrop-blur-xs transition-all duration-200 ${getColors()}`}>
      <span>{name}</span>
      {removable && (
        <button
          onClick={(e) => {
            e.preventDefault();
            onRemove(name);
          }}
          className="ml-2 p-0.5 rounded-md hover:bg-rose-100 text-slate-400 hover:text-rose-600 transition-colors focus:outline-none"
          title="Remove skill"
        >
          <X size={13} strokeWidth={2.5} />
        </button>
      )}
    </div>
  );
};

export default SkillTag;
