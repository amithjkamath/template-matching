---
title: Template Matching Demo
emoji: 🔍
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
short_description: Demonstration of template matching with waldo
---

# template-matching

This is a demonstration of how template matching works by computing correlation between the search space and the template. 

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## What is Template Matching?

Template Matching is a simple method where the location of a template in a scene is computed by sliding it all across the scene and computing a similarity.

## What situations could this method be applied to?

This method works best when the template is exactly replicated in the scene - at the same scale (size), not rotated or sheared. 

## When would it not work?

If the template is not exactly available in the scene (when there are size or rotation or other transformation changes), this method could fail catastrophically. 

## Are there better similarity measures than correlation?

Point based feature matching methods like SIFT, SURF, MSER and so on would work better in cases where the relative pose of the template with respect to the scene cannot be controlled.
