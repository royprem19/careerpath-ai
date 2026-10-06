import React from 'react';
import { X } from 'lucide-react';

const SkillTag = ({ name, removable = false, onRemove, variant = 'default' }) => {
  const getColors = () => {
    switch (variant) {
      case 'matched':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'missing-essential':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'missing-optional':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'surplus':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getColors()}`}>
      {name}
      {removable && (
        <button
          onClick={(e) => {
            e.preventDefault();
            onRemove(name);
          }}
          className="ml-2 focus:outline-none hover:text-red-600"
        >
          <X size={14} />
        </button>
      )}
    </div>
  );
};

export default SkillTag;
