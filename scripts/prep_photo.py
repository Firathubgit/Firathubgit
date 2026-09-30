"""
Prepare the portrait for ASCII conversion.

  1. cut the subject out of the background (rembg)
  2. boost local contrast (CLAHE) so dark curls and the beard keep their texture
  3. save a grayscale image + the subject mask as alpha -> assets/source-prepped.png

Run once whenever the photo changes:
    python scripts/prep_photo.py [input] [output]
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "assets", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "source-prepped.png")

cut = remove(Image.open(INP).convert("RGBA"), session=new_session("u2net_human_seg"))
rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])

gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
gray = clahe.apply(gray)

alpha = cv2.GaussianBlur(alpha, (0, 0), 1.0)
out = np.dstack([gray, gray, gray, alpha])
Image.fromarray(out, mode="RGBA").save(OUT)
print("wrote", OUT, out.shape)
