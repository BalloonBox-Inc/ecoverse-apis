'''This module manages the farm data transformation on ETL process e.g. clean, apply business rules, check for data integrity, and create aggregates.'''

import math
from pandas import DataFrame

from helpers.misc import AppSettings, ResponseFormatter
from models.carbon_sequestration import TreeCarbonSequestration, PlantationCarbonSequestration


class FarmData:
    '''Farm Data class.'''

    def add_trees_planted(data: list) -> list:
        '''Add estimated number of trees planted.'''
        for d in data:
            d['TreesPlanted'] = int(d['SphaSurvival']*d['EffectiveArea'])
        return data

    def add_farm_co2(data: list, settings: AppSettings) -> list:
        '''Add carbon sequestration per year and per day - FarmCO2y to list of objects.'''

        for d in data:  # pylint: disable=[E1133]
            co2 = PlantationCarbonSequestration.plantation_carbon_sequestration(
                co2=d['PlantCO2'],
                spha=d['SphaSurvival']*0.9,
                age=d['PlantAge'],
                settings=settings
            )
            d['FarmCO2y'] = co2

        return data

    def add_farm_radius(data: list, settings: AppSettings) -> list:
        '''Add farm radius to list of objects based on its area size.'''

        hectare = settings.UNIT_CONVERSION.area.haM2
        for d in data:  # pylint: disable=[E1133]
            d['FarmRadius'] = math.sqrt((d['FarmSize']*hectare)/math.pi)

        return data

    def add_tree_co2(data: list, settings: AppSettings) -> list:
        '''Add carbon sequestration - PlantCO2 (key) to list of objects.'''
        tree_co2 = FarmData.calc_tree_co2(settings=settings)

        df = DataFrame(data)
        df = FarmData.remove_hybrids(data=df)
        df['PlantCO2'] = df['SpeciesName'].map(tree_co2)

        return df.to_dict('records')

    def calc_tree_co2(settings: AppSettings) -> dict:
        '''Calculate the carbon sequestration based on tree characteristics.'''

        metrics = settings.PLANTATION_METRICS.plantationMetrics
        for tree in metrics:
            co2_seq = TreeCarbonSequestration.tree_carbon_sequestration(tree=tree, settings=settings)
            tree.update({'carbonSequestration': {tree['speciesName']: co2_seq}})
        metrics = [d['carbonSequestration'] for d in metrics]

        tree_co2 = {}
        for d in metrics:
            tree_co2.update(d)

        return tree_co2

    def groupby_farm_id(data: list) -> list:
        '''Group by farm id numbers.'''

        df = DataFrame(data)
        dfg = df.groupby(['FarmId', 'Latitude', 'Longitude', 'Province', 'FarmSize', 'GroupScheme']).agg({
            'UnitNumber': 'count',
            'ProductGroup': 'count',  # TODO: it must be unique count
            'EffectiveArea': 'mean',  # TODO: review
            'PlantCO2': 'mean',  # TODO: review
            'PlantAge': 'mean',  # TODO: review
            'SphaSurvival': 'mean'  # TODO: review
            # TODO: add products list
        })
        dfg.reset_index(drop=False, inplace=True)

        return dfg.to_dict('records')

    def groupby_farm_unit(data: list) -> list:
        '''Group by farm unit numbers.'''

        df = DataFrame(data)
        dfg = df.groupby(['FarmId', 'Latitude', 'Longitude', 'Province', 'FarmSize', 'GroupScheme', 'UnitNumber', 'ProductGroup']).agg({
            'SpeciesName': 'count',
            'EffectiveArea': 'mean',
            'PlantCO2': 'mean',
            'PlantAge': 'mean',
            'SphaSurvival': 'sum'  # TODO: review
            # TODO: add genus and species name
        })
        dfg.reset_index(drop=False, inplace=True)

        # dfg = DataFormatter.column_string_to_list(data=dfg, column='SpeciesName', sep=',')

        return dfg.to_dict('records')

    def remove_hybrids(data: DataFrame) -> DataFrame:
        '''Remove hybrid trees.'''
        return data[(data['SpeciesName'] != 'clones') & (data['SpeciesName'] != 'GxN')]

    def response_format(data: list) -> list:
        '''Format farm data keys and values.'''

        farm = data.copy()

        # keys
        farm = ResponseFormatter.obj_list_to_camel_case(data=farm)
        # values
        farm = ResponseFormatter.obj_list_strip_string(data=farm)

        return farm
