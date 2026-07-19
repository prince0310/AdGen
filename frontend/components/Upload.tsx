"use client";

import { useCallback, useState } from "react";
import { useDropzone, FileRejection } from "react-dropzone";

interface UploadProps {
  image: File | null;
  preview: string | null;
  description: string;
  onImageSelect: (file: File) => void;
  onDescriptionChange: (description: string) => void;
}

/**
 * Drag-and-drop / click-to-browse image uploader with an immediate preview.
 * Also collects a short product description from the user.
 */
export default function Upload({
  image,
  preview,
  description,
  onImageSelect,
  onDescriptionChange,
}: UploadProps) {
  const [validationError, setValidationError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[], rejectedFiles: FileRejection[]) => {
      if (rejectedFiles.length > 0) {
        setValidationError(
          "Unsupported file type. Please upload a PNG, JPG, or WEBP image."
        );
        return;
      }

      if (acceptedFiles.length > 0) {
        setValidationError(null);
        onImageSelect(acceptedFiles[0]);
      }
    },
    [onImageSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/png": [".png"],
      "image/jpeg": [".jpg", ".jpeg"],
      "image/webp": [".webp"],
    },
    multiple: false,
  });

  return (
    <div className="space-y-6">
      {/* Image Upload */}
      <div>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
          1. Upload Product Image
        </h2>

        <div
          {...getRootProps()}
          className={`group relative flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-8 text-center transition-colors ${isDragActive
              ? "border-accent-500 bg-accent-50"
              : "border-slate-200 bg-slate-50 hover:border-accent-400 hover:bg-accent-50/50"
            }`}
        >
          <input {...getInputProps()} aria-label="Upload product image" />

          {preview ? (
            <div className="flex flex-col items-center gap-3">
              <img
                src={preview}
                alt="Product preview"
                className="h-40 w-40 rounded-lg object-cover shadow-soft"
              />

              <p className="max-w-xs truncate text-sm font-medium text-slate-700">
                {image?.name}
              </p>

              <span className="text-xs text-accent-600 group-hover:underline">
                Click or drop a new image to replace
              </span>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-2">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-accent-100 text-accent-600">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={1.8}
                  className="h-6 w-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 16V4m0 0-4 4m4-4 4 4M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"
                  />
                </svg>
              </div>

              <p className="text-sm font-medium text-slate-700">
                {isDragActive
                  ? "Drop the image here"
                  : "Drag & drop a product image"}
              </p>

              <p className="text-xs text-slate-400">
                or click to browse — PNG, JPG, WEBP
              </p>
            </div>
          )}
        </div>

        {validationError && (
          <p className="mt-2 text-sm text-red-600" role="alert">
            {validationError}
          </p>
        )}
      </div>

      {/* Product Description */}
      <div>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
          2. Product Description
        </h2>

        <textarea
          value={description}
          onChange={(e) => onDescriptionChange(e.target.value)}
          placeholder={`Example:
• Healthy fruit drink
• Affordable
• Refreshing
• Target audience: Young professionals`}
          rows={6}
          className="w-full rounded-xl border border-slate-300 p-4 text-sm shadow-sm focus:border-accent-500 focus:outline-none focus:ring-2 focus:ring-accent-200"
        />

        <p className="mt-2 text-xs text-slate-500">
          Describe your product briefly. Mention its features, brand style,
          target audience, or anything you want the AI to consider when
          generating marketing scenes.
        </p>
      </div>
    </div>
  );
}