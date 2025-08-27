# Dispersed phase size modeling

(sec:diam-mgmt)=
## Equivalent diameter for dispersed phase

A fundamental aspect of modeling the interaction between liquid and gas phases lies in precisely
predicting the concentration of interfaces. Some models rely on either the interfacial area
concentration ($ai$) or an equivalent diameter ($Dsm$). In this context, the dispersed fluid is
depicted as a collection of bubbles with diverse diameters, which essentially acts as a topological
description for the fluid stage. This dispersed fluid is distinguished by two interlinked
attributes:
- a distribution of bubble diameters and
- the concentration of interfaces.
We can define the Sauter-Mean Diameter ($\mathit{Dsm}$) of the distribution ($f_d$) of sizes D as:

\begin{equation}
\newcommand{\pluseq}{\mathrel{+}=}
\newcommand{\minuseq}{\mathrel{-}=}
\newcommand{\timeseq}{\mathrel{*}=}
\newcommand {\parent} [1] {\left( #1 \right)}

\mathit{Dsm}=\frac{\int f_dD^3 dD}{\int f_d D^2 dD}
\end{equation}

The relationship between the void fraction ($\alpha$) and the Sauter-Mean Diameter ($\mathit{Dsm}$) hinges on
calculating the area concentration per unit volume ($A_i=\pi D^2$). This relationship can be
expressed as follows:

\begin{align}
\mathit{Dsm} &= \frac{\int f_dD^3 dD}{\int f_d D^2 dD}\\
             &=6\frac{\int f_d V dv}{\int f_d A_i dV}\\
             &=6\frac{\alpha}{ai}
\end{align}

Finally, to have a correct representation of the dispersed phase, it is sufficient to impose an
equivalent diameter, but it is also possible to add a transport equation for the interfacial area
concentration.

(Dsmuserdefine)=
### User defined diameter

#### Uniform diameter
It is possible to simply impose a constant diameter at every point in space. The model is
implemented in \texttt{Diametre_bulles_constant}:

```{code} c++
void Diametre_bulles_constant::set_param(Param& param)
{
  Param param(que_suis_je());
  param.ajouter("diametre", &d_bulle_, Param::REQUIRED);
  param.lire_avec_accolades_depuis(is);

  Pb_Multiphase& pb = ref_cast(Pb_Multiphase, pb_.valeur());
  int N = pb.nb_phases();
  const Discret_Thyd& dis=ref_cast(Discret_Thyd,pb.discretisation());
  Noms noms(N), unites(N);
  noms[0] = "diametre_bulles";
  unites[0] = "m";
  Motcle typeChamp = "champ_elem" ;
  const Domaine_dis& z = ref_cast(Domaine_dis, pb.domaine_dis());
  dis.discretiser_champ(typeChamp, z.valeur(), scalaire, noms , unites, N, 0, diametres_);

  champs_compris_.ajoute_champ(diametres_);

  for (int n = 0; n < pb.nb_phases(); n++) //recherche de n_l, n_g: phase {liquide,gaz}_continu en priorite
    if (pb.nom_phase(n).debute_par("liquide") && (n_l < 0 || pb.nom_phase(n).finit_par("continu")))  n_l = n;
  if (n_l < 0) Process::exit(que_suis_je() + ": liquid phase not found!");

  DoubleTab& tab_diametres = diametres_->valeurs();
  for (int i = 0 ; i < tab_diametres.dimension_tot(0) ; i++)
    for (int n = 0 ; n <N ; n++)
      if (n!=n_l) tab_diametres(i, n) = d_bulle_;

  return is;
}
```
Default value:
- $\texttt{d_ bulle_} =-100$.

#### Non-uniform diameter
It is possible to impose a user-defined diameter that varies spatially through the TRUST fields. The
model is implemented in `Diametre_bulles_champ`:

```{code} c++
void Diametre_bulles_champ::set_param(Param& param)
{
  Champ_Don diametres_don_;
  is >> diametres_don_;

  Pb_Multiphase& pb = ref_cast(Pb_Multiphase, pb_.valeur());
  int N = pb.nb_phases();
  const Discret_Thyd& dis=ref_cast(Discret_Thyd,pb.discretisation());
  Noms noms(N), unites(N);
  noms[0] = "diametre_bulles";
  unites[0] = "m";
  Motcle typeChamp = "champ_elem" ;
  const Domaine_dis& z = ref_cast(Domaine_dis, pb.domaine_dis());
  dis.discretiser_champ(typeChamp, z.valeur(), scalaire, noms , unites, N, 0, diametres_);
  champs_compris_.ajoute_champ(diametres_);
  diametres_->affecter(diametres_don_.valeur());
  diametres_.valeurs().echange_espace_virtuel();
  return is;
}
```
Default value:
- $\texttt{d_ bulle_ }=-100$.

(Dsmu1grp)=
## Interfacial area concentration with 1 group (incoming)

### The general equation
Two separated size-group methods are popular for the prediction of interfacial area
concentration. One based on having an arbitrary number of groups to reproduce a distribution,
referred as MUSIG or i-MUSIG {cite}`Wang2005,Das2010,Liao2011` and the other reproducing the
distribution thanks to the Mean Sauter diameter referred as IATE. The generalized Interfacial Area
Transport Equation (IATE) developed by Kocamustafaogullari and Ishii
{cite}`Kocamustafaogullari1994a,Kocamustafaogullari1994b`.

The general expression for adiabatic flows with $\psi^{internal}_{j}$ a source term and
$\psi^{intergroup}_j$ an intergroup term is then:

\begin{align}
\definecolor{codebackground}{RGB}{245, 245, 245}         % Gris clair pour le fond
\definecolor{codeword}{RGB}{0, 0, 0}                     % Noir pour le fond
\definecolor{codeborder}{RGB}{100, 100, 100}             % Gris pour la bordure
\definecolor{codekeyword1}{RGB}{255, 140, 0}             % Orange pour la première classe de mots clés
\definecolor{codekeyword2}{RGB}{22, 25, 237}             % bleu océan
\definecolor{codekeyword3}{RGB}{ 146, 41, 223}           % purple
\definecolor{codekeyword4}{RGB}{255, 50, 50}             % red

\frac{\partial a_{i}}{\partial t} + \underbrace{\nabla\cdot\parent{\mathbf{U} a_{i}}}_{\text{convection}} = &\underbrace{\frac{2}{3}\frac{a_{i}}{\alpha}\frac{D\alpha}{Dt}}_{\text{source of volume change}}\\\quad & + \underbrace{\sum_j \psi^{\text{intergroup}}_{j}}_{\text{intergroup sources}} + \underbrace{\sum_j \psi^{\text{internal}}_{j}}_{\text{intragroup sources}}.
\end{align}

The terms in green need new modeling linked to coalescence and break-up.

Let's remind that:

\begin{equation}
 \frac{D\alpha\rho_g}{Dt}=\alpha\frac{d\rho_g}{dt}+\rho_g\frac{D\alpha}{Dt}=\Gamma_{transfer}+\Gamma_{nucleation}
\end{equation}

Then we can substitute:

\begin{equation}
 \frac{D\alpha}{Dt}=\frac{1}{\rho_g}\parent{\Gamma_{\text{transfer}}+\Gamma_{\text{nucleation}}-\alpha\frac{d\rho_g}{dt}}
 \end{equation}

It gives the following equation:

\begin{equation}
\begin{aligned}
\frac{\partial a_{i}}{\partial t} + \underbrace{\nabla\cdot(\mathbf{U} a_{i})}_{\text{convection}} = \underbrace{-\frac{2}{3}\frac{a_{i}}{\rho_g}\frac{d\rho_g}{dt}}_{\text{Density change}}
+ \underbrace{\frac{2}{3}\frac{a_{i}}{\alpha}\frac{\Gamma_{\text{transfer}}}{\rho_g}}_{\text{Condensation}}
+ \underbrace{\frac{2}{3}\frac{a_{i}}{\alpha}\frac{\Gamma_{\text{nucleation}}}{\rho_g}}_{\text{Nucleation}}&
+ & \\
\underbrace{\sum_j \psi^{\text{intergroup}}_{j}}_{\text{intergroup sources}}
+ \underbrace{\sum_j \psi^{\text{internal}}_{j}}_{\text{intragroup sources}}.
\end{aligned}
\end{equation}

The density change model is:

\begin{equation}
    -\frac{2}{3}\frac{a_{i}}{\rho_g}\frac{d\rho_g}{dt}
\end{equation}

It is implemented in \texttt{Variation_rho_Elem_PolyMAC_P0}:
```{code} c++
Void Variation_rho::set_param(Param& param)
```

It fills the following matrices:
\begin{align}
    &M_{ai} \minuseq  \frac{2}{3}\frac{1-\frac{\rho_g^{n-1}}{\rho_g^n}}{\Delta t}\\
    &M_{T} \minuseq  \frac{2}{3} \frac{a^n_i}{\Delta t} \frac{\rho_g^{n-1}}{(\rho_g^{n})^2}(-\texttt{dT_rho})\\
    &M_{P} \minuseq  \frac{2}{3}\frac{a^n_i}{\Delta t} \frac{\rho_g^{n-1}}{(\rho_g^{n})^2}(-\texttt{dP_rho})\\
    &\texttt{secmem} \pluseq  \frac{2}{3}a^n_i\frac{1-\frac{\rho_g^{n-1}}{\rho_g^n}}{\Delta t}
\end{align}

For example, the chain rule for the temperature gives:

\begin{align}
    \frac{d\parent{\frac{1}{\rho_g}\frac{d\rho_g}{dt}}}{dT}
    & = \frac{d\rho_g}{dT} \parent{\frac{d}{d\rho_g} \parent{\frac{1}{\rho_g}} \frac{d\rho_g}{dt} + \frac{1}{\rho_g} \frac{d}{d\rho_g} \parent{\frac{d\rho_g}{dt}}}\\
& = \frac{d\rho_g}{dT} \parent{-\parent{\frac{1}{\rho_g^2}} \frac{d\rho_g}{dt} + \frac{1}{\rho_g} \frac{d}{d\rho_g} \parent{\frac{d\rho_g}{dt}}}
\end{align}

Regarding the discret form, it gives:
\begin{equation}
   \frac{d\rho_g}{dT}\parent{-\parent{\frac{1}{\parent{\rho_g^n}^2}} \frac{\rho_g^n - \rho_g^{n-1}}{\Delta t} + \frac{1}{\rho_g^n\Delta t}} = \frac{1}{\Delta t} \frac{d\rho_g}{dT} \parent{\frac{\rho_g^{n-1}}{(\rho_g^n)^2}}
\end{equation}

The Condensation model is:
\begin{equation}
 \frac{2}{3}\frac{a_i}{\alpha \rho_g} G,
\end{equation}
with G given by a correlation.

The Condensation term is implemented in \texttt{Source_Flux_interfacial_base} as:
\begin{equation}
\texttt{secmem} \pluseq \frac{2}{3}\frac{a_i^n}{\alpha^n\rho_g^n} G^n
\end{equation}

If the condensation is not making the phase evanescent then:
\begin{align}
    &M_\alpha  \minuseq  \frac{-2}{3}\frac{a_i^n}{(\alpha^n)^2}\rho_g^n G^n\\
    &M_T  \minuseq  \frac{-2}{3}\frac{a_i^n}{\alpha^n\parent{\rho_g^n}^2} G^n \frac{d\rho_l}{dT}+\frac{2}{3}\frac{a_i^n}{\alpha^n\rho_g} \frac{dG}{dT}\\
    &M_P  \minuseq  \frac{-2}{3}\frac{a_i^n}{\alpha^n\parent{\rho_g^n}^2} G^n \frac{d\rho_g}{dP}+\frac{2}{3}\frac{a_i^n}{\alpha^n\rho_g} \frac{dG}{dP}\\
    &M_{a_i}  \minuseq  \frac{2}{3}\frac{1}{\alpha^n\rho_g^n} G^n
\end{align}

For the other source terms, refer to the models.


### The Yao Morel model
The model is described in {cite:t}`Yao2004`.

The equation is:
\begin{align}
\frac{\partial a_{i}}{\partial t}
+ \underbrace{\nabla\cdot(\mathbf{U} a_{i})}_{\text{convection}}
&= \underbrace{\frac{2}{3} \frac{a_{i}}{\alpha} \parent{\frac{\Gamma_{\text{condensation}}}{\rho_g}
- \frac{\alpha_g}{\rho_g} \frac{d \rho_g}{d t}}}_{\text{source of volume change}}\\
&+ \underbrace{\pi d_{\text{dep}}^2\Phi_N}_{\text{Nucleation}}
+ \underbrace{\frac{36\pi}{3}\parent{\frac{\alpha}{a_i}}^2{\Phi_{\text{coal}}}}_{\text{Coalescence}}
+ \underbrace{\frac{36\pi}{3}\parent{\frac{\alpha}{a_i}}^2{\Phi_{\text{breakup}}}}_{\text{Break-up}}.
\end{align}

The Coalescence model is:
\begin{align}
\frac{36\pi}{3}\parent{\frac{\alpha}{a_i}}^2\Phi_{\text{Coal}}
&=- \frac{36\pi}{3}\parent{\frac{\alpha}{a_i}}^2 \parent{\varepsilon d_b}^{1/3} \cdot \frac{\alpha^2}{d_b^4} \cdot K_{c1} \cdot \frac{1}{g\parent{\alpha} + K_{c2}\alpha \sqrt{We/We_{cr}}} \cdot \exp\parent{-K_{c3} \sqrt{\frac{We}{We_{cr}}}} \\
&= {\color{mydarkorchid} \frac{\pi}{3\times 6^{5/3}}\alpha^{1/3}a_i^{5/3}\varepsilon^{1/3}} \cdot {\color{myslateblue} K_{c1} \frac{-1}{g\parent{\alpha} + K_{c2}\alpha \sqrt{We/We_{cr}}} \cdot \exp\parent{-K_{c3} \sqrt{\frac{We}{We_{cr}}}}},
\end{align}

with
- $K_{c1} = 2.86$
- $K_{c2} = 1.922$
- $K_{c3} = 1.017$
- $We_{cr} = 1.24$
- $g(\alpha) = \frac{\alpha_\text{max}^{1/3}-\alpha^{1/3}}{\alpha_\text{max}^{1/3}}$
- $\alpha_\text{max} = \frac{\pi}{6}$.

The Coalescence model is implemented as
\begin{equation}
\frac{36\pi}{3}\parent{\frac{\alpha}{a_i}}^2\Phi_{\text{Coal}} = f_1 \parent{\alpha,\ ai,\ k,\ \varepsilon} f_2\parent{\alpha,\ ai,\ k,\ \varepsilon}
\end{equation}
so that for the sake of simplicity
\begin{equation}
\mathrm{d}\parent{f_1 f_2} = f_2 \mathrm{d} f_1
\end{equation}
in `Coalescence_bulles_1groupe_PolyMAC_P0`:
```{code} c++
void Coalescence_bulles_1groupe_PolyMAC_P0::set_param(Param& param)
{
  Param param(que_suis_je());
  param.ajouter("beta_k", &beta_k_);
}
```
and `Coalescence_bulles_1groupe_Yao_Morel`:
```{code} c++
void Coalescence_bulles_1groupe_Yao_Morel::set_param(Param& param)
```
Default values:
- $\texttt{beta_k_} = 0.09$
- $\texttt{Kc1} = 2.86$
- $\texttt{Kc2} = 1.922$
- $\texttt{Kc3} = 1.017$
- $\texttt{alpha_max_1_3} = (\frac{\pi}{6})^{1/3}$
- $\texttt{We_cr} = 1.24$.

{\color{red} Warning}: The following part describes the matrix filling for the $k-\varepsilon$ model, as an example, but it is currently not implemented since only the $k-\tau$ and $k-\omega$ models are available and are the only ones implemented for the source terms.

For the $k-\varepsilon$ model:
\begin{align}
    &M_{\alpha} \minuseq \frac{\pi}{3\times 6^{5/3}}\frac{1}{3}(\alpha^n)^{-2/3}(a_i^n)^{5/3}(\varepsilon^n)^{1/3} {\color{myslateblue} f_2^n}\\
    &M_{a_i} \minuseq \frac{\pi}{3\times 6^{5/3}}\frac{5}{3}(\alpha^n)^{1/3}(a_i^n)^{2/3}(\varepsilon^n)^{1/3} {\color{myslateblue} f_2^n}\\
    &M_{k}=0\\
    &M_{\varepsilon} \minuseq \frac{\pi}{3\times 6^{5/3}}\frac{1}{3}(\alpha^n)^{-2/3}(a_i^n)^{5/3}(\varepsilon^n)^{-2/3} {\color{myslateblue} f_2^n}\\
    &\text{secmem} \pluseq \frac{\pi}{3\times 6^{5/3}}(\alpha^n)^{1/3}(a_i^n)^{5/3}(\varepsilon^n)^{1/3} {\color{myslateblue} f_2^n}
\end{align}

If the $k-\tau$ turbulence model is used,
\begin{equation}
\varepsilon = \frac{k^2}{\text{max}(k\tau, \text{visc_turb.limiteur()} \nu_l)}\times \text{beta_k_}.
\end{equation}

If the $k-\omega$ turbulence model is used,
\begin{equation}
\varepsilon = k \times \omega \times\text{beta_k_}.
\end{equation}

The Break-up model is:
\begin{aligne}
\frac{36\pi}{3}\parent{\frac{\alpha}{a_i}}^2\Phi_{\text{breakup}}
&=- \frac{36\pi}{3}\parent{\frac{\alpha}{a_i}}^2 \parent{\varepsilon d_b}^{1/3} \cdot \frac{\alpha(1-\alpha)}{d_b^4} \cdot K_{b1} \cdot \frac{1}{1 + K_{b2}\alpha_l \sqrt{We/We_{cr}}} \cdot \text{exp}\parent{- \frac{We}{We_{cr}}}\\
& = {\color{mydarkorchid} \frac{\pi}{3\times 6^{5/3}}\alpha^{-2/3}(1-\alpha)a_i^{5/3}\varepsilon^{1/3}} \cdot K_{b1} \cdot \frac{1}{1 + K_{b2}(1-\alpha) \sqrt{We/We_{cr}}} \cdot \text{exp}\parent{- \frac{We}{We_{cr}}},
\end{align}
with
- $K_{b1} = 1.6$,
- $K_{b2} = 0.42$,
- $We_{cr} = 1.24$.

The Break-up model is implemented as
\begin{equation}
\frac{36\pi}{3}\parent{\frac{\alpha}{a_i}}^2\Phi_{\text{breakup}}={\color{mydarkorchid}f_1(\alpha,ai,k,\varepsilon)}{\color{myslateblue} f_2(\alpha,ai,k,\varepsilon)}
\end{equation}
so that for the sake of simplicity
\begin{equation}
d({\color{mydarkorchid}f_1}{\color{myslateblue} f_2})={\color{myslateblue} f_2}d{\color{mydarkorchid} f_1}
\end{equation}
in `Rupture_bulles_1groupe_PolyMAC_P0`:
```{code} c++
void Rupture_bulles_1groupe_PolyMAC_P0::set_param(Param& param)
{
  Param param(que_suis_je());
  param.ajouter("beta_k", &beta_k_);
}
```
and `Rupture_bulles_1groupe_Yao_Morel`:
```{code} c++
void Rupture_bulles_1groupe_Yao_Morel::set_param(Param& param)
```
Default values:
- $\texttt{beta_k_} = 0.09$
- $\texttt{Kb1} = 1.6$
- $\texttt{Kb2} = 0.42$
- $\texttt{We_cr} = 1.24$.

{\color{red} Warning}: The following part describes the matrix filling for the $k-\varepsilon$
model, as an example, but it is currently not implemented since only the $k-\tau$ and $k-\omega$
models are available and are the only ones implemented for the source terms.

For the $k-\varepsilon$ model:
\begin{align}
    &M_{\alpha} \minuseq \frac{\pi}{3\times 6^{5/3}}\frac{-2}{3}(\alpha^n)^{-5/3}\alpha_l^n(a_i^n)^{5/3}(\varepsilon^n)^{1/3} {\color{myslateblue} f_2^n}\\
    &M_{\alpha_l} \minuseq \frac{\pi}{3\times 6^{5/3}}(\alpha^n)^{-2/3}(a_i^n)^{5/3}(\varepsilon^n)^{1/3} {\color{myslateblue} f_2^n}\\
    &M_{a_i} \minuseq \frac{\pi}{3\times 6^{5/3}}\frac{5}{3}(\alpha^n)^{1/3}\alpha_l^n(a_i^n)^{2/3}(\varepsilon^n)^{1/3} {\color{myslateblue} f_2^n}\\
    &M_{k}=0\\
    &M_{\varepsilon} \minuseq \frac{\pi}{3\times 6^{5/3}}\frac{1}{3}(\alpha^n)^{-2/3}\alpha_l^n(a_i^n)^{5/3}(\varepsilon^n)^{-2/3} {\color{myslateblue} f_2^n}\\
    &\text{secmem}  \pluseq  \frac{\pi}{3\times 6^{5/3}}\frac{1}{3}(\alpha^n)^{-2/3}\alpha_l^n(a_i^n)^{5/3}(\varepsilon^n)^{-2/3} {\color{myslateblue} f_2^n}\\
\end{align}

If the $k-\tau$ turbulence model is used,
\begin{equation}
\varepsilon=\frac{k^2}{\max(k\tau,\ \text{visc_turb.limiteur()} \nu_l)}\times beta\_k\_.
\end{equation}

If the $k-\omega$ turbulence model is used
\begin{equation}
\varepsilon=k\times \omega\times beta\_k\_.
\end{equation}

The Nucleation model is:
\begin{equation}
\pi d_{dep}^2\Phi_N = \pi d_{dep}^2\frac{\Phi_{e}}{L_{\text{vap}} \rho_g \frac{\pi}{6}d_\text{dep}^3}=6\frac{\Phi_{\text{nucleation}}}{\text{max}(d_{\text{nuc}},10^{-8})\rho_g L_{\text{vap}}}
\end{equation}
with $\Phi_{e}$ wall heat transfer.

The Nucleation model is implemented in `Nucleation_paroi_PolyMAC_P0`:
```{code} c++
void Nucleation_paroi_PolyMAC_P0::set_param(Param& param)
```
This terms injected only on boundary elements and is fully explicit:
\begin{equation}
\texttt{secmem} \pluseq 6\frac{\Phi_{\text{nucleation}}^n}{\text{max}(d_{\text{nuc}}^n,10^{-8})\rho_g^n L_{\text{vap}}^n}
\end{equation}


## Interfacial area concentration with 2 groups (incoming)
### The equations
A particular case of the solution can be obtained if we consider two groups of bubbles. For example,
experimentally a limit can be observed between quasi-spherical and distorted bubbles. Then we can
separate the distribution of those groups into 2 distinct distributions on either side of the
critical diameter $\mathit{Dsmc}=4\sqrt{\tfrac{\sigma}{g\parent{\rho_l - \rho_g}}}$, with $\sigma$
the surface tension, $g$ gravity and $\rho_g$ and $\rho_l$ respectively the densities of the gas and
the liquid. For the first group we get:

\begin{equation}
\begin{aligned}
\frac{\partial a_{i1}}{\partial t}
+ \underbrace{\nabla\parent{a_{i1}\mathbf{U}_{g1}}}_{\text{convection}}
=&\underbrace{\frac{2}{3}\frac{a_{i1}}{\alpha_{g1}}\parent{-\frac{\alpha_{g1}}{\rho_g}\frac{d \rho_g}{dt}}}_{\text{Density change}}
- \underbrace{\chi_d\parent{\frac{D_{smc}}{D_{sm1}}}^2\frac{a_{i1}}{\alpha_{g1}}\parent{-\frac{\alpha_{g1}}{\rho_g}\frac{d \rho_g}{dt}}}_{\text{Density sliding}}\\
&+ \underbrace{\frac{2}{3}\frac{a_{i1}}{\alpha_{g1}}\parent{\frac{\color{myteal}\Gamma_{g1}}{\rho_g}}}_{\text{Mass transfer}}
- \underbrace{\chi_d\parent{\frac{D_{smc}}{D_{sm1}}}^2\frac{a_{i1}}{\alpha_{g1}}\parent{\frac{\color{myteal}\Gamma_{g1}}{\rho_g}}}_{\text{Mass transfer sliding}} \\
& + \underbrace{\color{myteal}\sum_j \psi^{\text{intergroup}}_{1j}}_{\text{intergroup sources}}
+ \underbrace{\color{myteal}\sum_j \psi^{\text{internal}}_{1j}}_{\text{intragroup sources}}.
\end{aligned}
\end{equation}

For the second group, we get:
\begin{equation}
\begin{aligned}
\frac{\partial a_{i2}}{\partial t}
+ \underbrace{\nabla\parent{a_{i2}\mathbf{U}_{g2}}}_{\text{convection}}=\underbrace{\frac{2}{3}\frac{a_{i2}}{\alpha_{g2}}\parent{-\frac{\alpha_{g2}}{\rho_g}\frac{d \rho_g}{dt}}}_{\text{Density change}}
+ \underbrace{\chi_d\parent{\frac{D_{smc}}{D_{sm1}}}^2\frac{a_{i1}}{\alpha_{g1}}\parent{-\frac{\alpha_{g1}}{\rho_g}\frac{d \rho_g}{dt}}}_{\text{Density sliding}}&+ & \\
\underbrace{\frac{2}{3}\frac{a_{i2}}{\alpha_{g2}}\parent{\frac{\color{myteal}\Gamma_{g2}}{\rho_g}}}_{\text{Mass transfer}}
+\underbrace{\chi_d\parent{\frac{D_{smc}}{D_{sm1}}}^2 \frac{a_{i1}}{\alpha_{g1}} \parent{\frac{\color{myteal}\Gamma_{g1}}{\rho_g}}}_{\text{Mass transfer sliding}} +& \\
\underbrace{\sum_j \psi^{\text{intergroup}}_{2j}}_{\text{intergroup sources}}
+ \underbrace{\sum_j \psi^{\text{internal}}_{2j}}_{\text{intragroup sources}}.
\end{aligned}
\end{equation}

The different mass transfer are:
\begin{equation}
\begin{aligned}
\Gamma_{g1} = \underbrace{-\frac{\rho_g}{1+\chi_d \parent{\frac{Dsmc}{Dsm1}}^3}{\color{myteal}\sum_j \eta^{\text{inter}}_j}}_{\text{Intergroup}}
+ \underbrace{\frac{\chi_d\parent{\frac{D_{smc}}{D_{sm1}}}^3}{1+\chi_d \parent{\frac{Dsmc}{Dsm1}}^3}\alpha_{g1}\parent{\frac{d\rho_{g}}{dt}}}_{\text{Density group shift}}&+& \\
\underbrace{\frac{1}{1+\chi_d \parent{\frac{Dsmc}{Dsm1}}^3}\Gamma_{\text{condensation g1}}}_{\text{Condensation}}
+ \underbrace{\frac{\chi_d\parent{\frac{D_{smc}}{D_{sm1}}}^3}{1+\chi_d \parent{\frac{\mathit{Dsmc}}{\mathit{Dsm1}}}^3}\Gamma_{\text{Nucleation g1}}}_{\text{Nucleation}}.
\end{aligned}
\end{equation}

\begin{equation}
\begin{aligned}
\Gamma_{g2} = \underbrace{\frac{\rho_g}{1+\chi_d \parent{\frac{Dsmc}{Dsm1}}^3}{\color{myteal}\sum_j \eta^{\text{inter}}_j}}_{\text{Intergroup}}
- \underbrace{\frac{\chi_d\parent{\frac{D_{smc}}{D_{sm1}}}^3}{1+\chi_d \parent{\frac{Dsmc}{Dsm1}}^3}\alpha_{g1}\parent{\frac{d\rho_{g}}{dt}}}_{\text{Density group shift}}&+& \\
\underbrace{\Gamma_{\text{condensation\ g2}}+\frac{\chi_d \parent{\frac{Dsmc}{Dsm1}}^3}{1+\chi_d \parent{\frac{Dsmc}{Dsm1}}^3}\Gamma_{\text{condensation g1}}}_{\text{Condensation}}
- \underbrace{\frac{\chi_d\parent{\frac{D_{smc}}{D_{sm1}}}^3}{1+\chi_d \parent{\frac{Dsmc}{Dsm1}}^3}\Gamma_{\text{Nucleation g1}}}_{\text{Nucleation}}.
\end{aligned}
\end{equation}

$\chi_d$ is equal to $1$ for a uniform distribution profile. Indeed, because there is no prior
determination of the form of the solution of the distribution, the easiest from to consider is a
uniform distribution.

During the averaging process proposed in {cite}`Kataoka2012` , two new terms emerged from the
instantaneous equation: a diffusion term and a lift term. For example, the diffusion term can be
implemented as:

\begin{equation}
K\sqrt{u^{\prime 2}}D_{sm}\nabla a_i=K\sqrt{\frac{2k}{3}} D_{sm}\nabla a_i,
\end{equation}

with $K$ a constant equal to $1/3$. However, it is essential to note that these terms have not yet
been fully validated in various configurations {cite}`Rassame2023`. For the implementation in the
code, we must rewrite it to get rid of $D_{sm}$. For the first group we have:

\begin{equation}
\begin{aligned}
\frac{\partial a_{i1}}{\partial t}+\underbrace{\nabla\parent{a_{i1}\mathbf{U}_{g1}}}_{\colorbox{codebackground}{convection}}=\underbrace{\frac{2}{3}\frac{a_{i1}}{\alpha_{g1}}\parent{-\frac{\alpha_{g1}}{\rho_g}\frac{d \rho_g}{dt}}}_{\colorbox{codebackground}{Density\ change}}-\underbrace{\frac{\chi_d}{36}D_{smc}^2\parent{\frac{a_{i1}}{\alpha_{g1}}}^3\parent{-\frac{\alpha_{g1}}{\rho_g}\frac{d \rho_g}{dt}}}_{\colorbox{codebackground}{Density\ sliding}} &+& \\\underbrace{\frac{2}{3}\frac{a_{i1}}{\alpha_{g1}}\parent{\frac{\color{myteal}\Gamma_{g1}}{\rho_g}}}_{\colorbox{codebackground}{Mass\ transfer}}-\underbrace{\frac{\chi_d}{36}D_{smc}^2\parent{\frac{a_{i1}}{\alpha_{g1}}}^3\parent{\frac{\color{myteal}\Gamma_{g1}}{\rho_g}}}_{\colorbox{codebackground}{Mass\ transfer\ sliding}}+& \\\underbrace{\color{myteal}\sum_j \psi^{intergroup}_{1j}}_{\colorbox{codebackground}{intergroup\ sources}}+\underbrace{\color{myteal}\sum_j \psi^{internal}_{1j}}_{\colorbox{codebackground}{intragroup sources}}.
\end{aligned}
\end{equation}

For the second group, we obtain:
\begin{equation}
\begin{aligned}
\frac{\partial a_{i2}}{\partial t}+\underbrace{\nabla\parent{a_{i2}\mathbf{U}_{g2}}}_{\colorbox{codebackground}{convection}}=\underbrace{\frac{2}{3}\frac{a_{i2}}{\alpha_{g2}}\parent{-\frac{\alpha_{g2}}{\rho_g}\frac{d \rho_g}{dt}}}_{\colorbox{codebackground}{Density\ change}}+\underbrace{\frac{\chi_d}{36}D_{smc}^2\parent{\frac{a_{i1}}{\alpha_{g1}}}^3\parent{-\frac{\alpha_{g1}}{\rho_g}\frac{d \rho_g}{dt}}}_{\colorbox{codebackground}{Density\ sliding}}&+ & \\
\underbrace{\frac{2}{3}\frac{a_{i2}}{\alpha_{g2}}\parent{\frac{\color{myteal}\Gamma_{g2}}{\rho_g}}}_{\colorbox{codebackground}{Mass\ transfer}} +\underbrace{\frac{\chi_d}{36}D_{smc}^2\parent{\frac{a_{i1}}{\alpha_{g1}}}^3\parent{\frac{\color{myteal}\Gamma_{g1}}{\rho_g} }}_{\colorbox{codebackground}{Mass\ transfer\ sliding}} +& \\
\underbrace{\color{myteal}\sum_j \psi^{\text{intergroup}}_{2j}}_{\colorbox{codebackground}{intergroup\ sources}} + \underbrace{\color{myteal}\sum_j \psi^{\text{internal}}_{2j}}_{\colorbox{codebackground}{intragroup sources}}.
\end{aligned}
\end{equation}

The different mass transfer are:
\begin{equation}
\begin{aligned}
\Gamma_{g1} = \underbrace{-\frac{\rho_g}{1+\frac{\chi_d}{216}Dsmc^3\parent{\frac{a_{i1}}{\alpha_{g1}}}^3}{\color{myteal}\sum_j \eta^{inter}_j}}_{\colorbox{codebackground}{Intergroup}}+ \underbrace{\frac{\frac{\chi_d}{216}Dsmc^3\parent{\frac{a_{i1}}{\alpha_{g1}}}^3}{1+\frac{\chi_d}{216}Dsmc^3\parent{\frac{a_{i1}}{\alpha_{g1}}}^3}\alpha_{g1}\parent{\frac{d\rho_{g}}{dt}}}_{\colorbox{codebackground}{Density\ group\ shift}}&+& \\
\underbrace{\frac{1}{1+\frac{\chi_d}{216}Dsmc^3\parent{\frac{a_{i1}}{\alpha_{g1}}}^3}\Gamma_{\text{condensation g1}}}_{\colorbox{codebackground}{Condensation}}+\underbrace{\frac{\frac{\chi_d}{216}Dsmc^3\parent{\frac{a_{i1}}{\alpha_{g1}}}^3}{1+\frac{\chi_d}{216}Dsmc^3\parent{\frac{a_{i1}}{\alpha_{g1}}}^3}\Gamma_{\text{Nucleation g1}}}_{\colorbox{codebackground}{Nucleation}}.
\end{aligned}
\end{equation}

\begin{equation}
\begin{aligned}
\Gamma_{g2}=\underbrace{\frac{\rho_g}{1+\frac{\chi_d}{216}Dsmc^3(\frac{a_{i1}}{\alpha_{g1}})^3}{\color{myteal}\sum_j \eta^{inter}_j}}_{\colorbox{codebackground}{Intergroup}}- \underbrace{\frac{\frac{\chi_d}{216}Dsmc^3(\frac{a_{i1}}{\alpha_{g1}})^3}{1+\frac{\chi_d}{216}Dsmc^3(\frac{a_{i1}}{\alpha_{g1}})^3}\alpha_{g1}\parent{\frac{d\rho_{g}}{dt}}}_{\colorbox{codebackground}{Density\ group\ shift}}&+& \\
\underbrace{\Gamma_{\text{condensation g2}} + \frac{\frac{\chi_d}{216}Dsmc^3(\frac{a_{i1}}{\alpha_{g1}})^3}{1+\frac{\chi_d}{216}Dsmc^3(\frac{a_{i1}}{\alpha_{g1}})^3}\Gamma_{\text{condensation g1}}}_{\colorbox{codebackground}{Condensation}}-\underbrace{\frac{\frac{\chi_d}{216}Dsmc^3(\frac{a_{i1}}{\alpha_{g1}})^3}{1+\frac{\chi_d}{216}Dsmc^3(\frac{a_{i1}}{\alpha_{g1}})^3}\Gamma_{\text{Nucleation g1}}}_{\colorbox{codebackground}{Nucleation}}.
\end{aligned}
\end{equation}

### The source terms
All source term models are based on five categories of mechanism: the Random Collisions (RC), the
Wake Entrainment (WE), the Turbulent Impacts (TI), the Shearing-off (SO) and the Surface Instability
(SI) (see {numref}`Figure %s <2group>`). The RC is a bubble coalescence phenomenon where $2$ bubbles collide
and merge because of a turbulent eddy of comparable size. The WE happens when one smaller bubble is
in the wake of a bigger one, accelerates and collides it. The TI is due to turbulent eddies that
break-up bubbles. The SO is a break-up phenomenon that source from the shearing-off of cap
bubbles. The SI is due to the break-up of large bubbles due to their surface instability.

The number of processes and the dimensionless coefficient can strongly differ from one model to another:
- The {cite:t}`Sun2004` model was developed for a $2$ group configuration with a $200 \times  10$ $mm^2$ confined rectangular channel data. The effect of the wall is then very significant. It was performed for liquid superficial velocity between $0.32$ and $2.84$ m/s and gas velocity between $0.39$ and $2.01$ m/s. It deals with cap-bubbly and churn-turbulent flows.
- The {cite:t}`Smith2012` model was developed for a $2$ group configuration with $0.102$ mm and $0.152$ mm diameter pipes. It deals with bubbly, cap-bubbly and churn-turbulent flows.
- The {cite:t}`Schlegel2015` model was developed for a $2$ group configuration with large diameter channels. It deals with bubbly and cap-bubbly flows. Several constitutive relations and correlations were used to tune this model.
- The {cite:t}`Fu2002` model was developed for a $2$ group configuration for small round pipe.
- {cite:t}`Dave2016` proposed new Smith coefficient based on optimization with genetic algorithm on all TOPFLOW DN200 (pipe $195.3$ mm).

```{figure} /images/bulles2.png
:width: 800px
:name: 2group
:align: center
:alt: 2-groupe bubble mechanisms.

Representation of 2 group bubble mechanisms.
```

The coefficients of the previous models are summarized in the following table:

| Coefficient       | Sun {cite}`Sun2004`      | Smith {cite}`Smith2012`  | Schlegel {cite}`Schlegel2015` | Fu {cite}`Fu2002` | Dave {cite}`Dave2016` |
|-------------------|----------------------|----------------------|---------------------------|------------------|-----------------------|
| $C^{(1)}_{RC}$    | $0.005$              | $0.01$               | $0.01$                    | $0.0041$         | $0.26$                |
| $C^{(12,2)}_{RC}$ | $0.005$              | $0.01$               | $0.05$                    | $0.005$          | $0.41$                |
| $C^{(2)}_{RC}$    | $0.005$              | $0.01$               | $0.01$                    | $0.005$          | $1.00$                |
| $C_{RC0}$         | $3.0$                | $3.0$                | $3.0$                     | $3.0$            | $3.0$                 |
| $C_{RC1}$         | $3.0$                | $3.0$                | $3.0$                     | $3.0$            | $3.0$                 |
| $\alpha_{g1,max}$ | $0.62$               | $0.62$               | $0.62$                    | $0.75$           | $0.62$                |
| $C^{(1)}_{WE}$    | $0.002$              | $0.002$              | $0.002$                   | $0.002$          | $0.001$               |
| $C^{(12,2)}_{WE}$ | $0.002$              | $0.01$               | $0.02$                    | $0.015$          | $0.017$               |
| $C^{(2)}_{WE}$    | $0.005$              | $0.01$               | $0.05$                    | $10.$            | $0.021$               |
| $C^{(1)}_{TI}$    | $0.1$                | $0.05$               | $0.05$                    | $0.0085$         | $0.013$               |
| $C^{(12,2)}_{TI}$ | $0.02$               | $0.04$               | $0.02$                    | $0.02$           | $0.006$               |
| $C^{(2)}_{TI}$    | $0.02$               | $0.01$               | $0.01$                    | $0.02$           | $0.023$               |
| $We_{cr1}$        | $6.5$                | $1.2$                | $1.2$                     | $6.0$            | $6.0$                 |
| $We_{cr2}$        | $7.0$                | $1.2$                | $ 1.2$                    | $6.0$            | $6.0$                 |
| $C_{SO}$          | $3.8 \times 10^{-5}$ | $2.5 \times 10^{-5}$ | $5.0 \times 10^{-5}$      | $0.031$          | $1.4 \times 10^{-5}$  |
| $We_{c,SO}$       | $4500$               | $4000$               | $10$                      | $4500$           | $4500$                |



The model implemented is the one of Smith.

The source/sink terms of Random Collision (RC) are modeled as follows:
\begin{equation}
 \phi_{RC}^{(1)} = -0.17 C_{RC}^{(1)} \lambda_{RC}^{(1)} \frac{{\color{mydarkorchid} \varepsilon^{1/3} \alpha_{g1} a_{i1}^{5/3} }}{ \alpha_{g1,max}^{1/3} \left( \alpha_{g1,max}^{1/3} - \alpha_{g1}^{1/3} \right) } \left[ 1 - \exp \left( - C_{RC1} \frac{ \alpha_{g1,max}^{1/3} \alpha_{g1}^{1/3} }{ \alpha_{g1,max}^{1/3} - \alpha_{g1}^{1/3}}\right) \right]
\end{equation}

\begin{equation}
 \phi_{RC,2}^{(11,2)} = 4.1 C_{RC}^{(1)} \lambda_{RC}^{(1)} \frac{{\color{mydarkorchid} \varepsilon^{1/3} \alpha_{g1} a_{i1}^{5/3}} }{ \alpha_{g1,max}^{2/3} } \left[ 1 - \exp \left( - C_{RC1} \frac{ \alpha_{g1,max}^{1/3} \alpha_{g1}^{1/3} }{ \alpha_{g1,max}^{1/3} - \alpha_{g1}^{1/3}}\right) \right]  \left( 1 - \frac{2}{3} D_{c1}^{*} \right).
 \end{equation}

\begin{equation}
  \phi_{RC,1}^{(12,2)} = -1.14 C_{RC}^{(12,2)} \lambda_{RC}^{(12,2)} {\color{mydarkorchid}\varepsilon^{1/3} \alpha_{g1}^{2/3} \alpha_{g2}^{4/3} a_{i1} a_{i2}^{2/3} }\left[ 1 - \exp \left( - C_{RC1} \frac{ \alpha_{g1,max}^{1/3} \alpha_{g1}^{1/3} }{ \alpha_{g1,max}^{1/3} - \alpha_{g1}^{1/3}}\right) \right].
\end{equation}

\begin{equation}
\phi_{RC,2}^{(12,2)} = 1.80 C_{RC}^{(12,2)} \lambda_{RC}^{(12,2)}{\color{mydarkorchid}\varepsilon^{1/3} \alpha_{g1}^{5/3} \alpha_{g2}^{1/3} a_{i2}^{5/3} }\left[ 1 - \exp \left( - C_{RC1} \frac{ \alpha_{g1,max}^{1/3} \alpha_{g1}^{1/3} }{ \alpha_{g1,max}^{1/3} - \alpha_{g1}^{1/3}}\right) \right].
\end{equation}

\begin{equation}
\phi_{RC}^{(2)} = -95.7 C_{RC}^{(2)} \lambda_{RC}^{(2)} {\color{mydarkorchid} \varepsilon^{1/3}} \frac{ {\color{mydarkorchid}\alpha_{g2}^{7/3}} }{ D_h^2 } \frac{1}{{\color{mydarkorchid}a_{i2}^{1/3}}} \left[ 1 - \exp \left( -C_{RC2} \alpha_{g2}^{1/2} \right) \right] \left( 1-0.37 D_{c2}^{*3} \right).
\end{equation}

\begin{equation}
 \eta_{RC,2}^{(11,2)} = 3.15 C_{RC}^{(1)} \lambda_{RC}^{(1)} \frac{ {\color{mydarkorchid}\varepsilon^{1/3} \alpha_{g1}^2 a_{i1}^{2/3}} }{ \alpha_{g1,max}^{2/3} } \left[ 1 - \exp \left( - C_{RC1} \frac{ \alpha_{g1,max}^{1/3} \alpha_{g1}^{1/3} }{ \alpha_{g1,max}^{1/3} - \alpha_{g1}^{1/3}}\right) \right]  \left( 1 - \frac{2}{3} D_{c1}^{*} \right).
\end{equation}

\begin{equation}
\eta_{RC,2}^{(12,2)} = 1.44 C_{RC}^{(12,2)} \lambda_{RC}^{(12,2)} {\color{mydarkorchid}\varepsilon^{1/3} \alpha_{g1}^{5/3} \alpha_{g2}^{4/3} a_{i2}^{2/3}} \left[ 1 - \exp \left( - C_{RC1} \frac{ \alpha_{g1,max}^{1/3} \alpha_{g1}^{1/3} }{ \alpha_{g1,max}^{1/3} - \alpha_{g1}^{1/3}}\right) \right].
\end{equation}

$\lambda_{RC}^{(1)}$, $\lambda_{RC}^{(12,2)}$, $\lambda_{RC}^{(2)}$ are defined as follows:
 \begin{align}
 & \lambda_{RC}^{(1)} = \exp \left( - C_{RC0} \frac{ D_{sm1}^{5/6} \rho_l^{1/2} \varepsilon^{1/3} }{ \sigma^{1/2} } \right), \\
 & \lambda_{RC}^{(2)} = \exp \left( - C_{RC0} \frac{ D_{sm2}^{5/6} \rho_l^{1/2} \varepsilon^{1/3} }{ \sigma^{1/2} } \right), \\
 & \lambda_{RC}^{(12,2)} = \lambda_{RC}^{(2)}.
 \end{align}

In the above equations, $C_{RC}^{(1)}$, $C_{RC}^{(12,2)}$, $C_{RC}^{(2)}$ are three constant
coefficients. $C_{RC1}$, $C_{RC2}$ are coefficients accounting for effective range of influence of
turbulent eddies. $\alpha_{g1,max}$ is the dense packing limit for Group 1 bubbles. $D_h$ is the
hydraulic diameter. $C_{RC0}$ is a constant coefficient.

The source/sink terms of Wake Entrainment (WE) are modeled as follows:
\begin{equation}
\phi_{WE}^{(1)} = - 0.17 C_{WE}^{(1)} C_{D1}^{1/3} U_{r1} {\color{mydarkorchid}a_{i1}^2}.
\end{equation}

\begin{equation}
 \phi_{WE,2}^{(11,2)} = 2.57 C_{WE}^{(11,2)} C_{D1}^{1/3} U_{r1} {\color{mydarkorchid}a_{i1}^2} \left( 1 - \frac{2}{3} D_{c1}^{*} \right).
\end{equation}

\begin{equation}
\phi_{WE,l1}^{(12,2)} = - 0.33 C_{WE}^{(12,2)} U_{w12} {\color{mydarkorchid} a_{i1} a_{i2}}.
\end{equation}

\begin{equation}
\phi_{WE,g2}^{(12,2)} = 0.922 C_{WE}^{(12,2)} U_{w12} {\color{mydarkorchid}\alpha_{g1} \frac{ a_{i2}^2 }{ \alpha_{g2} }}.
\end{equation}

\begin{equation}
\phi_{WE}^{(2)} = -1.02 C_{WE}^{(2)} \left[ 1 - \exp( - 0.7 \alpha_{g2} ) \right] U_{rw2} {\color{mydarkorchid} \frac{ a_{i2}^2 }{ \alpha_{g2} }} \left( 1 - 0.10 D_{c2}^{*2} \right).
\end{equation}

\begin{equation}
 \eta_{WE,2}^{(11,2)} = 3.85 C_{WE}^{(1)} C_{D1}^{1/3} U_{r1} {\color{mydarkorchid}\alpha_{g1} a_{i1}} \left( 1 - \frac{2}{3} D_{c1}^{*} \right).
\end{equation}

\begin{equation}
\eta_{WE,2}^{(12,2)} = 0.33 C_{WE}^{(12,2)} U_{w12} {\color{mydarkorchid} \alpha_{g1} a_{i2}}.
\end{equation}

In the above equation
\begin{align*}
 & U_{rw2} = 0.94 U_{r2} C_{D2}^{1/3}, \\
 & U_{w12} = U_{rw2} + U_{r1} - U_{r2}, \\
 & D_{c2}^{*}=\frac{D_c}{D_{sm2}},
\end{align*}
and
\begin{align*}
 & C_{D1} = \frac{2}{3} D_{sm1} \sqrt[]{ \frac{ g \Delta \rho }{ \sigma} } \left( \frac{ 1+17.67 [f(\alpha_{g1})]^{6/7} }{ 18.67 f(\alpha_{g1}) } \right)^2 \, \text{with} \, f(\alpha_{g1}) = (1 - \alpha_{g1})^{1.5}, \\
 & C_{D2} = \frac{8}{3} (1-\alpha_{g2})^2.
\end{align*}

In the above equations $C_{WE}^{(1)}$, $C_{WE}^{(11,2)}$, $C_{WE}^{(12,2)}$, $C_{WE}^{(2)}$ are
constant coefficients.

The source/sink terms of Turbulent Impact (TI) are modeled as follows:
\begin{equation}
 \phi_{TI}^{(1)} = 0.12 C_{TI}^{(1)} {\color{mydarkorchid}\varepsilon^{1/3}  \left( 1-\alpha_g \right) \left( \frac{ a_{i1}^{5/3} }{ \alpha_{g1}^{2/3} } \right)} \exp \left( - \frac{ We_{cr1} }{ We_1 } \right) \sqrt[]{ 1 - \frac{ We_{cr1} }{ We_1 } }.
 \end{equation}

\begin{equation}
\phi_{TI,1}^{(2,1)} = 6.165 C_{TI}^{(2,1)} {\color{mydarkorchid}\varepsilon^{1/3} \left( 1 - \alpha_g \right) \left( \frac{ a_{i2}^{5/3} }{ \alpha_{g2}^{2/3} } \right)} \exp \left( - \frac{ We_{cr2} }{ We_2 } \right) \sqrt[]{ 1 - \frac{ We_{cr2} }{ We_2 } } \left( 0.212 D_{c2}^{*13/3} - 0.167 D_{c2}^{*5} \right).
 \end{equation}

 \begin{equation}
 \phi_{TI,2}^{(2)} = 0.378 C_{TI}^{(2)} {\color{mydarkorchid}\varepsilon^{1/3} \left( 1-\alpha_g \right) \left( \frac{ a_{i2}^{5/3} }{ \alpha_{g2}^{2/3} } \right)} \exp \left( - \frac{ We_{cr2} }{ We_2 } \right) \sqrt[]{ 1 - \frac{ We_{cr2} }{ We_2 } } \left( 1 - 0.212 D_{c2}^{*13/3} \right),
 \end{equation}

 \begin{equation}
\eta_{TI,2}^{(2,1)} = -11.65 C_{TI}^{(2,1)}{\color{mydarkorchid} \varepsilon^{1/3} \left( 1 - \alpha_g \right) \alpha_{g2}^{1/3} a_{i2}^{2/3} }\exp \left( - \frac{ We_{cr2} }{ We_2 } \right) \sqrt[]{ 1 - \frac{ We_{cr2} }{ We_2 } } \left( 0.15 D_{c2}^{*16/3} - 0.117 D_{c2}^{*6} \right).
 \end{equation}

 \begin{equation}
 \eta_{TI,1}^{(2,1)} = - \eta_{TI,2}^{(2,1)},
 \end{equation}
with the following expressions for $We_1$ and $We_2$:
 \begin{align*}
 & We_1 = \frac{2 \rho_l \varepsilon^{2/3} (D_{sm1})^{5/3} }{\sigma}, \\
 & We_2 = \frac{2 \rho_l \varepsilon^{2/3} (D_{sm2})^{5/3} }{\sigma}.
 \end{align*}

$C_{TI}^{(1)}$, $C_{TI}^{(2,1)}$, $C_{TI}^{(2)}$ are constant coefficients. $We_{cr1}$, $We_{cr2}$
are critical Weber number for breakup due to turbulent impact.

The source/sink terms of Shearing-off (SO) are modeled as follows:
 \begin{equation}
 \phi_{SO,1}^{(2,12)} = 8.0 C_{SO} \frac{ \rho_l^{3/5} U_{g2}^{1/5} \sigma^{2/5} }{ \rho_g D_h^{2/5} We_c^{3/5} } {\color{mydarkorchid}\frac{ a_{i2}^2 }{ \alpha_{g2} }} \left[ 1 - \left( \frac{ We_{c,SO} }{ We_{m2} } \right)^4 \right] .
  \end{equation}

 \begin{equation}
\phi_{SO,2}^{(2,12)} = -0.36 C_{SO} \left( \frac{ \sigma }{ \rho_g U_{g2} }  \right) {\color{mydarkorchid} \frac{ a_{i2}^3 }{ \alpha_{g2}^2 } }\left[ 1 - \left( \frac{ We_{c,SO} }{ We_{m2} } \right) \right].
  \end{equation}

 \begin{equation}
  \eta_{SO,2}^{(2,12)} = - 2.33 C_{SO} \left( \frac{ \sigma }{ \rho_g U_{g2} }  \right){\color{mydarkorchid} \frac{ a_{i2}^2 }{ \alpha_{g2} }} \left[ 1 - \left( \frac{ We_{c,SO} }{ We_{m2} } \right)^4 \right].
\end{equation}

 \begin{equation}
 \eta_{SO,1}^{(2,12)} = - \eta_{SO,2}^{(2,12)}.
 \end{equation}

$C_{SO}$ is a constant coefficient. $We_{c,SO}$ is a critical weber number for shearing-off of small
bubbles from large cap bubbles. $We_{m2}$, $We_c$, $D_h$.

The source/sink terms of Surface Instability (SI) are modeled as follows:
 \begin{align}
 \begin{split}
 & \phi_{SI}^{(2)} = 2.616 \times 10^{-4} C_{RC}^{(2)} \varepsilon^{1/3} \frac{1}{D_h^2} {\color{mydarkorchid}\alpha_{g2}^2} \left( \frac{\sigma}{g \Delta \rho} \right)^{1/6} \left[ 1 - \exp\left( - C_{RC2} \alpha_{g2}^{1/2} \right)  \right], \\
 & + 1.425 \times 10^{-7} C_{WE}^{(2)}( 1 - \exp(-0.7 \alpha_{g2}) ) U_{rw2} {\color{mydarkorchid}\alpha_{g2}^2} \left( \frac{\sigma}{g \Delta \rho} \right)^{-1},
 \end{split}
 \end{align}

$C_{RC}^{(2)}$ and $C_{WE}^{(2)}$ are constant coefficients from Random collision and Wake
Entrainment source terms. $D_h$ is the hydraulic diameter.
