Rebuild this animation 1:1: Duolingo's XP gain on the leaderboard - a gem flies in from the bottom nav and a purple "+128 XP" pill pops onto the leaderboard's floating button with a springy bounce, while the header's XP total ticks up to its new value.

## Integration
Integration: stack-agnostic spec - springs given as stiffness/damping, timed motions as duration + curve; map every value to your framework and animation library of choice.

## Scene
Dark leaderboard: ranked rows (avatar, name, XP), "PROMOTION ZONE" divider, bottom tab bar with the league tab active. Header shows the user's XP total.

## Motion spec
Pattern: projectile + counter update, ~1.5s.
- A small gem springs off the league tab icon (scale 0.5 -> 1, 200ms) and arcs up to the header (bezier path, 450ms, ease-in).
- On arrival: the header's XP numeral ticks up to the new total (500ms, ease-out, tabular-nums) with a highlight flash (accent background fade, 300ms).
- Simultaneously the floating "+128 XP" pill pops in over the tab bar (scale 0.6 -> 1 with overshoot, spring ~380/16), holds ~2s, then collapses back (scale 1 -> 0.6, fade, 250ms).
- The leaderboard rows never move.

## Calibration
- The arc path sells "the XP came from the league" - a straight fly-up reads as a toast.
- The pill is chunky and purple; don't render it as a subtle caption.

## Reduced motion
Numeral sets instantly; pill fades in and out (200ms).

## Don't miss
- Gem launch and pill pop are offset by ~150ms - cause, then effect.
- The pill floats above the tab bar; it never pushes layout.
