# rugby_data_processing

Python scripts to extract interesting data from IRB PDF match reports
and save it in CSV.

* [scripts/match_penalty.py](match_penalty.py) converts IRB penalty match reports PDFs to csv format
* [scripts/match_score.py](match_score.py) converts IRB scoring match reports PDFs to csv format
* [scripts/get_score.sh](get_scores.sh) executes match_score.py and concatenates results
* [scripts/get_penalties.sh](get_penalties.sh) executes match_penalty.py and concatenates results
* (pandashells.examples.sh) [data/pandashells.examples.sh] examples of data manipulation with (pandashells)[https://github.com/robdmc/pandashells]

Results from 2014-2015 World Sevens Series:
* (full_score.csv)[data/full_score.csv]
* (full_pen.csv)[data/full_pen.csv]
