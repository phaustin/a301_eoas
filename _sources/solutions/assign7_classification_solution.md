---
jupytext:
  cell_metadata_filter: -all
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.6
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(week11:classification_solution)=
# Assign7 Classification problem -- solution

- Make a jupyter notebook that reproduces the false color examples
  in{ref}`week10:false_color_examples` for your scene (you'll need to rerun  {ref}`week4:clip_bands` version 3 to get the clipped fmask, and rerun {ref}`week2:hls` to download all of the HLS tifs for bands 1,2,3,4,5,6,7,9,10,11,fmask if you don't have them).
- Choose one band combination that looks interesting, and compare it with the land classification you created using {ref}`week9:land_classes` for your image with the same bounding box and pixel size -- comment on an y similarities and differences you can find.  Is the classification accurate?

