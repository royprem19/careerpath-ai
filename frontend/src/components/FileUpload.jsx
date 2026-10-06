import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, Lock } from 'lucide-react';

const FileUpload = ({ onFileSelect, selectedFile, onClear, disabled = false, onDisabledClick }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (disabled) {
      if (onDisabledClick) onDisabledClick();
      return;
    }
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [disabled, onDisabledClick, onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    disabled: disabled,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
  });

  if (selectedFile) {
    return (
      <div className="border-2 border-primary-500 rounded-xl p-6 bg-primary-50 flex items-center justify-between shadow-sm">
        <div className="flex items-center space-x-4">
          <div className="bg-primary-100 p-3 rounded-full text-primary-600">
            <FileText size={24} />
          </div>
          <div>
            <p className="font-semibold text-gray-800">{selectedFile.name}</p>
            <p className="text-sm text-gray-500">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
        </div>
        <button
          type="button"
          onClick={onClear}
          className="text-gray-400 hover:text-red-500 hover:bg-red-50 p-2 rounded-full transition-colors"
        >
          <X size={20} />
        </button>
      </div>
    );
  }

  return (
    <div
      {...getRootProps({
        onClick: (e) => {
          if (disabled) {
            e.preventDefault();
            e.stopPropagation();
            if (onDisabledClick) onDisabledClick();
          }
        }
      })}
      className={`border-2 border-dashed rounded-2xl p-7 sm:p-9 flex flex-col items-center justify-center transition-all duration-200 relative ${
        disabled
          ? 'border-slate-300 bg-slate-50/70 cursor-not-allowed opacity-90'
          : isDragActive
          ? 'border-indigo-500 bg-indigo-50/60 cursor-pointer scale-[1.01]'
          : 'border-indigo-200/90 bg-gradient-to-b from-indigo-50/40 via-purple-50/20 to-white/90 hover:border-indigo-400 hover:bg-indigo-50/30 cursor-pointer'
      }`}
    >
      <input {...getInputProps()} disabled={disabled} />
      
      {disabled && (
        <div className="absolute top-3 right-3 bg-amber-100 text-amber-800 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1 border border-amber-200 shadow-2xs">
          <Lock size={10} /> Sign In Required
        </div>
      )}

      <div className={`w-12 h-12 rounded-full mb-3 flex items-center justify-center transition-transform group-hover:scale-110 ${
        disabled 
          ? 'bg-slate-200 text-slate-500' 
          : 'bg-gradient-to-tr from-cyan-100 via-blue-100 to-purple-100 text-blue-600 shadow-xs border border-purple-200/50'
      }`}>
        {disabled ? <Lock size={22} /> : <Upload size={22} />}
      </div>
      <p className="text-sm font-bold text-slate-800 mb-0.5 text-center">
        {disabled ? 'Sign In to Upload Resume' : isDragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
      </p>
      <p className="text-xs text-slate-400 mb-4 text-center">Supports PDF or DOCX up to 5MB</p>
      
      <button 
        type="button"
        className={`font-semibold py-1.5 px-6 rounded-xl text-xs transition-all shadow-xs ${
          disabled 
            ? 'bg-primary-600 text-white hover:bg-primary-700' 
            : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-md shadow-indigo-500/20 hover:scale-105'
        }`}
      >
        {disabled ? 'Sign In to Browse' : 'Browse Files'}
      </button>
    </div>
  );
};

export default FileUpload;
