(sec:multi-turbulence)=
# Multiphase turbulence RANS modeling

:::{attention}
Rewrite from latex in progress.
:::

## Introduction

## Eddy-viscosity models

### k-omega model
The Wilcox version of the $k-\omega$ model is described in details by \cite{Wilcox1988}. The turbulent viscosity is defined by $\nu_t = \frac{k}{\omega}$. The two equations are:

\begin{align}
\newcommand{\parent}[1]{\left(#1\right)}
		&\partial_t \rho_l k + \nabla \cdot ( \rho_l k \vec{u_l}) -
		\nabla\parent{ \rho_l(\nu_l + \sigma_k \nu_t) \underline{\nabla} k} =
		  \underline{\underline{\tau_R}}::\underline{\underline{\nabla}}\vec{u_l}
		 - \beta_{k}\rho k \omega
		\\
		&\partial_t  \rho_l \omega + \nabla \cdot \parent{\alpha_l \rho_l \omega \vec{u_l}} - \nabla\parent{\rho_l(\nu_l + \sigma_{\omega} \nu_t} \underline{\nabla} \omega) =
		 \alpha_{\omega}  \frac{\omega}{k}\underline{\underline{\tau_R}}::\underline{\underline{\nabla}}\vec{u_l}
		 - \beta_{\omega}\rho \omega^2
\end{align}

The default values of the constants are
- $\alpha_{\omega} = 0.55$,
- $\beta_{k} = 0.09$,
- $\beta_{\omega} = 0.075$,
- $\sigma_k = 0.5$,
- $\sigma_{\omega} = 0.5$.

This model {cite:t}`Kok1999` was introduced after the Menter SST $k-\omega$ model
({cite:t}`Menter1993,Menter2003`) showed the importance of cross-diffusion. The differences with the
1988 Wilcox model reside in the addition of a cross-diffusion term (${ \sigma_d\frac{
\rho_l}{\omega} } \text{max}\left\{{\underline{\nabla}k \cdot \underline{\nabla} \omega}, 0\right\}
$) and a modification of the value of some constants. The turbulent equations are:

\begin{align}
\newcommand{\acco}[1]{\lbrace #1 \rbrace}
	\label{eq_omega_Kok}
		&\partial_t \rho_l k + \nabla \cdot \parent{\rho_l k \vec{u_l}} =
		\underline{\underline{\tau_R}}::\underline{\underline{\nabla}}\vec{u_l}
		 - \beta_{k}\rho k \omega
		+ \nabla\parent{\rho_l(\nu_l + \sigma_k \nu_t) \underline{\nabla} k}
		\\
		&\partial_t  \rho_l \omega + \nabla \cdot \parent{\alpha_l \rho_l \omega \vec{u_l}} =
		 \alpha_{\omega} \frac{\omega}{k}\underline{\underline{\tau_R}}::\underline{\underline{\nabla}}\vec{u_l}
		 - \beta_{\omega}\rho \omega^2
		 +\nabla\parent{\rho_l\parent{\nu_l + \sigma_{\omega}\nu_t} \underline{\nabla} \omega}
		 + \sigma_d\frac{\rho_l}{\omega} \text{max}\acco{\underline{\nabla}k \cdot \underline{\nabla} \omega,\ 0}
\end{align}

The values of the constants are	$\alpha_{\omega} = 0.5$, $\beta_{k} = 0.09$, $\beta_{\omega} = 0.075$, $\sigma_k = 2/3$, $\sigma_{\omega} = 0.5$ and $\sigma_d = 0.5$.

The 2006 Wilcox $k_\omega$ model \cite{Wilcox2006} is the same as the Kok $k-\omega$ with different coefficients. It is an update of the 1988 Wilcox $k-\omega$ model. The turbulent equations are the same as in equation \ref{eq_omega_Kok}. A notable difference is the introduction of a blending function for $\beta_{\omega}$.

The values of the constants are: $\alpha_{\omega} = 0.52$, $\beta_{k} = 0.09$, $\beta_{\omega} = 0.0705\cdot f(\Omega_{ij},S_{ij})$, $\sigma_k = 0.6$, $\sigma_{\omega} = 0.5$ , $\sigma_d = 0.125$.

### k-tau model

This is a variation of the 1999 Kok $k-\omega$. In this model \cite{Ktau2000}, the time scale $\tau = \frac{1}{\omega}$ is introduced. We therefore have $\nu_t = k\tau$. There is an additional diffusion term that comes out of the calculation ( $- 8  \rho_l(\nu_l + \sigma_{\omega} \nu_t) ||\underline{\nabla}\sqrt{\tau}||^2$). The turbulent equations become:

\begin{align} \label{eq_tau}
		&\partial_t \rho_l k + \nabla \cdot ( \rho_l k \vec{u_l})
		=  \underline{\underline{\tau_R}}::\underline{\underline{\nabla}}\vec{u_l}
		- \frac{\beta_{k}\rho k}{\tau}
		+ \nabla( \rho_l(\nu_l + \sigma_k \nu_t) \underline{\nabla} k) \\
		&\partial_t  \rho_l \tau + \nabla \cdot ( \rho_l \tau \vec{u_l})
		=  - \alpha_{\omega}  \frac{\tau}{k}\underline{\underline{\tau_R}}::\underline{\underline{\nabla}}\vec{u_l}
	  	 + \beta_{\omega}\rho
		 +\nabla( \rho_l(\nu_l + \sigma_{\omega} \nu_t) \underline{\nabla} \tau)\\
 		 + \sigma_d \rho_l \tau \times{} \text{min}\acco{\underline{\nabla}k \cdot \underline{\nabla} \tau,\ 0}
 		 - 8  \rho_l\parent{\nu_l + \sigma_{\omega} \nu_t} ||\underline{\nabla}\sqrt{\tau}||^2
\end{align}

The $- 8  \rho_l(\nu_l + \sigma_{\omega} \nu_t) ||\underline{\nabla}\sqrt{\tau}||^2$ term presents important numerical difficulties close to the wall. In order to limit these issues, we have tried to implicit this term in 3 different ways.

The constants are the same than in the 1999 Kok $k-\omega$ model: $\alpha_{\omega} = 0.5$, $\beta_{k} = 0.09$, $\beta_{\omega} = 0.075$, $\sigma_k = 2/3$, $\sigma_{\omega} = 0.5$, $\sigma_d = 0.5$.

## LES

## Two-phase specific models

### Eddy-viscosity model

The Sato model {cite:t}`Sato1981` is added in `Viscosite_turbulente_sato.cpp`. The original formula is
\begin{equation}
\epsilon''=\parent{1-\exp\parent{-\frac{y^+}{A^+}}}^2 k_1 \alpha \frac{D_b}{2}U_B.
\end{equation}
with the coefficient $A^+=16$ and $k_1 = 1.2$. The bubble diameter $D_b$ is modeled to take the deformation of the bubble into account at the wall. The velocity $U_B$, defined in the article, is the relative velocity. Very poor notation, in our humble opinion. The following expression is defined:
\begin{equation}
    D_b = \begin{cases}
    0\ \text{if}\ 0 < y < 20~\text{\mu m},\\
    4y\parent{\widehat{D_B}-y}/\widehat{D_B}\ \text{if}\ 20~\text{\mu m} < y < \widehat{D_B}/2,\\
    \widehat{D_B}\ \text{if}\ \widehat{D_B}/2 < y < R.
    \end{cases}
\end{equation}
with $\widehat{D_B}$ the cross-sectional mean diameter of the bubbles.

In TrioCFD, the squared coefficient depending on $y^+$ is not implemented. The bubble diameter is taken as is without the prescribed function.

### Source terms

The HZDR model is described in the paper {cite:t}`Rzehak2013a,Rzehak2013b,Rzehak2015,Colombo2021`. Their approach is to add a production term $S_{k}^{\text{BI}}$ to the $k$ equation and a dissipation term $S_{\omega}^{\text{BI}}$ to the $\omega$ equation. The general assumption is to consider that _all energy lost by the bubble to drag is converted to turbulent kinetic energy in the wake of the bubble_ {cite:t}`Rzehak2013b`.

In comparison with the current version of the code, they implemented those two additional terms in a $k-\omega$ SST turbulence model. In CMFD, only the production and dissipation terms have been extracted and implemented without (yet) the SST additional process. Thus the prescribed coefficient might not be well suited.

The two terms are related by the expression
\begin{equation}
    S_{\omega}^{\text{BI}} = \frac{1}{C_{\mu} k_l} \mathcal{S}_{\varepsilon}^{\text{BI}} - \frac{\omega_L}{k_L}S_{k}^{\text{BI}}
\end{equation}
with
\begin{equation}
    \mathcal{S}_{\varepsilon}^{\text{BI}} = C_{\varepsilon B}\frac{S_{k}^{\text{BI}}}{\tau} = C_{\varepsilon B}\frac{S_{k}^{\text{BI}}\varepsilon_l}{k_l}
\end{equation}

% Dissip = Cepsilon/(Cnu*db*sqrt(k))*prodHZDR
% avec ProdHZDR = Ck*3/4*Cd/diam*alpha_g/alpha_l*ur^3
% Cd =

In the code, the added dissipation term takes the following form
\begin{equation}
    S_{\omega}^{\text{BI}} = \frac{C_{\varepsilon}}{C_{\nu}D_b\sqrt{k}}\mathcal{S}_{k}^{\text{BI}}
\end{equation}
with
\begin{align}
\newcommand{\norm}[1]{\left|\left| #1 \right|\right|}
    &\mathcal{S}_{k}^{\text{BI}} = \frac{3}{4}C_k\frac{C_d}{D_b}\frac{\alpha_g}{\alpha_l}u_r^3\\
    &C_d = \max\parent{\min\parent{\frac{16}{\mathit{Re}_b}\parent{1+0.15\mathit{Re}_b^{0.687}},\ \frac{48}{\mathit{Re}_b}},\ \frac{8\mathit{Eo}}{3\parent{\mathit{4+Eo}}}}\\
    &\mathit{Eo} = \frac{g\norm{\rho_l - \rho_g}D_b^2}{\sigma}\\
    &\mathit{Re}_b = \frac{D_b u_r}{\nu_l}
\end{align}
It is derived directly from Source_base and currently only implemented in PolyMAC.

The added production term in the turbulent kinetic energy equation is defined in Production_HZDR_PolyMAC_P0. The added term in the dissipation equation is defined in Source_Dissipation_HZDR_PolyMAC_P0. TODO: To avoid code duplication, the dissipation source term should call the production source term.

### Bubble-induced turbulence transport equations

By two-phase turbulence, we mean the effect of the bubbles on the turbulence in the liquid phase. To
model this, we implemented the models developed during the PhD of Antoine du Cluzeau
{cite:t}`duCluzeau2019`. Following the work of {cite:t}`Risso2018`, the
authors divide the velocity fluctuations caused by the movement of bubbles in the fluid in two
parts: wake-induced turbulence and wake-induced fluctuations. The total Reynolds stress tensor is
the sum of all single-phase (calculated using 2-equation turbulence models) and two-phase
turbulence.

\begin{equation}
	\underline{\underline{\tau_R}} 	=
	      \underline{\underline{\tau_R}}_{\text{single-phase}}
		+ \underline{\underline{\tau_R}}_{\text{WIF}}
		+ \underline{\underline{\tau_R}}_{\text{WIT}}
\end{equation}
This model is only available in PolyMAC, for now.

#### Wake-induced fluctuations}

Wake-induced fluctuations are the anisotropic effects of the average wake. These fluctuations are
primarily in the direction of the liquid-gas velocity difference, i.e. in the vertical direction. No
transport equation is necessary to model this term.

\begin{equation}
	\underline{\underline{\tau_R}}_{\text{WIF}} =
	\alpha_v |\overrightarrow{u_v}-\overrightarrow{u_l}|^2
	\begin{bmatrix}
		3/20 & 0 & 0 \\
		0 & 3/20 & 0 \\
		0 & 0 & 1/5+3C_v/2
	\end{bmatrix}
\end{equation}
with $C_v = 0.36$.

During his internship, Moncef El Moatamid defined a new formulation using the work of {cite:t}`Biesheuvel1984`
\begin{equation}
	\underline{\underline{\tau_R}}_{\text{WIF}} =
	\alpha_v \parent{\frac{3}{20}u_r^2 \underline{\underline{I}} + \parent{\frac{1}{20}+0.25\times{}\frac{3}{2}\gamma^3}\underline{u_r}\underline{u_r}}
\end{equation}
This formulation allows to have a tensor for the second part of the equation

#### Wake-induced turbulence

Wake-induced turbulence is the isotropic contribution of bubbles to the velocity fluctuations. It
comes from the instabilities of bubble wakes. It takes the shape of an additional transport equation
for a specific kinetic energy $k_{WIT}$.

\begin{align}
	&\underline{\underline{\tau_R}}_{\text{WIT}} = k^{WIT}\frac{2}{3}\delta_{ij}\\
	&\frac{D k^{WIT}}{Dt} =
			\underbrace{C_D\nabla^2 k^{WIT} }_\text{Diffusion}
				- \underbrace{\frac{2 \nu_l C_D' Re_b}{C_\Lambda^2 d_b^2}k^{WIT} }_\text{Dissipation}
				+ \underbrace{\alpha_v \frac{(\rho_l-\rho_v)}{\rho_l} g |\vec{u_v}-\vec{u_l}|\left(0.9 - exp\left(-\frac{Re_b}{Re_b^c}\right)\right) }_\text{Production}
\end{align}
where $C_\Lambda = 2.7$, $Re_b^c = 170$, $C_D'$ is a user-inputted drag coefficient and $C_D$ is a turbulent diffusion coefficient.

This model is implemented in `Energie_cinetique_turbulente_WIT.cpp` and inherits from `Convection_Diffusion_std`. The different terms of the right-hand side of the equations must be modeled. Thus, we have
\begin{itemize}
    \item Viscosite_turbulente_WIT
    \item Dissipation_WIT_PolyMAC_P0
    \item Production_WIT_PolyMAC_P0
\end{itemize}

As specified above, it is currently only available with PolyMAC. To take the WIT into account in the momentum equation, one must specify its presence in the diffusion term using\footnote{This syntax might evolve to avoid repeating the names.}

```{code} c++
diffusion {
  turbulente multiple {
    k_omega k_omega { }
    WIT WIT { }
    WIF WIF { }
  }
}
```

Then, in the WIT equation bloc, the model for the turbulente diffusion of WIT is specified
```{code} c++
diffusion { turbulente SGDH_WIT { } }
```

For the turbulent viscosity, an additional diffusion term must be specified in the data file to model the turbulent transport of WIT. Two models are available, a single gradient diffusion one and a generalized gradient diffusion one.

**Production_WIT**

\begin{equation}
    \alpha{}g u_r\frac{\rho_l - \rho_g}{\rho_l}\parent{0.9 - \exp\parent{Re_b-Re_c}}
\end{equation}
with
\begin{align}
    \mathit{Re}_b = \frac{D_b u_r}{\nu_l}.
\end{align}
The Reynolds number $\mathit{Re}_c$ is a user parameter with a default value of 170~{cite:t}`duCluzeau2019`. Only the `secmem` matrix is filled.

**Dissipation_WIT**

Drag coefficient from Tomiyama, same than HZDR.
\begin{equation}
    \frac{2\nu C_d \mathit{Re}_b k_{\text{WIT}}}{C_{\lambda}^2 D_b^2}
\end{equation}
with
\begin{align}
    &C_d = \max\parent{\min\parent{\frac{16}{\mathit{Re}_b}\parent{1+0.15\mathit{Re}_b^{0.687}},\ \frac{48}{\mathit{Re}_b}},\ \frac{8\mathit{Eo}}{3\parent{\mathit{4+Eo}}}}\\
    &\mathit{Eo} = \frac{g\norm{\rho_l - \rho_g}D_b^2}{\sigma}\\
    &\mathit{Re}_b = \frac{D_b u_r}{\nu_l}
\end{align}
 Only the `secmem` matrix is filled.

**Transport_turbulent_SGDH_WIT**
It comes from the paper of {cite:t}`Almeras2014`.
It computes a characteristic time scale of the form
\begin{equation}
    \tau = \frac{2}{3} \alpha_g u_r \frac{D_b}{\delta^3} \gamma^{2/3}
\end{equation}
with $\delta$ the wake size, $\gamma$ the bubble aspect ratio and $C_s$ a constant
Then it modifies the viscosity as
\begin{equation}
    \nu = \frac{\mu_0}{\nu_0}C_s \tau
\end{equation}

```{code} c++
  Param param(que_suis_je());
  param.ajouter("Aspect_ratio", &gamma_);   // rapport de forme des bulles
  param.ajouter("Influence_area", &delta_); // parametre modele d'Almeras 2014 (taille du sillage)
  param.ajouter("C_s", &C_s);               // parametre modele d'Almeras 2014
```

**Transport_turbulent_GGDH_WIT**

Same as SGDH but works with $\nu(i, \text{liq. idx},$ $\text{dim I}, \text{dim J})$ and $R_{ij}$

```{code} c++
  param.ajouter("Aspect_ratio", &gamma_); // rapport d'aspet des bulles
  param.ajouter("Influence_area", &delta_); // parametre modele d'Almeras 2014 (taille du sillage)
  param.ajouter("C_s", &C_s); // parametre modele d'Almeras 2014
  //param.ajouter("vitesse_rel_attendue", &ur_user, Param::REQUIRED); // valeur de ur a prendre si u_r(i,0)=0
  param.ajouter("Limiteur_alpha", &limiteur_alpha_, Param::REQUIRED); // valeur minimal de (1-alpha) pour utiliser le modele d'Almeras
```

**Viscosite_turbulente_WIT**

With the Reynolds_stress method, it fills the diagonal with $2/3 \times k_{\text{WIT}}$.
```{code} c++
param.ajouter("limiter|limiteur", &limiter_);
```

## Boundary conditions
