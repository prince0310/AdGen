"use client";

import { useState } from "react";
import Upload from "@/components/Upload";
import ScenarioSelector, {
  DEFAULT_SCENARIOS,
} from "@/components/ScenarioSelector";
import GenerateButton from "@/components/GenerateButton";
import Progress from "@/components/Progress";
import Gallery from "@/components/Gallery";
import { generateSceneImages } from "@/services/api";
import { GeneratedImage } from "@/types";

// Scenarios selected by default when the page loads (all 10, per the brief).
const DEFAULT_SELECTED_IDS = DEFAULT_SCENARIOS.map((s) => s.id);

export default function Home() {
  // --- Lifted state, shared across all child components via props ---
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  // NEW: Product description
  const [description, setDescription] = useState("");

  const [selectedScenarios, setSelectedScenarios] = useState<string[]>(
    DEFAULT_SELECTED_IDS
  );
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState({
    completed: 0,
    total: 0,
  });
  const [generatedImages, setGeneratedImages] = useState<GeneratedImage[]>([]);

  function handleImageSelect(file: File) {
    setImage(file);
    setPreview(URL.createObjectURL(file));
  }

  async function handleGenerate() {
    if (
      !image ||
      description.trim() === "" ||
      selectedScenarios.length === 0
    )
      return;

    const scenariosToGenerate = DEFAULT_SCENARIOS.filter((s) =>
      selectedScenarios.includes(s.id)
    );

    setLoading(true);
    setGeneratedImages([]);
    setProgress({
      completed: 0,
      total: scenariosToGenerate.length,
    });

    try {
      const images = await generateSceneImages(
        {
          image,
          description,
          scenarios: scenariosToGenerate,
        },
        (completed, total) => setProgress({ completed, total })
      );

      setGeneratedImages(images);
    } catch (error) {
      console.error("Generation failed:", error);
    } finally {
      setLoading(false);
    }
  }

  const canGenerate =
    !!image &&
    description.trim().length > 0 &&
    selectedScenarios.length > 0;

  return (
    <main className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          Product Scene Generator
        </h1>

        <p className="mt-2 text-base text-slate-500">
          Generate AI marketing images from a single product image.
        </p>
      </div>

      {/* Main Card */}
      <div className="rounded-2xl border border-slate-100 bg-white p-6 shadow-card sm:p-8">
        <div className="flex flex-col gap-8">
          <Upload
            image={image}
            preview={preview}
            description={description}
            onImageSelect={handleImageSelect}
            onDescriptionChange={setDescription}
          />

          <ScenarioSelector
            scenarios={DEFAULT_SCENARIOS}
            selectedScenarios={selectedScenarios}
            onChange={setSelectedScenarios}
          />

          <div className="flex flex-col gap-4">
            <GenerateButton
              loading={loading}
              disabled={!canGenerate}
              onClick={handleGenerate}
            />

            {!canGenerate && !loading && (
              <p className="-mt-2 text-center text-xs text-slate-400">
                Upload an image, enter a product description, and select at
                least one scenario to generate images.
              </p>
            )}

            <Progress
              loading={loading}
              completed={progress.completed}
              total={progress.total}
            />
          </div>

          <Gallery images={generatedImages} />
        </div>
      </div>
    </main>
  );
}