# LSCDBenchmark

  * [General](#general)
  * [Usage](#usage)
  * [Tasks](#tasks)
    + [Lemma Level](#lemma-level)
    + [Usage Level](#usage-level)
  * [Metrics](#metrics)
  * [Sub-evaluations](#sub-evaluations)
  * [Datasets](#datasets)
 * [BibTex](#bibtex)


### General

Benchmark for Lexical Semantic Change Detection.

### Usage

- get_data.sh
- evaluate.sh
- evaluate.py

- input: CSV files in folders for task/one CSV file?
- output: CSV file with results for all tasks and metrics

===Standard Split===

#### Tasks

lemma level:
- binary change (sense loss or gain)
- graded change 1 (divergence of word sense distribution)
- graded change 2 (compare metric)

usage level:
- choose which level

#### Metrics

|Name | Code | Applicability | Comment |
| --- | --- | --- | --- |
| Spearman correlation | `evaluation/spr.py` | DURel, SURel, SemCor LSC, SemEval*, Ru\* | - outputs rho (column 3) and p-value (column 4) |
| Average Precision | `evaluation/ap.py` | SemCor LSC, SemEval*, DIACR-Ita | - outputs AP (column 3) and random baseline (column 4) |
| F1/accuracy | | | |


#### Sub-Evaluations

- POS
- hard binary changes (which are not also graded changes)
- hard graded changes (which are not also binary changes)
- extended data sets
- very clean cases

#### Datasets

| Dataset | Language | Corpus 1 | Corpus 2 | Download | Comment |
| --- | --- | --- | --- | --- | --- |
| DURel | German | DTA18 | DTA19  | [Dataset](https://www.ims.uni-stuttgart.de/data/durel), [Corpora](https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/wocc) | - version from Schlechtweg et al. (2019) at `testsets/durel/` |
| SURel | German | SDEWAC | COOK | [Dataset](https://www.ims.uni-stuttgart.de/data/surel), [Corpora](https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/wocc) | - version from Schlechtweg et al. (2019) at `testsets/surel/` |
| SemCor LSC | English | SEMCOR1 | SEMCOR2 | [Dataset](https://www.ims.uni-stuttgart.de/data/lsc-simul), [Corpora](https://www.ims.uni-stuttgart.de/data/lsc-simul) | |
| SemEval Eng | English | CCOHA 1810-1860 | CCOHA 1960-2010 | [Dataset](https://www.ims.uni-stuttgart.de/data/sem-eval-ulscd), [Corpora](https://www.ims.uni-stuttgart.de/data/sem-eval-ulscd) | |
| SemEval Ger | German | DTA 1800-1899 | BZND 1946-1990 | [Dataset](https://www.ims.uni-stuttgart.de/data/sem-eval-ulscd), [Corpora](https://www.ims.uni-stuttgart.de/data/sem-eval-ulscd) | |
| SemEval Lat | Latin | LatinISE -200-0 | LatinISE 0-2000 | [Dataset](https://www.ims.uni-stuttgart.de/data/sem-eval-ulscd), [Corpora](https://www.ims.uni-stuttgart.de/data/sem-eval-ulscd) | |
| SemEval Swe | Swedish | Kubhist2 1790-1830 | Kubhist2 1895-1903 | [Dataset](https://www.ims.uni-stuttgart.de/data/sem-eval-ulscd), [Corpora](https://www.ims.uni-stuttgart.de/data/sem-eval-ulscd) | |
| RuSemShift1 | Russian | RNC 1682-1916 | RNC 1918-1990 | [Dataset](https://github.com/juliarodina/RuSemShift), [Corpora](https://rusvectores.org/static/corpora/) | |
| RuSemShift2 | Russian | RNC 1918-1990 | RNC 1991-2016 | [Dataset](https://github.com/juliarodina/RuSemShift), [Corpora](https://rusvectores.org/static/corpora/) | |
| RuShiftEval1 | Russian | RNC 1682-1916 | RNC 1918-1990 | [Dataset](https://github.com/akutuzov/rushifteval_public), [Corpora](https://rusvectores.org/static/corpora/) | |
| RuShiftEval2 | Russian | RNC 1918-1990 | RNC 1991-2016 | [Dataset](https://github.com/akutuzov/rushifteval_public), [Corpora](https://rusvectores.org/static/corpora/) | |
| RuShiftEval3 | Russian | RNC 1682-1916 | RNC 1991-2016 | [Dataset](https://github.com/akutuzov/rushifteval_public), [Corpora](https://rusvectores.org/static/corpora/) | |
| DIACR-Ita | Italian | Unità 1945-1970 | Unità 1990-2014 | [Dataset](https://github.com/diacr-ita/data/tree/master/test), [Corpora](https://github.com/swapUniba/unita/) | |
| other Italian data set | | | | | |

#### Leaderboard

Compare [here](https://sapienzanlp.github.io/xl-wsd/)

BibTex
--------

```
```
