"use client";

import { GeneratedImage } from "@/types";

interface GalleryProps {
  images: GeneratedImage[];
}

/**
 * Responsive gallery of generated scene images.
 * 1 column on mobile, 2 on tablet, 4 on desktop.
 */
export default function Gallery({ images }: GalleryProps) {
  if (images.length === 0) return null;

  return (
    <div>
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
        Generated Images
      </h2>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {images.map((image, index) => (
          <div
            key={image.scenarioId}
            className="animate-fade-in overflow-hidden rounded-xl border border-slate-200 bg-white shadow-soft transition-shadow hover:shadow-card"
            style={{ animationDelay: `${index * 60}ms`, animationFillMode: "backwards" }}
          >
            <div className="aspect-square w-full overflow-hidden bg-slate-100">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={image.imageUrl}
                alt={`Generated scene: ${image.scenarioLabel}`}
                className="h-full w-full object-cover"
              />
            </div>
            <div className="flex items-center justify-between gap-2 p-3">
              <p className="truncate text-sm font-medium text-slate-800">
                {image.scenarioLabel}
              </p>
              <button
                type="button"
                disabled
                title="Download will be available once the backend is connected"
                className="flex shrink-0 items-center gap-1 rounded-lg border border-slate-200 px-2.5 py-1.5 text-xs font-medium text-slate-400 cursor-not-allowed"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={1.8}
                  className="h-3.5 w-3.5"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 4v12m0 0-4-4m4 4 4-4M4 20h16"
                  />
                </svg>
                Download
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
