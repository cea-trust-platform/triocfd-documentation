# Setup your development environment

:::{note}
These steps are mostly intended as a tutorial for internal developers (at CEA). As such, links are using the internal network. If you do  not have access, use the github repository. To obtain externalpackages (all dependencies for TRUST), use [wget](wget).
:::

## Clone TrioCFD
Before developing, you need to clone the Git repository of TrioCFD and its dependencies (Trust).

To do that, you have to use the ``` git clone ``` command, which take as argument an url to a git repo and downloads it.

To download everything you need, use the following commands:
```bash
git clone ssh://gitolite@ssh-codev-tuleap.intra.cea.fr:2044/triocfd/triocfd-code.git
git clone ssh://gitolite@ssh-codev-tuleap.intra.cea.fr:2044/trust/trust-code.git
cd trust-code
git clone ssh://gitolite@ssh-codev-tuleap.intra.cea.fr:2044/trust/externalpackages.git
```
After using these command, your current directory will have these directories, each following a git repository:
```bash
triocfd-code
trust-code
  | externalpackages
```
In each of these repositories, there are two important branches: 
- `master`: most recent official version: 1.x.x
- `next` : continuous integration branch. Finalized developments are regularly uploaded there. Once ready, it will become the next official release (in master branch).

:::{note}
:name: wget

For external collaborators, you can obtain TRUST/TrioCFD from [Github](https://github.com/cea-trust-platform) and externalpackages with
```
wget ftp://ftp.cea.fr/pub/TRUST/externalpackages/externalpackages-next.tar
tar xf externalpackages-next.tar
```
:::

## Checkout correct branch
When you start developing at first, you probably want to start from the branch `next`. To reach it, use 
```bash
git checkout next
```
Before compiling the code, you have to do this in each repository (trio, trust and external packages).


Then, to compile the code, you first compile TRUST, then TrioCFD:
```bash
# in trust-code
./configure && make

# in triocfd-code
baltik_build_configure -execute
make optim # or make debug, or both
```

:::{caution}

Sometimes the branch ```next``` of the Trust repository may be in advance compared the branch ```next``` of TrioCFD !

This may happen if an integration is done on Trust that impacts TrioCFD, and the integration of fixes for TrioCFD is delayed.

In this case, TrioCFD will not compile with the branch ```next``` from Trust.

To solve this, you have to go to the correct Trust commit. This is indicated by the file ``` src/trust.commit ``` in the TrioCFD repository.
This file contains the hash of the Trust commit on which TrioCFD was last compiled. To go to the correct commit on trust, use (in trust-code directory)
```bash
git checkout <hash>
```
where ```<hash>``` is the content of the file ``` src/trust.commit ```.
:::

## Create your working branch
Before you begin development, you will need to create your own **branch**.

When you first start developing, you probably want to start from the most recent developments, which are on branch `next`. If you followed the tutorial in the [previous section](#checkout-correct-branch), you should be on this branch. You can check with git status, as explained in the previous section.


:::{admonition} For internal developpers (CEA)
:class: important

Please follow the procedure described below to choose the name for your branch.
:::


In order to help tracking undergoing development, we ask you to follow some **rules** in naming branches:

- Your branch has to have a describing ticket in the [Tuleap Bugtracker](https://codev-tuleap.intra.cea.fr/plugins/tracker/?tracker=764), and the ticket number must be in the branch name. To do that, follow these steps:
  - First, go to the [Tuleap Bugtracker](https://codev-tuleap.intra.cea.fr/plugins/tracker/?tracker=764) and create a ticket describing your planned developments. You will be able to update this description later.

  - The ticket will be given a six-digits number like 123456

  - Then, in the name of your branch, include the text 'TCFD123456', preferably at the end so it is easier to use auto-completion of branch name.

  - This is mostly for long term developments implementing new features (if you create a branch with a small fix and do a PR right after, no need).

- Tip: to help keep track of your own branches, you can start the name of your branches with a unique short alias that belongs to you.

- To help people (and yourself) know what the branch is about, add keywords or a short description (up to 5 words) in the name.

- The result should look like `name/short_description_TCFD123456`. Then you can easily find all your branches with autocompletion when you type `git checkout name/`.

- Often, you will need to change some code in TRUST alongside your developments in TrioCFD. In this case, use the **same name** for corresponding branches in both codes.



After finding a suitable branch name, you can create the branch with the following commands:
```bash
git checkout -b <branch_name>
git push -u origin <branch_name>
```

See the [git tutorial section on branches](./git-tutorial/branch.md) for more information.