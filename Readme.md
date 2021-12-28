# Advent of Code 2021

## setup
Codes were written using python 3.9. The only non-official modules used are *numpy*, *pandas*, *z3* and *Cython*

To compile the cython files run:
```sh
python setup.py build_ext --inplace
```

this command will generate several *module_c.so.cpython-39-your-archi.so* files in the required folders


## code organization

in each dir, you can find :
* `input.txt` the input of the exercise
* a file `c.py` that compute both answers at the same time, or 2 files `c_part1.py` and `c_part2.py` when both parts are very different

sometimes there are also module files. They can be python file or cython file that needs to be compiled.

## day per day
* day 1: pure python
* day 2: pandas
* day 3: numpy
* day 4: numpy
* day 5: numpy
* day 6: pure python
* day 7: numpy
* day 8: 2 solutions, one in pure python and one in z3
* day 9: numpy
* day 10: pure python
* day 11: numpy
* day 12: pure python
* day 13: numpy
* day 14: pure python
* day 15: numpy + cython. To use the cython version change the import in the file *c.py*.
  * python: part 1: 0.1005 seconds, part 2: 2.4491117000579834 seconds
  * cython: part 1: 0.008 seconds, part 2: 0.247 seconds
* day 16: pure python
* day 17: 3 versions are available, one in pure python, one in cython using python annotation and one in cython using pyx file
  * python run in 0.0457 s
  * python with cython annotation run in 0.0137 s
  * cython pyx file run in 0.0003 s (yes, 100 times faster, mainly because we use c++ std::vector instead of python list )
* day 18: pure python and cython
* day 19: cython
* day 20: numpy + cython
* day 21: python
* day 22: numpy for part1, pure python for part 2
* day 23: pure python or cython
  * pure python runs in 54 s
  * cython runs in 4 s
* day 24: z3
* day 25:
  * numpy runs in 0.07903742790222168 s
  * pure python runs in 9.99944257736206 s
  * cython runs in 0.06466269493103027 s


## things learned:
* *heapq* is really powerful when working on sorted list. See day 15 for an application
* *z3* is a great tool for constraints solving. See days 8 and 23
* *Counter* are basically the same as  *defaultdict(lambda: 0)*
* profiling: as simple as a `python -m cProfile -o out.prof script.py` then `snakeviz out.prof`
* cython is fast. It also provide a great visualization to understand the c code generated from python.
  * annotating python file to gain some speed work well. See day 17
  * pyx files are a bit more complex to use. Need to compile to do tests, but allow to easily use c and cpp tools, which provide more speed-up (std::vector are insane compare to python list). But beware complex data structure and strings. For these case a mix of python and cython may be best
