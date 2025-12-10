# BioBB LSVS Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Smina_run
Wrapper of the smina molecular docking software.
### Get help
Command:
```python
smina_run -h
```
    usage: smina_run [-h] [-c CONFIG] --input_ligands_sdf_path INPUT_LIGANDS_SDF_PATH --input_receptor_pdbqt_path INPUT_RECEPTOR_PDBQT_PATH --input_site_coords_path INPUT_SITE_COORDS_PATH --output_sdf_path OUTPUT_SDF_PATH [--output_log_path OUTPUT_LOG_PATH]
    
    Prepares input ligand for an smina Virtual Screening.
    
    options:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
      --output_log_path OUTPUT_LOG_PATH
                            Path to the log file. Accepted formats: log.
    
    required arguments:
      --input_ligands_sdf_path INPUT_LIGANDS_SDF_PATH
                            Path to the input SDF ligands. Accepted formats: sdf.
      --input_receptor_pdbqt_path INPUT_RECEPTOR_PDBQT_PATH
                            Path to the input PDBQT receptor. Accepted formats: pdbqt.
      --input_site_coords_path INPUT_SITE_COORDS_PATH
                            Path to the yaml-file containing the binding site size and coordinates. Accepted formats: yml.
      --output_sdf_path OUTPUT_SDF_PATH
                            Path to the output SDF file. Accepted formats: sdf.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_ligands_sdf_path** (*string*): Path to the input SDF ligands. File type: input. [Sample file](https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/data/smina/smina_ligands.sdf). Accepted formats: SDF
* **input_receptor_pdbqt_path** (*string*): Path to the input PDBQT receptor. File type: input. [Sample file](https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/data/smina/smina_receptor.pdbqt). Accepted formats: PDBQT
* **input_site_coords_path** (*string*): Path to the yaml-file containing the binding site size and coordinates. File type: input. [Sample file](https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/data/smina/smina_site_coords.yml). Accepted formats: YML
* **output_sdf_path** (*string*): Path to the output SDF file. File type: output. [Sample file](https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/reference/smina/ref_output_smina.sdf). Accepted formats: SDF
* **output_log_path** (*string*): Path to the log file. File type: output. [Sample file](https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/reference/smina/ref_output_smina.log). Accepted formats: LOG
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **cpu** (*integer*): (1) the number of CPUs to use..
* **exhaustiveness** (*integer*): (8) exhaustiveness of the global search (roughly proportional to time)..
* **num_modes** (*integer*): (9) maximum number of binding modes to generate..
* **min_rmsd_filter** (*integer*): (1) minimum RMSD between output poses..
* **energy_range** (*integer*): (3) maximum energy difference between the best binding mode and the worst one displayed (kcal/mol)..
* **binary_path** (*string*): (smina) path to smina in your local computer..
* **scoring** (*string*): (vinardo) scoring function to be used..
* **seed** (*integer*): (1234) random number generator seed..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
* **sandbox_path** (*string*): (./) Parent path to the sandbox directory..
* **container_path** (*string*): (None) Container path definition..
* **container_image** (*string*): (biocontainers/smina:v1.1.2-5b1-deb_cv1) Container image definition..
* **container_volume_path** (*string*): (/tmp) Container volume path definition..
* **container_working_dir** (*string*): (None) Container working directory definition..
* **container_user_id** (*string*): (None) Container user_id definition..
* **container_shell_path** (*string*): (/bin/bash) Path to default shell inside the container..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_lsvs/blob/master/biobb_lsvs/test/data/config/config_smina_run.yml)
```python
properties:
  check_extensions: true
  cpu: 2
  exhaustiveness: 2
  num_modes: 1
  remove_tmp: true

```
#### [Docker config file](https://github.com/bioexcel/biobb_lsvs/blob/master/biobb_lsvs/test/data/config/config_smina_run_docker.yml)
```python
properties:
  container_image: biocontainers/smina:v1.1.2-5b1-deb_cv1
  container_path: docker
  container_user_id: '1001'
  container_volume_path: /tmp

```
#### Command line
```python
smina_run --config config_smina_run.yml --input_ligands_sdf_path smina_ligands.sdf --input_receptor_pdbqt_path smina_receptor.pdbqt --input_site_coords_path smina_site_coords.yml --output_sdf_path ref_output_smina.sdf --output_log_path ref_output_smina.log
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_lsvs/blob/master/biobb_lsvs/test/data/config/config_smina_run.json)
```python
{
  "properties": {
    "cpu": 2,
    "exhaustiveness": 2,
    "num_modes": 1,
    "check_extensions": true,
    "remove_tmp": true
  }
}
```
#### [Docker config file](https://github.com/bioexcel/biobb_lsvs/blob/master/biobb_lsvs/test/data/config/config_smina_run_docker.json)
```python
{
  "properties": {
    "container_path": "docker",
    "container_image": "biocontainers/smina:v1.1.2-5b1-deb_cv1",
    "container_volume_path": "/tmp",
    "container_user_id": "1001"
  }
}
```
#### Command line
```python
smina_run --config config_smina_run.json --input_ligands_sdf_path smina_ligands.sdf --input_receptor_pdbqt_path smina_receptor.pdbqt --input_site_coords_path smina_site_coords.yml --output_sdf_path ref_output_smina.sdf --output_log_path ref_output_smina.log
```
