HOW TO DEFINE MESHING ?
======================================

**Mesh refinement**

 * Around ten discretization points between two walls (which correspond generally to a number of faces) are necessary to get correct profiles. This can sometimes be incompatible with a correct y+ placement (see below) so a compromise must be done. With less than five points, the profiles will be irrelevant.
 * If only global exchanges are the objectives, fewer cells might be used since wall laws and mass and heat conservation are sufficient to respect the flux balances.
 * It is better to avoid small cells in regions of high velocity (impact on the stability time step).
 * In order to avoid small meshes in corners, it is better not to use the option *verifierCoin* but to swap the orientation of the tetrahedrons in corners during the mesh generation process.

**Boundary layers**

 * The evaluation of wall influenced quantities (pressure loss, wall temperature, fluxes) is influenced by the near wall mesh quality and especially the control of cell size. Two or three layers of regular cells allow good prediction. This can be obtained on some geometry by using prismatic elements and then cut them in regular tetrahedral cells, or by using the TrioCFD *Extruder_bord* data.

**Tetra quality for *general* meshes**

 * In VEF discretization, attention will be given to angles between two cell faces. A histogram giving the proportion of cells in several ranges can be found in the *.err* file since the 1.6.1 version. In case of a great part of obtuse cells, some non-physical phenomena due to the diffusion operator features can be observed.
 * When using optimization tools of mesh generators, several optimization steps should be performed on the whole mesh (e.g. Laplace smoothing) with the objective to reduce globally the angles of the dihedral between two adjacent tetra faces.
 * Significant changes in the mesh size of two adjacent tetras should be avoided. A propagation factor of 20% seems to be an upper limit (5% recommended).
 * Meshing a 3D geometry with isotropic cells in all directions is the ideal way not to disturb the numerical models for a 3D flow. However for a flow with slow physical variation in a given direction (1D-flow), it can be shown that stretching the mesh up to a hundred times in this preferred direction doesn't much degrade the results. A stretch in both the preferred and the transverse directions up to thirty times doesn't affect them either.

**Tetra quality for *TrioCFD made* meshes**

 * Using TrioCFD extruding tools: the *Extrude* option (one hexahedron divided in 14 tetrahedra) can lead to cells having angles over 90 degres. Prefer *Extruder_en20*, unless the number of cells is limited as cutting into 20 tetrahedrons can lead to a great number of very thin cells.. In that case, *Extruder_en3* can be used, but the result must be checked carefully.
