'''This module calculates carbon sequestration based on the following:
./supporting_data/pdf/carbon_sequestration.pdf'''

from helpers.misc import AppSettings, DataAggregator
from model.plantation_metrics import PlantationMetrics


class CarbonSequestration:
    '''Carbon Sequestration class.'''

    def tree_green_weight(height: float, diameter: float, root: float) -> float:
        '''
        Determines the weight of a tree when it is alive.

            :param height: Trunk height in feet.
            :param diameter: Trunk diameter in inches.
            :param root: Average root weight in percentage.

            :returns [float]: Tree green weight in pounds.
        '''
        if diameter < 11:
            coeff = 0.25
        else:
            coeff = 0.15
        return (coeff*height*diameter**2)*(1+root)

    def tree_dry_weight(green_weight: float, dry_matter: float) -> float:
        '''
        Determines the dry weight of a tree.

            :param green_weight: Tree green weight in pounds.
            :param dry_matter: Average dry matter in percentage.

            :returns [float]: Tree dry weight in pounds.
        '''
        return green_weight*dry_matter

    def tree_carbon_weight(dry_weight: float, carbon_content: float) -> float:
        '''
        Determines the carbon weight of a tree.

            :param dry_weight: Tree dry weight in pounds.
            :param carbon_content: Average carbon content in percentage.

            :returns [float]: Tree carbon weight in pounds.
        '''
        return dry_weight*carbon_content

    def tree_carbon_dioxide_sequestered(carbon_weight: float, settings: AppSettings) -> float:
        '''
        Determines the weight of carbon dioxide sequestered by a tree.

            :param carbon_weight: Tree carbon weight in pounds.

            :returns [float]: Tree CO2 sequestered in pounds.
        '''
        carbon = settings.ATOMIC_WEIGHT.carbon
        carbon_dioxide = settings.ATOMIC_WEIGHT.carbonDioxide
        co2_carbon_ratio = carbon_dioxide/carbon
        return carbon_weight*co2_carbon_ratio

    def plantation_carbon_dioxide_sequestered(co2: float, spha: float, settings: AppSettings) -> float:
        '''
        Determines the weight of carbon dioxide sequestered by a plantation.
        Assume the trees were planted at the same time and grew equally, i.e. the plantation trees have the same age and size.

            :param co2: Tree CO2 sequestered in pounds.
            :param spha: The number of stems per hectare.

            :returns [float]: Plantation CO2 sequestered in tons per hectare.
        '''
        ton = settings.UNIT_CONVERSION.weight.tonLb
        return co2*spha/ton

    def tons_per_hectare_per_year(tree: dict, spha: float, age: float, settings: AppSettings) -> float:
        '''
        Determines the weight of carbon sequestered per hectare per year of a plantation.

            :param tree: Plantation trees data dictionary.
            :param spha: Plantation stems per hectare.
            :param age: Plantation age in years.

            :returns [float]: Plantation CO2 sequestered in tons per hectare per year.
        '''
        height = PlantationMetrics.tree_height(tree=tree, settings=settings)
        diameter = PlantationMetrics.tree_diameter(tree=tree, settings=settings)

        green_weight = CarbonSequestration.tree_green_weight(
            height=height,
            diameter=diameter,
            root=DataAggregator.list_mean(tree['rootDryMass']['measure'])
        )

        dry_weight = CarbonSequestration.tree_dry_weight(
            green_weight=green_weight,
            dry_matter=DataAggregator.list_mean(tree['dryBiomass']['measure'])
        )

        carbon_weight = CarbonSequestration.tree_carbon_weight(
            dry_weight=dry_weight,
            carbon_content=DataAggregator.list_mean(tree['carbonConcentration']['measure'])
        )

        carbon_dioxide_seq = CarbonSequestration.tree_carbon_dioxide_sequestered(
            carbon_weight=carbon_weight,
            settings=settings
        )

        plantation_co2_seq = CarbonSequestration.plantation_carbon_dioxide_sequestered(
            co2=carbon_dioxide_seq,
            spha=spha,
            settings=settings
        )

        return plantation_co2_seq/age
