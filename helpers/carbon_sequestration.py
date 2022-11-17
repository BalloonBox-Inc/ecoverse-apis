'''This module calculates carbon sequestration based on the following:
https://www.unm.edu/~jbrink/365/Documents/Calculating_tree_carbon.pdf'''

from config import Settings


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

    def tree_carbon_dioxide_sequestered(carbon_weight: float, settings: Settings) -> float:
        '''
        Determines the weight of carbon dioxide sequestered by a tree.

            :param carbon_weight: Tree carbon weight in pounds.

            :returns [float]: Tree CO2 sequestered in pounds.
        '''
        carbon = settings.ATOMIC_WEIGHT.carbon
        carbon_dioxide = settings.ATOMIC_WEIGHT.carbonDioxide
        co2_carbon_ratio = carbon_dioxide/carbon
        return carbon_weight*co2_carbon_ratio

    def forest_carbon_dioxide_sequestered(co2: float, spha: float, settings: Settings) -> float:
        '''
        Determines the weight of carbon dioxide sequestered by a forest.
        Assume the trees were planted at the same time and grew equally, i.e. the forest trees have the same age and size.

            :param co2: Tree CO2 sequestered in pounds.
            :param spha: The number of stems per hectare.

            :returns [float]: Forest CO2 sequestered in tons per hectare.
        '''
        ton = settings.UNIT_CONVERSION.weight.tonLb
        return co2*spha/ton
