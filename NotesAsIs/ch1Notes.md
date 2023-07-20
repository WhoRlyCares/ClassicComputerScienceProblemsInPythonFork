---
up: [ClassicComputerScienceProblems]
tags: [cs101, recursion]
aliases:
---

# ClassicCompSciProblems Ch1

## 1.1 Recursion Рекурсия

 - Рекурсивные функции вызывают сами себя.
 - Создание аргумента, хранящего состояние, позволяет вычислять значение один раз, но в наивной реализации не 
   уменьшает количество вызовов.
 - Python имеет готовый кэш LastRecentlyUsedCache at functools.lru_cache. Который в рантайме генерирует 
   предвычисленные значия для функций.
 - Хорошее итеративное решение, обычно быстрее рекурсии. Но требует базы и итерации, с начала, а не конца.
 - Генераторы могут оказаться решением, так как хранят стейт в себе из коробки.

```python
def fib_statefull(n: int, state=None) -> int:
    """Statefull doesn't need to recalculate encountered values"""
    if not state:
        state = {0: 0, 1: 1, 2: 1}
    if n in state.keys():
        return state[n]
    else:
        return fib_statefull(n - 1, state) + fib_statefull(n - 2, state)

import functools
@functools.lru_cache(maxsize=None)
def fib_auto_cache(n: int) -> int:
    """lru cache - LastRecentlyUsed basically state created and managed by interpreter"""
    return 2 if n < 2 else (fib_auto_cache(n - 1) + fib_auto_cache(n - 2))
```

## 1.2 Compression Сжатие

 - Компромисс время-пространство
 - Типизация: int min size 28byte  `sys.getsizeof(i)`
 - 

