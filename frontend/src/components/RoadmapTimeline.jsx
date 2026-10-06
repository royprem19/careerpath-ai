import React from 'react';
import { ExternalLink, BookOpen, Clock, Code2, CheckCircle2 } from 'lucide-react';

const RoadmapTimeline = ({ roadmap = [] }) => {
  if (!roadmap || roadmap.length === 0) {
    return (
      <div className="text-center py-10 text-gray-500 bg-slate-50 rounded-xl border border-dashed border-gray-200">
        <CheckCircle2 size={32} className="mx-auto text-emerald-500 mb-2" />
        <p className="font-semibold text-gray-700">No skill gaps detected!</p>
        <p className="text-xs text-gray-500">You already possess all essential competencies defined for this occupation.</p>
      </div>
    );
  }

  return (
    <div className="relative border-l-2 border-primary-200 ml-4 py-2 space-y-6">
      {roadmap.map((item, index) => (
        <div key={index} className="ml-6 relative">
          <div className="absolute -left-[33px] top-1 bg-white border-4 border-primary-600 rounded-full w-5 h-5 z-10 shadow-sm"></div>
          
          <div className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 hover:border-primary-200 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3 gap-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold px-2 py-0.5 rounded bg-primary-100 text-primary-800">
                  Week {item.week}
                </span>
                <h4 className="text-base font-bold text-gray-900">{item.skill}</h4>
              </div>
              <span className="inline-flex items-center text-xs text-gray-500 bg-gray-100 px-2.5 py-1 rounded-full w-fit">
                <Clock size={12} className="mr-1" /> {item.duration}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
              {/* Course */}
              <div className="bg-slate-50 p-3.5 rounded-lg border border-slate-100">
                <p className="text-xs text-gray-500 font-semibold uppercase tracking-wider mb-1.5">Recommended Course</p>
                {item.url ? (
                  <a 
                    href={item.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-primary-600 hover:text-primary-700 font-semibold text-sm group"
                  >
                    <BookOpen size={16} className="mr-1.5 shrink-0 text-primary-500" />
                    <span className="group-hover:underline line-clamp-1">{item.course}</span>
                    <ExternalLink size={13} className="ml-1 shrink-0 text-gray-400 group-hover:text-primary-600" />
                  </a>
                ) : (
                  <div className="flex items-center text-gray-800 font-medium text-sm">
                    <BookOpen size={16} className="mr-1.5 text-gray-500 shrink-0" />
                    <span>{item.course}</span>
                  </div>
                )}
                <div className="flex items-center gap-2 mt-1.5 text-xs text-gray-500">
                  <span>Platform: <strong className="text-gray-700">{item.platform}</strong></span>
                  {item.is_free !== undefined && (
                    <span className={`px-1.5 py-0.2 rounded text-[10px] font-semibold ${item.is_free ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>
                      {item.is_free ? 'Free' : 'Paid'}
                    </span>
                  )}
                </div>
              </div>

              {/* Project */}
              <div className="bg-primary-50/50 p-3.5 rounded-lg border border-primary-100">
                <p className="text-xs text-primary-700 font-semibold uppercase tracking-wider mb-1.5 flex items-center gap-1">
                  <Code2 size={13} /> Hands-on Capstone Task
                </p>
                <p className="text-xs text-slate-700 leading-relaxed font-medium">
                  {item.project}
                </p>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default RoadmapTimeline;
