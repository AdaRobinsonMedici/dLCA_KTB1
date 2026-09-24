# Article-to-repository map

The repository follows the article's three layers: framework, workflow and demonstration. This map uses subjects rather than final figure numbers because numbering and filenames must be checked against the accepted manuscript.

| Article component | Repository location | Current evidence status |
| --- | --- | --- |
| General framework and scope | [Framework](framework.md), README Mermaid diagram | Conceptual documentation; not a replacement for the manuscript equations |
| MATLAB/Python interface | [Setup notebook](../notebooks/01_matlab_engine_setup.ipynb), [model requirements](../model/README.md) | Setup guidance; matching model/helper still required |
| Time-varying background | [ENTSO-E notebook](../notebooks/02_entsoe_background.ipynb) | Acquisition code; complete verified annual input panel not included |
| Dynamic inventory and LCIA | [Framework notebook](../notebooks/03_dynamic_lca_framework.ipynb) | Development code; mapping, units and time-axis checks pending |
| Environmental and price-based scheduling | [Framework notebook](../notebooks/03_dynamic_lca_framework.ipynb) | Development calculations; annual results need reconciliation |
| Independence/sensitivity analysis | [Framework notebook](../notebooks/03_dynamic_lca_framework.ipynb) | Diagnostics present; finite validated outputs required |
| Hourly LCI table/electronic matrix | [Data catalogue](../data/README.md) | Final hourly matrix and illustrative rows not yet exported |
| Publication figures | [Figure guide](../figures/README.md) | Validated image/data pairs pending |
| Manuscript and Supporting Information | [Release checklist](release-checklist.md) | Final approved versions are not uploaded in this build |

The draft manuscript and SI refer to `dLCA_KTB1_Control`. The repository prepared here is **dLCA_KTB1**. Update both documents to the final repository/release URL before submission so their availability statements point to the correct material.
