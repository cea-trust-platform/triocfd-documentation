(sec:interfa-forces)=
# Interfacial forces models

This chapter details the physical models for the Two-fluid approach. First, the definition of fluid
properties is defined using two methods, through the dataset (section~\ref{sec:fluid_properties} and
through an external software (section~\ref{sec:fluid-prop-ext}). Then the interfacial forces are
described in section~\ref{sec:interfa-forces}. Some particular source terms for the momentum
(section~\ref{sec:analytical}) and the mass equations (section~\ref{sec:injection}). The management
of the dispersed phase diameter is described in section~\ref{sec:diam-mgmt}.

The interfacial forces defined below are source terms that can be added to the momentum equation and
represent the mechanical interactions between the phases. Then the equations of motion for each
phase velocities are coupled by the interfacial forces.

## The Drag force
The general expression of the drag force is:

\begin{equation}
\newcommand{\parent}[1]{\left(#1\right)}
\definecolor{myteal}{RGB}{0,128,128}
\definecolor{myslateblue}{RGB}{106,90,205}
\definecolor{mydarkorchid}{RGB}{153,50,204}
\newcommand {\norm} [1] {\vert #1 \vert}

\overrightarrow{F_{l\rightarrow g}^D}= - \frac{3}{4} C_D \frac{\alpha_g\rho_l}{d_b} \norm{\norm{\overrightarrow{u_g}-\overrightarrow{u_l}}} \parent{\overrightarrow{u_g}-\overrightarrow{u_l}}=-f^{D}||\overrightarrow{u_g}-\overrightarrow{u_l}||\left(\overrightarrow{u_g}-\overrightarrow{u_l}\right)
\end{equation}

The force is implemented in:
```{code} c++
void Source_Frottement_interfacial_base::set_param(Param& param)
{
  Param param(que_suis_je());
  param.ajouter("a_res", &a_res_);
  param.ajouter("dv_min", &dv_min);
  param.ajouter("exp_res", &exp_res);
  param.ajouter("beta", &beta_);
  param.lire_avec_accolades_depuis(is);

  const Pb_Multiphase& pbm = ref_cast(Pb_Multiphase, equation().probleme());
  if (pbm.has_correlation("frottement_interfacial")) correlation_ = pbm.get_correlation("frottement_interfacial"); //correlation fournie par le bloc correlation
  else correlation_.typer_lire(pbm, "frottement_interfacial", is); //sinon -> on la lit
  return is;
}
```

Default values:
- $\texttt{a_res_} = -1.$,
- $\texttt{dv_min} = 0.01$,
- $\texttt{beta_}= 1.$,
- $\texttt{exp_res} = 2$.

The interfacial drag operator must fill coeff tab so that :
- $\text{coeff}({\color{myteal}k1}, {\color{mydarkorchid}k2}, 0) = f^{D}||\overrightarrow{u_{{\color{myteal}k1}}}-\overrightarrow{u_{{\color{mydarkorchid}k2}}}||;$
- $\text{coeff}({\color{myteal}k1}, {\color{mydarkorchid}k2}, 1) = f^{D};$ (it is the derivative of $\text{coeff}({\color{myteal}k1}, {\color{mydarkorchid}k2}, 0)$ with respect to the relative velocity)
- $\text{coeff}({\color{mydarkorchid}k2}, {\color{myteal}k1}, 0) = \text{coeff}({\color{myteal}k1}, {\color{mydarkorchid}k2}, 0);$
- $\text{coeff}({\color{mydarkorchid}k2}, {\color{myteal}k1}, 1) = \text{coeff}({\color{myteal}k1}, {\color{mydarkorchid}k2}, 1);$

Availability of drag force models in TrioCFD/CMFD.

| Model                  | Used | Validated | Test case                                        |
|------------------------|------|-----------|--------------------------------------------------|
| Constant               | Yes  | Yes       | TrioCFD/Tube analytique & Trust/Tube analytique, |
| Composant              | Yes  | No        |                                                  |
| Ishii Zuber Deformable | Yes  | No        |                                                  |
| Ishii Zuber            | Yes  | No        |                                                  |
| Tomiyama               | Yes  | Yes       | TrioCFD/CoolProp & TrioCFD/Gabillet              |
| Weber                  | Yes  | No        |                                                  |
| Wallis                 | Yes  | No        |                                                  |
| Sonnenburg             | Yes  | No        |                                                  |
| Garnier                | Yes  | No        |                                                  |
| Rusche                 | Yes  | No        |                                                  |
| Simmonet               | Yes  | No        |                                                  |
| Zenit                  | Yes  | No        |                                                  |

### Constant drag coefficient
The model is implemented in :
```{code} c++
void Frottement_interfacial_bulles_constant::set_param(Param& param)
{
param.ajouter("coeff_derive", &C_d_, Param::REQUIRED);
param.ajouter("rayon_bulle", &r_bulle_);
}
```
Default values:
- $\texttt{r_bulles_}=-1$,
- $\texttt{C_d_}=-123.$.

If no rayon_bulle is specified, it takes d_bulles.

The model implemented is :
\begin{equation}
   f^{D}=\frac{3}{4}\frac{C_d\alpha_g\rho_l}{d_b}.
\end{equation}

### Composant drag coefficient
The model is implemented in :
```{code} c++
void Frottement_interfacial_bulles_composant::set_param(Param& param)
{
param.ajouter("coeff_derive", &C_d_, Param::REQUIRED);
param.ajouter("rayon_bulle", &r_bulle_);
}
```
Default values:
- $\texttt{r_bulle_}=-100$
- $\texttt{C_d}=-100.$.

The model implemented is:
\begin{equation}
   f^{D}_{ij}=\frac{3}{4}\frac{C_d\alpha_i\alpha_j\rho_m}{d_b},
\end{equation}
with $\rho_m=\sum_k \alpha_k \rho_k$ and $i \neq j$.

### Ishii-Zuber : viscous regime
The model is described in {cite:t}`Ishii1979` and is implemented in:
```{code} c++
void Frottement_interfacial_Ishii_Zuber_Deformable::set_param(Param& param)
{
  param.ajouter("beta", &beta_);
  param.ajouter("constante_gravitation", &g_);
}
```
Default values:
- $\texttt{g_}=9.81$,
- $\texttt{beta_}=1.$.

The model implemented is:
\begin{equation}
   f^{D}=\frac{1}{2}\alpha_g\rho_l\sqrt{\frac{\left(\rho_l-\rho_g\right)\times{}g}{\sigma}}\frac{1}{\sqrt{max\left(1-\alpha_g,\ 0.001\right)}}.
\end{equation}
If $\alpha_l < 10^{-6}$, then $f^D\times{}\alpha_l\times{}10^{-6}$.

### Ishii-Zuber : viscous regime and particle regime
The model is also described in {cite:t}`Ishii1979` and is implemented as:
```{code} c++
void Frottement_interfacial_Ishii_Zuber::set_param(Param& param)
{
  param.ajouter("beta", &beta_);
  param.ajouter("constante_gravitation", &g_);
}
```
Default values:
- $\texttt{g_}=9.81$,
- $\texttt{beta_}=1.$.

The model implemented is:
\begin{equation}
   f^{D}=\frac{3}{4}\frac{\text{max}\parent{\frac{24}{Re_b}\left(1+0.1Re_b^{0.75}\right),\ \frac{2}{3}\sqrt{\frac{\left(\rho_l-\rho_g\right)g d_b^2}{\sigma}}}\beta \alpha_g\rho_l}{d_b },
\end{equation}
with $Re_b=\frac{\rho_l d (u_g-u_l)}{\mu_l}$.

### Tomiyama : contaminated drag coefficient
The model is described in {cite:t}`Tomiyama1998` and is implemented in:
```{code} c++
void Frottement_interfacial_Tomiyama::set_param(Param& param)
{
  param.ajouter("beta", &beta_);
  param.ajouter("constante_gravitation", &g_);
  param.ajouter("contamination", &contamination_);
}
```
Default values:
- $\texttt{g_}=9.81$,
- $\texttt{beta_}=1.$,
- $contamination=0$.

The model implemented is:
\begin{equation}
f_D =\frac{3}{4}\frac{\alpha_g\rho_l}{d} \begin{cases} \max(\min(16/Re_b(1+.15Re^{.687}), 48/Re_b), 8Eo/(3+12)) \text{, No contamination (0)}\\
	\max(\min(24/Re_b(1+.15Re_b^{.687}), 72/Re_b), 8Eo/(3Eo+12)) \text{, Slight contamination (1)}\\
	\max(24/Re_b(1+.15Re_b^{.687}), 8Eo/(3Eo+12)) \text{, High contamination (2)} \end{cases}
\end{equation}
with
- $Eo = \frac{g(\rho_l-\rho_v)d^2}{\sigma}$,
- $Re_b=\frac{\rho_l d_b (u_g-u_l)}{\mu_l}$.

If $\alpha_l < \num{1.e-6}$, then $f^D\times{}\alpha_l\times{}\num{1e6}$.

This formulation was chosen as shown in {cite:t}`Sugrue2017`, it yields similar results as other
closures and one can adjust the level of contamination.

### Bubble critical diameter (incoming)
The model is described partially in {cite:t}`Kuo1988` and is implemented in:
```{code} c++
void Frottement_interfacial_Weber::set_param(Param& param)
{
    param.ajouter("Weber_critique", &We_c);
}
```
Default values:
- $We_ c=8.$.

The model implemented is:
\begin{equation}
   f^{D}=\frac{6\alpha_g}{\pi d_b^{*3}}\frac{24}{Re_b}(1+0.1Re_b^{0.75}),
\end{equation}
with $d_b^*= \frac{\sigma}{\rho_l(u_g-u_l)^2}We_c$, $Re_b=\frac{\rho_l d_b^* (u_g-u_l)}{\mu_l}$.

{\color{red} Warning}: not homogeneous

### Wallis: annular flow
The model is described in {cite:t}`Wallis1970` and is implemented in:
```{code} c++
void Frottement_interfacial_Wallis::set_param(Param& param)
```
The model implemented is:
\begin{equation}
   f^{D}=\num{5e-3}\times{}\rho_g\frac{4\sqrt{\alpha_g}}{D_h}\parent{1+300\frac{1-\sqrt{1-\alpha_g}}{2}}
\end{equation}

### Sonnenburg: drift flux ?
The model is described in REFNEC and is implemented in:
```{code} c++
void Frottement_interfacial_Sonnenburg::set_param(Param& param)
```
The model implemented is:
\begin{equation}
   f^{D}=\rho_l\frac{\alpha_l\alpha_g}{D_h}\Big(\frac{16}{9}(1-\alpha_g^*(1-\frac{9}{16}\sqrt{\frac{\rho_g}{\rho_l}}))\frac{1-\alpha_g^{*40}}{tanh(32\alpha_g^*)}\Big)^2,
\end{equation}
with $\alpha_g^*=min(max(\alpha_g,0.001),0.999)$

### Garnier: bubble swarm correction
The model is described in {cite:t}`Garnier2002` and is implemented in:
```{code} c++
void Frottement_interfacial_Garnier::set_param(Param& param)
```
The model implemented is:
\begin{equation}
   f^{D}_{new}=f^{D}\begin{cases} \alpha_l\times 114.2,\text{ if }\alpha_l< 0.5  \\
          \parent{1-\alpha_g^{1/3}}^{-2},\text{ if not}.
   \end{cases}
\end{equation}
{\color{red} Warning}: Validated for $\alpha_g  < 0.35$, $D_{sm} < 5.5mm$.

### Rusche: swarm correction
The model is described in {cite:t}`Rusche2000` and is implemented in:
```{code} c++
void Frottement_interfacial_Rusche::set_param(Param& param)
```
The model implemented is:
\begin{equation}
   f^{D}_{new}=f^{D}\parent{\exp\parent{3.64\alpha_g}+\alpha_g^{0.864}}
\end{equation}
{\color{red} Warning}: Validated for $\alpha_g  < 0.5$.

### Simonnet: bubble swarm correction
The model is described in {cite:t}`Simonnet2007` and is implemented in:
```{code} c++
void Frottement_interfacial_Simonnet::set_param(Param& param)
```
The model implemented is:
\begin{equation}
   f^{D}_{new}=f^{D}\alpha_l\parent{\alpha_l^{25} + \parent{4.8\frac{\alpha_g}{\alpha_l}}^{25}}^{-2/25}
\end{equation}
{\color{red} Warning}: Validated for $\alpha_g  < 0.3$, $D_{sm} < 10 mm$.

### Zenit: bubble swarm correction
The model is described in {cite:t}`Zenit2001` and is implemented in:
```{code} c++
void Frottement_interfacial_Zenit::set_param(Param& param)
```
The model implemented is:
\begin{equation}
   f^{D}_{new}=f^{D}\frac{\parent{1+3\alpha_g}^2}{\alpha_l^2}
\end{equation}
{\color{red} Warning}: Validated for  $\alpha_g  < 0.18$.

## The Lift force
The general expression of the lift force is:
\begin{equation}
	\overrightarrow{F_{l\rightarrow v}^L}
	= -C_L \rho_l \alpha_g \parent{\overrightarrow{u_g} - \overrightarrow{u_l}} \wedge \overrightarrow{u_l}
	= -f^L\parent{\overrightarrow{u_g} - \overrightarrow{u_l}} \wedge \overrightarrow{u_l}
\end{equation}

The force is implemented in:
```{code} c++
void Source_Portance_interfaciale_base::set_param(Param& param)
{
  Param param(que_suis_je());
  param.ajouter("beta", &beta_);
  param.ajouter("g", &g_);
  param.lire_avec_accolades_depuis(is);

  Pb_Multiphase *pbm = sub_type(Pb_Multiphase, equation().probleme()) ? &ref_cast(Pb_Multiphase, equation().probleme()): NULL;

  if (!pbm || pbm->nb_phases() == 1) Process::exit(que_suis_je() + ": not needed for single-phase flow!");

  for (int n = 0; n < pbm->nb_phases(); n++) //recherche de n_l, n_g: phase {liquide,gaz}_continu en priorite
    if (pbm->nom_phase(n).debute_par("liquide") && (n_l < 0 || pbm->nom_phase(n).finit_par("continu")))  n_l = n;

  if (n_l < 0) Process::exit(que_suis_je() + ": liquid phase not found!");

  if (pbm->has_correlation("Portance_interfaciale")) correlation_ = pbm->get_correlation("Portance_interfaciale"); //correlation fournie par le bloc correlation
  else correlation_.typer_lire((*pbm), "Portance_interfaciale", is); //sinon -> on la lit

  pbm->creer_champ("vorticite"); // Besoin de vorticite

  return is;
}
```
Default values:
- $\texttt{beta_} = 1.$,
- $\texttt{g_} = 9.81$.

The interfacial lift operator must fill `out.Cl` tab so that:
- $Cl({\color{myteal}k1}, {\color{mydarkorchid}k2}) = f^L ;$
- $Cl({\color{mydarkorchid}k2}, {\color{myteal}k1}) = Cl({\color{myteal}k1}, {\color{mydarkorchid}k2});$

Availability of lift force models in TrioCFD/CMFD:

| Model    | Used | Validated | Test case                                                        |
|----------|------|-----------|------------------------------------------------------------------|
| Constant | Yes  | Yes       | TrioCFD/Tube analytique, TrioCFD/CoolProp, Trust/Tube analytique |
| Sugrue   | Yes  | Yes       | TrioCFD/CoolProp, TrioCFD/Gabillet                               |
| Tomiyama | Yes  | No        |                                                                  |

### Constant lift coefficient
The model is implemented in:
```{code} c++
void Portance_interfaciale_Constante::set_param(Param& param)
{
  param.ajouter("Cl", &Cl_, Param::REQUIRED);
}
```
Default values:
- $\texttt{Cl_}=-123.$

The model implemented is:
\begin{equation}
   f^{L} = C_L\rho_l\alpha_g\text{max}\parent{\text{min}\parent{\frac{\alpha_l - 0.05}{0.25},\ 1 },\ 0}
\end{equation}
The void fraction correction is used to damp the lift at too high void fractions.


### Sugrue
The model is described in REFNEC and is implemented in:
```{code} c++
void Portance_interfaciale_Sugrue::set_param(Param& param)
{
  param.ajouter("constante_gravitation", &g_);
}
```
Default values:
- $\texttt{g_}=9.81$.

The model implemented is:
\begin{equation}
   f^{L} = \rho_l\alpha_g \max\parent{1.0155-0.0154\exp\parent{8.0506\alpha_g},\ 0} \times \text{min}\parent{5.0404-5.0781(Wo)^{0.0108},\ 0.03}
\end{equation}
with
- the wobbling number $\mathit{Wo}=\min\parent{\frac{k_lEo}{\max\parent{\parent{u_g-u_l}^2,\ 10^{-8}}},\ 6.}$
- the Eotvos number $\mathit{Eo}=\frac{g\parent{\rho_l-\rho_g}d_b^2}{\sigma}$

### Tomiyama: lift sign reversal
The model is described in {cite:t}`Tomiyama2002` and is implemented in:
```{code} c++
void Portance_interfaciale_Tomiyama::set_param(Param& param)
{
  param.ajouter("constante_gravitation", &g_);
}
```
Default values:
- $\texttt{g_}=9.81$.

The model implemented is:
\begin{equation}
   f^{L} = \rho_l\alpha_g\begin{cases}
   \min\parent{0.288\tanh\parent{(0.121 \times Re_b},\ f\parent{\mathit{Eo}}}\text{, if } \mathit{Eo}<4 \\
   f(\mathit{Eo}) \text{, if } 4 \leq \mathit{Eo} \leq 10.7 \end{cases}
\end{equation}
with
- the Eotvos number $\mathit{Eo}=\frac{g\parent{\rho_l-\rho_g}d_b^2}{\sigma}$
- $f\parent{\mathit{Eo}} = 0.00105\times{}\mathit{Eo}^3 - 0.0159\times{}\mathit{Eo}^2 - 0.0204\times{} \mathit{Eo} + 0.474$.

## The Added mass force
The general expression of the added mass force is:
\begin{equation}

\newcommand{\pluseq}{\mathrel{+}=}
\newcommand{\minuseq}{\mathrel{-}=}
\newcommand{\timeseq}{\mathrel{*}=}

\overrightarrow{F_{l\rightarrow v}^{AM}}= C_{AM}\alpha_g\rho_l\frac{D(u_g-u_l)}{Dt}=f^{AM}\frac{D(u_g-u_l)}{Dt}
\end{equation}

The model is implemented in:
```{code} c++
void Masse_ajoutee_base::set_param(Param& param)
{
*     IN:
 *         alpha[n]  -> void fraction
 *         rho[n]    -> density
 *
 *     IN/OUT:
 *        a_r(k, l)   -> update in momentum equation
 *
 *     NB: no need of derivative because it is past void fraction
}
```

Default values:
- $\texttt{limiter_liquid_} = 0.5$.

The added mass operator must add to `a_r` tab so that:
- $a_r({\color{myteal}k1},  {\color{myteal}k1} ) \pluseq f^{AM};$ coefficient in front of $\frac{D(u_{{\color{myteal}k1}})}{Dt}$ in ${\color{myteal}k1}$ equation
- $a_r({\color{myteal}k1},  {\color{mydarkorchid}k2} ) \minuseq f^{AM};$ coefficient in front of $\frac{D(u_{{\color{mydarkorchid}k2}})}{Dt}$ in ${\color{myteal}k1}$ equation
- $a_r({\color{mydarkorchid}k2}, {\color{mydarkorchid}k2} ) \pluseq f^{AM};$ coefficient in front of $\frac{D(u_{{\color{mydarkorchid}k2}})}{Dt}$ in ${\color{mydarkorchid}k2}$ equation
- $a_r({\color{mydarkorchid}k2},  {\color{myteal}k1} ) \minuseq f^{AM};$ coefficient in front of $\frac{D(u_{{\color{myteal}k1}})}{Dt}$ in ${\color{mydarkorchid}k2}$ equation

Availability of added mass force models in TrioCFD/CMFD

| Model       | Used | Validated | Test case                                      |
|-------------|------|-----------|------------------------------------------------|
| Constant    | Yes | Yes       | TrioCFD/Tube analytique, Trust/Tube analytique |
| Wijngaarden | Yes | No        |                                                |
| Zuber       | Yes | No        |                                                |


### Constant added mass coefficient
The model is implemented in:
```{code} c++
void Masse_ajoutee_Coef_Constant::set_param(Param& param)
{
  param.ajouter("beta", &beta);
  param.ajouter("inj_ajoutee_liquide", &inj_ajoutee_liquide_);
  param.ajouter("inj_ajoutee_gaz", &inj_ajoutee_gaz_);
  param.ajouter("limiter_liquid", &limiter_liquid_);
}
```

Default values:
- $\texttt{beta}=0.5$,
- $\texttt{inj_ajoutee_liquid_}=1.$
- $\texttt{inj_ajoutee_gaz_}=1.$
- $\texttt{limiter_liquid_} = 0.5$.

The model implemented is:
\begin{equation}
   f^{AM}=\min\parent{\beta \rho_l\alpha_g,\ \rho_l\alpha_l\times{}\text{limiter_liquid_}}
\end{equation}

{\color{red} Warning}: direct void fraction influence limited at $\alpha_{gmax}=\frac{\texttt{limiter_liquid_}}{\texttt{limiter_liquid_}+\texttt{beta}}$ with the default value $\alpha_{gmax}=0.5$.

For the injected mass flux $\dot{m}_{inj}$,
\begin{equation}
   \dot{m}_{inj}=\min\parent{\texttt{beta}\rho_l,\texttt{limiter_liquid_}\times \frac{\alpha_l}{\alpha_g}}\times\dot{m}\times{}\begin{cases} \texttt{inj_ajoutee_gaz_},\text{ for gas phase,}\\ \texttt{inj_ajoutee_liquid_}, \text{for liquid phase.}
   \end{cases}
\end{equation}
If $\alpha_g< 0.0001$, no limiter part.

### Wijngaarden: two bubbles interaction
The model is described in {cite:t}`Biesheuvel1984` and is implemented in:
```{code} c++
void Masse_ajoutee_Wijngaarden::set_param(Param& param)
{
  param.ajouter("beta", &beta);
  param.ajouter("inj_ajoutee_liquide", &inj_ajoutee_liquide_);
  param.ajouter("inj_ajoutee_gaz", &inj_ajoutee_gaz_);
  param.ajouter("limiter_liquid", &limiter_liquid_);
}
```
Default values:
- $\texttt{beta}=0.5$
- $\texttt{inj_ajoutee_liquid_}=1.$
- $\texttt{inj_ajoutee_gaz_}=1.$
- $\texttt{limiter_liquid_} = 0.5$.

The model implemented is:
\begin{equation}
   f^{AM}=\min\parent{\beta\parent{1 + 2.78\alpha_g} \rho_l\alpha_g,\ \rho_l\alpha_l\times{}\texttt{limiter_liquid_}}
\end{equation}
{\color{red} Warning}: direct void fraction influence limited at:
\begin{equation}
    \alpha_{gmax}=\frac{5}{139\beta} \parent{\sqrt{25\texttt{beta}+328\texttt{beta} \times \texttt{limiter_liquid_}+25 \texttt{limiter_liquid_}^2} -5\parent{\texttt{beta}+\texttt{limiter_liquid_}}}.
\end{equation}
Default value:
- $\alpha_{gmax}\approx 0.34$

For the injected mass flux $\dot{m}_{inj}$,
\begin{equation}
   \dot{m}_{inj}=\min\parent{\texttt{beta}(1+2.78\alpha_g),\ \texttt{limiter_liquid_}\frac{\alpha_l}{\alpha_g}} \rho_l\dot{m}\times\begin{cases} \texttt{inj_ajoutee_gaz_},\text{ for gas phase},\\ \texttt{inj_ajoutee_liquid_},\text{ for liquid phase}.
   \end{cases}
\end{equation}
If $\alpha_g< 0.0001$, no limiter part.

{\color{red} Warning}: Corrected value in {cite:t}`Biesheuvel1984` is 3.32 instead of 2.78.

### Zuber: swarm of compliant bubbles
The model is described in {cite:t}`Zuber1964` and is implemented in:
```{code} c++
void Masse_ajoutee_Zuber::set_param(Param& param)
{
  param.ajouter("beta", &beta);
  param.ajouter("inj_ajoutee_liquide", &inj_ajoutee_liquide_);
  param.ajouter("inj_ajoutee_gaz", &inj_ajoutee_gaz_);
  param.ajouter("limiter_liquid", &limiter_liquid_);
}
```
Default values:
- $\texttt{beta}=0.5$
- $\texttt{inj_ajoutee_liquid_}=1.$
- $\texttt{inj_ajoutee_gaz_}=1.$
- $\texttt{limiter_liquid_} = 0.5$.

The model implemented is:
\begin{equation}
   f^{AM}=\min\parent{\beta\frac{1 + 2\alpha_g}{\max\parent{1 - \alpha_g, 0.001}} \rho_l\alpha_g,\ \rho_l\alpha_l \texttt{limiter_liquid_}}
\end{equation}
{\color{red} Warning}: direct void fraction influence limited at:
\begin{equation}
\alpha_{gmax}=\begin{cases}
        \frac{\sqrt{\texttt{beta}^2 + 12\texttt{beta}\times \texttt{limiter_liquid_}} - \texttt{beta} - 2\texttt{limiter_liquid_}}{2\parent{2\texttt{beta} - \texttt{limiter_liquid_}}},\text{ if }2\texttt{beta}-\texttt{limiter_liquid_}\neq 0 \\
        \frac{2}{5},\text{ otherwise}.
    \end{cases}
\end{equation}

Default value:
- $\alpha_{gmax}\approx 0.303$

For the injected mass flux $\dot{m}_{inj}$,
\begin{equation}
   \dot{m}_{inj}=\min\parent{\beta\frac{1 + 2\alpha_g}{\alpha_l},\ \texttt{limiter_liquid_}\frac{\alpha_l}{\alpha_g}} \rho_l\dot{m}\times\begin{cases} \texttt{inj_ajoutee_gaz_},\text{ for gas phase},\\ \texttt{inj_ajoutee_liquid_},\text{ for liquid phase}.
   \end{cases}
\end{equation}
If $\alpha_g< 0.0001$, no limiter part.


## The Dispersion force
The general expression of the turbulent dispersion force is:
\begin{equation}
\overrightarrow{F_{l\rightarrow v}^T}= - f^T \nabla \alpha_g
\end{equation}

The force is implemented in:
```{code} c++
void Source_Dispersion_bulles_base::set_param(Param& param)
{
  Param param(que_suis_je());
  param.ajouter("beta", &beta_);
  param.lire_avec_accolades_depuis(is);

  Pb_Multiphase *pbm = sub_type(Pb_Multiphase, equation().probleme()) ? &ref_cast(Pb_Multiphase, equation().probleme()): NULL;

  if (!pbm || pbm->nb_phases() == 1) Process::exit(que_suis_je() + ": not needed for single-phase flow!");

  if (pbm->has_correlation("Dispersion_bulles")) correlation_ = pbm->get_correlation("Dispersion_bulles"); //correlation fournie par le bloc correlation
  else Process::exit(que_suis_je() + ": the turbulent dispersion correlation must be defined in the correlation bloc.");

  return is;
}
```

Default values:
- $\texttt{beta_} = 1.$.

The added mass operator must add to `out.Ctd` tab so that:
- $Ctd({\color{myteal}k1}, {\color{mydarkorchid}k2})=f^{T};$ coefficient in front of $\nabla \alpha_{{\color{myteal}k1}}$
- $Ctd({\color{mydarkorchid}k2}, {\color{myteal}k1})=f^{T};$ coefficient in front of $\nabla \alpha_{{\color{mydarkorchid}k2}}$

Availability of dispersion force models in TrioCFD/CMFD.

| Model              | Used | Validated | Test case                                      |
|--------------------|------|-----------|------------------------------------------------|
| Constant bubble    | Yes  | Yes       | TrioCFD/Tube analytique, Trust/Tube analytique |
| Constant turbulent | Yes  | Yes       | TrioCFD/Tube analytique,                       |
| Lopez              | Yes  | No        |                                                |
| Burns              | Yes  | Yes       | TrioCFD/CoolProp, TrioCFD/Gabillet             |


### Constant bubble dispersion coefficient
The model is described in {cite:t}`Marfaing2016` and is implemented in:
```{code} c++
void Dispersion_bulles_turbulente_constante::set_param(Param& param)
{
  param.ajouter("D_td_star", &D_td_star_, Param::REQUIRED);
}
```
The model implemented is:
\begin{equation}
   f^{T}=D_{td}\rho_l (u_g-u_l)^2
\end{equation}

### Constant turbulent dispersion coefficient
The model is described in {cite:t}`Bertodano1994` and is implemented in:
```{code} c++
void Dispersion_bulles_turbulente_constante::set_param(Param& param)
{
  param.ajouter("C_td", &C_td_);
}
```
Default values:
- $\texttt{C_td_}=0.1$.

The model implemented is:
\begin{equation}
   f^{T} = C_{td}\rho_l k_l
\end{equation}

### Lopez de Bertodano: Stokes regime
The model is described in {cite:t}`Bertodano1998` and is implemented in:
```{code} c++
void Dispersion_bulles_turbulente_Bertodano::set_param(Param& param)
```

Default values:
- $\texttt{Prt_} = 0.9$.

The model implemented is:
\begin{equation}
   f^{T} = 2\rho_l k_l \frac{1}{\parent{1 + St}\times St},
\end{equation}
with
- $St=\frac{\tau^F}{\tau^t}$
- $\tau^t=\frac{\nu_t}{k_l}$
- $\tau^F = \frac{\frac{4}{3}\rho_g d}{C_d\rho_l\parent{u_g - u_l}}$.

{\color{red} Warning}, in the literature:
\begin{equation}
   f^{T}=\rho_lk_l\frac{C_{\mu}^{1/4}}{(1+St)St},
\end{equation}
with $\tau^t=C_{\mu}^{3/4}\frac{k_l}{\varepsilon_l}$.

### Burns: Favre averaged drag
The model is described in {cite:t}`Burns2004` and is implemented in:
```{code} c++
void Dispersion_bulles_turbulente_constante::set_param(Param& param)
{
  param.ajouter("minimum", &minimum_);
  param.ajouter("a_res", &a_res_);
  param.ajouter("g_", &g_);
  param.ajouter("coefBIA_", &coefBIA_);
}
```

Default values:
- $\texttt{Prt_} = .9 $
- $\texttt{minimum_} = -1.$
- $\texttt{a_res_} = -1.$
- $\texttt{g_} = 9.81$
- $\texttt{C_lambda_} = 2.7$
- $\texttt{gamma_} = 1.$
- $\texttt{coefBIA_} = 0.$

The model implemented is:
\begin{equation}
   F^{T} = \frac{f^D\norm{\vec{u_g} - \vec{u_l}}\parent{\nu_t + \nu_{\parent{BIA}}}}{\mathit{Pr}_t} \parent{\frac{1}{\alpha_g}\nabla \alpha_g - \frac{1}{\alpha_l}\nabla \alpha_l}
\end{equation}
with
- $\nu_t = C_\mu\frac{k^2}{\varepsilon}$,
- $\nu_{\text{BIA}} = \texttt{coefBIA_} \frac{k_{\text{WIT}}}{\omega_{\text{WIT}}}$,
- $\omega_{\text{WIT}} = 2\mu_l \frac{Re_b}{C_{\lambda}^2 d^2} \max\parent{\min\parent{\frac{16}{Re_b}\parent{1 + 0.15\times{}\mathit{Re}_b^{0.687}},\ \frac{48}{\mathit{Re}_b}},\ 8\frac{\mathit{Eo}}{3\parent{\mathit{Eo} + 4}}}$.

{\color{red} Warning} in the literature:
\begin{equation}
   f^{T}=\frac{f^D\norm{\vec{u_g} - \vec{u_l}}\nu_t}{\mathit{Pr}_t}\parent{\frac{1}{\alpha_g} + \frac{1}{1 - \alpha_g}}
\end{equation}

## The Wall force
### Antal: wall lubrication
The model is described in {cite:t}`Antal1991` and is implemented in:
```{code} c++
void Correction_Antal_PolyMAC_P0::set_param(Param& param)
{
  param.ajouter("Cw1", &Cw1_);
  param.ajouter("Cw2", &Cw2_);
}
```
Default values:
- $\texttt{Cw1_} =  -0.1$,
- $\texttt{Cw2_} =  0.147$.

The model implemented is:
\begin{equation}
   F^{WL} = C_{WL}\alpha_g\rho_l\frac{\parent{\vec{u_g} - \vec{u_l}}^2}{d_b}\vec{n},
\end{equation}
with
\begin{equation}
   C_{WL} = \max\parent{-C_{W1} + C_{W2}\frac{d_b}{2y},\ 0}
\end{equation}

{\color{red} Warning} This force was developped for fully developed laminar bubbly two-phase flows.

### Lubchenko: wall force dumping

WARNING: ONLY IN POLYMAC

The model is partially described in {cite:t}`Lubchenko2018` and the dumping is implemented in:
```{code} c++
void Correction_Lubchenko_PolyMAC_P0::set_param(Param& param)
{
  param.ajouter("beta_lift", &beta_lift_);
  param.ajouter("beta_disp", &beta_disp_);
  param.ajouter("portee_disp", &portee_disp_);
  param.ajouter("portee_lift", &portee_lift_);
  param.ajouter("use_bif", &use_bif_);
}
```

Default values:
- $\texttt{beta_lift_} =  1. $
- $\texttt{beta_disp_} =  1. $
- $\texttt{portee_disp_}= 1.$
- $\texttt{portee_lift_}= 1.$.

The wall force dumping implemented is a mix between the one proposed by {cite:t}`Lubchenko2018` and
BIF near-wall dumping.  The first part is a lift dumping close to the wall as:

\begin{equation}
	C_L \rightarrow \begin{cases} 0 \quad\text{, if } y/d_b < 1/2\times{}\texttt{portee_lift_}  \\
	C_L\parent{3\parent{\frac{2y}{d_b} - 1}^2 - 2\parent{\frac{2y}{d_b} - 1}^3} \quad\text{, if } 1/2\times{}\texttt{portee_lift_} \leq y/d_b < 1\times{}\texttt{portee_lift_} \\
	C_L \quad\text{, if } y/d_b \geq 1\times\texttt{portee_lift_} \end{cases}
\end{equation}

The second part is a dispersion balanced force $F^{Tcorr}$ in the range $y/d <
1\times\texttt{portee_disp_}$ obtained from the dispersion force by replacing
$\underline{\nabla}\alpha_g$ by:

\begin{equation}
	 \underline{\nabla}\alpha_g = \alpha_g\frac{1}{y}\frac{d_b\times\texttt{portee_disp_} - 2y}{d_b\times\texttt{portee_disp_} - y}\ \overrightarrow{n}
\end{equation}

The last part aims to cancel the BIF contribution $0.5d$ away from the wall.
Test cases are available in TrioCFD/CoolProp and TrioCFD/Gabillet.

## The Tchen force
{\color{red} Warning}: This force is a good example of implementation but we discourage its use.

The general expression of the Tchen force {cite}`Tchen1947` is:
\begin{equation}
\overrightarrow{F_{l\rightarrow g}}= \alpha_g\rho_l \frac{\partial \overrightarrow{u_l}}{\partial t}
\end{equation}
The force is implemented in:
```{code} c++
void Source_Force_Tchen_base::set_param(Param& param)
```
It is discritized in right side of the equation `secmem` as:
\begin{equation}
 \alpha_g^n\rho_l^n \frac{u_l^n-u^{n-1}}{\Delta t}
\end{equation}

The following picture explains the volume management due to velocity located in faces:
ADD FIGURE FROM PDF

Black squares represents a mesh element. The blue dashed rectangle is \texttt{domaine.volumes_entrelaces()} and the blue hached part is \texttt{domaine.volumes_entrelaces_dir()}.
label: entrelace

The local void fraction $\alpha_{\text{loc}}$ is computed from cells on both sides of the face (called here
top and bottom) as follows:

\begin{equation}
    \alpha_{\text{loc}}=\begin{cases} \alpha_k(\text{bottom}) \times \frac{\text{volume entrelace bottom}}{\text{volume entrelace}} +  \alpha_k(\text{top}) \times \frac{\text{volume entrelace top}}{\text{volume entrelace}},\text{ if not toward a boundary},\\
        \alpha_k(\text{bottom}),\text{ otherwise}.
    \end{cases}
\end{equation}

One can refer to Figure \ref{entrelace} to understand volume entrelace. The density is computed the
same way. Finally, we add in `secmem` the full term and in `mat` (incremental velocity matrix)
without the increment of velocity, as follows:

\begin{align}
   & \text{fac} = \alpha_{\text{loc}} \times \rho_{\text{loc}}\\
   & \text{secmem}  \pluseq \text{fac}\times \frac{u^n - u^{n-1}}{\Delta t}\begin{cases}1,\text{ if in gas},\\ -1,\text{ if in liquid} \end{cases}.\\
   & M_v \minuseq \frac{\text{fac}}{\Delta t}\begin{cases}1,\text{ if in gas},\\ -1,\text{ if in liquid} \end{cases}.
\end{align}
