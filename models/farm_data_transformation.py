'''This module manages the farm data transformation on ETL process e.g. clean, apply business rules, check for data integrity, and create aggregates.'''

import math
import pandas as pd

from helpers.misc import AppSettings, ResponseFormatter
from models.carbon_sequestration import CarbonSequestration
from models.plantation_metrics import PlantationMetrics


class FarmData:
    '''Farm Data class.'''

    def groupby_farm_id(data: list) -> list:
        '''Group by farms by their farm ID.'''

        df = pd.DataFrame(data)
        dfg = df.groupby([
            'FarmId', 'Latitude', 'Longitude', 'Province', 'FarmSize', 'GroupScheme', 'ProductGroup', 'GenusName', 'SpeciesName'
        ]).agg({
            'UnitNumber': 'count',
            'EffectiveArea': 'sum',
            'PlantAge': 'mean',
            'SphaSurvival': 'sum'  # TODO: review
        })
        dfg.reset_index(drop=False, inplace=True)

        return dfg.to_dict('records')

    def calc_radius(data: list, settings: AppSettings) -> list:
        '''Calculate the farm radius based on its area size.'''

        hectare = settings.UNIT_CONVERSION.area.haM2
        for d in data:  # pylint: disable=[E1133]
            d['FarmRadius'] = math.sqrt((d['FarmSize']*hectare)/math.pi)

        return data

    def calc_co2(data: list, settings: AppSettings):
        '''Calculate the farm carbon sequestration based on its plantation characteristics.'''

        metrics = settings.PLANTATION_METRICS.plantationMetrics
        for d in data:  # pylint: disable=[E1133]
            spha = d['SphaSurvival']
            genus = d['GenusName']
            species = d['SpeciesName']

            if not spha:
                spha = 1  # TODO: update spha

            if not isinstance(genus, list):
                tree = PlantationMetrics.tree(data=d, metrics=metrics)
                co2 = CarbonSequestration.tons_per_hectare_per_year(tree=tree, spha=spha*0.9, age=d['PlantAge'], settings=settings)
            else:
                co2 = 0
                temp = d.copy()
                for gene, spec in zip(genus, species):
                    temp['GenusName'] = gene
                    temp['SpeciesName'] = spec
                    tree = PlantationMetrics.tree(data=temp, metrics=metrics)
                    co2 += CarbonSequestration.tons_per_hectare_per_year(tree=tree, spha=spha, age=d['PlantAge'], settings=settings)
                co2 = co2/len(genus)

            d['CarbonSequesteredPerYear'] = co2
            d['CarbonSequesteredPerDay'] = co2/365

        return data

    def format(data: list) -> list:
        '''Format farm data keys and values.'''

        farm = data.copy()

        # keys
        farm = ResponseFormatter.obj_list_to_camel_case(data=farm)
        # values
        farm = ResponseFormatter.obj_list_strip_string(data=farm)

        return farm
