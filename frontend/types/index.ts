/**
 * Shared type definitions for the Product Scene Generator app.
 */

/** A single marketing scenario the user can generate a scene for. */
export interface Scenario {
  id: string;
  label: string;
  /** Short description shown on the card to help the user picture the scene. */
  description: string;
  /** Emoji used as a lightweight visual anchor for the card (no icon library needed). */
  emoji: string;
}

/** A generated image tied back to the scenario it was created for. */
export interface GeneratedImage {
  scenarioId: string;
  scenarioLabel: string;
  imageUrl: string;
}

/** Payload the frontend will eventually send to the backend generation endpoint. */
export interface GenerateRequestPayload {
  image: File;
  description: string;
  scenarios: Scenario[];
}

/** Response shape expected back from the backend generation endpoint. */
export interface GenerateResponsePayload {
  images: GeneratedImage[];
}
