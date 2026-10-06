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
      className={`border-2 border-dashed rounded-2xl p-8 sm:p-10 flex flex-col items-center justify-center transition-all duration-200 relative ${
        disabled
          ? 'border-gray-300 bg-gray-50/70 cursor-not-allowed opacity-90'
          : isDragActive
          ? 'border-primary-500 bg-primary-50 cursor-pointer'
          : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50 cursor-pointer'
      }`}
    >
      <input {...getInputProps()} disabled={disabled} />
      
      {disabled && (
        <div className="absolute top-3 right-3 bg-amber-100 text-amber-800 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1 border border-amber-200">
          <Lock size={10} /> Sign In Required
        </div>
      )}

      <div className={`p-4 rounded-full mb-3 ${disabled ? 'bg-gray-200 text-gray-500' : 'bg-blue-100 text-primary-600'}`}>
        {disabled ? <Lock size={28} /> : <Upload size={28} />}
      </div>
      <p className="text-base font-semibold text-gray-800 mb-1">
        {disabled ? 'Sign In to Upload Resume' : isDragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
      </p>
      <p className="text-xs text-gray-500 mb-4">Supports PDF or DOCX up to 5MB</p>
      
      <button 
        type="button"
        className={`font-semibold py-2 px-6 rounded-xl text-xs shadow-xs transition-colors ${
          disabled 
            ? 'bg-primary-600 text-white hover:bg-primary-700' 
            : 'bg-white text-primary-600 border border-primary-200 hover:bg-primary-50'
        }`}
      >
        {disabled ? 'Sign In to Browse' : 'Browse Files'}
      </button>
    </div>
  );
};

export default FileUpload;
