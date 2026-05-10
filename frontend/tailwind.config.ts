// MedXAI Tailwind config — locked white theme.
// Source of truth for color tokens: MEDXAI_PROMPT.md Section 11.1.
// The theme linter (scripts/lint_theme.py) refuses any commit under
// frontend/ that introduces dark-mode-only patterns or forbidden tokens.
//
// This file ships in Phase 0; the full Next.js app is scaffolded in Phase 7
// (see docs/decisions/0002-defer-frontend-scaffold-to-phase-7.md).

import type { Config } from "tailwindcss";

const config: Config = {
  // No `darkMode` — see ADR 0002. v1 is white-only.
  content: [
    "./app/**/*.{ts,tsx,mdx}",
    "./components/**/*.{ts,tsx,mdx}",
    "./lib/**/*.{ts,tsx}",
    "./content/**/*.{md,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Locked tokens — Section 11.1.
        background: "#FFFFFF",
        surface: "#FAFAFA",
        border: "#E5E7EB",
        "text-primary": "#111827",
        "text-secondary": "#4B5563",
        "text-muted": "#9CA3AF",
        accent: "#2563EB",      // clinical blue — single accent
        success: "#059669",     // emerald
        warning: "#D97706",     // amber
        danger: "#DC2626",      // red — only for red-flag content
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: [
          "JetBrains Mono",
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "monospace",
        ],
        serif: [
          "Source Serif 4",
          "ui-serif",
          "Georgia",
          "serif",
        ],
      },
      boxShadow: {
        soft: "0 1px 2px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.04)",
      },
      spacing: {
        // Section 11.1: card padding ≥ 24, section spacing ≥ 64.
        "card-pad": "1.5rem",
        "section-gap": "4rem",
      },
    },
  },
  plugins: [],
};

export default config;
