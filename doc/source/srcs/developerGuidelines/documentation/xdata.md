:::{index} single: XDATA
:::
# XDATA

Xdata is a special format used to document valid keywords useable in trust datasets (`.data` files).

It is made of special c++ comments added to the source code at specific places, that must start with specific tags. These comments must start with one of:

 - `// XD`, used at the begining of every class derived from `Objet_U` that may be read in a `.data` file as a keyword.

 - `// XD_ADD_P`, used after every `param.ajouter` used to add a keyword to a class derived from `Objet_U`.

See below for the syntax each of these tags must follow.

## Tag XD_ADD_P (most common for users)
It must look like that:
```
param.ajouter("tutu", &tutu);  // XD_ADD_P <type> <description>
```
The name of the param is extracted from the first argument of `param.ajouter`, so the XD_ADD_P tag  **must** be on the same line.

- `<type>` can be one of the following:

  - `int`: means the param is a single integer value
  - `double`: means the param is a single floating point number
  - `chaine`: means either 
    - a single word without space (i.e. `my_keyword_without_space`) 
    - **or** (this is weird!!) a full block encompassed in curly braces. Example: `toto` is a chaine, and `{ how do you { do } }` is also a `chaine`, but `titi toto` is not. In particular, this must be used when adding another object derived from `Objet_U` as parameter, or when adding a non standard parameter with `param.ajouter_non_std`.
  - `rien`: this means the keyword does not expect a value after. Used for flags, when only the presence of the keyword is activating a boolean parameter.

- `<description>` must be a sentence describing the effect of the parameter. It **must** be written on a single line, which is kinda problematic, but hard to avoid.

:::{attention}
If you see existing XD_ADD_P tags that are not following these rules, **they are wrong !!!**

Please follow the rules in this documentation, anything else is either deprecated or experimental.
:::




## Tag XD
It must look like that:
```
// XD  <keyword>  <base>  <synonym_for_the_kw>  <with_brace>  <description>
```
- `<keyword>`
- `<base>`
- `<synonym_for_the_kw>`
- `<with_brace>`: flag that can take one of the following values:
  - `-1`: inherits from the parent class
  - `0`: keyword does not expect braces when read in the dataset. Names of the attributes are not used for reading or writing.  Example : `Champ_Uniforme 3 0. 0. 0.`
  - `1`: keyword expects curly braces, the name of the attributes is explicitly provided. Example: `Lire sch { tinit 0. tmax 0. }`

- `<description>`


## Advanced

See the doc in Trust for advanced usage (with examples)
```
$TRUST_ROOT/Outils/trustify/doc/README_user.md
$TRUST_ROOT/Outils/trustify/doc/README_dev.md
```



### Note to self: 

What XD_ADD_P should become in my opinion: 
- int, double, flags as they are right now
- chaine for a char string, either no space or surrounded with ""
- objet_u for an object derived from objet_u, between brackets.
- arrayOfXXX for an array, where arrays have their own parsers
- and **nothing else !!!** especially **not** mot_cle_non_standard

Then we would have a true file format worthy of being called as such. Nearly as powerful and flexible as json, and constrained to a clean standard. We are not that far from that, it's only a little bit of work (and the acceptation of changement from a lot of people, the hardest part probably)

Then comments will need to be addressed properly