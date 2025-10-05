# type: ignore
import pytest
from biobb_common.tools import test_fixtures as fx
from biobb_lsvs.smina.smina_run import smina_run


class TestSminaRunDocker():
    def setup_class(self):
        fx.test_setup(self, 'smina_run_docker')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_smina_run_docker(self):
        smina_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_sdf_path'])
        assert fx.not_empty(self.paths['output_log_path'])


@pytest.mark.skip(reason="singularity currently not available")
class TestSminaRunSingularity():
    def setup_class(self):
        fx.test_setup(self, 'smina_run_singularity')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_smina_run_singularity(self):
        smina_run(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_sdf_path'])
        assert fx.not_empty(self.paths['output_log_path'])
