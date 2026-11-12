# Scalpx — Scalp & Hair Clinic website

Static multi-page site (no build tooling needed for hosting).

- `build.py` generates the HTML pages into `public/` (`python3 build.py`)
- `public/` — deployable site (HTML, CSS, JS, self-hosted Instrument Sans font, optimised WebP images)
- Pages: Home, About, Treatments, Results, Blog, Login/Create account, Dashboard (auth-protected), Book consultation
- Auth is a **client-side demo** (localStorage + SHA-256). Replace with Supabase/Auth.js before real users sign up.
- `videos/` — desktop & mobile walkthrough videos
- `POST.md` — launch copy with SEO keywords + hashtags

Deploy: Vercel with output directory `public` (see `vercel.json`).
