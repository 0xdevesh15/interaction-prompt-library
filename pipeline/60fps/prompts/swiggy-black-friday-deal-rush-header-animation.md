Rebuild this animation 1:1: Swiggy's Black Friday "DEAL RUSH" header - food items orbit a circular dotted track behind the bold deal typography, each carrying a springy price badge, while a live countdown ticks below.

## Integration
Integration: stack-agnostic spec - springs given as stiffness/damping, timed motions as duration + curve; map every value to your framework and animation library of choice.

## Scene
Dark purple header card: "Black Friday" eyebrow, huge "DEAL RUSH" type, "New deals, every hour!" subline. Behind/right of the type: a dotted elliptical orbit with 3-4 food photos (in circular masks) traveling it, each with a small price chip ("₹69", "₹29"). Below the card: "LIVE DEALS end in 00:11:46" countdown and the deal grid.

## Motion spec
Pattern: ambient orbit loop.
- Food items travel the dotted ellipse continuously (~10s per revolution, linear), scaling slightly at the front of the orbit (1.0) vs the back (0.7) with matching opacity for depth.
- Price badges ride with their items but counter-rotate to stay upright; when an item passes the front-center, its badge does a small spring pop (scale 1 -> 1.15 -> 1, 300ms).
- The dotted track is static; items swap z-order as they pass behind the typography.
- Countdown digits tick each second (last two digits roll down 200ms).

## Calibration
- Depth scaling (front big / back small) is what makes it an orbit instead of a flat carousel.
- The badge pop is the only spring in the system - one beat per orbit per item.

## Reduced motion
Items parked at fixed orbit positions; countdown still ticks.

## Don't miss
- Items pass BEHIND the "DEAL RUSH" type at the orbit's back half.
- Circular image masks with thin white borders.
