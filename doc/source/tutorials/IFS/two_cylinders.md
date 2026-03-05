# Two Cylinders ALE (2D)


## Description of the setup

{numref}`fig:cylinders_mesh` shows the geometry of the test case you will run in this tutorial. 

It consists of the annulus region between two coaxial cylinders, with the inner cylinder having an imposed motion.

The inner cylinder has harmonic motion : $U_x = A \sin(w \times t)$ where A is
the amplitude of displacement and w the angular frequency of displacement.

```{figure} FIGURES/2cylinders_mesh.png
:class: custom-image-class
:name: fig:cylinders_mesh
:alt: Mesh of two concentric circles

Geometry of the test case
```



## Tutorial setup

First, go to an empty directory and copy the base TrioCFD test case from which we will start: `TwoCylindersALE_jdd1`
```
triocfd -copy TwoCylindersALE_jdd1 && cd TwoCylindersALE_jdd1
```

Open the datafile `TwoCylindersALE_jdd1.data` in a text editor of your choice.



## Modifying the test case


Start by making the following changes in the file `FTD_all_VDF.data`. The goal is to have a simulation fast enough so that you will be able to visualize what happens. The results will probably not be very valid physically.

- In the `Scheme_euler_implicit` block:
    - Set `nb_pas_dt_max` to a large number.
    - Set `facsec` to 30 and `facsec_max` to 100.
    - Set `tmax` to 2.

- In the `Post_processing` of the problem:
    - set `format` to lata.
    - set `dt_post` to 0.1.

- Change the amplitude and frequency of the displacement to 0.1 and 2 respectively:
    - The formula is `0.1*2*cos(2*t)`.
    - You have to make this change in two places:
        - The speed of the mesh boundary: `Imposer_vit_bords_ALE`.
        - The `CircleA` `boundary_conditions` of `Navier_Stokes_standard_ALE`.



## Running and visualizing the simulation

Now, you can run the calculation:
```
triocfd TwoCylindersALE_jdd1
```


It should run in a few minutes at most. If it takes too long, you may increase the `facsec`.

Once it is done, open with visit (you can do it before the end and reopen from visit to obtain new postprocessed timesteps).
```
visit -o TwoCylindersALE_jdd1.lata
```

Display the Mesh and the vector field `VITESSE_SOM_dom`, then start the time slider.

Over the total time (=2), you should see the inside circle go to the right then come back to the left.

The velocity field is probably not correct because we set a facsec way too high in our implicit scheme, in order to shorten the simulation for the sake of this exercise.


```{dropdown} Click to display expected result

:::{figure} ./FIGURES/2cylinders_end_result.png

:::
```