## Assignment

MAS664 HW

## Overview

A persistent API service that enables rubric generation,
refinement/validation, and scoring. It also enables rubrics to be saved for future evaluations.

Sample workflow: 

- Rubric Builder: Call the rubric builder endpoint to create success criteria for a given prompt / topic 

- Refiner + Memory: Refine and save the rubric via their respective endpoints

- Scorer / Validator: Use the scoring endpoint to assess a given input and along rubric dimensions. 

## Current URL / Usage
https://mas664-continued-production.up.railway.app

## Architecture Diagram

![Architecture Diagram](<Architecture Diagram.png>)

### Misc
- The page is left open for demonstration purposes; endpoints may return errors if spending caps are hit