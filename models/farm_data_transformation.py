'''This module manages the farm data transformation on ETL process e.g. clean, apply business rules, check for data integrity, and create aggregates.'''

import math
from pandas import DataFrame
from sqlalchemy.orm import Session

from database import crud, models
from helpers.misc import AppSettings, DataFormatter, ResponseFormatter
from models.carbon_sequestration import TreeCarbonSequestration, PlantationCarbonSequestration


class FarmData:
    '''Farm Data class.'''

    def retrieve_farms(db: Session, settings: AppSettings) -> list:
        '''Retrive all farms from the database.'''

        # extract
        farm = DataFormatter.class_to_dict_list(
            lst=crud.get_table(
                db=db,
                table=models.FarmsTable
            )
        )

        ha = DataFormatter.class_to_dict_list(
            lst=crud.get_table(
                db=db,
                table=models.PricingTable
            )
        )

        # transform
        data = FarmData.add_tree_co2(data=farm, settings=settings)
        data = FarmData.groupby_farm_id(data=data)
        data = FarmData.add_scientific_name(data=data)
        data = FarmData.add_farm_radius(data=data, settings=settings)
        data = FarmData.add_farm_co2(data=data, settings=settings)
        data = FarmData.add_trees_planted(data=data)
        data = FarmData.add_hectare_price(data=data, ha=ha)
        data = FarmData.response_format(data=data)

        # TODO: this data must come from the source partners, remove it after it
        for d in data:
            if d['groupScheme'] == 'Sri Trang Thailand':
                d['isFscCertified'] = True
            else:
                d['isFscCertified'] = False

        return data

    def add_farm_co2(data: list, settings: AppSettings) -> list:
        '''Add carbon sequestration per year and per day - FarmCO2y to list of objects.'''

        for d in data:
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
        for d in data:
            d['FarmRadius'] = math.sqrt((d['FarmSize']*hectare)/math.pi)

        return data

    def add_hectare_price(data: list, ha: list) -> list:
        '''Add farm hectare price.'''
        ha = FarmData.map_hectare_price(data=ha)
        for d in data:
            d['hectareUsd'] = ha[d['GroupScheme']]
        return data

    def add_scientific_name(data: list) -> list:
        '''Add tree scientific name (genus + species).'''
        for d in data:
            d['ScientificName'] = sorted(list({f'{i} {j}' for i, j in zip(d['GenusName'], d['SpeciesName'])}))
        return data

    def add_tree_co2(data: list, settings: AppSettings) -> list:
        '''Add carbon sequestration - PlantCO2 (key) to list of objects.'''
        tree_co2 = FarmData.calc_tree_co2(settings=settings)

        df = DataFrame(data)
        df = FarmData.remove_hybrids(data=df)
        df['PlantCO2'] = df['SpeciesName'].map(tree_co2)

        return df.to_dict('records')

    def add_trees_planted(data: list) -> list:
        '''Add estimated number of trees planted.'''
        for d in data:
            d['TreesPlanted'] = int(d['SphaSurvival']*d['EffectiveArea'])
        return data

    def calc_tree_co2(settings: AppSettings) -> dict:
        '''Calculate the carbon sequestration (pounds) based on tree characteristics.'''

        metrics = settings.PLANTATION_METRICS.plantationMetrics
        for tree in metrics:
            co2_seq = TreeCarbonSequestration.tree_carbon_sequestration(tree=tree, settings=settings)
            tree.update({'carbonSequestration': {tree['speciesName']: co2_seq}})
        metrics = [d['carbonSequestration'] for d in metrics]

        tree_co2 = {}
        for d in metrics:
            tree_co2.update(d)

        return tree_co2

    def map_hectare_price(data: list) -> dict:
        '''Fetch hectare price by Group Scheme.'''
        price = {}
        for d in data:
            price[d['groupScheme']] = d['hectareUsd']
        return price

    def groupby_farm_id(data: list) -> list:
        '''Group by farm id numbers.'''

        df = DataFrame(data)
        dfg = df[df['IsActive']].groupby(['GroupScheme', 'Country', 'Province', 'FarmId', 'Latitude', 'Longitude', 'FarmSize', 'IsActive']).agg({
            'UnitNumber': 'count',
            'EffectiveArea': 'sum',
            'SphaSurvival': 'mean',
            'PlantCO2': 'mean',
            'PlantAge': 'mean',
            'ProductGroup': list,
            'GenusName': list,
            'SpeciesName': list
        }).reset_index(drop=False)

        # remove duplicates
        dfg = FarmData.remove_duplicates(data=dfg, col='ProductGroup').sort_values(by=['GroupScheme', 'FarmSize'], ascending=[True, False])
        dfg = dfg.drop_duplicates(subset=['Latitude', 'Longitude'], keep='first')

        return dfg.to_dict('records')

    def remove_duplicates(data: DataFrame, col: str) -> DataFrame:
        '''Remove duplicates from values (list) of a given column.'''
        data[col] = data.apply(lambda x: sorted(list(set(x[col]))), axis=1)  # pylint: disable=[E1137]
        return data

    def remove_hybrids(data: DataFrame) -> DataFrame:
        '''Remove hybrid trees.'''
        return data[(data['SpeciesName'] != 'clones') & (data['SpeciesName'] != 'GxN')]

    def response_format(data: list) -> list:
        '''Format farm data keys and values.'''

        farm = data.copy()

        # keys
        farm = ResponseFormatter.obj_list_case_converter(data=farm, fmt='camel')
        # values
        farm = ResponseFormatter.obj_list_strip_string(data=farm)

        return farm
