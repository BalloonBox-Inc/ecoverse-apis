'''This module finds the appopriate metrics based on a given tree from the following:
./docs/json/plantation_metrics.json'''

from helpers.misc import AppSettings, DataAggregator, UnitMeasureConversion


class PlantationMetrics:
    '''Plantation Metrics class.'''

    def tree(data: dict, metrics: list) -> list:
        '''Returns a tree data specifations.'''
        try:
            genus = data['GenusName'].strip().lower()
            species = data['SpeciesName'].strip().lower()
            return [d for d in metrics if d['genusName'] == genus and d['speciesName'] == species][0]
        except (AttributeError, IndexError, KeyError):
            return []

    def tree_height(tree: dict, settings: AppSettings):
        '''Returns a tree height in a standard metric.'''
        return UnitMeasureConversion.length(
            value=DataAggregator.list_mean(tree['height']['measure']),
            unit_in=tree['height']['unit'],
            unit_out='ft',
            settings=settings
        )

    def tree_diameter(tree: dict, settings: AppSettings):
        '''Returns a tree diameter in a standard metric.'''
        return UnitMeasureConversion.length(
            value=DataAggregator.list_mean(
                tree['diameterBreastHeight']['measure']),
            unit_in=tree['diameterBreastHeight']['unit'],
            unit_out='in',
            settings=settings
        )
