import os

import cv2
import numpy as np
import torch

from .PixelOE.pixeloe import pixelize

script_directory = os.path.dirname(os.path.abspath(__file__))


class PixelOE:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "img": ("IMAGE",),
                "mode": (["contrast", "center", "k-centroid", "bicubic", "nearest"],),
                "target_size": ("INT", {
                    "default": 256,
                    "min": 0,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "patch_size": ("INT", {
                    "default": 6,
                    "min": 0,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "thickness": ("INT", {
                    "default": 1,
                    "min": 0,
                    "max": 4096,
                    "step": 1,
                    "display": "number"
                }),
                "color_matching": ("BOOLEAN", {
                    "default": False
                }),
                "contrast": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "round": 0.001,
                    "display": "number"
                }),
                "saturation": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "round": 0.001,
                    "display": "number"
                }),
                "colors": ("INT", {
                    "default": 256,
                    "min": 1,
                    "max": 256,
                    "step": 1,
                    "display": "number"
                }),
                "no_upscale": ("BOOLEAN", {
                    "default": False
                }),
                "no_downscale": ("BOOLEAN", {
                    "default": False
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "process"

    CATEGORY = "Pixelize"

    def process(self, img, mode, target_size, patch_size, thickness, color_matching, contrast, saturation, colors, no_upscale, no_downscale):

        img = img.squeeze().numpy()
        img = (img * 255).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        img_pix = pixelize(img, mode, target_size, patch_size, thickness, color_matching, contrast, saturation, colors, no_upscale, no_downscale)

        img_pix = cv2.cvtColor(img_pix, cv2.COLOR_BGR2RGB)
        img_pix_t = np.array(img_pix).astype(np.float32) / 255.0
        img_pix_t = torch.from_numpy(img_pix_t)[None,]
        return (img_pix_t,)


NODE_CLASS_MAPPINGS = {
    "PixelOE": PixelOE,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "PixelOE": "PixelOE",
}