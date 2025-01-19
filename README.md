# Project KTB1: dLCA of Lovastatin Production

**Author**: ADA ROBINSON
**Date**: 2025-01-05  
**Environment**: `pharma`
**Software & Library Versions**
- Brightway25 version 1.0.6  
- bw2io version 0.9.4  
- Numpy version 1.24.4  
- Python version 3.11.11
  
**Data Sources**:  
- Ecoinvent v3.10 (cut-off system)  
- KTB1 model - DTU (https://github.com/Boskabadi/KTB1-DLCA)
- entsoe -  (https://transparency.entsoe.eu/) 

---

## Project Overview
> **What**: This notebook focuses on **electricity demand** KTB1 model for lovastatin production, and sets up a Brightway2.5 environment to perform a first dynamic LCA calculation for a whole day.

> **How**:

1. We import the necessary libraries (Brightway2.5, bw2io, etc.) and data sources (Ecoinvent 3.10).
2. We read and prepare two CSV files:
3. A file with hourly electricity demand for the KTB1 process (e.g. the CSTR, Hydrocyclone, Centrifuge, and Pump data).
4. A file with hourly electricity production shares for DK (e.g. fraction of coal, wind, biomass, etc.).
5. We map each electricity generation technology to the relevant Brightway activity in the custom database.
6. We build a functional unit (FU) matrix for each hour by multiplying the KTB1 electricity consumption by the respective technology shares.
7. We then perform an LCA calculation using the ReCiPe 2016 v1.03 endpoint (E), total: ecosystem quality method to obtain the impact score at each point

> **Why (Intended Outcome)**: We aim to quantify and compare the environmental impacts of the hourly electricity consumption in lovastatin production using bw_temporalis, capturing time-varying emissions and impacts.
