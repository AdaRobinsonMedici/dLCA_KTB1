# Reproduction guide

## Current status

The repository contains inspectable development notebooks and existing legacy data. It does **not yet contain a fully verified annual reproduction package**. Repository-quality tests check packaging only. They must not be reported as scientific validation.

## 1. Inspect without running the model

Read the [notebook guide](../notebooks/README.md), [data catalogue](../data/README.md) and [model requirements](../model/README.md). You can view the notebooks on GitHub without installing MATLAB or Brightway. Outputs have deliberately been cleared because the stored development outputs are not a reconciled publication result set.

## 2. Prepare an isolated environment

The supplied development materials record Python 3.10.18 and Brightway25 1.1.0. The original repository README instead recorded Python 3.11.11 and Brightway25 1.0.6. These are different development environments, not interchangeable verified configurations.

[requirements-notebooks.txt](../requirements-notebooks.txt) is a **candidate dependency list inferred from imports and recorded metadata**, not a lockfile. Review it before installing into a fresh environment. It does not install MATLAB or supply ecoinvent.

```bash
python -m venv .venv
```

Activate the environment using the command for your platform, then install the candidate dependencies if appropriate:

```bash
python -m pip install -r requirements-notebooks.txt
```

Follow [notebook 01](../notebooks/01_matlab_engine_setup.ipynb) and official MathWorks compatibility guidance for MATLAB Engine. The uploaded model records MATLAB R2025b/25.2; one notebook header instead recorded Engine 25.1. Confirm the actual author-tested combination before creating the paper release.

## 3. Configure local resources

Use [.env.example](../.env.example) as a list of environment-variable names. Do not put credentials in a tracked notebook. A `.env` file is not loaded automatically: set variables in the shell or in your local notebook launcher. The notebooks explain their defaults and required paths.

Place private inputs in `data/local/`, the locally obtained model and helper in `model/local/`, and generated exports in `results/`. These locations are ignored by Git. Do not use the legacy root-level Danish electricity CSV as the annual DK2 input.

Obtain the matching KTB1 model plus `step_and_get_DI.m` from the authors. A similarly named upstream model is not automatically interchangeable with the modified model used to produce the manuscript.

## 4. Resolve the scientific run prerequisites

The following points were identified in the supplied development files. Cell indices refer to the **original main notebook**, before repository introduction/configuration cells were added. Stored-output observations are historical diagnostics, not a fresh execution.

| Check | Evidence to resolve | Required before a paper release |
| --- | --- | --- |
| Full-year background coverage | Original cell 23 reports 8,736 hours rather than 8,760 | Confirm UTC interval convention, query endpoint and complete matching generation/price indices |
| Electricity-share normalization | Original cell 23 reports a maximum sum deviation of 0.5 | Resolve missing/duplicated technologies and verify hourly share sums |
| Foreground sampling | Original cells 34–35 show gaps in the recorded hour sequence | Validate the helper's sampling semantics and integrate using actual intervals |
| Annual operation horizon | Original cells 52–53 score 5,399 intervals from 5,400 timestamps | Declare whether timestamps denote samples or interval boundaries and reconcile totals |
| Wastewater inventory mapping | Original cells 40 and 45 include a water-production mapping and unit warning | Confirm the intended treatment dataset, flow quantities and conversions |
| Exact LCIA method | Original cell 47 uses a partial-name lookup; stored output selects a “no LT” variant | Record the full method tuple and matching database release |
| Annual results | Original cell 80 stored results differ from manuscript percentages | Regenerate schedules and summary tables from one authoritative run |
| Independence analysis | Original cells 90 and 94 include differing cosines and non-finite Sobol outputs | Re-run and validate diagnostics before making independence claims |

These checks are not resolved by clearing outputs, renaming files or passing repository CI. Scientific calculations are retained for author review rather than changed to force agreement with the paper.

## 5. Freeze a reproducible result set

After resolving the checks, run from a clean kernel in the confirmed environment. Save input provenance, UTC indices, foreground inventory, exact dataset mappings, full method identifier, schedules, numerical summaries and figure source data. Record the source-code commit and input checksums.

Compare regenerated results to the final manuscript and Supporting Information, including functional units and units in every table and graph. Only then create the paper tag and archived release described in the [release checklist](release-checklist.md).
