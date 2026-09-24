# Paper release checklist

This checklist separates repository presentation from scientific and publication readiness. No paper release or DOI has been created by the packaging update.

## Code and data

- [ ] Supply the matching MATLAB model and `step_and_get_DI.m`, with provenance and permissions.
- [ ] Confirm and export the author-tested environment; do not label the candidate dependency list a lockfile.
- [x] Align the generation exporter and main notebook filenames through shared configuration.
- [ ] Confirm complete UTC generation and price coverage and missing-value treatment.
- [ ] Resolve the time, unit, mapping and method questions in [Reproduction](reproduction.md).
- [ ] Run the workflow from a clean kernel using the documented inputs.
- [ ] Regenerate annual results, schedules, statistics and figure data from the same run.
- [ ] Verify every headline percentage, denominator and reported unit against the final manuscript.
- [ ] Export the complete hourly LCI matrix and illustrative rows requested by reviewers.

## Publication and rights

- [ ] Confirm which manuscript and SI versions may be distributed; remove unresolved comments/private metadata.
- [ ] Confirm institutional ownership and release approval for added code, models, figures and data.
- [ ] Retain upstream notices; do not change the existing licence without necessary approvals.
- [ ] Review third-party data permissions; do not include ecoinvent dumps or credentials.
- [ ] Keep unpublished controller/invention details outside the public release unless explicitly cleared.
- [ ] Update manuscript and SI links to `https://github.com/AdaRobinsonMedici/dLCA_KTB1` and the exact release.
- [ ] Confirm author names, final article title and DOI before adding publication metadata.

## Freeze the snapshot

- [ ] Confirm repository checks pass and distinguish them from the scientific run.
- [ ] Review the complete file list and final outputs with the coauthors.
- [ ] Create a paper tag, for example `v1.0.0-paper`, only after reconciliation.
- [ ] Archive the approved snapshot through an authorised service and record its DOI when issued.
- [ ] Update CITATION.cff and release notes with real metadata.

A branch or pull request in a public repository is not a private review channel. Do not use one to hold confidential source material.
