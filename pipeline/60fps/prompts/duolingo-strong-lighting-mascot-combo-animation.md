Rebuild this animation 1:1: Duolingo's in-lesson combo moment - mid-exercise, a lightning flash wipes the screen and a muscle-bound owl flexes full-screen under a "COMBO x15" headline with an electric aura, then the whole tableau shrinks away to the bottom as the next exercise slides in.

## Integration
Integration: stack-agnostic spec - springs given as stiffness/damping, timed motions as duration + curve; map every value to your framework and animation library of choice.

## Scene
Dark lesson screen ("Repeat after Lily" speaking exercise). On combo: full-screen takeover with the muscular flexing owl, electric aura, green "COMBO x15" headline. Then it exits downward and the next exercise ("Repeat after Bea") enters.

## Motion spec
Pattern: full-screen takeover interrupt, ~2.5s.
- Trigger: a lightning bolt flash sweeps the screen (2 bolt frames, 120ms) as the exercise content blurs out (200ms).
- The buff owl rises from the bottom (translateY 40% -> 0, spring ~280/18) with an electric aura pulsing behind it (scale 1 -> 1.08, 700ms loop) and small bolt flickers at its shoulders (every ~900ms).
- "COMBO x15" scales in above (spring ~380/16, 250ms).
- Hold ~1.2s, then the whole tableau slides down and off (350ms, ease-in) as the next exercise slides up from below (300ms, ease-out), progress bar advancing.

## Calibration
- This is an interrupt, not a screen: fast in, short hold, decisive exit.
- The owl is comically muscular - the contrast with the normal mascot is the joke.

## Reduced motion
Combo banner fades in and out (250ms) without takeover.

## Don't miss
- The exit is part of the choreography - the lesson resumes immediately, no dead time.
- The aura keeps pulsing for the whole hold; freezing it makes the takeover feel like a modal.
