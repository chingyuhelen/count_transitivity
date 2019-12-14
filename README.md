# count_transitivity


## Usage

#### To get a file of sentences containing keywords, extracted from Chinese datasets:

```bash
python find_patterns_map.py > data.txt
```

news dataset 1: 1991-2004 (content)
news dataset 2: 1991-2004 (headline)
news dataset 3: 2004-2017 (content)


#### To get json files processed from the txt file(data.txt):
dataset1:{'vn':{'關心': {'': [sent1, ...]}, 
                }
          'pnv:{'關心': {'對': [sent1, ...]}
                }
          }

```bash 
cat data.txt | python save_to_json.py

```

#### Calculate the transitivity of each keyword(verb) to see whether the results support our predictions:
transitive usage: V N (e.g., 我很+關心+這件[事]。)

intransitive usage: P N V (e.g., 我[對]這件[事]很+關心+。)


```bash 
python count_transitivity.py

```
 
 
 
