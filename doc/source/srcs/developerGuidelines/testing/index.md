# Test your code !

Test cases are separated in two categories, each covering a distinct need:

* [verification tests](./tests.md): those are very short tests that will only serve to check basic functionality of the code, and can be lauched often (multiple times a day by everyone) or in debug mode (a lot slower). They are meant to check that the code can run without crashing, and that no drastical regression in computations has been introduced.

* [validation tests](./validation.md): those are langer test cases that will produce results with physical meaning, which can then be compared to analytical solutions or experimental data.

These tests are detailed in the two following sections:
```{toctree}
:maxdepth: 1

./tests.md
./validation.md
```

For information, it should be noted that validation tests are automatically converted to verification tests by extracting the simulation cases defined in the validation test, and reducing the number of iteration (to 3). This means that in a lot of cases, writing validation tests will be enough to cover both verification and validation.

However, verification tests are easier to write than validation tests. Thus, it is common during development to start by writing simple test cases that will ensure you don't break your previous develpments, then at the end, before integration, replace these small verification tests by a validation test properly documented.