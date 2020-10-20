# blazegraph-load-pipeline
Pipeline to generate triples aligning to Wikidata Schema for any KGTK graph and loading the created triples to Blazegraph

**Steps to run the pipeline**

* Create a new conda environment

  ```bash
  conda create --name kgtk_env python=3.7
  ```

* Activate the newly created environment

  ```bash
  conda activate kgtk_env
  ```

* Install Dependencies

  ```bash
  pip install -r requirements.txt
  ```

**Default parameters that the notebook takes**

```python
# Generate triples parameter

#kgtk_path takes in the directory which contains the kgtk subgraph
kgtk_path = '/Users/rijulvohra/Documents/work/Novartis-ISI/kgtk_development/data/Q28885102'
output_filename = 'pharma_product_concat.tsv.gz'
triple_filename = 'pharma_triple.ttl'
triple_generation_log = 'pharma_log.txt'
properties_file_path = './properties.tsv'

# Load triples to blazegraph
wikibase_ui_port = '10001'
wikibase_sparql_port = '10002'
wikibase_proxy_port = '10003'
wikibase_qs_port = '10005'
wikibase_volume = '.'
docker_name = 'blazegraphpipeline'
create_new = False
stop_docker = "No"
blazegraph_image = 'wikibase/wdqs:0.3.10'
ttl_path = ''

#Parameterize whether you want to run just the generate_wikidata_triples part or loading to blazegraph part
only_gen_triples = False
only_load_triples = False
both_gen_and_load_triples = False
```



The notebook can be run in three modes:

* If you only want to generate the triples, then set the **only_gen_triples** parameter to be **True**

  ```bash
  papermill combined_pipeline.ipynb combined_pipeline_op.ipynb -p only_gen_triples True
  ```

* Likewise, if you just want to load the triples to  blazegraph, then set the **only_load_triples** parameter to be **True**

  ```bash
  papermill combined_pipeline.ipynb combined_pipeline_op.ipynb -p only_load_triples True -p create_new True -p ttl_path /Users/rijulvohra/Documents/work/Novartis-ISI/kgtk_development/data/Q28885102/pharma_triple.ttl.gz
  ```

  This example command takes in a parameter **create_new**. Set this parameter to **True** only if you want to create a new docker container with the default ports. Also, pass the path of the gzipped ttl file to the **ttl_path** parameter.

* If you want to run it in the third mode where the triples are first generated and then loaded to the Blazegraph, then set the **both_gen_and_load_triples** to be **True**.

  ```bash
  papermill combined_pipeline.ipynb combined_pipeline_op.ipynb -p both_gen_and_load_triples True -p create_new True
  ```

   

**Note:**

* Before running the notebook make sure that your Docker Daemon is running. If you don't have a docker installed on your system. Install it from [here](https://docs.docker.com/get-docker/)
* If you are loading a small subgraph on your local laptop, then the default blazegraph image would work fine. But if you are loading a large subgraph on a server, set the **blazegraph_image** parameter in the papermill command to **rijboy/blazegraph-load**



**Stop a docker container**

To stop the containers running using the default paramters, you could simply run:

```bash
python stop_docker.py
```

