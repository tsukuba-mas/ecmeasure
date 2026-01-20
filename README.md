# ecmeasure
Echo chamber measures implemented by Python proposed in the paper Kataoka et al. (2026):

- Hiro Kataoka, Jérôme Euzenat, and Koji Hasebe. Coherent belief and opinion propagation produces more echo chambers. AAMAS 2026, 9 pages, May 2026. [Link to the paper will be made available upon publications]

## Overview of the measure
For details, please read the corresponding paper.
The defined measures counts the number of strongly connected components with the three features of echo chambers: homogeneity, segregation, and reinforcement [[Mahmoudi et al., 2024](https://doi.org/10.1109/ACCESS.2024.3353054)].
Homogeneity tests whether agents' opinions/beliefs are (roughly) the same within a single subset of agents; segregation tests whether such subset is enough less-connected to other subsets of agents; reinforcement tests whether their opinions/beliefs are getting closer.

## Implementation and how to use
Each of the features and the measure itself are defined in separate files:

- **Homogeneity** is tested by functions in `homogeneity.py`;
- **Segregation** is tested by functions in `segregation.py`;
- **Reinforcement** is tested by functions in `reinforcemenet.py`;
- Finally, the echo chamber measures $eo^t$ and $eb^t$ are provided in `ecmeasures.py`.

## Interface
In principle, if you want to test the proposed measures, import `ecmeasures.py` and use the functions `eo` and `eb`.
In most of the cases, they are enough.
For their interface, see the source code.

If you want to customize details (e.g., use the drastic distance instead of the Hamming distance), use `eo_raw` or `eb_raw`.
These functions are customizable version of `eo` and `eb`.

## Tests
See codes under the `tests` directory.
Tests can be executed through:

```
$ uv run pytest tests/*.py
```

## License
MIT