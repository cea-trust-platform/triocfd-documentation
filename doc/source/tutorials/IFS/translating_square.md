# Translating Square ALE (2D)


## Description of the setup

{numref}`fig:translating_square_geometry` shows the geometry of the test case you will run in this tutorial. 

This test case aims to validate the ALE (Arbitrary Lagrangian–Eulerian) implementation in TrioCFD against the [SPHERIC benchmark Test 6](https://www.spheric-sph.org/tests/test-06), which represents a 2D incompressible flow around a translating square cylinder in a rectangular tank.

```{figure} FIGURES/translating_square_geometry.png
:class: custom-image-class
:name: fig:translating_square_geometry
:alt: Geometry of the translating square setup

Geometry of the test case
```



## Tutorial setup

This tutorial will use a TrioCFD validation form as its base. It is a jupyter Notebook that is used to start  a list of TrioCFD simulations and displays various postprocessed results.

First, go to an empty directory and copy the validation form from which we will start: `TranslatingSquare_ALE_CoarseMesh`.
Note that you must have sourced the TrioCFD environment before this step.
```
cp -r $(find $project_directory -name TranslatingSquare_ALE_CoarseMesh) . && cd TranslatingSquare_ALE_CoarseMesh
```


Now, use the following commands:

- `Run_fiche`, which will start jupyter and open the notebook in the web browser.
    - Do that and execute all cells
    - Note: the run takes around 5 minutes. You can directly jump to the next step to save time.

- `Run_fiche -export_pdf`, which will run all the content of the notebook and generate a pdf report from the output of the cells.
    - Resulting pdf is located in `./build/rapport.pdf`

- Now, copy the file `./build/rapport.pdf` and the `build` directory:
    - `cp build/rapport.pdf initial.pdf`
    - `mv build initial_build`


## Modifying the test cases in the validation form

Now, edit the file `src/TranslatingSquare_ALE_CoarseMesh.data`:

- Replace `ALE { amont }` convection scheme by `ALE { muscl }`

- Change the `Solver_moving_mesh_ALE`:
    - replace `PETSC GCP { precond ssor { omega 1.5 } seuil 1e-7 impr }` into `petsc cholesky { }`


Now, use the command:
```
Run_fiche -export_pdf
```
This will rerun the simulations, postprocessings and generate the pdf report.

Now, open both the new report and the initial one:

```
cp build/rapport.pdf modified.pdf
evince initial.pdf modified.pdf &
```


What do you think of the results ? Are they better/worse/unchanged ?

Compare the `*.TU` files between the `initial_build` and `build` directories.

What can you conclude ?

<!-- 
```{dropdown} Click to display expected result



``` -->
