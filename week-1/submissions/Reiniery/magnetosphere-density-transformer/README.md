# Magnetosphere density transformer

**Author:** Reiniery Villalta (UCLA) · **Field:** space physics / magnetospheric physics · **Class level:** 1 · **Agent budget:** 5 hours

The solver receives aligned THEMIS electron-density observations and five-minute OMNI SYM-H histories from 2009–2013. It must train and save one transformer model, report year-separated performance, and visualize both prediction quality and quiet/disturbed equatorial magnetosphere reconstructions.

## Difficulty

The task asks for a continuous, time-dependent density reconstruction from sparse spacecraft trajectories rather than ordinary interpolation at observed locations. Density spans many orders of magnitude, the three THEMIS probes sample the system irregularly, geomagnetic history matters, and evaluation shifts forward to an entirely unseen year. Space physicists who construct empirical magnetospheric models must make these same choices about temporal alignment, spatial representation, validation, and extrapolation.

The density and position measurements are real derived observations from THEMIS probes A, D, and E supplied by the author. SYM-H comes from NASA Goddard Space Flight Center's [SPDF five-minute High Resolution OMNI archive](https://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/). The authoring script filters to `L <= 10`, aligns each target with the preceding 60 five-minute SYM-H bins, and packages the public and hidden year ranges as compressed arrays.

## Reference solution

The reference solution groups the 60-value SYM-H history into 12 chronological patches, embeds them with sinusoidal positional encoding, adds an L/MLT context token, and processes the tokens with a two-layer transformer encoder. It trains on 2009–2011, selects the lowest-RMSE checkpoint on 2012, evaluates 2013, exports a CPU TorchScript model, and produces the requested metrics and figures.

The reference run obtained RMSE/R² of 1144.8/0.771 on training, 2002.9/0.621 on validation, 8898.9/0.251 on the visible 2013 test set, and 19297.4/0.075 on the hidden 2014 set. The much lower hidden-year score is expected distribution shift and is part of the scientific difficulty.

## Verification

The offline verifier checks that all four artifacts exist and parse, that both figures are readable at a useful resolution, and that the TorchScript model accepts the specified 63-column input and emits finite non-negative densities. It then evaluates all 144,566 hidden 2014 observations and requires RMSE no greater than 19,900 cm⁻³ and R² of at least 0.02.

The reference model has about 600 cm⁻³ of RMSE margin and 0.055 of R² margin, allowing competent alternatives with different attention layouts or optimizers to pass. A no-skill constant-mean prediction has R² of zero and approximately 20,062 cm⁻³ RMSE, so it fails both the skill requirement and the RMSE ceiling; malformed files, negative densities, and models that only memorize the visible years also fail.

## Attempts

See `authoring/attempts.md`.
