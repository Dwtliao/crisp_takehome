# Claude Code Instructions — Happy Pastures Creamery

## Critical Patterns — Read Before Every Change

### Persona Arrays Are Hardcoded In Multiple Places
Whenever adding a new persona (e.g. `'original'`), it must be added to ALL of these arrays:
- `showPitch()` — detects saved pitches before showing pitch screen
- `checkAndShowSavedPitchNotice()` — notice on original pitch screen
- `checkForSavedPitch()` — saved pitch list on refinement screen
- delete handler `remaining` check in `showSavedPitchChoice()`

Missing any one of these causes "can't delete" or "not showing" bugs.

### Never Call `.click()` Programmatically Inside an onclick Handler
Calling `element.click()` from within an `onclick` or event handler causes fetch() to fail in some browsers.
Always extract logic into a named function and call it directly.
- BAD: `useHistoryAddress()` calling `addressBtn.click()`
- GOOD: `useHistoryAddress()` calling `searchByAddress(address)` directly

### initializeVoiceNotes Must Be Called From ALL Pitch Screen Entry Points
It is called in `displayPitch()` but must also be called in `showSavedPitchChoice()`.
If skipped, `currentRestaurantForNotes` stays stale and notes appear for the wrong restaurant.

### Backend Changes Require Server Restart
Python does NOT auto-reload. After any `.py` change: Ctrl+C then `./start_app.sh`.

### Cache Results (feature branch) Can Mask Backend Changes
If location cache is active, refreshing the page won't re-run the backend filter.
User must click "Clear Cache + Refresh" to see updated filter results.

### Nominatim Geocoding Is Rate-Limited (1 req/sec)
Errors from Nominatim are transient. The code has a silent 1-second retry.
Do NOT show "Address not found" for network/rate-limit errors — show "try again."

## Architecture Quick Reference

### Frontend File Structure (split 2026-02-22)
Previously one monolithic `index.html` (3,228 lines). Now split into:
- `frontend/index.html` — HTML only (~294 lines)
- `frontend/style.css` — all CSS (~709 lines)
- `frontend/app.js` — all JS (~2,223 lines)

FastAPI's `StaticFiles` serves the entire `frontend/` dir, so no server config needed.
Frontend-only changes (CSS/JS/HTML) do NOT require a server restart — just hard-refresh (`Cmd+Shift+R`).

### Three Screens (not two)
1. Location screen → 2. Restaurant list → 3. Pitch screen → 3b. Refinement screen
State flows via JS variables: `currentLocation`, `currentRestaurantData`, `originalPitchData`, `lastLoadedSavedPitch`, `currentRestaurantForNotes`

### localStorage Keys
- `happy_pastures_rejected_restaurants` — rejection memory
- `happy_pastures_saved_pitches` — saved pitches keyed by `{name}_{lat}_{lon}_{persona}`
- `happy_pastures_voice_notes` — voice notes keyed by `{name}_{lat}_{lon}`
- `happy_pastures_restaurant_list_cache_v1` — location cache (feature branch)
- `happy_pastures_address_history` — recent address searches

### Persona List (always use this complete set in order)
`['original', 'walking', 'chef', 'manager', 'gatekeeper']`

### Pitch Save Key Format
`getSavedPitchKey(restaurant, persona)` → `{name}_{lat.toFixed(2)}_{lon.toFixed(2)}_{persona}`

## Common Mistakes To Avoid
- Forgetting `'original'` in persona arrays (added 2026-02-22)
- Not restarting server after Python changes
- Using `querySelectorAll` without checking if it picks up stale DOM elements
- Assuming `height: 100%` works when parent only has `min-height` (use explicit height or flex)
- Not checking if a new feature's init function is called from ALL entry points to a screen
