# Отдача статики через nginx

```bash
wrk -t2 -c50 -d10s http://127.0.0.1:80/static/images/image.png
```

Running 10s test @ http://127.0.0.1:80/static/images/image.png
  2 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    38.52ms    6.97ms 115.93ms   88.77%
    Req/Sec   651.43     52.50   747.00     77.23%
  13105 requests in 10.10s, 2.75GB read
Requests/sec:   1297.19
Transfer/sec:    278.41MB

```bash
wrk -t1 -c50 -d10s http://127.0.0.1:80/static/images/image.png
```

Running 10s test @ http://127.0.0.1:80/static/images/image.png
  1 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    39.68ms    6.73ms 132.87ms   87.58%
    Req/Sec     1.27k    92.36     1.44k    68.32%
  12722 requests in 10.10s, 2.67GB read
Requests/sec:   1259.59
Transfer/sec:    270.30MB

# Отдача статики через gunicorn

```bash
wrk -t2 -c50 -d10s http://127.0.0.1:8000/static/images/image.png
```

Running 10s test @ http://127.0.0.1:8000/static/images/image.png
  2 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    58.63ms    2.76ms  76.44ms   94.42%
    Req/Sec   426.55     15.90   454.00     86.00%
  8500 requests in 10.02s, 1.79GB read
Requests/sec:    848.58
Transfer/sec:    182.54MB

```bash
wrk -t1 -c50 -d10s http://127.0.0.1:8000/static/images/image.png
```

Running 10s test @ http://127.0.0.1:8000/static/images/image.png
  1 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    58.85ms    2.97ms  72.89ms   92.25%
    Req/Sec   849.87     24.23     0.89k    80.00%
  8464 requests in 10.01s, 1.78GB read
Requests/sec:    845.64
Transfer/sec:    181.91MB

# Отдача динамики через gunicorn

```bash
wrk -t2 -c50 -d10s http://127.0.0.1:8000
```

Running 10s test @ http://127.0.0.1:8000
  2 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   603.53ms   74.61ms 684.78ms   95.30%
    Req/Sec    40.13      5.77    60.00     73.00%
  808 requests in 10.07s, 28.05MB read
Requests/sec:     80.27
Transfer/sec:      2.79MB

```bash
wrk -t1 -c50 -d10s http://127.0.0.1:8000
```

Running 10s test @ http://127.0.0.1:8000
  1 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   570.68ms   71.02ms 640.12ms   95.79%
    Req/Sec    85.41      9.20   101.00     76.00%
  856 requests in 10.06s, 29.71MB read
Requests/sec:     85.10
Transfer/sec:      2.95MB

# Отдача динамики через nginx

```bash
wrk -t2 -c50 -d10s http://127.0.0.1:80
```

Running 10s test @ http://127.0.0.1:80
  2 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   532.83ms  169.99ms 688.33ms   81.86%
    Req/Sec    39.12     15.78    70.00     54.47%
  485 requests in 10.07s, 16.84MB read
Requests/sec:     48.15
Transfer/sec:      1.67MB

```bash
wrk -t1 -c50 -d10s http://127.0.0.1:80 
```

Running 10s test @ http://127.0.0.1:80
  1 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   602.09ms   76.95ms 682.04ms   95.30%
    Req/Sec    80.57      7.78   101.00     74.00%
  808 requests in 10.06s, 28.06MB read
Requests/sec:     80.34
Transfer/sec:      2.79MB

# Отдача динамики через nginx с кешированием

```bash
wrk -t2 -c50 -d10s http://127.0.0.1:80
```

Running 10s test @ http://127.0.0.1:80
  2 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    22.09ms    9.31ms  82.44ms   82.99%
    Req/Sec     1.16k   233.02     1.70k    72.00%
  23153 requests in 10.02s, 804.41MB read
Requests/sec:   2310.99
Transfer/sec:     80.29MB

```bash
wrk -t1 -c50 -d10s http://127.0.0.1:80
```

Running 10s test @ http://127.0.0.1:80
  1 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    41.48ms  150.84ms   1.96s    97.22%
    Req/Sec     2.02k   524.98     2.86k    72.73%
  19920 requests in 10.01s, 692.22MB read
  Socket errors: connect 0, read 0, write 0, timeout 30
Requests/sec:   1989.25
Transfer/sec:     69.13MB