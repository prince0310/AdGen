"use client";

interface ProgressProps {
  loading: boolean;
  completed: number;
  total: number;
}

/**
 * Progress indicator shown only while generation is in progress.
 * Renders nothing when `loading` is false to keep the layout clean.
 */
export default function Progress({ loading, completed, total }: ProgressProps) {
  if (!loading) return null;

  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="animate-fade-in rounded-xl border border-accent-100 bg-accent-50 p-4">
      <div className="mb-2 flex items-center justify-between">
        <p className="text-sm font-medium text-accent-700">Generating Images...</p>
        <p className="text-sm font-semibold text-accent-700">
          {completed} / {total} Completed
        </p>
      </div>
      <div className="h-2.5 w-full overflow-hidden rounded-full bg-accent-100">
        <div
          className="h-full rounded-full bg-accent-600 transition-all duration-500 ease-out"
          style={{ width: `${percentage}%` }}
          role="progressbar"
          aria-valuenow={percentage}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>
    </div>
  );
}
