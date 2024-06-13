**Exercise 5**

**CockroachDB**

**SETUP**

|                                          |                   |
| :--------------------------------------: | :---------------: |
|            **API Load tester**           |    K6 (main.JS)   |
| **API Load tester programming language** |     Javascript    |
|             **API platform**             | Google cloud run  |
|   **API platform programming language**  | Python(basic.py)  |
|   **(Micro)Framework used for server**   |       Flask       |
|           **DB Driver library**          |     Psycopg 3     |

**RESULTS**

|                                     |                       |                              |                            |                                         |                      |
| ----------------------------------- | --------------------- | ---------------------------- | -------------------------- | --------------------------------------- | -------------------- |
| **Number of users**                 | **Duration(seconds)** | **Average request time (s)** | **Median request time(s)** | **Throughput****(requests per second)** | **Failure rate (%)** |
| **1**                               |                       | **0.178**                    | **0.091**                  | **23**                                  |                      |
| **10**                              | **60**                | **0.312**                    | **0.16**                   | **14**                                  | **1**                |
| **35**                              | **600**               | **1.15**                     | **0.54**                   | **24**                                  | **4**                |
| **50**                              | **600**               | **2**                        | **0.81**                   | **20**                                  | **6**                |
| **50 (without list own purchases)** | **600**               | **1.88**                     | **0.85**                   | **22**                                  | **5**                |
| **100**                             | **60**                | **5**                        | **2**                      | **16**                                  | **4**                |
| **100**                             | **600**               | **3.95**                     | **1.62**                   | **23**                                  | **5**                |
| **500**                             | **300**               | **16**                       | **8**                      | **18**                                  | **61**               |
| **1000**                            | **600**               | **17**                       | **11**                     | **54**                                  | **95**               |

**NOTE : Changing the load API testing machine from personal laptop to a Google VM(4GB RAM) didn’t change the result.**

**Exercise requirements**

- **Query to get a random user each time :** 

```
@app.route('/get1row', methods=['GET'])
def case12():
    with psycopg.connect(URL) as conn:
        print("Connected to DB")
        cursor = conn.cursor()
        query = '''
        SELECT email, password FROM users ORDER BY RANDOM() LIMIT 1;
        '''
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return make_response('Balance was not found.', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        else:
            return jsonify(email=result[0], password=result[1])
        cursor.close()
    conn.close()            
                                                           
```
- Every time a user session ends, another user starts a new session.In K6 each session is a ‘Virtual user’/VU. VUs execute in parallel.

- Introduce an user think time and pick 3 random functions after login. 

```
 const allActions = [listOwnSales, listOwnPurchases, createoffer, listOffersAndBuyFirstExistingOffer, offerbyuseridAndDeleteFirstIfExists];
    const selectedActions = [];

    while (selectedActions.length < 3) {
        const randomIndex = Math.floor(Math.random() * allActions.length);
        selectedActions.push(allActions[randomIndex]);
    }

    // Execute the selected actions

    selectedActions.forEach((action) => {
        action(selfuid, loginHeaders);
        const actualThinkTime = simulateThinkTime(1, 0.5);
        console.log(" Sleep time "+actualThinkTime+"s");
    	sleep(actualThinkTime)
    });

function generateRandomNormal(mean, stdDev) {
    const u1 = Math.random();
    const u2 = Math.random();

    // Apply the Box-Muller transform
    const z0 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);

    // Scale and shift to match the desired mean and standard deviation
    const randomValue = mean + stdDev * z0;

    return randomValue;
}

function simulateThinkTime(mean, stdDev) {
    const thinkTime = generateRandomNormal(mean, stdDev);
    return thinkTime;
}

```
- **Main errors seem to be on the API level.**

Top most errors are with not being able to connect to DB. 

\
![](https://lh7-us.googleusercontent.com/docsz/AD_4nXe26hW_mljsebQbDgy71G0SC4rvMtWVWnpmIzOGyHALRkxSNnOZRXVHSRrrWPSXvWwJ3DuJZyUakFw96s6W7_kv_Wt5QW-MtbW-7Gt9aYhl3kz-yb_VMGFOCczyLPgyvkmjsFNfWUIR3qJIdEI4lacfM7-p?key=cEMignUubnI0jXKvq9x8ig)

**K6 setup** 

- **K6 installation windows**

|                                          |
| ---------------------------------------- |
|                     **choco install k6** |

- **K6 usage  : 1000 users and run for 10 minutes**

|                                                       |
| ----------------------------------------------------- |
|                   **k6 run -vu 1000 -d 600s main.js** |

- **K6 output** 
                                                                                                                                        
```
     data_received..................: 116 MB 351 kB/s
     data_sent......................: 1.8 MB 5.5 kB/s
     http_req_blocked...............: avg=25.88ms  min=0s      med=0s     max=688.29ms p(90)=0s      p(95)=360.69ms
     http_req_connecting............: avg=12.14ms  min=0s      med=0s     max=470.42ms p(90)=0s      p(95)=116.82ms
     http_req_duration..............: avg=15.57s   min=44.29ms med=7.61s  max=1m0s     p(90)=49.25s  p(95)=1m0s
       { expected_response:true }...: avg=13.1s    min=44.29ms med=6.83s  max=59.67s   p(90)=37.14s  p(95)=46.98s
     http_req_failed................: 61.33% ✓ 5830      ✗ 3675
     http_req_receiving.............: avg=21.54ms  min=0s      med=5.79ms max=3.29s    p(90)=24.56ms p(95)=48.36ms
     http_req_sending...............: avg=106.96µs min=0s      med=0s     max=10ms     p(90)=518.2µs p(95)=543.15µs
     http_req_tls_handshaking.......: avg=13.73ms  min=0s      med=0s     max=374.11ms p(90)=0s      p(95)=215.93ms
     http_req_waiting...............: avg=15.55s   min=32.1ms  med=7.58s  max=1m0s     p(90)=49.22s  p(95)=1m0s
     http_reqs......................: 9505   28.801543/s
     iteration_duration.............: avg=23.48s   min=52.82ms med=10.86s max=3m21s    p(90)=1m0s    p(95)=1m11s
     iterations.....................: 5834   17.677875/s
     vus............................: 382    min=382     max=500
     vus_max........................: 500    min=500     max=500


running (5m30.0s), 000/500 VUs, 5834 complete and 382 interrupted iterations
default ✓ [======================================] 500 VUs  5m0s
DEBU[0331] Usage report sent successfully
DEBU[0331] Everything has finished, exiting k6 normally!


```
- **Throughput =  http\_reqs** 

- **Median is obtained from med in and Average is in avg in** 

```
 http_req_duration..............: avg=15.57s   min=44.29ms med=7.61
```

