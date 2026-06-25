
__author__ = ["POD/LCA Team"]
__copyright__ = "University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


def run_operational(building,
                    operational_method='eplus',
                    eplus_path=None,
                    eplus_output_path=None,
                    idf_path=None,
                    weather_file_path=None,
                    ):
    

    if eplus_path:
        building.set_eplus_path(eplus_path)
    if eplus_output_path:
        building.set_eplus_out_folder(eplus_output_path)
    if idf_path:
        building.set_idf_file_path(idf_path)
    if weather_file_path:
        building.set_weather_file_path(weather_file_path)
    
    building.operational_energy_method = operational_method

    print(building.get_operational_impacts())
    # return operational_impacts
