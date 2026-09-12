# Karmayogi+ — SIH prototype

This frontend is a visual product prototype for an AI-enabled Skill Intelligence and Adaptive Learning Platform integrated with the iGOT Karmayogi ecosystem.

The previous learning-platform frontend has been replaced. Backend and database projects remain independent and unchanged.

## Run

Run `npm ci`, then `npm run dev` and open http://localhost:3000.
Validate with `npm run lint` and `npm run build`.

## Structure

- `src/app`: page entry point, metadata, and responsive styles.
- `src/components/karmayogi`: landing page, product UI mockups and local interactions.
- `src/components/ui/button.tsx` and `src/lib/utils.ts`: shared primitives.
- `public/fonts`: self-hosted Inter Tight fonts.

The layout keeps the Divi Pixel visual rhythm while communicating the Karmayogi+ intelligence loop. The product controls are local prototype interactions; synthetic data, mock integration and future production capability are explicitly labeled.
