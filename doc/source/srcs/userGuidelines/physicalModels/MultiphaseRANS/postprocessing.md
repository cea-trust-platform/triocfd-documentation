(sec:postprocessing)=
# Post-processing

This chapter is an introduction or a reminder on the types of
post-processing available in TrioCFD/TRUST (section
[1.1](#post-type)) as well
as the various variables accessible (section
[1.2](#post-variables))
for correctly visualizing the TrioCFD multiphase calculations.

(post-type)=
## Types of post-processing

Regarding the case under study and the variables of interest, `TRUST`
offers a range of options for post-processing:

-   Individual points of interest ('`Point`' keyword),

-   Distributed points along a linear path ( '`Segment`' keyword),

-   Points arranged according to a predefined layout ('`Plan`' keyword),

-   Points arranged within a parallelepiped structure ('`Volume`'
    keyword),

-   Fields across the entire domain. The '`Fields`' keyword demands
    specifying the field's location on the mesh (faces, elements, or
    vertices), the field's name, the post-processing time, and a backup
    file,

-   Statistical measurement can be applied to fields to compute the mean
    value, standard deviation, or correlation between two fields.The
    '`Statistics`' keyword requires defining a time window, time step,
    and the desired statistical methods.

(post-variables)=
## Variables easily accessible

In order to ease computation post-processing, some variables are already
accessible with keywords. They are summarized in the following tables.

### Mesh-related keyword
| Name                            | Notation                         | Keyword              | Unit  |
|---------------------------------|----------------------------------|----------------------|-------|
| Cell volumes                    | $V_{cell}$                       | `Volume_maille`      | $m^3$ |
| Stability time steps            | $\Delta t$                       | `Pas_de_temps`       | $s$   |
| Volumetric porosity             | $\epsilon$                       | `Porosite_volumique` |       |
| Distance to the wall            | $y_w$                            | `Distance_Paroi`     | $m$   |
| Cell Courant number (VDF only)  | $C_o=\frac{u\Delta t}{\Delta x}$ | `Courant_maille`     |       |
| Cell Reynolds number (VDF only) | $Re=\frac{u\Delta x}{\nu}$       | `Reynolds_maille`    |       |

### Mass keywords
| Name                      | Notation         | Keyword           | Unit          |
|---------------------------|------------------|-------------------|---------------|
| Density                   | $\rho$           | `masse_volumique` | $kg.m^{-3}$   |
| Void fraction             | $\alpha$         | `Alpha`           | dimensionless |
| Mass balance on each cell | $\nabla \cdot u$ | `Divergence_U`    | $m^3.s^{-1}$  |


### Momentum equation keywords
| Name                                    | Notation                      | Keyword                     | Unit               |
|-----------------------------------------|-------------------------------|-----------------------------|--------------------|
| Velocity                                | $u$                           | `Vitesse` or `Velocity`     | $m.s^{-1}$         |
| Velocity residual                       | $u_{res}$                     | `Vitesse_residu`            | $m.s^{-2}$         |
| Kinetic energy per elements             | $\frac{1}{2}\rho u^2$         | `Energie_cinetique_elem`    | $kg.m^{-1}.s^{-2}$ |
| Total kinetic energy                    | $\frac{1}{2}\rho u^2$         | ` Energie_cinetique_totale` | $kg.m^{-1}.s^{-2}$ |
| Vorticity                               | $w=rotu$                      | `Vorticite`                 | $s^{-1}$           |
| Pressure in incompressible flow         | $\frac{P}{\rho}+ gz$          | `Pression`                  | $Pa.m^3.kg^{-1}$   |
| Pressure in incompressible flow         | $P+\rho$ gz                   | `Pression_pa` or `Pressure` | $Pa$               |
| Pressure in compressible flow           | $P$                           | `Pression`                  | $Pa$               |
| Hydrostatic pressure                    | $\rho gz$                     | `Pression_hydrostatique`    | $Pa$               |
| Total pressure                          | $P_{tot}$                     | `Pression_tot`              | $Pa$               |
| Pressure gradient                       | $\nabla (\frac{P}{\rho}+ gz)$ | `Gradient_pression`         | $m.s^{-2}$         |
| Velocity gradient                       | $\nabla u$                    | `gradient_vitesse`          | $s^{-1}$           |
| Local shear strain rate                 | $\sqrt{2S_{ij}S_{Sij}}$       | `Taux_cisaillement`         | $s^{-1}$           |
| Viscous force                           |                               | `Viscous_force`             | $kg.m^2.s^{-1}$    |
| Pressure force                          |                               | `Pressure_force`            | $kg.m^2.s^{-1}$    |
| Total force                             |                               | `Total_force`               | $kg.m^2.s^{-1}$    |
| Viscous force along X                   |                               | `Viscous_force_x`           | $kg.m^2.s^{-1}$    |
| Viscous force along Y                   |                               | `Viscous_force_y`           | $kg.m^2.s^{-1}$    |
| Viscous force along Z                   |                               | `Viscous_force_z`           | $kg.m^2.s^{-1}$    |
| Pressure force along X                  |                               | `Pressure_force_x`          | $kg.m^2.s^{-1}$    |
| Pressure force along Y                  |                               | `Pressure_force_y`          | $kg.m^2.s^{-1}$    |
| Pressure force along Z                  |                               | `Pressure_force_z`          | $kg.m^2.s^{-1}$    |
| Total force along X                     |                               | `Total_force_x`             | $kg.m^2.s^{-1}$    |
| Total force along Y                     |                               | `Total_force_y`             | $kg.m^2.s^{-1}$    |
| Total force along Z                     |                               | `Total_force_z`             | $kg.m^2.s^{-1}$    |
| Component velocity along X              | $u_X$                         | `VitesseX`                  | $m.s^{-1}$         |
| Component velocity along Y              | $u_Y$                         | `VitesseY`                  | $m.s^{-1}$         |
| Component velocity along Z              | $u_Z$                         | `VitesseZ`                  | $m.s^{-1}$         |
| Source term in non Galinean referential | $a$                           | `Acceleration_terme_source` | $m.s^{-2}$         |

### Energy equation keywords
| Name                         | Notation   | Keyword                        | Unit              |
|------------------------------|------------|--------------------------------|-------------------|
| Temperature                  | $T$        | `Temperature`                  | $K$               |
| Temperature residual         | $T_{res}$  | `Temperature_residu`           | $K.s^{-1}$        |
| Temperature variance         | $Var(T)$   | `Variance_Temperature`         | $K^{2}$           |
| Temperature dissipation rate |            | `Taux_Dissipation_Temperature` | $K^2.s^{-1}$      |
| Temperature gradient         | $\nabla T$ | `Gradient_temperature`         | $K.m^{-1}$        |
| Heat exchange coefficient    | $h$        | `H_echange_Tref`               | $W.m^{-2}.K^{-1}$ |
| Internal energy              | $U$        | `energie_interne`              | $J$               |
| Enthalpy                     | $H$        | `enthalpie`                    | $J$               |
| Irradiancy                   | $I$        | `Irradiance`                   | $W.m^{-2}$        |
| Volumic thermal power        | $P_w$      | `Puissance_volumique`          | $W.m^{-3}$        |

### Turbulence equations keywords
| Name                            | Notation      | Keyword                          | Unit            |
|---------------------------------|---------------|----------------------------------|-----------------|
| Turbulent viscosity             | $\nu_t$       | `Viscosite_turbulente`           | $m^2.s^{-1}$    |
| Turbulent dynamic viscosity     | $\mu_t$       | `Viscosite_dynamique_turbulente` | $kg.m.s^{-1}$   |
| Turbulent kinetic energy        | $\rho k$      | `Energy`                         | $kg.m^2.s^{-2}$ |
| Turbulent dissipation rate      | $\varepsilon$ | `Eps`                            | $m^2.s^{-3}$    |
| Specific dissipation rate       | $\omega$      | `omega`                          | $s^{-1}$        |
| Specific dissipation time scale | $\tau$        | `tau`                            | $s$             |
| Q-criteria                      | $Q$           | `Critere_Q`                      | $s^{-1}$        |
| Distance to the wall            | $y^+$         | `Y_plus`                         |                 |
| Friction velocity               | $u^*$         | `U_star`                         | $m.s^{-1}$      |
| Turbulent heat flux             |               | `Flux_Chaleur_Turbulente`        | $m.K.s^{-1}$    |

### Two-phase models keywords
| Name              | Notation   | Keyword    | Unit       |
|-------------------|------------|------------|------------|
| Drag force        | $F_D$      | `Drag`     | $N.m^{-3}$ |
| Lift force        | $F_L$      | `Lift`     | $N.m^{-3}$ |
| Dispersion force  | $F_{Disp}$ | `Disp`     | $N.m^{-3}$ |
| Lubrication force | $F_{Lub}$  | `Lub`      | $N.m^{-3}$ |
| Bubble diameter   | $d_b$      | `d_bulles` | $m$        |

Let's notice that physical properties (conductivity, diffusivity, etc)
can also be post-processed. Furthermore, the `Definitionchamps` keyword
can be used to create new or more complex fields for advanced
post-processing.
