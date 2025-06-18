# Homogeneous Mixture model

This chapter focuses on the modeling of homogeneous mixtures through TrioCFD multiphase. The [first
part](#HEM:eva) is a review of the use of the evanescence operator ; the [second part](#HEM:model)
describes the equilibrium models dedicated to mixtures.

(HEM:eva)=
## Homogeneous evanescence for mixture modeling
The `Pb_multiphase` framework allows to model a mixture by taking advantage of the evanescence
operator described in the [dedicated section] REF sec:evanescence. By choosing the correct values of
`alpha_res` to 1 and `alpha_res_min` to 0.5, one can reduce the system to three partial differential
equations corresponding to the dynamics of a mixture. Without any model, this approach can be
referred to as the Homogeneous Equilibrium Model as the two phases can be considered dynamically
locked and at the same temperature. This can be the starting point of a homogeneous relaxation model
approach by adding different models to describe the relation between the two phases.

Imposing the above-mentioned values lead to a simplification of Equation REF eq:evanescence_momentum:

\begin{equation}
\newcommand{\parent}[1]{\left(#1\right)}
\definecolor{myteal}{RGB}{0,128,128}
\definecolor{myslateblue}{RGB}{106,90,205}
\definecolor{mydarkorchid}{RGB}{153,50,204}
\label{eq:evanescence_momentum_HEM}
\begin{pmatrix}
{\mathcal{Q}_{\text{pred}}} \\
{\mathcal{Q}_{\text{mino}}}
\end{pmatrix}
\Longrightarrow
\begin{pmatrix}
{\mathcal{Q}_{\text{pred}}} +  {\mathcal{Q}_{\text{mino}}} \\
{v_{\text{mino}} = v_{\text{pred}} + v_{\text{drift}}}
\end{pmatrix}
\end{equation}

(HEM:model)=
## Dedicated mixture modeling

(sec:phyical_modeling_drift_velocity)=
### Drift velocity
The drift velocity of a gas phase $u_{gj}$ is defined as the velocity of the gas phase $u_g$ with
respect to the volume center of the mixture $j$. The area average $\prec F\succ $ of a quantity $F$
over the cross-sectional area $A$ is defined by:

\begin{equation}
    \prec F\succ=\frac{1}{A}\int_A FdA
\end{equation}
The one-dimensional drift-flux model is defined as:
\begin{equation}
    \frac{\prec j_g\succ}{\prec \alpha_g \succ}=C_0 \prec j\succ+V_{g0},
\end{equation}
with
\begin{align}
    &C_0 = \frac{\prec \alpha_g j \succ}{\prec \alpha_g \succ \prec  j \succ},\\
    &V_{g0} = \frac{\prec \alpha_g u_{gj} \succ}{\prec \alpha_g \succ}.
\end{align}

The model is implemented in:
```{code} c++
void Vitesse_derive_base::set_param(Param& param)
```
The drift velocity operator must fill $vr$ and $dvr$ tabs for each dimension $d$ so that:
- $\texttt{vr}({\color{myteal}k1}, {\color{mydarkorchid}k2}, d)$ Relative velocity in dimension d
- $\texttt{dvr}({\color{myteal}k1}, {\color{mydarkorchid}k2}, d, \texttt{dimension}*{\color{mydarkorchid}k2}+d)$ Relative velocity derivative regarding the inlet superficial velocity $\texttt{v}(d, {\color{mydarkorchid}k2})$
- $\texttt{vr}({\color{mydarkorchid}k2}), {\color{myteal}k1}, d)=-\texttt{output.vr}({\color{myteal}k1}, {\color{mydarkorchid}k2}), d)$
- $\texttt{dvr}({\color{myteal}k1}, {\color{mydarkorchid}k2}), d, \texttt{dimension}*{\color{mydarkorchid}k2}+d)=-\texttt{vr}({\color{myteal}k1}, {\color{mydarkorchid}k2}), d, \texttt{dimension}*{\color{mydarkorchid}k2}+d)$

The following table summarises the availability of drift velocity models in TRUST/TrioCFD:
| Model           | Used | Validated | Test case                                            |
|-----------------|------|-----------|------------------------------------------------------|
| Constant bubble | Yes  | Yes       | TRUST : canal bouillant drift & TrioCFD : Drift flux |
| Ishii-Hibiki    | Yes  | Yes       | TRUST : canal bouillant drift & TrioCFD : Drift flux |
| Spelt           | Yes  | No        |                                                      |
| Forces          | Yes  | Yes       | TRUST : canal bouillant drift & TrioCFD : Drift flux |


### Constant
The model is described in \textcite{ishii1977one} and is implemented in:
```{code} c++
void Vitesse_derive_constante::set_param(Param& param)
{
  param.ajouter("C0", &C0, Param::REQUIRED);
  param.ajouter("vg0_x", &vg0[0], Param::REQUIRED);
  param.ajouter("vg0_y", &vg0[1], Param::REQUIRED);
  if (dimension == 3) param.ajouter("vg0_z", &vg0[2], Param::REQUIRED);
}
```

### Ishii-Hibiki : Bubbly flow
The model is described in \textcite{HIBIKI2002707} and is implemented in:
```{code} c++
void Vitesse_derive_Ishii::set_param(Param& param)
{
  param.ajouter("subcooled_boiling", &sb_, Param::REQUIRED);
}
```
Default values:
- $\texttt{sb_} = 0$ (0: no, 1: yes),
- $\texttt{Cinf} = 1.2$,
- $\texttt{theta} = 1.75$,
- $\texttt{zeta} = 18.0$.

The implemented model is:
\begin{align}
  & C_0=\parent{\texttt{Cinf}+\parent{1-\texttt{Cinf}} \sqrt{\frac{\rho_g}{\rho_l}}}\parent{1-\texttt{sb_}\ exp(-\texttt{zeta}\times\alpha_g)}\\
  & \vec{V_{g0}} =-\sqrt{2}\parent{\frac{\parent{\rho_l-\rho_g}g\sigma}{\rho_l^2}}^{1/4}\parent{1-\alpha_g}^{\texttt{theta}} \frac{\vec{g}}{|g|}
\end{align}

### Spelt Biesheuvel
The model is described in \textcite{Spelt1997} and is implemented in:
```{code} c++
void Vitesse_derive_Spelt_Biesheuvel::set_param(Param& param)
```
Default values  $\texttt{Prt_} = 1.$

\begin{equation}
  \vec{V_{g0}} =\parent{-(u_g-u_l)\frac{\vec{g}}{|g|}+\frac{\nu_{\text{Spelt}}\nabla \alpha_g}{\max(\alpha_g,0.0001)}}\parent{1-C_0\alpha_g}
\end{equation}
with
- $C_0=1.0$,
- $\nu_{\text{Spelt} = \frac{\parent{C_\mu^{1/4}k^{1/2}}^2L }{u_g-u_l}\parent{\frac{1}{2}+\frac{3}{8}\parent{\frac{\tau^2}{\lambda_t}}^2\frac{\lambda_t}{L}}$,
- $L=C_\mu^{3/4}\frac{k^{3/2}}{\varepsilon}$,
- $\tau=\frac{u_g - u_l}{2g}$,
- $\lambda_t=\sqrt{10\nu_l\frac{k}{\varepsilon}}$,
- $\varepsilon=C_\mu \frac{k^2}{\nu_t}$.

### Forces
The model is implemented in:
```{code} c++
void Vitesse_derive_Forces::set_param(Param& param)
{
  param.ajouter("alpha_lim", &alpha_lim_);
}
```
Default values : $\texttt{alpha_lim_}=10^{-5}$.

\begin{equation}
  \vec{V_{g0}} =\parent{-\parent{u_g-u_l}\frac{\vec{g}}{|g|}+\frac{F^{\text{dispersion}}+F^{\text{lift}}}{f^DU_r}}\parent{1-C_0\alpha_g}
\end{equation}

(sec:phyical_modeling_frictionl_multiplier)=
### Two-phase frictional multiplier
The frictional pressure drop in gas–liquid flow can be expressed as a function of a two-phase friction multiplier \cite{FARAJI2022111863}, based on empirical correlations and both pure liquid friction $f_l$ and pure gas friction $f_g$.

The general expression of the two-phase frictional multiplier is:
\begin{equation}
    \Phi_{k}^2=\frac{(\frac{\partial p}{\partial z})|_{\text{Two-phase}}}{(\frac{\partial p}{\partial z})|_{\text{Single phase k}}}
\end{equation}
```{code} c++
void Multiplicateur_diphasique_base::set_param(Param& param)
```
The available input parameters are:
```{code} c++
const double alpha ; // Void fraction
const double rho ; //  Density
const double v ;  //Velocity
const double f ;  // Darcy coefficient as if all the flow rate was in phase k
const double mu ;  // Viscosity
const double Dh ;  // Hydraulic diameter
const double gamma ;  // Surface tension
```
The interfacial heat flux operator must fill $\mathit{coeff}$ tab so that:
- $\mathit{coeff}(k, 0)$ multiplier for the single phase friction factor
- $\mathit{coeff}(k, 1)$ multiplier for the mix friction factor

### Homogeneous
The model is implemented in :
```{code} c++
void Multiplicateur_diphasique_homogene::set_param(Param& param)
{
  param.ajouter("alpha_min", &alpha_min_);
  param.ajouter("alpha_max", &alpha_max_);
}
```
Default values : $\texttt{alpha_min_}= 0.9995$, $\texttt{alpha_max_} = 1$.\\
The model implemented is :
\begin{align}
& \Phi^2= 1+x\parent{\frac{\rho_l}{\rho_g}-1}\\
& \mathit{coeff}(n_l, 0) = \text{Frag}_l\times\Phi^2,\\
& \mathit{coeff}(n_g, 0) = \frac{\text{Frag}_g}{\alpha_g^2}
\end{align}
with
- $\text{Frag}_g = \min\parent{\max\parent{\frac{\alpha_g-\texttt{alpha_min_}}{\texttt{alpha_max_}-\texttt{alpha_min_}},0},1}$
- $\text{Frag}_l=1-\text{Frag}_g$

### Fridel: horizontal and vertical smooth tubes with $\mu_l/\mu_g<1000$
The model is described in \textcite{friedel1979improved} and is implemented in:
```{code} c++
void Multiplicateur_diphasique_Friedel::set_param(Param& param)
{
  param.ajouter("alpha_min", &alpha_min_);
  param.ajouter("alpha_max", &alpha_max_);
  param.ajouter("min_lottes_flinn", &min_lottes_flinn_);
  param.ajouter("min_sensas", &min_sensas_);
}
```
Default values:
- $\texttt{alpha_min_} = 1$,
- $\texttt{alpha_max_} = 1.1$,
- $\texttt{min_lottes_flinn_} = 0$,
- $\texttt{min_sensas_} = 0$.

The model implemented is:
\begin{equation}
   \Phi^2= E+\frac{3.24FH}{Fr^{0.0454}We^{0.035}}
\end{equation}
if $F_k \min\parent{1, 1.14429\alpha_l^{0.6492}} < \Phi^2 F_m \alpha_l^2$ and $\texttt{min_sensas}=1$ and $\texttt{min_lottes_flinn_}=1$:
\begin{align}
    &\mathit{coeff}(n_l, 0) = \frac{\text{Frac}_l}{\alpha_l^2},\\
    &\mathit{coeff}(n_g, 0) = \frac{Frac_g}{\alpha_l^2},
\end{align}
else
\begin{align}
    &\text{coeff}(n_l, 1) = \text{Frag}_l\times\Phi^2,\\
    &\text{coeff}(n_g, 1) = \text{Frag}_g\times\Phi^2
\end{align}
with
- $\text{Frag}_g=\min\parent{\max\parent{\frac{\alpha_g - \texttt{alpha_min_}}{\texttt{alpha_max_} - \texttt{alpha_min_}}, 0}, 1}$,
- $\text{Frag}_l=1-\text{Frag}_g$,
- $E=(1-x)^2+x^2\frac{\rho_lf_g}{\rho_gf_l}$
- $F=x^{0.78}(1-x)^{0.224}$
- $G=\alpha_l\rho_lu_l+\alpha_g\rho_gu_g$
- $H=(\frac{\rho_l}{\rho_g})^{0.91}(\frac{\mu_g}{\mu_l})^{0.19}(1-\frac{\mu_g}{\mu_l})^{0.7}$
- $x=\frac{\alpha_g \rho_gu_g}{G}$
- $\mathit{Fr}=\frac{\parent{\alpha_l\rho_lu_l+\alpha_g \rho_gu_g}^2}{9.81D_h\rho_m^2}$
- $\mathit{We}=\frac{G^2D_h}{\sigma \rho_m}$
- $\rho_m=\frac{1}{\frac{x}{\rho_g}+\frac{1-x}{\rho_l}}$

### Lottes and Flinn: sodium two-phase pressure drop
The model is described in \textcite{lottes1956method} and is implemented in:
```{code} c++
void Multiplicateur_diphasique_Lottes_Flinn::set_param(Param& param)
{
  param.ajouter("alpha_min", &alpha_min_);
  param.ajouter("alpha_max", &alpha_max_);
}
```
Default values : $\texttt{alpha_min_} = 0.9$, $\texttt{alpha_max_} = 0.95$. \\
The model implemented is :
\begin{equation}
    \mathit{coeff}(n_l, 0) = \begin{cases}\frac{\max\parent{\alpha_l - 1+ \texttt{alpha_max_}, 0}}{\parent{1-\texttt{alpha_min_}}^2},\text{ if }\alpha_l<1-\texttt{alpha_min_}\\
    \frac{1}{\alpha_l^2},\text{ otherwise}.
    \end{cases},
\end{equation}
\begin{equation}
    \mathit{coeff}(n_g, 0) = \min\parent{\max\parent{\frac{\alpha_g-\texttt{alpha_min_}}{\texttt{alpha_max_}-\texttt{alpha_min_}}, 0} ,1}
\end{equation}

### Muller-Steinhagen: air–water, water-hydrocarbons and refrigerants in pipes
The model is described in \textcite{MULLERSTEINHAGEN1986297} and is implemented in:
```{code} c++
void Multiplicateur_diphasique_Muhler_Steinhagen::set_param(Param& param)
{
  param.ajouter("alpha_min", &alpha_min_);
  param.ajouter("alpha_max", &alpha_max_);
  param.ajouter("min_lottes_flinn", &min_lottes_flinn_);
  param.ajouter("min_sensas", &min_sensas_);
  param.ajouter("a", &a_);
  param.ajouter("b", &b_);
  param.ajouter("c", &c_);
}
```
Default values:
- $\texttt{alpha_min_} = 1$,
- $\texttt{alpha_max_} = 1.1$
- $\texttt{a_} = 2$
- $\texttt{b_} = 1$
- $\texttt{c_} = 3$
- $\texttt{min_lottes_flinn_} = 0$
- $\texttt{min_sensas_} = 0$.

The model implemented is:
- if
  - $F_k min(1,1.14429\alpha_l^{0.6492}) < \rho_l F_m \alpha_l^2 \frac{f_m^*}{f_l}$
  - $\texttt{min_sensas}=1$
  - $\texttt{min_lottes_flinn_}=1$
  - then:

\begin{equation}
    \mathit{coeff}(n_l, 0) = \frac{\min\parent{1, 1.14429\alpha_l^{0.6492}}}{\alpha_l^2}.
\end{equation}
- else

\begin{align}
    & \mathit{coeff}(n_l, 1) = \text{Frac}_l\times\rho_l\frac{f_m^*}{f_l},\\
    & \mathit{coeff}(n_g, 1) = \text{Frac}_g\rho_g\frac{f_m^*}{f_g}
\end{align}
with
- $\text{Frac}_g=\min\parent{\max\parent{\frac{\alpha_g-\texttt{alpha_min_}}{\texttt{alpha_max_}-\texttt{alpha_min_}},0},1}$
- $\text{Frac}_l=1-\text{Frac}_g$,
- $G=\alpha_l\rho_lu_l+\alpha_g\rho_gu_g$
- $x=\frac{\alpha_g \rho_gu_g}{G}$
- $fm^*=\parent{\frac{f_l}{\rho_l}+ax^b\parent{\frac{f_g}{\rho_g}-\frac{f_l}{\rho_l}}}(1-x)^{1/c}+\frac{f_g}{\rho_g}x^c.$
