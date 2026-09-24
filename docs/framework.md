# Framework and scope

## The contribution

The project addresses a computational problem: how to connect time-varying process inventories to time-varying background inventories and calculate environmental indicators on a shared time basis. The proposed framework is intended for continuous operations and a declared gate-to-gate boundary.

The mathematical formulation, the software implementation and the process demonstration are distinct. A different foreground model does not require a different conceptual framework, but it does require a new interface, inventory mapping, unit checks and application-specific validation. Generality is a design property, not evidence that every industry has already been tested.

## Three layers

| Layer | What belongs here | What it does not establish |
| --- | --- | --- |
| Mathematical framework | Time-indexed foreground/background coupling and impact assessment | A new life-cycle impact characterization method |
| Computational workflow | Data interfaces, time alignment, inventory mapping and calculation | A universally plug-and-play integration for every simulator |
| KTB1 demonstration | A continuous biomanufacturing benchmark and historical electricity signals | A validated commercial lovastatin plant or a complete product life cycle |

## Inputs and outputs

Foreground inputs carry process quantities, units and time information. Background inputs describe the relevant supply conditions over time. Inventory mappings connect those quantities to an LCA database and an explicitly selected LCIA method. Time alignment and unit consistency are prerequisites to interpreting the results.

The environmental output is a time-resolved LCIA signal. Electricity prices form a separate economic input. Comparing schedules under the two objectives does not make electricity price a substitute for environmental impact.

## Demonstrated scope and limits

- KTB1 supplies a simulated process foreground; it is a benchmark, not an operated industrial plant.
- The application uses a gate-to-gate operational boundary. Upstream burdens assigned through background datasets are not the same thing as extending the modeled process to a full product life cycle.
- Historical-data replay demonstrates the computational workflow. It is not evidence of deployment on a live plant.
- Campaign scheduling is separate from closed-loop model-predictive control. An LCA-driven MPC controller is not implemented in these notebooks.
- Claims about final annual savings and statistical independence require the reconciled, reproducible result set. Development outputs are not a substitute.

For implementation details, continue to the [reproduction guide](reproduction.md).
