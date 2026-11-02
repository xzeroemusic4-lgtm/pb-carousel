# frame.md: RAC reel

Series look for "Desi Systems": navy blueprint 3D, learned from a reference reel's look only.

## Tokens

| Token | Value | Use |
| --- | --- | --- |
| stage | `#0d2443` | Background and fog |
| prop blue | `#2f63b0` | Seats and benches |
| pale blue | `#7fa9d8` | Side berths |
| text | `#e9f0ff` | Titles and chips |
| yellow | `#f7c948` | The hero seat and key words |
| red | `#ff4d63` | Bad news only |
| green | `#3ee08f` | Confirmed only |

## Type

- Space Grotesk 700 for titles, JetBrains Mono uppercase for overlines, chips and the header.
- Never 3D text. Numerals slide digit by digit out of overflow masks with an accent bar.

## Rules

- Keep content between y 190 and y 1540, clear of Instagram's top bar and caption area.
- Glow is real selective bloom on emissive objects (strength 0.2, radius 0.28), never sprites.
- Scenes change through a fog dip or one continuous camera move, only after the last word.
- render(t) never draws inside the GSAP setter: the runtime sweeps the whole timeline on load.
