# Grid Configuration

Beyond simple lists, Malet's YAML config supports list comprehensions, grid sequences, and field grouping for complex experiment designs.

## List comprehension

Generate grid values using Python-like expressions inside the YAML config:

```yaml
lr: [10**{-i};1:1:5]
```

The general syntax is `[{expression};{start}:{step}:{end}]`, which is equivalent to `[expression for i in range(start, end, step)]`. The expression can use the variable `i` and standard arithmetic operators.

More examples:

```yaml
lr: [10**{-i};1:1:5]          # [0.1, 0.01, 0.001, 0.0001]
width: [2**{i};5:1:10]        # [32, 64, 128, 256, 512]
dropout: [{i*0.1};1:1:6]      # [0.1, 0.2, 0.3, 0.4, 0.5]
```

## Grid sequences

Run a sequence of different grids by passing a list of dictionaries under `grid`:

```yaml
grid:
    - optimizer: sgd
      lr: [0.001, 0.01]
      seed: [1, 2, 3]

    - optimizer: adam
      lr: [0.005]
      seed: [1, 2, 3]
```

This runs 2 x 3 = 6 configs for SGD, then 1 x 3 = 3 configs for Adam (9 total), instead of the full Cartesian product. This is useful when certain hyperparameter combinations are irrelevant and you don't want to waste compute.

## Grouping

Grouping ties multiple fields together so they vary in lockstep rather than forming a Cartesian product:

```yaml
grid:
    group:
        optimizer: [[sgd], [adam]]
        lr: [[0.001, 0.01], [0.005]]
    seed: [1, 2, 3]
```

Here `optimizer` and `lr` are paired — `(sgd, [0.001, 0.01])` and `(adam, [0.005])` — then crossed with `seed`. This is equivalent to the grid sequence above but more compact.

The general pattern:

```yaml
grid:
    group:
        cfg1: [A1, B1]
        cfg2: [A2, B2]
    cfg3: [1, 2, 3]
```

produces the same runs as:

```yaml
grid:
    - cfg1: A1
      cfg2: A2
      cfg3: [1, 2, 3]

    - cfg1: B1
      cfg2: B2
      cfg3: [1, 2, 3]
```

The grouped fields `cfg1` and `cfg2` have paired values `(A1, A2)` and `(B1, B2)` — they are not crossed against each other.

### Multiple groups

You can create multiple independent groups using a list under `group`:

```yaml
grid:
    group:
        - cfg1: [A1, B1]
          cfg2: [A2, B2]
        - cfg3: [C1, D1]
          cfg4: [C2, D2]
    cfg5: [1, 2, 3]
```

Each group `(cfg1, cfg2)` and `(cfg3, cfg4)` is internally paired, but the two groups are crossed against each other and against `cfg5`.
