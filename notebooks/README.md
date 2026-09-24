# Notebook guide

Read the [framework scope](../docs/framework.md) first. The notebook names describe their role in the computational workflow; KTB1 remains the demonstration case.

| Order | Notebook | Purpose | External prerequisites |
| --- | --- | --- | --- |
| 1 | [MATLAB Engine setup](01_matlab_engine_setup.ipynb) | Prepare the Python-to-MATLAB interface | Compatible MATLAB installation and Python environment |
| 2 | [ENTSO-E background](02_entsoe_background.ipynb) | Retrieve generation and day-ahead price signals | ENTSO-E account/API access and network |
| 3 | [Dynamic LCA framework](03_dynamic_lca_framework.ipynb) | Inspect coupling, LCIA, scheduling and diagnostic analysis | Brightway, licensed ecoinvent, KTB1, interface helper and verified input data |

## What has been cleaned

Stored outputs and execution counts are cleared. Credential placeholders and local machine paths are replaced with local configuration. Notebook introductions distinguish the general framework from the demonstration. Incomplete optional snippets are presented as inactive documentation instead of executable cells.

## What has not been claimed

The notebooks have not been rerun through a complete MATLAB/Brightway annual analysis in this repository build. They are not a locked environment or a verified reproduction of the manuscript. Known mapping, sampling and result-reconciliation questions are listed in [Reproduction](../docs/reproduction.md).

Do not use “Run All” until you have read the prerequisites and reviewed the database setup cells. Brightway setup can create or modify local projects and databases. Run in an isolated research environment and retain your existing project backups.

The exact changes are listed in [Notebook changes](../docs/notebook-changes.md).
