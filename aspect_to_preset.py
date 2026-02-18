class AspectToPresetRes:
    """
    Detect aspect ratio from an IMAGE and output a preset (W,H):
      - square:    1024x1024
      - portrait:   832x1216
      - landscape: 1216x832

    Then optionally scale by an integer multiplier and snap to multiples of `snap_to`.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "square_threshold_pct": ("INT", {"default": 15, "min": 0, "max": 50, "step": 1}),
                "multiplier": ("FLOAT", {"default": 1.00, "min": 0.00, "max": 8.00, "step": 0.01}),
                "snap_to": ("INT", {"default": 8, "min": 1, "max": 64, "step": 1}),
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "mode")
    FUNCTION = "run"
    CATEGORY = "utils"

    def run(self, image, square_threshold_pct, multiplier, snap_to):
        # Comfy IMAGE tensor is typically [B,H,W,C]
        if len(image.shape) != 4:
            raise ValueError(f"Unexpected IMAGE shape: {tuple(image.shape)}")

        h = int(image.shape[1])
        w = int(image.shape[2])

        # Aspect ratio test
        mn = min(w, h)
        mx = max(w, h)
        r = (mx / mn) if mn > 0 else 1.0

        thresh = 1.0 + (float(square_threshold_pct) / 100.0)

        # Base preset
        if r <= thresh:
            base_w, base_h = 1024, 1024
            mode = "square"
        else:
            if w > h:
                base_w, base_h = 1216, 832
                mode = "landscape"
            else:
                base_w, base_h = 832, 1216
                mode = "portrait"

        # Scale equally (keeps aspect ratio identical)
        m = float(multiplier)
        out_w = int(round(base_w * m))
        out_h = int(round(base_h * m))

        # Snap to latent-safe grid
        step = max(1, int(snap_to))
        out_w = (out_w // step) * step
        out_h = (out_h // step) * step

        # Hard floor just in case
        out_w = max(step, out_w)
        out_h = max(step, out_h)

        return (out_w, out_h, mode)


NODE_CLASS_MAPPINGS = {
    "AspectToPresetRes": AspectToPresetRes,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectToPresetRes": "Aspect Ratio → Preset Resolution",
}

