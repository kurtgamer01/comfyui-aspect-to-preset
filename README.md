# Aspect Ratio to Preset Resolution (ComfyUI Node)

A lightweight utility node for ComfyUI that:

- Detects the aspect ratio of an input IMAGE
- Selects a preset resolution (Square, Portrait, Landscape)
- Applies a floating point multiplier
- Snaps the final resolution to a latent safe grid

Designed to be deterministic, simple, and pipeline friendly.

---

## Overview

Given an input image tensor, the node:

1. Determines whether the image is Square, Portrait, or Landscape.
2. Maps it to a base preset resolution.
3. Applies a decimal multiplier.
4. Snaps the final width and height to a configurable multiple.

### Base Presets

- Square: 1024 x 1024
- Portrait: 832 x 1216
- Landscape: 1216 x 832

### Outputs

- `width` (INT)
- `height` (INT)
- `mode` (STRING: square, portrait, landscape)

The node does not resize images directly. It outputs resolution values for downstream nodes such as Empty Latent Image or KSampler.

---

## Inputs

### image (IMAGE)

Standard ComfyUI image tensor in the form `[B, H, W, C]`.

### square_threshold_pct (INT, default: 15)

Defines how close width and height must be to count as square.

Example with default 15 percent:

- If aspect ratio is less than or equal to 1.15, the image is treated as square.
- Otherwise, it is classified as portrait or landscape.

Increase this value if you want more images treated as square.

### multiplier (FLOAT, default: 1.00, step: 0.01)

Scales the preset resolution equally in both dimensions.

Examples using the Square preset:

| Multiplier | Result      |
|------------|-------------|
| 1.00       | 1024 x 1024 |
| 1.25       | 1280 x 1280 |
| 0.75       | 768 x 768   |
| 2.00       | 2048 x 2048 |

- Supports two decimal places.
- Rounded before snapping.
- Maintains exact aspect ratio prior to snapping.

Note: Snapping may introduce a very small ratio deviation, typically no more than a few pixels, which is negligible for diffusion workflows.

### snap_to (INT, default: 8)

Snaps the final width and height to a multiple of this value.

Example with snap_to = 8:

- 1279 becomes 1272
- 1283 becomes 1280

Recommended values:

- 8 for standard latent safe grid. Recommended.
- 16 for additional alignment safety.
- 64 only if a specific workflow requires it.

For most diffusion models, 8 is correct.

---

## Output Guarantees

The node ensures:

- Integer dimensions
- Latent safe snapping
- Minimum size enforcement
- Deterministic output
- No hidden scaling behavior

## Installation

Clone the repository into your ComfyUI custom_nodes directory:

cd /path/to/ComfyUI/custom_nodes

git clone https://github.com/kurtgamer01/comfyui-aspect-to-preset.git

Restart ComfyUI and refresh the browser.


