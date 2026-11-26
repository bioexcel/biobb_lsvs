# Biobb Large Scale Virtual Screening changelog

## [Unreleased]

### Changes

* [CHANGE] `smina_run` reads the site coordinates file when it is launched, not when it is created: a missing file is reported by the input file check like the other inputs, and a step skipped by `restart` does not read it.
* [FIX] `smina_run`: `min_rmsd_filter` and `energy_range` are floats (smina accepts decimals, ie: a 0.5 Å RMSD filter); they were documented as integers from 1.
* [FIX] `smina_run`: the `seed` range is documented in the format of the other properties, so the JSON schema no longer marks `seed` as a workflow property.
* [DOCS] `smina_run`: the container properties document their real defaults (`container_volume_path` "/data", `container_shell_path` "/bin/bash -c"), the sample file links point to the `main` branch (the `master` links were broken), and the command line help describes the block instead of "Prepares input ligand for an smina Virtual Screening".

## What's new in version [5.1.0](https://github.com/bioexcel/biobb_lsvs/releases/tag/v5.1.0)?

### New features

* First release
* smina module: smina tool

