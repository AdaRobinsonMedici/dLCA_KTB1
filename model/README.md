# KTB1 model and MATLAB interface

KTB1 is the demonstration foreground model. It is not the general dLCA framework itself.

The supplied development notebook calls a MATLAB/Simulink model and `step_and_get_DI.m`. The helper is not present in the supplied package. The uploaded `.slx` is a modified development model whose exact upstream provenance and redistribution permissions must be confirmed before adding it here. This build documents the interface without uploading the model binary or inventing the missing helper.

The manuscript cites the [Boskabadi/KTB1 upstream project](https://github.com/Boskabadi/KTB1). Its model description is:

Boskabadi, M. R.; Ramin, P.; Kager, J.; Sin, G.; Mansouri, S. S. *KT-Biologics I (KTB1): A Dynamic Simulation Model for Continuous Biologics Manufacturing.* Computers & Chemical Engineering 2024, 188, 108770. https://doi.org/10.1016/j.compchemeng.2024.108770

## Local setup checklist

- Obtain the exact model revision used for the paper and retain upstream notices.
- Obtain `step_and_get_DI.m` and required MATLAB dependencies from the authors.
- Place local files under `model/local/` or configure another local directory.
- Set the model stem explicitly; do not assume a renamed upload matches the original notebook model name.
- Confirm signal names, units, time units and ordering returned by the helper.
- Check that successive samples correspond to the intended physical time intervals.
- Verify the MATLAB/Python/Engine release combination.

Do not substitute a guessed helper that returns similarly shaped arrays: matching dimensions do not establish matching physical meaning.
