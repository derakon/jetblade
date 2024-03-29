zones = {
    'jungle' : {
        'elevationRange' : [0, .5],
        'regions' : {
            'grass' : {
                'frequency' : 1,
                'color' : (0, 255, 0),
                'tunnelTypes' : {
                    'wave' : 16,
                    'bumpy' : 16,
                    'room' : 6,
                    'straight' : 4,
                },
                'environments' : {
                    'water' : 1,
                    None: 1,
                },
                'tunnelWidths' : range(8, 14),
                'tunnelLengths' : range(25, 56),
                'furnitureFrequency' : 4,
            },
            'cave' : {
                'base': 'grass',
                'color': (0, 0, 128),
            },
            'mossycave': {
                'base': 'grass',
                'color': (64, 128, 64),
            },
        },
    },
    'hotzone' : {
        'elevationRange' : [.5, 1],
        'regions' : {
            'lava' : {
                'frequency' : 2,
                'color' : (255, 0, 0),
                'tunnelTypes' : {
                    'wave' : 8,
                    'bumpy' : 8,
                    'room' : 2,
                    'straight' : 2,
#                    'maze' : 1,
                },
                'tunnelWidths' : range(8, 13),
                'tunnelLengths' : range(20, 41),
                'furnitureFrequency' : 8,
            },
            'techpipe' : {
                'frequency' : 1,
                'color' : (128, 128, 128),
                'aligned' : 1,
                'tunnelTypes' : {
                    'straight' : 4,
#                    'maze' : 1,
                    'room' : 2,
                    'pit' : 4,
                },
                'tunnelWidths' : [8],
                'tunnelLengths' : range(20, 51, 5),
                'furnitureFrequency' : 8,
            },
        },
    },
#    'surface' : {
#        'elevationRange' : [0, .2]
#    },
#    'ocean' : {
#        'elevationRange': [.1, .7]
#    },
#    'ice' : {
#        'elevationRange': [0, .4]
#    },
#    'hell' : {
#        'elevationRange' : [.9, 1]
#    },
}
