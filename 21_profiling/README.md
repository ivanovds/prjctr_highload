# Profilfing

As a profiler was used **cProfile** python profiler.
https://docs.python.org/3/library/profile.html


Profiling example for a single dataset test:

```
         606 function calls (406 primitive calls) in 0.001 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.001    0.001 <string>:1(<module>)
        1    0.000    0.000    0.001    0.001 bst.py:138(from_array)
    201/1    0.001    0.000    0.001    0.001 bst.py:142(sorted_array_to_bst)
      100    0.000    0.000    0.000    0.000 bst.py:3(__init__)
        1    0.000    0.000    0.001    0.001 {built-in method builtins.exec}
      301    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

Selected 10 values for datasets with different sizes:

```
    201/1    0.002    0.000    0.002    0.002 bst.py:142(sorted_array_to_bst)
    401/1    0.004    0.000    0.004    0.004 bst.py:142(sorted_array_to_bst)
    801/1    0.007    0.000    0.008    0.008 bst.py:142(sorted_array_to_bst)
   1601/1    0.009    0.000    0.011    0.011 bst.py:142(sorted_array_to_bst)
   3201/1    0.030    0.000    0.052    0.052 bst.py:142(sorted_array_to_bst)
   6401/1    0.050    0.000    0.058    0.058 bst.py:142(sorted_array_to_bst)
  12801/1    0.081    0.000    0.096    0.096 bst.py:142(sorted_array_to_bst)
  25601/1    0.159    0.000    0.188    0.188 bst.py:142(sorted_array_to_bst)
  51201/1    0.289    0.000    0.359    0.359 bst.py:142(sorted_array_to_bst)
```

As you can see **ncalls** has linear relationship, while **tottime** has **log(n)**

```
     ┌────────────────────────────────────────────────────────────────────────────────────┐
0.289┤                                                                                   •│
     │                                                                                    │
     │                                                                                    │
0.241┤                                                                                    │
     │                                                                                    │
     │                                                                                    │
     │                                                                                    │
0.193┤                                                                                    │
     │                                                                                    │
     │                                                                         •          │
0.146┤                                                                                    │
     │                                                                                    │
     │                                                                                    │
0.098┤                                                                                    │
     │                                                              •                     │
     │                                                                                    │
     │                                                                                    │
0.050┤                                                    •                               │
     │                                          •                                         │
     │                               •                                                    │
0.002┤•         •          •                                                              │
     └┬─────────┬──────────┬─────────┬──────────┬─────────┬─────────┬──────────┬─────────┬┘
      201      401        801                  5.0                 7.0                 9.0 
```
