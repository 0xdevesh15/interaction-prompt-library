Rebuild this animation 1:1: Duolingo's hyped perfect-lesson celebration - the owl yells with joy, beak wide open on a green burst, "Perfect lesson!" and "Take a bow!" land, and reward chips (+40 XP, 100% accuracy, time) pop in one by one above the CLAIM XP button.

## Integration
Integration: stack-agnostic spec - springs given as stiffness/damping, timed motions as duration + curve; map every value to your framework and animation library of choice.

## Scene
Light screen: yelling owl (beak open, eyes squeezed shut, arms up) center on a green burst backdrop, "Perfect lesson!" headline, "Take a bow!" subline, three reward chips, blue CLAIM XP button.

## Motion spec
Pattern: explosive entrance + reward cascade, ~2.5s.
- Entrance: burst scales in fast (250ms, slight overshoot) as the owl springs in (scale 0.7 -> 1.05 -> 1, spring ~300/15) with tiny orange feathers/confetti popping at its sides (6 pieces, 400ms arcs).
- Yell loop: the owl's whole body shakes with excitement (translateX +-2px at 8Hz for 400ms, then rests 2s) and its beak opens wider on each shake.
- Chips: pop in left to right (spring ~400/16, 130ms stagger), accuracy chip last with a glow pulse.
- Copy and button rise in below (250ms each, ease-out).

## Calibration
- This is the loudest celebration in the set - fast entrance, visible shake, confetti. Don't tame it.
- The shake is a burst, not a loop; continuous shaking reads as a glitch.

## Reduced motion
Owl fades in; chips fade in together (200ms).

## Don't miss
- Eyes squeezed + beak open is the specific expression - not a smile.
- Same chip cascade rhythm as the other celebration screens.
