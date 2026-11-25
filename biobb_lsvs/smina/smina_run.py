#!/usr/bin/env python3

"""Module containing the sminaRun class and the command line interface."""

import yaml
from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject


class SminaRun(BiobbObject):
    """
    | biobb_lsvs SminaRun
    | Wrapper of the smina molecular docking software.
    | This class performs docking of ligands to a predefined site on a target protein via the `smina <https://sourceforge.net/projects/smina/>`_ software.

    Args:
        input_ligands_sdf_path (str): Path to the input SDF ligands. File type: input. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/data/smina/smina_ligands.sdf>`_. Accepted formats: sdf (edam:format_3814).
        input_receptor_pdbqt_path (str): Path to the input PDBQT receptor. File type: input. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/data/smina/smina_receptor.pdbqt>`_. Accepted formats: pdbqt (edam:format_1476).
        input_site_coords_path (str): Path to the yaml-file containing the binding site size and coordinates. File type: input. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/data/smina/smina_site_coords.yml>`_. Accepted formats: yml (edam:format_3750), yaml (edam:format_3750).
        output_sdf_path (str): Path to the output SDF file. File type: output. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/reference/smina/ref_output_smina.sdf>`_. Accepted formats: sdf (edam:format_3814).
        output_log_path (str) (Optional): Path to the log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/reference/smina/ref_output_smina.log>`_. Accepted formats: log (edam:format_2330).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **cpu** (*int*) - (1) [1~1000|1] the number of CPUs to use.
            * **exhaustiveness** (*int*) - (8) [1~10000|1] exhaustiveness of the global search (roughly proportional to time).
            * **num_modes** (*int*) - (9) [1~1000|1] maximum number of binding modes to generate.
            * **min_rmsd_filter** (*int*) - (1) [1~1000|1] minimum RMSD between output poses.
            * **energy_range** (*int*) - (3) [1~1000|1] maximum energy difference between the best binding mode and the worst one displayed (kcal/mol).
            * **binary_path** (*string*) - ('smina') path to smina in your local computer.
            * **scoring** (*string*) - ('vina') scoring function to be used.
            * **seed** (*int*) - (1234) [-9999999-9999999] random number generator seed.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.
            * **container_path** (*str*) - (None) Container path definition.
            * **container_image** (*str*) - ('biocontainers/smina:v1.1.2-5b1-deb_cv1') Container image definition.
            * **container_volume_path** (*str*) - ('/tmp') Container volume path definition.
            * **container_working_dir** (*str*) - (None) Container working directory definition.
            * **container_user_id** (*str*) - (None) Container user_id definition.
            * **container_shell_path** (*str*) - ('/bin/bash') Path to default shell inside the container.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_lsvs.smina.smina_run import smina_run
            prop = {
                'binary_path': 'smina'
            }
            smina_run(input_ligands_sdf_path='/path/to/myLigands.sdf',
                            input_receptor_pdbqt_path='/path/to/myReceptor.pdbqt',
                            input_site_coords_path='/path/to/mySiteCoords.yml',
                            output_sdf_path='/path/to/newStructure.sdf',
                            output_log_path='/path/to/newLog.log',
                            properties=prop)

    Info:
        * wrapped_software:
            * name: smina
            * version: >=October 15, 2019
            * license: GNU GPL v2
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self,
        input_ligands_sdf_path,
        input_receptor_pdbqt_path,
        input_site_coords_path,
        output_sdf_path,
        output_log_path=None,
        properties=None,
        **kwargs,
    ) -> None:
        super().__init__(**locals())

        # Parse box centroid and dimensions from input_site_coords YAML
        self.coords = self.parse_site_coords()

    def parse_site_coords(self):
        """Parse box centroid position and side lengths from site_coord.yml"""
        with open(self.io_dict["in"]["input_site_coords_path"], 'r') as sc:
            coords = yaml.safe_load(sc)
        return coords

    def run(self) -> None:
        """Execute the :class:`sminaRun_run <smina.smina_run.sminaRun_run>` smina.smina_run.sminaRun_run object."""

        # create cmd
        self.cmd = [
            self.binary_path,
            "--ligand",
            self.stage_io_dict["in"]["input_ligands_sdf_path"],
            "--receptor",
            self.stage_io_dict["in"]["input_receptor_pdbqt_path"],
            "--cpu",
            str(self.cpu),
            "--exhaustiveness",
            str(self.exhaustiveness),
            "--num_modes",
            str(self.num_modes),
            "--center_x",
            str(self.coords["centroid"]["x"]),
            "--center_y",
            str(self.coords["centroid"]["y"]),
            "--center_z",
            str(self.coords["centroid"]["z"]),
            "--size_x",
            str(self.coords["size"]["x"]),
            "--size_y",
            str(self.coords["size"]["y"]),
            "--size_z",
            str(self.coords["size"]["z"]),
            "--scoring",
            str(self.scoring),
            "--seed",
            str(self.seed),
            "--min_rmsd_filter",
            str(self.min_rmsd_filter),
            "--energy_range",
            str(self.energy_range),
            "--out",
            self.stage_io_dict["out"]["output_sdf_path"],
            "--verbosity",
            "1",
        ]
        if self.stage_io_dict["out"].get("output_log_path"):
            self.cmd.extend([">", self.stage_io_dict["out"]["output_log_path"]])

        # Run Biobb block
        self.run_biobb()


def smina_run(
    input_ligands_sdf_path: str,
    input_receptor_pdbqt_path: str,
    input_site_coords_path: str,
    output_sdf_path: str,
    output_log_path: Optional[str] = None,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`SminaRun <smina.smina_run.SminaRun>` class and
    execute the :meth:`launch() <smina.smina_run.SminaRun.launch>` method."""
    return SminaRun(**dict(locals())).launch()


smina_run.__doc__ = SminaRun.__doc__
main = SminaRun.get_main(smina_run, 'Prepares input ligand for an smina Virtual Screening.')

if __name__ == "__main__":
    main()
