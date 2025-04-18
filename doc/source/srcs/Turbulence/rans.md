# Reynolds-averaged Navier-Stokes modeling

Generalities about the turbulence models available in TrioCFD are given in this section. The recommended model is the {math}`k-\omega` SST model.

## Reynolds equations
The statistical treatment of the instantaneous Navier-Stokes equations lead to the decomposition of a field {math}`F` in a mean part (written {math}`\bar{F}`) and a fluctuating part (written {math}`f'`) using the Reynolds decomposition. We introduce the following decomposition
```{math}
\rho = \bar{\rho} + \rho', \quad u_i = \bar{u}_i + u_i', \quad P = \bar{P} + P'
```

## {math}`k-\varepsilon` model

description of the {math}`k-\varepsilon` model

## Realizable {math}`k-\varepsilon` model

description of the realizable {math}`k-\varepsilon` model

## Low-Reynolds {math}`k-\varepsilon` models

Wall functions are used to bypass the need to solve the Navier-Stokes equations and the turbulence
model near the wall. The {math}`k-\varepsilon` model, when combined with a wall function, enables
the simulation of the core flow while avoiding excessive computational costs associated with a very
fine mesh near the wall. However, this type of model is not suitable when the first mesh point is
located within the viscous sublayer {math}`(y+ < 30)`. As the Reynolds number increases, the
thickness of this viscous sublayer becomes negligible, making the {math}`k-\varepsilon` model with a
wall function well-suited for high Reynolds number flows. This is why it is also referred to as the
high-Reynolds {math}`k-\varepsilon` model.

In contrast, when studying flows with low Reynolds numbers, the viscous sublayer becomes more
significant, making the use of a wall function inappropriate. For low Reynolds number flows, it may be
more advantageous to use models known as low-Reynolds models, which incorporate damping functions
and discretization-dependent terms to account for the numerical resolution of the viscous
sublayer. These models also facilitate the study of the entire flow, particularly near the wall,
addressing phenomena such as recirculation effects and separation in complex geometries.

The low-Reynolds {math}`k-\varepsilon` model keeps the transport equation for {math}`k` from the
basic {math}`k-\varepsilon` model unchanged but modifies the equation for {math}`\varepsilon` by
adding damping terms in the region close to the wall, where the Reynolds number is locally
lower. Due to the need for a finer wall mesh, this model is consequently more computationally
expensive than the standard {math}`k-\varepsilon` model.

```{math}
&\frac{\partial\overline{k}}{\partial t} + \overline{U}_{j}\frac{\partial\overline{k}}{\partial x_{j}} = \nu_{T}\left(\frac{\partial\overline{U}_{i}}{\partial x_{j}} + \frac{\partial\overline{U}_{j}}{\partial x_{i}}\right)\frac{\partial\overline{U}_{i}}{\partial x_{j}} + \frac{\partial}{\partial x_{j}}\left[\left(\nu + \frac{\nu_{T}}{\sigma_{k}}\right)\frac{\partial\overline{k}}{\partial x_{j}}\right] - \overline{\epsilon} - \overline{\mathcal{K}}\\
&\frac{\partial\overline{\epsilon}}{\partial t} + \overline{U}_{j}\frac{\partial\overline{\epsilon}}{\partial x_{j}} = C_{\epsilon_{1}}\nu_{T}\frac{\overline{\epsilon}}{\overline{k}}f_{\epsilon_{1}}\left(\frac{\partial\overline{U}_{i}}{\partial x_{j}} + \frac{\partial\overline{U}_{j}}{\partial x_{i}}\right)\frac{\partial\overline{U}_{i}}{\partial x_{j}} + \frac{\partial}{\partial x_{j}}\left[\left(\nu + \frac{\nu_{T}}{\sigma_{\epsilon}}\right)\frac{\partial\overline{\epsilon}}{\partial x_{j}}\right] - C_{\epsilon_{2}}f_{\epsilon_{2}}\frac{\overline{\epsilon}^{2}}{\overline{k}} + \overline{\mathcal{E}}\\
&\nu_{T} = C_{\eta}f_{\eta}\frac{\overline{k}^{2}}{\overline{\epsilon}}

```

### Launder & Spalding model
The two extra terms {math}`\overline{\mathcal{K}}` and {math}`\overline{\mathcal{E}}` are defined by
```{math}
\overline{\mathcal{K}} = 2\nu\left(\frac{\partial\overline{k}^{1/2}}{\partial x_j}\right)^2 \quad \quad
\overline{\mathcal{E}} = 2.0\nu\nu_{T}\left(\frac{\partial^{2}\overline{U}_{i}}{\partial x_j \partial x_l}\right)
```
with the coefficient and dampings functions
```{math}
f_{\epsilon_{1}} = 1,\quad f_{\epsilon_{2}} = 1.0 - 0.3\exp\left(-Re_{t}^{2}\right), \quad f_{\eta} = \exp\left(\frac{-2.5}{\left(1+\mathit{Re}_t/50\right)}\right)
```
where {math}`\mathit{Re}_t = \frac{\overline{k}^2}{\nu\overline{\varepsilon}}` is the turbulent Reynolds number. The following constants are used
```{math}
C_{\eta}=0.09 \quad C_{\epsilon_{1}}=1.44 \quad C_{\epsilon_{2}}=1.92 \quad \sigma_{k}=1.0 \quad \sigma_{\epsilon}=1.3
```

### Jones & Launder model

### Lam & Bremhorst model

### Launder & Sharma model

## {math}`k-\omega` SST model
 Description of the {math}`k-\omega` SST model


# Useful bibliography
## For the hurried reader
- [[link](https://cel.hal.science/cel-01521982v1 "link")] (french) E. Goncalves (2017) Lessons on turbulence modeling

## For the patient reader
- [[link](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470610848)] R. Schiestel (2008) Modeling and Simulation of Turbulent Flows
