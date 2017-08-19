# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNATransformers


class CottageTransformer(object):
    colors = {'1': (1, 1, 1, 1),
     '2': (0.9, 0.9, 0.9, 1),
     '3': (0.8, 0.8, 0.8, 1),
     '4': (0.7, 0.7, 0.7, 1),
     '5': (0.6, 0.6, 0.6, 1),
     '6': (0.5, 0.5, 0.5, 1)}

    def apply(self, nodePath, name):
        number = name[2]
        if number in self.colors:
            nodePath.find('**/rooftop').setColorScale(*self.colors[number])


class BRPondTransformer(object):

    def apply(self, nodePath, name):
        nodePath.find('**/collision_BRpd_floor').setTag('footstepCode', 'snow')


class BrrrghTransformer(object):

    def apply(self, nodePath, name):
        for path in nodePath.findAllMatches('**/+CollisionNode'):
            if 'snow' in path.getName():
                path.setTag('footstepCode', 'snow')


class SnowmanTransformer(object):

    def apply(self, nodePath, name):
        nodePath.find('**/floor').setTag('footstepCode', 'snow')


class SnowpileTransformer(object):

    def apply(self, nodePath, name):
        nodePath.find('**/+CollisionNode').setTag('footstepCode', 'snow')


snowpileTransformer = SnowpileTransformer()
AllTransformers = {'tt_cottage': CottageTransformer(),
 'street_BR_pond': BRPondTransformer(),
 'the_burrrgh': BrrrghTransformer(),
 'prop_snowman': SnowmanTransformer(),
 'prop_snow_pile_full': snowpileTransformer,
 'prop_snow_pile_half': snowpileTransformer,
 'prop_snow_pile_quarter': snowpileTransformer}