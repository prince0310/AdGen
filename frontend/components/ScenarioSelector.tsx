"use client";

import { Scenario } from "@/types";

/** The 10 default marketing scenarios available for generation. */
export const DEFAULT_SCENARIOS: Scenario[] = [
  { id: "beach-goa", label: "Beach in Goa", description: "Sunny shoreline, warm tones", emoji: "🏖️" },
  { id: "night-party", label: "Night Party", description: "Neon lights, high energy", emoji: "🎉" },
  { id: "office-desk", label: "Office Desk", description: "Clean, professional setting", emoji: "💼" },
  { id: "gym-workout", label: "Gym Workout", description: "Active, athletic backdrop", emoji: "🏋️" },
  { id: "mountain-trek", label: "Mountain Trek", description: "Outdoor adventure vibe", emoji: "⛰️" },
  { id: "luxury-restaurant", label: "Luxury Restaurant", description: "Elegant, upscale dining", emoji: "🍽️" },
  { id: "rainy-weather", label: "Rainy Weather", description: "Moody, atmospheric scene", emoji: "🌧️" },
  { id: "summer-picnic", label: "Summer Picnic", description: "Bright outdoor gathering", emoji: "🧺" },
  { id: "festival-celebration", label: "Festival Celebration", description: "Colorful and festive", emoji: "🎆" },
  { id: "college-campus", label: "College Campus", description: "Youthful, casual setting", emoji: "🎓" },
];

interface ScenarioSelectorProps {
  scenarios: Scenario[];
  selectedScenarios: string[];
  onChange: (selectedIds: string[]) => void;
}

/**
 * Responsive grid of selectable scenario cards.
 * Toggling a card adds/removes its id from `selectedScenarios`.
 */
export default function ScenarioSelector({
  scenarios,
  selectedScenarios,
  onChange,
}: ScenarioSelectorProps) {
  function toggleScenario(id: string) {
    if (selectedScenarios.includes(id)) {
      onChange(selectedScenarios.filter((s) => s !== id));
    } else {
      onChange([...selectedScenarios, id]);
    }
  }

  return (
    <div>
      <div className="mb-3 flex items-baseline justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          2. Select scenarios
        </h2>
        <span className="text-xs text-slate-400">
          {selectedScenarios.length} selected
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        {scenarios.map((scenario) => {
          const isSelected = selectedScenarios.includes(scenario.id);
          return (
            <button
              key={scenario.id}
              type="button"
              onClick={() => toggleScenario(scenario.id)}
              aria-pressed={isSelected}
              className={`relative flex flex-col items-start gap-1 rounded-xl border p-3 text-left transition-all hover:-translate-y-0.5 ${
                isSelected
                  ? "border-accent-500 bg-accent-50 shadow-soft"
                  : "border-slate-200 bg-white hover:border-accent-200 hover:shadow-soft"
              }`}
            >
              <div className="flex w-full items-start justify-between">
                <span className="text-xl leading-none">{scenario.emoji}</span>
                <span
                  className={`flex h-5 w-5 items-center justify-center rounded-full border-2 transition-colors ${
                    isSelected
                      ? "border-accent-500 bg-accent-500 text-white"
                      : "border-slate-300 bg-white"
                  }`}
                >
                  {isSelected && (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth={3}
                      className="h-3 w-3"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>
                  )}
                </span>
              </div>
              <p className="text-sm font-medium text-slate-800">{scenario.label}</p>
              <p className="text-xs text-slate-400">{scenario.description}</p>
            </button>
          );
        })}
      </div>
    </div>
  );
}
