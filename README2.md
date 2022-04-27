# LSCDBenchmark

  * [General](#general)
  * [Data Loading](#usage)
  * [Scoring](#tasks)
  * [Baselines](#baselines)
    + [Bert](#Bert-Baseline)
    + [XLMR](#XLMR-Baseline)
    + [Random](#Random-Baseline)
  * [Sub-evaluations](#sub-evaluations)
  * [Datasets](#datasets)
 * [BibTex](#bibtex)


### General

Benchmark for Lexical Semantic Change Detection.

### Data loading

`load_data(data_path=None,lemma=None,preprocessing='context')`

#### Parameters:
  + data_path: Absolute path to the data directory
  + lemma: The lemma for which usages are to be loaded from the data directory. If `None` all of the lemmas from the    `data_path` are loaded.
  + preprocessing: There are various preprocessed (e.g. lemmatized, tokenized) versions of the usages, this parameter selects a particular version and loads it

#### Output:
  The function returns a list of tuples where each item corresponds to one data point and has the following values:

  - `(lemma,identifier,date,grouping,preprocessing,context_tokenized,indexes_target_token_tokenized,context_lemmatized)`

### Scoring
It takes a number of command line arguments and a number of configurable parameters (a yaml file) to compute various evaluation metrics. The metrics are computed for all possible combinations of the values of the parameters `filter_label`, `filter_threshold` and `evaluation_type` explained below.
#### Command-line arguments:
+ `-p` Absolute path to a file containing predictions.
+ `-g` Absolute path to a file containing gold.
+ `-s`
+ `-a` Absolute path to a file containing annotation agreement scores. These are to be used to filter the data before computing the evaluation metrics.
+ `-o` Absolute path to the directory where output is to be stored.

#### Configurable parameters (scorer.yaml):
+ `filter_label`
If the data is to be filtered then this parameter contains the name of column on which filtering is to be applied (e.g. kri_full, kri2_full). Can be a single value or a list.
+ `filter_threshold`
The threshold value for the above given `filter_lable`. Can be a single value or a list.  
+ `evaluation_type`
One of the evaluation types i.e. `change_binary` or `change_graded`.
+ `plot`
A binary parameter which can be set to `true` if the plots are .......

An example version of the `scorer.yaml` is as below:


    filter_threshold:
      - 0.1
      - 0.2
    filter_label:
      - kri_full
      - kri2_full
    evaluation_type:
      - change_binary
    plot: 'False'

#### Output
The evaluation results are stored in `results.csv` file at the output path mentioned with the `-o` parameter. An example run output with the above mentioned configuration file is given below:

| evaluation_type |	filter |	threshold |	 spearmanr_correlation |	spearmanr_pvalue |	f1 |	accuracy | precision |	recall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|change_binary|	kri_full|	0.1|	--|	--|	0.44|	0.39|	0.32|	0.71|
|change_binary|	kri_full|	0.2|	--|	--|	0.48|	0.41|	0.36|	0.71|
|change_binary|	kri2_full|	0.1|	--|	--|	0.43|	0.41|	0.3|	0.71|
|change_binary|	kri2_full|	0.2|	--|	--|	0.43|	0.41|	0.3|	0.71|


#### Plotting:
To be discussed: The ploting functionality in this function requires floating point distances while the gold and prediction data is in binary formate. At the moment i am loading the scoring files, and then extracting scores for the predicted data to be passed to the ploting function, is this what we want?  
#### Example Usage:



### Baselines
#### Configuration File
The baseline systems expects a yaml configuration file with various configurtion parameters for each of the following baselines systes.
#### 1: Bert-Baseline
##### Configuration parameters:

+ language: The language code (e.g. 'en', 'sv')
+ type_sentences: i.e. lemma
+ layers: e.g. 1+12
+ is_len: e.g. False
+ f2:
+ max_samples:
+ path_output1: Path to the dirctory where the bert vectors for corpus1 are to be stored (e.g. `./output/vectors_xlmr_corpus1/` )
+ path_output2: Path to the dirctory where the bert vectors for corpus2 are to be stored (e.g. `./output/vectors_xlmr_corpus2/``
+ path_results: Path to the diretor where results are to be stored (e.g. `./results/`)
+ path_targets: Path to the directory whrer target words are to be found (e.g. `./targets/`)

#### 2: XMLR-Baseline
##### Configuration parameters:

+ language: The language code (e.g. 'en', 'sv')
+ type_sentences: i.e. lemma
+ layers: e.g. 1+12
+ is_len: e.g. False
+ f2:
+ max_samples:
+ path_output1: Path to the dirctory where the bert vectors for corpus1 are to be stored (e.g. `./output/vectors_xlmr_corpus1/` )
+ path_output2: Path to the dirctory where the bert vectors for corpus2 are to be stored (e.g. `./output/vectors_xlmr_corpus2/``
+ path_results: Path to the diretor where results are to be stored (e.g. `./results/`)
+ path_targets: Path to the directory whrer target words are to be found (e.g. `./targets/`)

Based on a number of configuration options, the script loads usages (from two different time-spans) of a list of target words using the load_data function, computes their bert vectors, and then  

#### 3: Random-Baseline
##### Configuration parameters:

+ language: The language code (e.g. 'en', 'sv')
+ path_results: Path to the diretor where results are to be stored (e.g. `./results/`)
+ path_targets: Path to the directory whrer target words are to be found (e.g. `./targets/`)
+ is_rel:

##### TODO:

Priority:
- [ ] extraction of sense description labels is done more elegantly in WSI-summer benchmark: semeeval_to_bts_rnc_convert.py
- [ ] use hydra or not?
- [ ] implement three scenarios of use (see picture I sent)

- [ ] ===Standard Split===
- [ ] Datasets should provide: dataset1/dev.data, dataset1/eval.data
- [ ] All downloaded datasets should be converted to the same structure
- [ ] converted data should be split into development set and training set
- [ ] Include MCL-WiC, binary labels vs scaled labels

#### Tasks

lemma level:
- binary change (sense loss or gain)
- graded change 1 (divergence of word sense distribution)
- graded change 2 (compare metric)
- clustering evaluation (already implemented)

usage level:
- novel sense identification

##### TODO:
- Accuracy and correlation on WiC
- Later WSI
-

#### Metrics

|Name | Code | Applicability | Comment |
| --- | --- | --- | --- |
| Spearman correlation | `evaluation/spr.py` | DURel, SURel, SemCor LSC, SemEval*, Ru\* | - outputs rho (column 3) and p-value (column 4) |
| Average Precision | `evaluation/ap.py` | SemCor LSC, SemEval*, DIACR-Ita | - outputs AP (column 3) and random baseline (column 4) |
| F1/accuracy | | | |

##### TODO:
- Recall and Precision

#### Sub-Evaluations

- POS
- hard binary changes (which are not also graded changes)
- hard graded changes (which are not also binary changes)
- extended data sets
- very clean cases

##### TODO:
- Nothing currently

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

##### TODO:
- Nothing

#### Leaderboard

#### Pre-trained models?

Compare [here](https://sapienzanlp.github.io/xl-wsd/)

BibTex
--------

```
```


#### TODO for Serge:

- [ ] Clean Up existing code
- [ ] Script for downloading all datasets
- [ ] Implementing of [Tasks](#Tasks)
- [ ] Cleaned Versions of Datasets
- [ ] ...

Notes:
> What structure/functions do we need?
> Load Function,
