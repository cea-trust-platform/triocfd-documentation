```{contents} Table of Contents
:depth: 3
```

# Reynolds-averaged Navier-Stokes modeling

Generalities about the turbulence models available in TrioCFD are given in this section. The recommended model is the $k-\omega$ SST model.

## Reynolds equations
The statistical treatment of the instantaneous Navier-Stokes equations lead to the decomposition of a field $F$ in a mean part (written $\bar{F}$) and a fluctuating part (written $f'$) using the Reynolds decomposition. We introduce the following decomposition
\begin{equation}
\rho = \bar{\rho} + \rho', \quad u_i = \bar{u}_i + u_i', \quad P = \bar{P} + P'
\end{equation}

## Generalities on eddy-viscosity models
Eddy-viscosity models are based on the analogy that turbulence plays for the flow the role viscosity plays for the fluid. Following Boussinesq hypothesis, the Reynolds stress is modeled as
\begin{equation}
R_{ij} \equiv -2 \nu_t S_{ij}S_{ij} + \frac{2}{3}k\delta_{ij}.
\end{equation}
This model introduces two new quantities, namely the turbulent viscosity $\nu_t$ and the turbulent kinetic energy $k$. To close this system, the turbulent viscosity is defined by dimensional analysis as
\begin{equation}
\nu_t = C_{\mu} f(k, X)
\end{equation}
with $X$ a variable which can be related to the turbulent kinetic energy dissipation ($\varepsilon$ or $\omega$ for instance) or the integral scale ($\ell$ for instance).

## The $k$-$\varepsilon$ models family

### Standard model
The standard $k$-$\varepsilon$ model was introduced by {cite:t}`Launder-Spalding_NumCompTurbFlow1974`. The turbulent viscosity is defined by
\begin{equation}
\nu_t = C_{\mu}\frac{k^2}{\varepsilon}
\end{equation}
with $\varepsilon$ the turbulent kinetic energy dissipation. Thus, one needs to solve two new transport equation for $k$ and $\varepsilon$:
\begin{equation}
\frac{\partial\overline{k}}{\partial t}+\overline{U}_{j}\frac{\partial\overline{k}}{\partial x_{j}} = \nu_{T}\left(\frac{\partial\overline{U}_{i}}{\partial x_{j}}+\frac{\partial\overline{U}_{j}}{\partial x_{i}}\right)\frac{\partial\overline{U}_{i}}{\partial x_{j}}+\frac{\partial}{\partial x_{j}}\left[\frac{\nu_{T}}{\sigma_{k}}\frac{\partial\overline{k}}{\partial x_{j}}\right]-\overline{\epsilon}
\end{equation}
\begin{equation}
\frac{\partial\overline{\epsilon}}{\partial t}+\overline{U}_{j}\frac{\partial\overline{\epsilon}}{\partial x_{j}} = C_{\epsilon_{1}}\nu_{T}\frac{\overline{\epsilon}}{\overline{k}}\left(\frac{\partial\overline{U}_{i}}{\partial x_{j}}+\frac{\partial\overline{U}_{j}}{\partial x_{i}}\right)\frac{\partial\overline{U}_{i}}{\partial x_{j}}+\frac{\partial}{\partial x_{j}}\left[\frac{\nu_{T}}{\sigma_{\epsilon}}\frac{\partial\overline{\epsilon}}{\partial x_{j}}\right]-C_{\epsilon_{2}}\frac{\overline{\epsilon}^{2}}{\overline{k}}
\end{equation}
It introduces five constants whose standard values are
\begin{equation}
C'_{\eta}=0.09, \quad C_{\epsilon_{1}}=1.44, \quad C_{\epsilon_{2}}=1.92, \quad \sigma_{k}=1.0, \quad \sigma_{\epsilon}=1.3.
\end{equation}

For specific type of flows, some authors suggest modifying the two coefficiens $C_{\varepsilon_1}$ and $C_{\varepsilon_2}$:

| Reference                            | $C_{\epsilon_{1}}$ | $C_{\epsilon_{2}}$ | Flows         |
|--------------------------------------|--------------------|--------------------|---------------|
| {cite:t}`Jones-Launder_IJHMT1972`    | 1.55               | 2.00               | High Reynolds |
| {cite:t}`Launder-Sharma_LettHMT1974` | 1.44               | 1.92               | Rotating      |
| {cite:t}`Chien_AIAA1982`             | 1.35               | 1.92               | Low Reynolds  |
| {cite:t}`Fan_etal_AIAA1993`          | 1.39               | 1.80               | Low Reynolds  |
| {cite:t}`Morgans-etal_Conf1999`      | 1.60               | 1.92               | Jet           |
| {cite:t}`Bahari-Hejazi_IJPMS2009`    | 1.40               | 1.92               | Buoyancy      |

One must keep in mind that the $C_{\varepsilon_2}$ constant was set to reproduce the decay of
turbulent kinetic energy in homogeneous isotropic turbulence. Those values must be modified with
caution. Details about modeling and the constants can be found in {cite:t}`Schiestel2008`.

### Realizable model

{cite:t}`Shi_etal_keps-realisable_CF1995` proposed a modification of the $k$-$\varepsilon$ model to ensure realizability of the turbulent kinetic energy using the Schwarz inequality. The two equations writes

\begin{equation}
\frac{\partial\overline{k}}{\partial t}+\overline{U}_{j}\frac{\partial\overline{k}}{\partial x_{j}} = \frac{\partial}{\partial x_{j}}\left(\frac{\nu_{T}}{\sigma_{k}}\frac{\partial\overline{k}}{\partial x_{j}}\right)+\left(2\nu_{T}S_{ij}-\frac{2}{3}\overline{k}\delta_{ij}\right)\frac{\partial\overline{U}_{i}}{\partial x_{j}}-\overline{\epsilon},
\end{equation}
\begin{equation}
\frac{\partial\overline{\epsilon}}{\partial t}+\overline{U}_{j}\frac{\partial\overline{\epsilon}}{\partial x_{j}} = \frac{\partial}{\partial x_{j}}\left[\frac{\nu_{T}}{\sigma_{\epsilon}}\frac{\partial\overline{\epsilon}}{\partial x_{j}}\right]+C_{1}S\epsilon-C_{2}\frac{\overline{\epsilon}^{2}}{\overline{k}+\sqrt{\nu\overline{\epsilon}}}
\end{equation}
with
\begin{align}
&S=\sqrt{2S_{ij}S_{ij}},\quad C_{1}=\max\left\{ 0.43,\,\frac{\eta}{5+\eta}\right\} ,\quad\eta=\frac{S\overline{k}}{\overline{\epsilon}}\\
&C_{\eta}=\frac{1}{A_{0}+A_{s}U^{(*)}\frac{\overline{k}}{\overline{\epsilon}}},\quad A_{0}=4,\quad A_{s}=\sqrt{6}\cos\phi,\\
&\phi=\frac{1}{3}\arccos\left(\sqrt{6}W\right),\quad W=\frac{S_{ij}S_{jk}S_{ki}}{(S_{ij}S_{ij})^{3/2}}\\
&U^{(*)}=\sqrt{S_{ij}S_{ij}+\tilde{\Omega}_{ij}\tilde{\Omega}_{ij}},\quad\tilde{\Omega}_{ij}=\Omega_{ij}-2\epsilon_{ijk}\omega_{k},\quad\Omega_{ij}=\overline{\Omega}_{ij}\epsilon_{ijk}\omega_{k}\label{eq:Coeff3_real}
\end{align}
where $\overline{\Omega}_{ij}$ is the mean rotation rate and $\overline{S}_{ij}$ the mean shear rate.

The validation of this model was done by {cite:t}`Angeli_Leterrier_keps-real_NT2018`.


### Low-Reynolds models

Wall functions are used to bypass the need to solve the Navier-Stokes equations and the turbulence
model near the wall. The $k$-$\varepsilon$ model, when combined with a wall function, enables
the simulation of the core flow while avoiding excessive computational costs associated with a very
fine mesh near the wall. However, this type of model is not suitable when the first mesh point is
located within the viscous sublayer $(y+ < 30)$. As the Reynolds number increases, the
thickness of this viscous sublayer becomes negligible, making the $k$-$\varepsilon$ model with a
wall function well-suited for high Reynolds number flows. This is why it is also referred to as the
high-Reynolds $k$-$\varepsilon$ model.

In contrast, when studying flows with low Reynolds numbers, the viscous sublayer becomes more
significant, making the use of a wall function inappropriate. For low Reynolds number flows, it may be
more advantageous to use models known as low-Reynolds models, which incorporate damping functions
and discretization-dependent terms to account for the numerical resolution of the viscous
sublayer. These models also facilitate the study of the entire flow, particularly near the wall,
addressing phenomena such as recirculation effects and separation in complex geometries.

The low-Reynolds $k$-$\varepsilon$ model keeps the transport equation for $k$ from the
basic $k$-$\varepsilon$ model unchanged but modifies the equation for $\varepsilon$ by
adding damping terms in the region close to the wall, where the Reynolds number is locally
lower. Due to the need for a finer wall mesh, this model is consequently more computationally
expensive than the standard $k$-$\varepsilon$ model.

\begin{equation}
\frac{\partial\overline{k}}{\partial t} + \overline{U}_{j}\frac{\partial\overline{k}}{\partial x_{j}} = \nu_{T}\left(\frac{\partial\overline{U}_{i}}{\partial x_{j}} + \frac{\partial\overline{U}_{j}}{\partial x_{i}}\right)\frac{\partial\overline{U}_{i}}{\partial x_{j}} + \frac{\partial}{\partial x_{j}}\left[\left(\nu + \frac{\nu_{T}}{\sigma_{k}}\right)\frac{\partial\overline{k}}{\partial x_{j}}\right] - \overline{\epsilon} - \overline{\mathcal{K}}
\end{equation}
\begin{align}
\frac{\partial\overline{\epsilon}}{\partial t} + \overline{U}_{j}\frac{\partial\overline{\epsilon}}{\partial x_{j}} = C_{\epsilon_{1}}\nu_{T}\frac{\overline{\epsilon}}{\overline{k}}f_{\epsilon_{1}}\left(\frac{\partial\overline{U}_{i}}{\partial x_{j}} + \frac{\partial\overline{U}_{j}}{\partial x_{i}}\right)\frac{\partial\overline{U}_{i}}{\partial x_{j}} &+ \frac{\partial}{\partial x_{j}}\left[\left(\nu + \frac{\nu_{T}}{\sigma_{\epsilon}}\right)\frac{\partial\overline{\epsilon}}{\partial x_{j}}\right] \\ &- C_{\epsilon_{2}}f_{\epsilon_{2}}\frac{\overline{\epsilon}^{2}}{\overline{k}} + \overline{\mathcal{E}}
\end{align}
\begin{equation}
\nu_{T} = C_{\eta}f_{\eta}\frac{\overline{k}^{2}}{\overline{\epsilon}}
\end{equation}

#### Launder & Spalding model
The model is defined in by equations (2.3-4) and (2.3-5) in {cite}`Launder-Spalding_NumCompTurbFlow1974`.

The two extra terms $\overline{\mathcal{K}}$ and $\overline{\mathcal{E}}$ are defined by
\begin{equation}
\overline{\mathcal{K}} = 2\nu\left(\frac{\partial\overline{k}^{1/2}}{\partial x_j}\right)^2 \quad \quad
\overline{\mathcal{E}} = 2.0\,\nu\,\nu_{T}\left(\frac{\partial^{2}\overline{U}_{i}}{\partial x_j \partial x_l}\right)
\end{equation}
with the coefficient and dampings functions
\begin{equation}
f_{\epsilon_{1}} = 1,\quad f_{\epsilon_{2}} = 1.0 - 0.3\exp\left(-Re_{t}^{2}\right), \quad f_{\eta} = \exp\left(\frac{-2.5}{\left(1 + \mathit{Re}_t/50\right)}\right)
\end{equation}
where $\mathit{Re}_t = \overline{k}^2/\nu\overline{\varepsilon}$ is the turbulent Reynolds number. The following constants are used
\begin{equation}
C_{\eta}=0.09 \quad C_{\epsilon_{1}}=1.44 \quad C_{\epsilon_{2}}=1.92 \quad \sigma_{k}=1.0 \quad \sigma_{\epsilon}=1.3
\end{equation}

#### Jones & Launder model
The model is defined in {cite}`Jones-Launder_IJHMT1972` and is very closed to the Launder & Spalding one. The terms $\mathcal{K}$ and $\mathcal{E}$ are defined by
\begin{equation}
\overline{\mathcal{K}}=2\nu\left(\frac{\partial\overline{k}^{1/2}}{\partial y}\right)^{2},\quad\overline{\mathcal{E}} = 2.0\,\nu\,\nu_{T}\left(\frac{\partial^{2}\overline{U}_{i}}{\partial y^{2}}\right).
\end{equation}
They differ only by the partial derivatives in the denominator. The 3D version is similar tout the Launder & Spalding model. The coefficient are
\begin{equation}
C_{\eta}=0.09,\quad C_{\epsilon_{1}}=1.55,\quad C_{\epsilon_{2}}=2, \quad \sigma_{k}=1.0, \quad \sigma_{\epsilon}=1.3.
\end{equation}

#### Lam & Bremhorst model
The model is defined in {cite}`Lam-Bremhorst_JFE1981`.

In this model, the extra terms $\mathcal{K}$ and $\mathcal{E}$ are nulls. The three functions $f_{\epsilon_{1}}$, $f_{\epsilon_{2}}$, $f_{\eta}$ are defined by
\begin{align}
&f_{\epsilon_{1}} = 1 + \left(\frac{A_{c}}{f_{\eta}}\right)^{3},\quad f_{\epsilon_{2}} = 1-\exp\left(-Re_{t}^{2}\right),\\
&f_{\eta} =\left(1 - \exp\left(-A_{\eta}Re_{y}\right)\right)^{2}\left(1 + \frac{A_{t}}{Re_{t}}\right)
\end{align}
with $Re_y=\overline{k}^{1/2}y/\nu$ the wall-based Reynolds number. The five coefficients are

\begin{align}
&A_{\eta}=0.0165,\quad A_{t}=20.5,\quad A_{c}=0.05,\\
&C_{\epsilon_{1}}=1.44, C_{\epsilon_{2}}=1.92.
\end{align}

#### Launder & Sharma model
The model is defined in {cite}`Launder-Sharma_LettHMT1974`.

This model was established for rotating flows using a rotating disc. The independent coordinates in this configuration are the radial distance to the disc axis $r$ and the normal distance to the disc surface $y$. In this case, additionnal terms which depend on the gradient of $V_{\theta}/r$ appear in the equations for $\overline{k}$ and $\overline{\varepsilon}$.

The functions $f_{\epsilon_{2}}$ and $f_{\eta}$ are defined by
\begin{equation}
f_{\epsilon_{2}} = 1.0 - 0.3\exp\left(-Re_{t}^{2}\right),\quad f_{\eta}=\exp\left(-3.4/\left(1+Re_{t}/50\right)^{2}\right)
\end{equation}
and the coefficients are defined by
\begin{equation}
C_{\eta}=0.09, C_{\epsilon_{1}}=1.44, C_{\epsilon_{2}}=1.92, \sigma_{k}=1.0, \sigma_{\epsilon}=1.3.
\end{equation}

#### EASM Baglietto model

To be documented.

## The $k$-$\omega$ models family
 Description of the general idea around the $k$-$\omega$ models. The only recommended model is the
 SST one.

### Standard model (Wilcox 2008)
The standard model is available just for testing reasons, it must not be used.

### Baseline model
Baseline model is available just for research purpose, it must not be used.

### SST model
The SST model is the way.

## Scalar models
About temperature

## References
```{bibliography}
```
