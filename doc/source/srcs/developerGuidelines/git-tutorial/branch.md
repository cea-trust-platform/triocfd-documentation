:::{index} single: git;branch
:::
# Manage branches

## Move between branches

The command to move between branches is
```bash
git checkout <branch_name>
```

To check that this worked, you can use ``` git status ```. The output should look like that:
```
On branch next
Your branch is up to date with 'origin/<branch_name>'.

nothing to commit, working tree clean
```

## Create a branch

To create a new branch, you have to use the command:
```bash
git checkout -b <branch_name>
```
or (longer, two steps)
```bash
git branch <branch_name>
git checkout <branch_name>
```

Once you do that, you will be on a new local branch. For now, this branch only exists in your own copy of the repository. If you only do this first step, the output of  ```git status``` will be:
```
On branch <branch_name>
nothing to commit, working tree clean
```
where there is no line about being up to date with origin.

In order to push your developments to the server, you need to create the branch on the remote repository. The easiest way to do this is with
```bash
git push -u origin <branch_name>
```

This command directly creates a branch with the name `<branch_name>` on the distant repo (origin) and pushes your local branch there. After this, you will be able to save your work easily to the correct distant branch using simply `git push`.

You can check that this worked with ```git status```, which should look like:
```
On branch <name>
Your branch is up to date with 'origin/<branch_name>'.

nothing to commit, working tree clean
```


In summary, to create a branch, **always** use the 2 following commands:
```bash
git checkout -b <branch_name>
git push -u origin <branch_name>
```

Always use these two commands to create a branch, as this will ensure they are configured correctly.

You can create **as many as you want/need**, don't be afraid to create more (it doesn't take more space on git, there is no bad consequence). Just try to clean them once in a while.