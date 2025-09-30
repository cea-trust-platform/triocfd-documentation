# Other types of models

## Analytical terms as source terms
This section describes some analytical terms that are implemented as source terms in matrix.

### Pressure term in energy equation
This term arises from the averaging of the pressure work term due to the transport of internal
energy instead of enthalpy. It represents the pressure work associated with changes in the
distribution of void fraction. Its expression is:

\begin{equation}
\newcommand {\parent} [1] {\left( #1 \right)}
\newcommand{\pluseq}{\mathrel{+}=}
\newcommand{\minuseq}{\mathrel{-}=}
\newcommand{\timeseq}{\mathrel{*}=}
    -P\parent{\frac{\partial \alpha_k}{\partial t}+\nabla \cdot (\alpha_k v_k)}
\end{equation}
It is implemented in:
```{code} c++
void Source_Travail_pression_Elem_base::set_param(Param& param)
```

### Gravity
Gravity is treated as a source term in \texttt{Pb_multiphase} and can't be as other problems from
TrioCFD and TRUST.

The common way to add gravity is to add in the momentum equation a source. For example, with 2 phases:
```{code} c++
source_qdm Champ_Fonc_xyz dom 6 0 0 0 0 -9.81 -9.81
```
One must use \texttt{Gravite_Multiphase} to get gravity in momentum equation when using drift correlation.
The model is implemented as:
```{code} c++
void Gravite_Multiphase::set_param(Param& param)
{
  Noms noms(D), unites(D);
  noms[0] = "gravite";
  unites[0] = "m/s^2";
  Motcle typeChamp = "champ_elem" ;
  const Domaine_dis& z = ref_cast(Domaine_dis, pb.domaine_dis());
  dis.discretiser_champ(typeChamp, z.valeur(), scalaire, noms , unites, D, 0, gravite_);
}
```

## Injected sources of mass
It is necessary in order to simulate injectors of non-condensable bubbles, otherwise it boils. It was added to simulate the Gabillet test case.

### Injection of mass
The model is implemented in:
```{code} c++
void Source_injection_masse_base::set_param(Param& param)
{
  Cerr << "Lecture du Champ de masse injectee" << finl;

  Champ_Don flux_masse_lu_;
  Motcle type;
  is >> type;

  flux_masse_lu_.typer(type);
  Champ_Don_base& ch_flux_masse_lu_ = ref_cast(Champ_Don_base,flux_masse_lu_.valeur());
  is >> ch_flux_masse_lu_;
  const int nb_comp = ch_flux_masse_lu_.nb_comp();

  equation().probleme().discretisation().discretiser_champ("champ_elem", equation().domaine_dis(), "pp", "1",nb_comp,0., flux_masse_);
  flux_masse_lu_->fixer_nb_comp(nb_comp);
  if (ch_flux_masse_lu_.le_nom()=="anonyme") ch_flux_masse_lu_.nommer("Flux_masse_injectee");

  for (int n = 0; n < nb_comp; n++) flux_masse_lu_->fixer_nom_compo(n, ch_flux_masse_lu_.le_nom() + (nb_comp > 1 ? Nom(n):""));
  for (int n = 0; n < nb_comp; n++) flux_masse_->fixer_nom_compo(n, ch_flux_masse_lu_.le_nom() + (nb_comp > 1 ? Nom(n):""));
  equation().discretisation().nommer_completer_champ_physique(equation().domaine_dis(),ch_flux_masse_lu_.le_nom(),"1/s",flux_masse_lu_,equation().probleme());
  equation().discretisation().nommer_completer_champ_physique(equation().domaine_dis(),ch_flux_masse_lu_.le_nom(),"1/s",flux_masse_,equation().probleme());
  flux_masse_.valeur().valeurs() = 0;
  flux_masse_.valeur().affecter(flux_masse_lu_);

  const Pb_Multiphase& pb = ref_cast(Pb_Multiphase, equation().probleme());
  int N = pb.nb_phases();
  if (N != flux_masse_.valeurs().line_size()) Process::exit(que_suis_je() + ": you must input as many fluxes as there are phases !!");

  return is;
}
```
In the mass equation:
\begin{equation}
    \texttt{secmem}  \pluseq  \rho_k f_{inj}
\end{equation}

### Momentum correction
When a fluid flow is injected through a wall with zero momentum via a Neumann boundary condition on the mass equation, it is necessary to correct the momentum equation.

The model is implemented in:
```{code} c++
void Injection_QDM_nulle_PolyMAC_P0::set_param(Param& param)
{
  Param param(que_suis_je());
  param.ajouter("beta", &beta_);
  param.lire_avec_accolades_depuis(is);
}
```
Default values:
- $\texttt{beta_} =1$.

Case 1: when bubbles are injected at the wall if not face from boundary
\begin{align}
    &\texttt{f_a_masse}=\rho_g U_{inj}\\
    &\texttt{f_a}=\rho_g U_{inj}
\end{align}
corr-ajouter_inj
\begin{align}
  &\texttt{secmem} \minuseq \texttt{surface}\times \texttt{f_a_masse}\times U^n\times \texttt{beta_}\\
  &M_v \pluseq \texttt{surface}\times \texttt{f_a_masse}\times \texttt{beta_}
\end{align}

Case 2: wall boiling if not face from boundary
\begin{align}
&\texttt{G}=\frac{q_p}{L_{vap}}\\
&\texttt{f_a_masse}  \minuseq \frac{\texttt{G}}{\texttt{surface}}\times \begin{cases} \frac{1}{\rho_g},\text{ if in gas,}\\-\frac{1}{\rho_l},\text{ if in liquid.} \end{cases}\\
&\texttt{f_a}  \minuseq \frac{\texttt{G}}{\texttt{surface}}\times \begin{cases} 1,\text{ if in gas,}\\-1,\text{ if in liquid.}\end{cases}
\end{align}
corr-ajouter_inj
\begin{align}
  &\texttt{secmem}  \minuseq  \texttt{surface} \times \texttt{f_a_masse}\times U^n\times \texttt{beta_}\\
  &M_v \pluseq \texttt{surface}\times \texttt{f_a_masse}\times \texttt{beta_}
\end{align}
