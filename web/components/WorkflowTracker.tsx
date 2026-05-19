import React from 'react';
import { STEP_NAMES } from '../lib-shared/types';

export interface WorkflowTrackerProps {
  currentStep: number;
  completed: boolean[];
  mode: 'wizard' | 'expert';
  onStepClick?: (stepIndex: number) => void;
}

const CheckIcon = React.memo(() => (
  <svg className="w-5 h-5" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
      fill="currentColor"
    />
  </svg>
));
CheckIcon.displayName = 'CheckIcon';

const ChevronRightIcon = React.memo(({ className = '' }: { className?: string }) => (
  <svg className={`w-4 h-4 ${className}`} viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path
      d="M5.5 3l5 5-5 5"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
));
ChevronRightIcon.displayName = 'ChevronRightIcon';

const SpinnerIcon = React.memo(() => (
  <svg className="w-5 h-5 animate-spin" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="10" cy="10" r="9" stroke="currentColor" strokeWidth="2" strokeOpacity="0.2" />
    <path
      d="M19 10C19 15 15 19 10 19"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
));
SpinnerIcon.displayName = 'SpinnerIcon';

export default React.memo(function WorkflowTracker({
  currentStep,
  completed,
  mode,
  onStepClick,
}: WorkflowTrackerProps) {
  const totalSteps = STEP_NAMES.length;
  const completedCount = completed.filter(c => c).length;
  const progress = totalSteps > 0 ? Math.round((completedCount / totalSteps) * 100) : 0;

  const handleStepClick = (index: number) => {
    if (mode === 'expert' && onStepClick) {
      onStepClick(index);
    }
  };

  return (
    <div className="bg-gray-800/40 backdrop-blur-xl rounded-xl p-4 sm:p-6 border border-gray-700/50">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-white font-semibold text-base sm:text-lg">工作流进度</h3>
        <div className="flex items-center gap-2">
          <span className="text-pink-400 font-bold text-lg sm:text-xl">{progress}%</span>
          <span className="text-gray-500 text-xs sm:text-sm">已完成</span>
        </div>
      </div>

      <div className="relative mb-6">
        <div className="h-1.5 bg-gray-700/50 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="space-y-3">
        {STEP_NAMES.map((stepName, index) => {
          const stepNum = index + 1;
          const isCompleted = completed[index];
          const isCurrent = stepNum === currentStep;
          const isPending = !isCompleted && !isCurrent;
          const isClickable = mode === 'expert' && onStepClick;

          return (
            <div
              key={stepNum}
              className={`
                relative flex items-center gap-3 p-3 rounded-lg transition-all duration-300
                ${isCurrent
                  ? 'bg-gradient-to-r from-pink-500/20 to-purple-500/20 border border-pink-500/30'
                  : isCompleted
                  ? 'bg-gray-700/30'
                  : 'bg-transparent opacity-60'
                }
                ${isClickable ? 'cursor-pointer hover:bg-gray-700/50' : ''}
              `}
              onClick={() => handleStepClick(index)}
            >
              <div
                className={`
                  relative w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0
                  transition-all duration-300
                  ${isCurrent
                    ? 'bg-gradient-to-r from-pink-500 to-purple-500 ring-2 ring-pink-500/30'
                    : isCompleted
                    ? 'bg-green-500/20 text-green-400'
                    : 'bg-gray-700 text-gray-500'
                  }
                `}
              >
                {isCompleted ? (
                  <CheckIcon />
                ) : isCurrent ? (
                  <SpinnerIcon />
                ) : (
                  <span className="text-sm font-medium">{stepNum}</span>
                )}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span
                    className={`
                      font-medium text-sm sm:text-base truncate
                      ${isCurrent ? 'text-pink-300' : isCompleted ? 'text-green-300' : 'text-gray-400'}
                    `}
                  >
                    {stepName}
                  </span>
                  {isClickable && (
                    <ChevronRightIcon className="text-gray-500 flex-shrink-0" />
                  )}
                </div>
              </div>

              {isCurrent && (
                <div className="flex-shrink-0">
                  <span className="px-2 py-1 bg-pink-500/20 text-pink-400 text-xs font-medium rounded-full">
                    进行中
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {mode === 'expert' && (
        <div className="mt-4 pt-4 border-t border-gray-700/50">
          <p className="text-xs text-gray-500 flex items-center gap-2">
            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            专家模式：点击任意步骤可跳转
          </p>
        </div>
      )}
    </div>
  );
});
