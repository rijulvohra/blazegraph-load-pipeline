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

![default parameters](./documentation_images/generate_triples_parameter.jpeg)



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

* Before running the notebook make sure that your Docker Daemon is running.
* If you are loading a small subgraph on your local laptop, then the default blazegraph image would work fine. But if you are loading a large subgraph on a server, set the **blazegraph_image** parameter in the papermill command to **rijboy/blazegraph-load**



**Stop a docker container**

To stop the containers running using the default paramters, you could simply run:

```bash
python stop_docker.py
```

