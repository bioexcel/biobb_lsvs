#!/usr/bin/env python3

"""Module containing the sminaRun class and the command line interface."""

import argparse
import os
import yaml
from typing import Optional
from random import randint

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger

from biobb_lsvs.smina.common import check_input_path, check_output_path


class sminaRun(BiobbObject):
    """
    | biobb_lsvs sminaRun
    | Wrapper of the smina molecular docking software.
    | This class performs docking of ligands to a predefined site on a target protein via the `smina <https://sourceforge.net/projects/smina/>`_ software.

    Args:
        input_ligands_sdf_path (str): Path to the input SDF ligands. File type: input. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/data/smina/smina_ligands.sdf>`_. Accepted formats: sdf (edam:format_3814).
        input_receptor_pdbqt_path (str): Path to the input PDBQT receptor. File type: input. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/data/smina/smina_receptor.pdbqt>`_. Accepted formats: pdbqt (edam:format_1476).
        input_site_coords_path (str): Path to the yaml-file containing the binding site size and coordinates. File type: input. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/data/smina/smina_box.pdb>`_. Accepted formats: yml (edam:format_1476).
        output_sdf_path (str): Path to the output SDF file. File type: output. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/reference/smina/ref_output_smina.pdbqt>`_. Accepted formats: sdf (edam:format_1476).
        output_log_path (str) (Optional): Path to the log file. File type: output. `Sample file <https://github.com/bioexcel/biobb_lsvs/raw/master/biobb_lsvs/test/reference/smina/ref_output_smina.log>`_. Accepted formats: log (edam:format_2330).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **cpu** (*int*) - (1) [1~1000|1] the number of CPUs to use.
            * **exhaustiveness** (*int*) - (8) [1~10000|1] exhaustiveness of the global search (roughly proportional to time).
            * **num_modes** (*int*) - (9) [1~1000|1] maximum number of binding modes to generate.
            * **min_rmsd_filter** (*int*) - (1) [1~1000|1] minimum RMSD between output poses.
            * **energy_range** (*int*) - (3) [1~1000|1] maximum energy difference between the best binding mode and the worst one displayed (kcal/mol).
            * **binary_path** (*string*) - ('smina') path to smina in your local computer.
            * **scoring** (*string*) - ('vinardo') scoring function to be used.
            * **seed** (*int*) - ('random') [-9999999-9999999] random number generator seed. 
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
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {
                "input_ligands_sdf_path": input_ligands_sdf_path,
                "input_receptor_pdbqt_path": input_receptor_pdbqt_path,
                "input_site_coords_path": input_site_coords_path
            },
            "out": {
                "output_sdf_path": output_sdf_path,
                "output_log_path": output_log_path,
            },
        }
        rand_seed = randint(-9999999,9999999)
        # Parse box centroid and dimensions from input_site_coords YAML
        self.coords = self.parse_site_coords()

        # Properties specific for BB
        self.cpu = properties.get("cpu", 1)
        self.exhaustiveness = properties.get("exhaustiveness", 8)
        self.num_modes = properties.get("num_modes", 9)
        self.scoring = properties.get("scoring", "vina")
        self.seed = properties.get("seed", rand_seed)
        self.min_rmsd_filter = properties.get("min_rmsd_filter", 1)
        self.energy_range = properties.get("energy_range", 3)
        self.binary_path = properties.get("binary_path", "smina")
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def check_data_params(self, out_log, err_log):
        """Checks all the input/output paths and parameters"""
        self.io_dict["in"]["input_ligands_sdf_path"] = check_input_path(
            self.io_dict["in"]["input_ligands_sdf_path"],
            "input_ligands_sdf_path",
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["in"]["input_receptor_pdbqt_path"] = check_input_path(
            self.io_dict["in"]["input_receptor_pdbqt_path"],
            "input_receptor_pdbqt_path",
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["in"]["input_site_coords_path"] = check_input_path(
            self.io_dict["in"]["input_site_coords_path"],
            "input_site_coords_path",
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["out"]["output_sdf_path"] = check_output_path(
            self.io_dict["out"]["output_sdf_path"],
            "output_sdf_path",
            False,
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["out"]["output_log_path"] = check_output_path(
            self.io_dict["out"]["output_log_path"],
            "output_log_path",
            True,
            self.out_log,
            self.__class__.__name__,
        )

    def parse_site_coords(self):
        """Parse box centroid and side lengths from site_coord.yml"""
        with open(self.io_dict["in"]["input_site_coords_path"], 'r') as sc:
            coords = yaml.safe_load(sc)
        return coords
    
    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`sminaRun_run <smina.smina_run.sminaRun_run>` smina.smina_run.sminaRun_run object."""

        # check input/output paths and parameters
        self.check_data_params(self.out_log, self.err_log)

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

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
            ">",
            self.stage_io_dict["out"]["output_log_path"],
        ]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # remove temporary folder(s)
        # self.tmp_files.extend([self.stage_io_dict.get("unique_dir", "")])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def smina_run(
    input_ligands_sdf_path: str,
    input_receptor_pdbqt_path: str,
    input_site_coords_path: str,
    output_sdf_path: str,
    output_log_path: Optional[str] = None,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`sminaRun <smina.smina_run.sminaRun>` class and
    execute the :meth:`launch() <smina.smina_run.sminaRun.launch>` method."""

    return sminaRun(
        input_ligands_sdf_path=input_ligands_sdf_path,
        input_receptor_pdbqt_path=input_receptor_pdbqt_path,
        input_site_coords_path=input_site_coords_path,
        output_sdf_path=output_sdf_path,
        output_log_path=output_log_path,
        properties=properties,
        **kwargs,
    ).launch()

    smina_run.__doc__ = sminaRun.__doc__


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Prepares input ligand for an smina Virtual Screening.",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )
    parser.add_argument("--config", required=False, help="Configuration file")

    # Specific args of each building block
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "--input_ligands_sdf_path",
        required=True,
        help="Path to the input SDF ligands. Accepted formats: sdf.",
    )
    required_args.add_argument(
        "--input_receptor_pdbqt_path",
        required=True,
        help="Path to the input PDBQT receptor. Accepted formats: pdbqt.",
    )
    required_args.add_argument(
        "--input_site_coords_path",
        required=True,
        help="Path to the smina box coordinates file. Accepted formats: yaml, yml.",
    )
    required_args.add_argument(
        "--output_sdf_path",
        required=True,
        help="Path to the output SDF file. Accepted formats: sdf.",
    )
    parser.add_argument(
        "--output_log_path",
        required=False,
        help="Path to the log file. Accepted formats: log.",
    )

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call of each building block
    smina_run(
        input_ligands_sdf_path=args.input_ligands_sdf_path,
        input_receptor_pdbqt_path=args.input_receptor_pdbqt_path,
        input_site_coords_path=args.input_site_coords_path,
        output_sdf_path=args.output_sdf_path,
        output_log_path=args.output_log_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
