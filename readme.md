# Stupid Airport Simulator

Simulate an airport with different concurrency models.

# Help

Run ``python airport.py --help`` for help.

# Usage

```
$ airport.py awaiting -n_planes 5 -n_runways 2
2020-12-23 17:20:08,237 - __main__ - INFO - assigned - Runway 0 will be assigned to 0 in 2020-12-23 17:20:08.237524 for 4 seconds
2020-12-23 17:20:08,237 - __main__ - INFO - assigned - Runway 1 will be assigned to 1 in 2020-12-23 17:20:08.237524 for 2 seconds
2020-12-23 17:20:08,238 - __main__ - INFO - assigned - Runway 1 will be assigned to 2 in 2020-12-23 17:20:10.237524 for 1 seconds
2020-12-23 17:20:08,238 - __main__ - INFO - assigned - Runway 1 will be assigned to 3 in 2020-12-23 17:20:11.237524 for 4 seconds
2020-12-23 17:20:08,238 - __main__ - INFO - assigned - Runway 0 will be assigned to 4 in 2020-12-23 17:20:12.237524 for 1 seconds
2020-12-23 17:20:08,239 - __main__ - INFO - start - Start land(0, 0, 4)
2020-12-23 17:20:08,239 - __main__ - INFO - start - Start land(1, 1, 2)
2020-12-23 17:20:10,240 - __main__ - INFO - landed - Plain 1 landed on 1
2020-12-23 17:20:10,240 - __main__ - INFO - start - Start land(2, 1, 1)
2020-12-23 17:20:11,240 - __main__ - INFO - start - Start land(3, 1, 4)
2020-12-23 17:20:11,240 - __main__ - INFO - landed - Plain 2 landed on 1
2020-12-23 17:20:12,240 - __main__ - INFO - landed - Plain 0 landed on 0
2020-12-23 17:20:12,240 - __main__ - INFO - start - Start land(4, 0, 1)
2020-12-23 17:20:13,241 - __main__ - INFO - landed - Plain 4 landed on 0
2020-12-23 17:20:15,241 - __main__ - INFO - landed - Plain 3 landed on 1
```
