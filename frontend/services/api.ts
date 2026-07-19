import axios from "axios";
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});
import { GeneratedImage, GenerateRequestPayload } from "@/types";

/**
 * API service layer.
 *
 * This file is the single seam between the UI and the backend. Right now every
 * function is mocked with timers and placeholder images. When the FastAPI
 * backend is ready, swap the internals of `generateSceneImages` for a real
 * `fetch("/api/generate", { method: "POST", body: formData })` call — the
 * function signature and the `onProgress` contract can stay the same.
 */

/** Deterministic-ish placeholder image URL per scenario, using picsum.photos seeds. */
function placeholderImageUrl(scenarioId: string): string {
  return `https://picsum.photos/seed/${scenarioId}/600/600`;
}

/**
 * Simulates calling the backend to generate one image per selected scenario.
 * Reports progress as each "image" finishes so the UI can animate a progress bar.
 */
export async function generateSceneImages(
  payload: GenerateRequestPayload,
  onProgress: (completed: number, total: number) => void
): Promise<GeneratedImage[]> {
  const formData = new FormData();
  formData.append("file", payload.image);

  const uploadResponse = await api.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  const analyzeResponse = await api.post("/analyze", {
    image_id: uploadResponse.data.image_id,
    description: payload.description,
  });

  const generateResponse = await api.post("/generate", {
    image_id: uploadResponse.data.image_id,
    scenarios: payload.scenarios.map((scenario) => scenario.label),
  });

  const results: GeneratedImage[] = generateResponse.data.images.map(
    (image: any, index: number) => ({
      scenarioId: payload.scenarios[index].id,
      scenarioLabel: image.scenario,
      imageUrl: `http://127.0.0.1:8000${image.image_url}`,
    })
  );

  onProgress(results.length, results.length);

  return results;
}