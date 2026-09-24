# Notebook packaging record

These notebooks are development implementations, not a verified reproduction of
the article. This record separates presentation, portability and security edits
from scientific work that remains unresolved. The supplied source files were
not modified. Their saved outputs were inspected but are not distributed as
validated results.

## Source mapping

| Supplied notebook | Repository copy |
| --- | --- |
| `Demo Install or Re-install MATLAB Engine.ipynb` | [`01_matlab_engine_setup.ipynb`](../notebooks/01_matlab_engine_setup.ipynb) |
| `Demo A-ENTSOE_python_online_clean.ipynb` | [`02_entsoe_background.ipynb`](../notebooks/02_entsoe_background.ipynb) |
| `Demo dLCA_framework_KTB1_clean.ipynb` | [`03_dynamic_lca_framework.ipynb`](../notebooks/03_dynamic_lca_framework.ipynb) |

All cell numbers below refer to **zero-based positions in the supplied source**,
not the numbered repository filenames or Jupyter execution counters. Added
introductory/configuration cells shift positions in the repository copies.

## Edits applied to all notebooks

- Added an explicit development-status notice and links to the reproduction
  notes and release checklist.
- Cleared saved outputs, errors and execution counts. This removes stale output;
  it does **not** resolve the underlying scientific or runtime problems.
- Removed cell metadata and machine-specific notebook metadata. Retained only a
  generic Python kernelspec and added stable, valid cell identifiers.
- Left scientific dependencies optional: no installation, model execution,
  Brightway calculation or ENTSO-E request was performed during packaging.

## Notebook 01: setup

Source cell 0 was rewritten as portable, opt-in documentation; empty source
cell 1 was omitted. Installation and connection-test commands are Markdown
examples, not executable notebook cells. The historical instructions to remove
packages and run an administrator shell were not retained as default actions.

The supplied model identifies MATLAB R2025b/25.2; the analysis notebook header
listed engine 25.1. The setup guide records this discrepancy and links the
official MathWorks R2025b instructions, which give an engine 25.2.2 installation
example. No engine installation or compatibility test was performed here.

## Notebook 02: ENTSO-E acquisition

| Source cells | Change |
| --- | --- |
| Added cells | Development introduction and repository-relative configuration. |
| 6 | Replaced the inline API-key placeholder with `os.environ["ENTSOE_API_KEY"]`. |
| 12 | Generation export uses the configured `GENERATION_CSV`; creates its local parent directory. |
| 18 | Price export uses `PRICE_CSV`; joined export goes to `OUTPUT_DIR`. |
| All other source cells | Query dates, regions, timezone conversions, resampling and calculations retained. |

The retained source annual window is **2024-08-11 00:00 to 2025-08-10 00:00**,
with `Europe/Paris` query timezone. This must be reviewed before a final annual
data extraction; packaging did not silently extend the window.

## Notebook 03: framework demonstration

| Source cells | Change |
| --- | --- |
| 0 | Replaced stale one-day/capacity-change introduction with framework-first scope, prerequisites and explicitly unverified environment provenance. |
| Added cells | Development-status notice and repository-relative configuration. |
| 6 | Replaced a malformed, partially commented database-import cell with an inactive example using `ECOINVENT_USERNAME` and `ECOINVENT_PASSWORD` environment variables. |
| 12–13 | Presented optional extra-method dictionary entries as inactive documentation, not executable or validated configuration. |
| 16 | Removed unused capacity-feedback constants (`ALPHA_GREEN`, `ALPHA_NEUTRAL`, `ALPHA_DIRTY`, `TAU_CLASSIFY`, `GREEN_TOL_PCT`), commented planning/control-mode selection, and commented `Q_TARGET` assignment. These had no downstream references in the supplied source. Active horizon, CIP, production and scheduling calculations retained. |
| 18, 32 | Replaced draft prerequisite notes with links to setup/acquisition notebooks. |
| 19, 25 | Replaced local CSV paths with configured `GENERATION_CSV` and `PRICE_CSV`. |
| 33 | Added local model/helper existence checks and configured MATLAB model path. The engine API and subsequent sampling calculation remain unchanged. |
| 38, 39, 44 | Converted syntactically invalid, partially commented optional search/diagnostic snippets to visibly inactive Markdown. Their source text is preserved for review. |
| 49, 65 | Reworded explanatory notes without changing calculations. |
| 61 | Preserved the warning about plotting post-processing in clearer language. No plotting transformations were changed. |
| 91 | Marked the source gradient interpretation as a draft requiring verification. |
| 29, 59, 62, 69, 72, 81, 84, 95 | Replaced machine-specific plot/export directories with `OUTPUT_DIR` and named subdirectories. Source cell 72's directory ending `.pn` becomes `results/lcia_FG-BG_DEC/`. |
| Markdown cells | Removed incomplete red HTML span formatting. |

The generation filename now aligns with notebook 02's default output, rather
than the original machine-specific generation filename. Dataset contents were
not supplied, regenerated or changed.

## Local configuration

Set environment variables before launching Jupyter. A `.env` file is **not**
automatically read. Do not add credentials to notebook cells or commit local
inputs, licensed database content or generated outputs.

| Variable | Default or role |
| --- | --- |
| `DLCA_INPUT_DIR` | Repository `data/local/`; local data inputs. |
| `DLCA_OUTPUT_DIR` | Repository `results/`; generated figures and joined acquisition export. |
| `DLCA_MODEL_DIR` | Repository `model/local/`; user-supplied model and helper. |
| `DLCA_MODEL_NAME` | `KTB1_DLCA1_newvariable_22_legacy`; `.slx` is appended when omitted. |
| `DLCA_GENERATION_CSV` | `DLCA_INPUT_DIR/dk2_generation_2024-08-11_2025-08-10.csv`. |
| `DLCA_PRICE_CSV` | `DLCA_INPUT_DIR/dk2_price_2024-08-11_2025-08-10.csv`. |
| `ENTSOE_API_KEY` | Required for ENTSO-E acquisition; no default. |
| `ECOINVENT_USERNAME`, `ECOINVENT_PASSWORD` | Referenced only in the inactive licensed-import example; no defaults. |

## Calculations deliberately left unresolved

The following observations come from source code and its historical saved
outputs. They are **not new numerical results**, and the source outputs could
be stale because cells had been executed out of order.

| Source evidence | Required review |
| --- | --- |
| Notebook 03 cell 23: 8,736 background hours and maximum share-sum deviation 0.5. | Verify annual endpoints, missing data and complete technology shares. |
| Cells 34–35: 481 sampled points across hours 1–947, including skipped hours; cell 52 subsequently treats adjacent rows as hourly. | Verify hourly sampling and integration against actual timestamps. |
| Cells 52–53: 5,400 timestamps but 5,399 scoring intervals. | Reconcile intervals, campaign duration and intended calendar coverage. |
| Cells 40, 45: wastewater/CIP wastewater map to ultrapure-water production; stored warning reports kg versus expected m³. | Confirm process meaning, dataset choice, units and inventory conversions. |
| Cell 47: substring matching selected the ReCiPe endpoint `(E) no LT` variant. | Confirm and select the exact intended LCIA method. |
| Cell 80: saved scenario totals imply approximately −14.85% impact/−14.08% cost for ENV and −25.32% cost/+3.01% impact for PRICE. | Reconcile saved outputs with manuscript results and regenerate verified evidence. |
| Cell 90: saved gradient cosines −0.180032 and +0.157091. | Reconcile gradient analysis and interpretation with manuscript values. |
| Cell 94: saved Sobol estimates are all NaN. | Establish a valid analysis and numerical evidence; clearing outputs does not fix this. |
| Cell 53 uses `.iloc` on a `DatetimeIndex`; cells 76 and 88 had saved undefined-variable errors. | Resolve execution order and runtime failures in a clean, authorized environment. |

The exact database mappings, selected-method resolver, input dates, time
integration, optimization and sensitivity calculations were not corrected in
this packaging pass. No controller was added. A notebook may pass JSON/schema
and Python syntax checks while still failing at runtime or producing scientifically
unverified outputs.

## Verification boundary

The repository copies were checked with `nbformat.validate` and Python AST
parsing after IPython input transformation, without executing the scientific
workflow. This verifies notebook structure and executable-cell syntax only.
End-to-end reproduction still depends on the input data, licensed software,
missing helper, author-approved scientific corrections and a clean full run.

See [reproduction notes](reproduction.md) and [release checklist](release-checklist.md).
