import React from 'react';
import { ExternalLink, BookOpen, Clock, Code2, CheckCircle2, Sparkles } from 'lucide-react';

const RoadmapTimeline = ({ roadmap = [] }) => {
  if (!roadmap || roadmap.length === 0) {
    return (
      <div className="text-center py-12 text-slate-500 bg-emerald-50/40 rounded-3xl border border-dashed border-emerald-200 p-8">
        <CheckCircle2 size={36} className="mx-auto text-emerald-600 mb-3" />
        <p className="font-black text-slate-900 text-lg">No skill gaps detected!</p>
        <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">You already possess all essential competencies defined for this industry role.</p>
      </div>
    );
  }

  return (
    <div className="relative border-l-2 border-indigo-200/80 ml-4 py-2 space-y-6">
      {roadmap.map((item, index) => (
        <div key={index} className="ml-6 relative">
          <div className="absolute -left-[33px] top-1.5 bg-white border-4 border-indigo-600 rounded-full w-5 h-5 z-10 shadow-xs"></div>
          
          <div className="glass-card rounded-2xl p-5 sm:p-6 border border-slate-200/80 shadow-sm hover:border-indigo-300 transition-all">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4 gap-2">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs font-black px-3 py-1 rounded-xl bg-indigo-50 text-indigo-700 border border-indigo-200/70 shadow-2xs">
                  Week {item.week}
                </span>
                <h4 className="text-base font-black text-slate-900">{item.skill}</h4>
                {(item.is_govt_initiative || item.initiative) && (
                  <span className="inline-flex items-center gap-1.5 text-xs font-bold px-3 py-1 rounded-full bg-orange-50 text-orange-900 border border-orange-200 shadow-2xs">
                    <span>🇮🇳</span> {item.initiative || 'Skill India / NPTEL'}
                  </span>
                )}
              </div>
              <span className="inline-flex items-center text-xs font-semibold text-slate-500 bg-slate-100/90 px-3 py-1 rounded-full w-fit">
                <Clock size={12} className="mr-1.5 text-slate-400" /> {item.duration}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Course Card */}
              <div className="bg-slate-50/80 p-4 rounded-xl border border-slate-200/70 flex flex-col justify-between">
                <div>
                  <p className="text-[10px] text-slate-400 font-extrabold uppercase tracking-wider mb-1.5">
                    Recommended Course
                  </p>
                  {item.url ? (
                    <a 
                      href={item.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-flex items-center text-indigo-600 hover:text-indigo-800 font-bold text-sm group"
                    >
                      <BookOpen size={16} className="mr-1.5 shrink-0 text-indigo-500" />
                      <span className="group-hover:underline line-clamp-1">{item.course}</span>
                      <ExternalLink size={13} className="ml-1.5 shrink-0 text-slate-400 group-hover:text-indigo-600" />
                    </a>
                  ) : (
                    <div className="flex items-center text-slate-800 font-bold text-sm">
                      <BookOpen size={16} className="mr-1.5 text-slate-500 shrink-0" />
                      <span>{item.course}</span>
                    </div>
                  )}
                </div>

                <div className="flex items-center justify-between pt-3 mt-3 border-t border-slate-200/50 text-xs">
                  <span className="text-slate-500 font-medium">Platform: <strong className="text-slate-800">{item.platform}</strong></span>
                  {item.is_free !== undefined && (
                    <span className={`px-2 py-0.5 rounded-md text-[10px] font-extrabold ${
                      item.is_free ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {item.is_free ? 'Free' : 'Paid'}
                    </span>
                  )}
                </div>
              </div>

              {/* Project Card */}
              <div className="bg-indigo-50/50 p-4 rounded-xl border border-indigo-100/90 flex flex-col justify-between">
                <div>
                  <p className="text-[10px] text-indigo-700 font-extrabold uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                    <Code2 size={13} /> Hands-on Capstone Task
                  </p>
                  <p className="text-xs text-slate-700 leading-relaxed font-semibold">
                    {item.project}
                  </p>
                </div>
                <div className="pt-2 text-[11px] font-bold text-indigo-600">
                  Proof-of-Skill Artifact
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default RoadmapTimeline;
