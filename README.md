# Cricinfo Stat Retriever
A script to retrieve data from Cricinfo Statsguru
## Running the Script
1. Pip install the dependicies
2. Run retrieve.py with the query as a command line argument
3. First argument should be the name, use '!' as prefix for women cricketers
    ``` bash
        python retrieve.py '!perry'
        python retrieve.py 'kohli'
    ```
4. Add filters, the supported filters are 
    1. Host nation (simply type the name) 
    2. Format (all,test,odi,t20i) 
    3. Venue (Home, away, neutral) 
    4. Opposition (usage-> vs COUNTRY)
    5. Time range (usage-> y/year/time start (to/-) end ) 
    ```
        python retrieve.py 'kohli @aus'
        python retrieve.py 'kohli @ test'
        python retrieve.py 'kohli @ neutral'
        python retrieve.py 'vvs @ vs AUS'
        python retrieve.py 'gautam gambhir @ time 1 jan 2006 - 31 dec 2008'
        python retrieve.py 'gautam gambhir @ y 1 jan 2006 to 31 dec 2008'
    ```
# Cricinfo Live Score Retrieval
A script to retrieve scoreboards from live cricket matches
## Running the Script
1. Pip install the dependicies
2. Run score_retrieval.py
3. Enter the match id from the list
