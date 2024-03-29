POLYHEDRONS = {
    'elongated_pentagonal_rotunda': {
        'vertices': [
            (-0.26010839, -0.80053131, 0.01968437),
            (-0.68097260, -0.49475556, 0.01968437),
            (-0.84172843, 0.00000000, 0.01968437),
            (-0.68097260, 0.49475556, 0.01968437),
            (-0.26010839, 0.80053131, 0.01968437),
            (0.26010839, 0.80053131, 0.01968437),
            (0.68097260, 0.49475556, 0.01968437),
            (0.84172843, 0.00000000, 0.01968437),
            (0.68097260, -0.49475556, 0.01968437),
            (0.26010839, -0.80053131, 0.01968437),
            (0.00000000, -0.71601697, -0.42283845),
            (-0.68097260, -0.22126141, -0.42283845),
            (-0.42086421, 0.57926990, -0.42283845),
            (0.42086421, 0.57926990, -0.42283845),
            (0.68097260, -0.22126141, -0.42283845),
            (-0.26010839, -0.35800848, -0.69633260),
            (-0.42086421, 0.13674707, -0.69633260),
            (0.00000000, 0.44252282, -0.69633260),
            (0.42086421, 0.13674707, -0.69633260),
            (0.26010839, -0.35800848, -0.69633260),
            (-0.26010839, -0.80053131, 0.53990115),
            (0.26010839, -0.80053131, 0.53990115),
            (0.68097260, -0.49475556, 0.53990115),
            (0.84172843, 0.00000000, 0.53990115),
            (0.68097260, 0.49475556, 0.53990115),
            (0.26010839, 0.80053131, 0.53990115),
            (-0.26010839, 0.80053131, 0.53990115),
            (-0.68097260, 0.49475556, 0.53990115),
            (-0.84172843, 0.00000000, 0.53990115),
            (-0.68097260, -0.49475556, 0.53990115),
        ],
        'faces': [
            (0, 1, 11, 15, 10), (0, 10, 9), (0, 9, 21, 20), (0, 20, 29, 1),
            (1, 2, 11), (1, 29, 28, 2), (2, 3, 12, 16, 11), (2, 28, 27, 3),
            (3, 4, 12), (3, 27, 26, 4), (4, 5, 13, 17, 12), (4, 26, 25, 5),
            (5, 6, 13), (5, 25, 24, 6), (6, 7, 14, 18, 13), (6, 24, 23, 7),
            (7, 8, 14), (7, 23, 22, 8), (8, 9, 10, 19, 14), (8, 22, 21, 9),
            (10, 15, 19), (11, 16, 15), (12, 17, 16), (13, 18, 17), (14, 19, 18),
            (15, 16, 17, 18, 19), (20, 21, 22, 23, 24, 25, 26, 27, 28, 29)
        ],
        'color_pattern': [0, 1, 2, 2, 1, 2, 0, 2, 1, 2, 0, 2, 1, 2, 0, 2, 1, 2, 0, 2, 1, 1, 1, 1, 1, 0, 3],
        'normals': [
            None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)]
        ]
    },
    'octagon_prism': {
        'vertices': [
            (-0.35740674, -0.86285621, 0.35740674),
            (-0.86285621, -0.35740674, 0.35740674),
            (-0.86285621, 0.35740674, 0.35740674),
            (-0.35740674, 0.86285621, 0.35740674),
            (0.35740674, 0.86285621, 0.35740674),
            (0.86285621, 0.35740674, 0.35740674),
            (0.86285621, -0.35740674, 0.35740674),
            (0.35740674, -0.86285621, 0.35740674),
            (-0.35740674, -0.86285621, -0.35740674),
            (-0.86285621, -0.35740674, -0.35740674),
            (-0.86285621, 0.35740674, -0.35740674),
            (-0.35740674, 0.86285621, -0.35740674),
            (0.35740674, 0.86285621, -0.35740674),
            (0.86285621, 0.35740674, -0.35740674),
            (0.86285621, -0.35740674, -0.35740674),
            (0.35740674, -0.86285621, -0.35740674)
        ],
        'faces': [
            (0, 1, 9, 8), (0, 8, 15, 7), (0, 7, 6, 5, 4, 3, 2, 1), (1, 2, 10, 9),
            (2, 3, 11, 10), (3, 4, 12, 11), (4, 5, 13, 12), (5, 6, 14, 13),
            (6, 7, 15, 14), (8, 9, 10, 11, 12, 13, 14, 15)
        ],
        'color_pattern': [1, 0, 2, 0, 1, 0, 1, 0, 1, 2],
        'normals': [
            None,
            None,
            [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)],
            None,
            None,
            None,
            None,
            None,
            None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)]
        ]
    },
    'truncated_tetrahedron': {
        'vertices': [
            (-0.42640143, -0.73854895, 0.52223297),
            (-0.85280287, 0.00000000, 0.52223297),
            (-0.42640143, 0.73854895, 0.52223297),
            (0.42640143, 0.73854895, 0.52223297),
            (0.85280287, -0.00000000, 0.52223297),
            (0.42640143, -0.73854895, 0.52223297),
            (-0.85280287, -0.49236596, -0.17407766),
            (0.00000000, 0.98473193, -0.17407766),
            (0.85280287, -0.49236596, -0.17407766),
            (-0.42640143, -0.24618298, -0.87038828),
            (0.00000000, 0.49236596, -0.87038828),
            (0.42640143, -0.24618298, -0.87038828)
        ],
        'faces': [
            (0, 1, 6), (0, 6, 9, 11, 8, 5), (0, 5, 4, 3, 2, 1), (1, 2, 7, 10, 9, 6),
            (2, 3, 7), (3, 4, 8, 11, 10, 7), (4, 5, 8), (9, 10, 11)
        ],
        'color_pattern': [0, 1, 1, 1, 0, 1, 0, 0],
        'normals': [None, None, None, None, None, None, None, None]
    },
    'pentagonal_rotunda': {
        'vertices': [
            (-0.29220218, -0.89930585, 0.32537191),
            (-0.76499524, -0.55580158, 0.32537191),
            (-0.94558612, 0.00000000, 0.32537191),
            (-0.76499524, 0.55580158, 0.32537191),
            (-0.29220218, 0.89930585, 0.32537191),
            (0.29220218, 0.89930585, 0.32537191),
            (0.76499524, 0.55580158, 0.32537191),
            (0.94558612, -0.00000000, 0.32537191),
            (0.76499524, -0.55580158, 0.32537191),
            (0.29220218, -0.89930585, 0.32537191),
            (0.00000000, -0.80436360, -0.17175213),
            (-0.76499524, -0.24856202, -0.17175213),
            (-0.47279306, 0.65074382, -0.17175213),
            (0.47279306, 0.65074382, -0.17175213),
            (0.76499524, -0.24856202, -0.17175213),
            (-0.29220218, -0.40218180, -0.47899169),
            (-0.47279306, 0.15361978, -0.47899169),
            (0.00000000, 0.49712404, -0.47899169),
            (0.47279306, 0.15361978, -0.47899169),
            (0.29220218, -0.40218180, -0.47899169),
        ],
        'faces': [
            (0, 1, 11, 15, 10), (0, 10, 9), (0, 9, 8, 7, 6, 5, 4, 3, 2, 1),
            (1, 2, 11), (2, 3, 12, 16, 11), (3, 4, 12), (4, 5, 13, 17, 12),
            (5, 6, 13), (6, 7, 14, 18, 13), (7, 8, 14), (8, 9, 10, 19, 14),
            (10, 15, 19), (11, 16, 15), (12, 17, 16), (13, 18, 17),
            (14, 19, 18), (15, 16, 17, 18, 19)
        ],
        'color_pattern': [0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
        'normals': [
            None, None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)],
            None, None, None, None, None, None, None, None, None, None, None, None, None, None
        ]
    },
    'augmented_truncated_tetrahedron': {
        'vertices': [
            (-0.35007002, -0.41770024, 0.49544036),
            (-0.70014004, 0.18863882, 0.49544036),
            (-0.35007002, 0.79497788, 0.49544036),
            (0.35007002, 0.79497788, 0.49544036),
            (0.70014004, 0.18863882, 0.49544036),
            (0.35007002, -0.41770024, 0.49544036),
            (-0.70014004, -0.21558722, -0.07622159),
            (0.00000000, 0.99709090, -0.07622159),
            (0.70014004, -0.21558722, -0.07622159),
            (-0.35007002, -0.01347420, -0.64788354),
            (0.00000000, 0.59286486, -0.64788354),
            (0.35007002, -0.01347420, -0.64788354),
            (-0.00000000, -0.88929729, 0.11433239),
            (-0.35007002, -0.68718427, -0.45732956),
            (0.35007002, -0.68718427, -0.45732956)
        ],
        'faces': [
            (0, 5, 4, 3, 2, 1), (0, 1, 6), (0, 6, 13, 12),
            (0, 12, 5), (1, 2, 7, 10, 9, 6), (2, 3, 7),
            (3, 4, 8, 11, 10, 7), (4, 5, 8), (5, 12, 14, 8),
            (6, 9, 13), (8, 14, 11), (9, 10, 11), (9, 11, 14, 13), (12, 13, 14)
        ],
        'color_pattern': [0, 1, 2, 1, 0, 1, 0, 1, 2, 1, 1, 1, 2, 1],
        'normals': [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    },
    'tambourine': {
        'vertices': [
            (-0.36349134, -0.87754573, 0.31270999),
            (-0.87754573, -0.36349134, 0.31270999),
            (-0.87754573, 0.36349134, 0.31270999),
            (-0.36349134, 0.87754573, 0.31270999),
            (0.36349134, 0.87754573, 0.31270999),
            (0.87754573, 0.36349134, 0.31270999),
            (0.87754573, -0.36349134, 0.31270999),
            (0.36349134, -0.87754573, 0.31270999),
            (-0.00000000, -0.94984865, -0.31270999),
            (-0.67164442, -0.67164442, -0.31270999),
            (-0.94984865, 0.00000000, -0.31270999),
            (-0.67164442, 0.67164442, -0.31270999),
            (0.00000000, 0.94984865, -0.31270999),
            (0.67164442, 0.67164442, -0.31270999),
            (0.94984865, -0.00000000, -0.31270999),
            (0.67164442, -0.67164442, -0.31270999)
        ],
        'faces': [
            (0, 1, 9), (0, 9, 8), (0, 8, 7), (0, 7, 6, 5, 4, 3, 2, 1),
            (1, 2, 10), (1, 10, 9), (2, 3, 11), (2, 11, 10),
            (3, 4, 12), (3, 12, 11), (4, 5, 13), (4, 13, 12),
            (5, 6, 14), (5, 14, 13), (6, 7, 15), (6, 15, 14),
            (7, 8, 15), (8, 9, 10, 11, 12, 13, 14, 15)
        ],
        'color_pattern': [1, 2, 1, 8, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 8],
        'normals': [
            None, None, None,
            [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)],
            None, None, None, None, None, None, None, None, None, None, None, None, None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)]
        ]
    },
    'parabiaugmented_hexagonal_prism': {
        'vertices': [
            (-0.31783725, -0.55051026, 0.31783725),
            (-0.63567449, 0.00000000, 0.31783725),
            (-0.31783725, 0.55051026, 0.31783725),
            (0.31783725, 0.55051026, 0.31783725),
            (0.63567449, -0.00000000, 0.31783725),
            (0.31783725, -0.55051026, 0.31783725),
            (-0.31783725, -0.55051026, -0.31783725),
            (-0.63567449, 0.00000000, -0.31783725),
            (-0.31783725, 0.55051026, -0.31783725),
            (0.31783725, 0.55051026, -0.31783725),
            (0.63567449, -0.00000000, -0.31783725),
            (0.31783725, -0.55051026, -0.31783725),
            (-0.86602540, -0.50000000, -0.00000000),
            (0.86602540, 0.50000000, 0.00000000)
        ],
        'faces': [
            (0, 6, 11, 5), (0, 5, 4, 3, 2, 1), (0, 1, 12),
            (0, 12, 6), (1, 2, 8, 7), (1, 7, 12),
            (2, 3, 9, 8), (3, 4, 13), (3, 13, 9),
            (4, 5, 11, 10), (4, 10, 13), (6, 7, 8, 9, 10, 11),
            (6, 12, 7), (9, 13, 10)
        ],
        'color_pattern': [0, 1, 2, 2, 0, 2, 0, 2, 2, 0, 2, 1, 2, 2],
        'normals': [
            None, [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)],
            None, None, None, None, None, None, None, None, None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)], None, None
        ]
    },
    'augmented_tridiminished_icosahedron': {
        'vertices': [
            (-0.34047064, -0.39925597, 0.27637473),
            (0.00000000, -0.50988159, -0.30286852),
            (-0.00000000, 0.06936166, -0.66086054),
            (-0.34047064, 0.53797929, -0.30286852),
            (-0.55089306, 0.24835767, 0.27637473),
            (0.34047064, -0.39925597, 0.27637473),
            (0.55089306, 0.24835767, 0.27637473),
            (0.34047064, 0.53797929, -0.30286852),
            (0.00000000, 0.64860491, 0.27637473),
            (0.00000000, -0.98224695, 0.18759247)
        ],
        'faces': [
            (0, 5, 6, 8, 4), (0, 4, 3, 2, 1), (0, 1, 9), (0, 9, 5),
            (1, 2, 7, 6, 5), (1, 5, 9), (2, 3, 7), (3, 4, 8), (3, 8, 7), (6, 7, 8)
        ],
        'color_pattern': [0, 2, 1, 1, 3, 1, 1, 1, 1, 1],
        'normals': [None, None, None, None, None, None, None, None, None, None]
    },
    'pentagonal_gyrocupolarotunda': {
        'vertices': [
            (-0.30240276, -0.93070001, -0.20579132),
            (-0.79170071, -0.57520424, -0.20579132),
            (-0.97859590, 0.00000000, -0.20579132),
            (-0.79170071, 0.57520424, -0.20579132),
            (-0.30240276, 0.93070001, -0.20579132),
            (0.30240276, 0.93070001, -0.20579132),
            (0.79170071, 0.57520424, -0.20579132),
            (0.97859590, -0.00000000, -0.20579132),
            (0.79170071, -0.57520424, -0.20579132),
            (0.30240276, -0.93070001, -0.20579132),
            (-0.30240276, -0.41622170, -0.52375641),
            (-0.48929795, 0.15898254, -0.52375641),
            (0.00000000, 0.51447831, -0.52375641),
            (0.48929795, 0.15898254, -0.52375641),
            (0.30240276, -0.41622170, -0.52375641),
            (-0.79170071, -0.25723915, 0.30868699),
            (0.00000000, -0.83244339, 0.30868699),
            (0.79170071, -0.25723915, 0.30868699),
            (0.48929795, 0.67346085, 0.30868699),
            (-0.48929795, 0.67346085, 0.30868699),
            (-0.30240276, -0.41622170, 0.62665207),
            (0.30240276, -0.41622170, 0.62665207),
            (0.48929795, 0.15898254, 0.62665207),
            (-0.00000000, 0.51447831, 0.62665207),
            (-0.48929795, 0.15898254, 0.62665207)
        ],
        'faces': [
            (0, 1, 10), (0, 10, 14, 9), (0, 9, 16), (0, 16, 20, 15, 1),
            (1, 2, 11, 10), (1, 15, 2), (2, 3, 11), (2, 15, 24, 19, 3),
            (3, 4, 12, 11), (3, 19, 4), (4, 5, 12), (4, 19, 23, 18, 5),
            (5, 6, 13, 12), (5, 18, 6), (6, 7, 13), (6, 18, 22, 17, 7),
            (7, 8, 14, 13), (7, 17, 8), (8, 9, 14), (8, 17, 21, 16, 9),
            (10, 11, 12, 13, 14), (15, 20, 24), (16, 21, 20), (17, 22, 21),
            (18, 23, 22), (19, 24, 23), (20, 21, 22, 23, 24)
        ],
        'color_pattern': [
            0, 1, 0, 2,
            1, 0, 0, 2,
            1, 0, 0, 2,
            1, 0, 0, 2,
            1, 0, 0, 2,
            2, 0, 0, 0,
            0, 0, 2
        ],
        'normals': [
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None
        ]
    },
    'elongated_triangular_gyrobicupola': {
        'vertices': [
            (-0.34781848, -0.60243929, 0.34781848),
            (-0.69563697, 0.00000000, 0.34781848),
            (-0.34781848, 0.60243929, 0.34781848),
            (0.34781848, 0.60243929, 0.34781848),
            (0.69563697, 0.00000000, 0.34781848),
            (0.34781848, -0.60243929, 0.34781848),
            (-0.34781848, -0.60243929, -0.34781848),
            (-0.69563697, 0.00000000, -0.34781848),
            (-0.34781848, 0.60243929, -0.34781848),
            (0.34781848, 0.60243929, -0.34781848),
            (0.69563697, -0.00000000, -0.34781848),
            (0.34781848, -0.60243929, -0.34781848),
            (0.00000000, -0.40162619, 0.91580369),
            (0.34781848, 0.20081310, 0.91580369),
            (-0.34781848, 0.20081310, 0.91580369),
            (-0.34781848, -0.20081310, -0.91580369),
            (-0.00000000, 0.40162619, -0.91580369),
            (0.34781848, -0.20081310, -0.91580369)
        ],
        'faces': [
            (0, 1, 7, 6), (0, 6, 11, 5), (0, 5, 12),
            (0, 12, 14, 1), (1, 2, 8, 7), (1, 14, 2),
            (2, 3, 9, 8), (2, 14, 13, 3), (3, 4, 10, 9),
            (3, 13, 4), (4, 5, 11, 10), (4, 13, 12, 5),
            (6, 7, 15), (6, 15, 17, 11), (7, 8, 16, 15),
            (8, 9, 16), (9, 10, 17, 16), (10, 11, 17),
            (12, 13, 14), (15, 16, 17)
        ],
        'color_pattern': [2, 2, 1, 0, 2, 1, 2, 0, 2, 1, 2, 0, 1, 0, 0, 1, 0, 1, 1, 1],
        'normals': [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    },
    'pentagonal_gyrobicupola': {
        'vertices': [
            (-0.30901699, -0.95105652, -0.00000000),
            (-0.80901699, -0.58778525, -0.00000000),
            (-1.00000000, -0.00000000, -0.00000000),
            (-0.80901699, 0.58778525, -0.00000000),
            (-0.30901700, 0.95105652, -0.00000000),
            (0.30901699, 0.95105652, -0.00000000),
            (0.80901699, 0.58778525, -0.00000000),
            (1.00000000, -0.00000000, -0.00000000),
            (0.80901699, -0.58778525, -0.00000000),
            (0.30901699, -0.95105652, -0.00000000),
            (-0.30901699, -0.42532540, -0.32491970),
            (-0.50000000, 0.16245985, -0.32491970),
            (0.00000000, 0.52573111, -0.32491970),
            (0.50000000, 0.16245985, -0.32491970),
            (0.30901699, -0.42532540, -0.32491970),
            (0.00000000, -0.52573111, 0.32491970),
            (0.50000000, -0.16245985, 0.32491970),
            (0.30901699, 0.42532540, 0.32491970),
            (-0.30901699, 0.42532540, 0.32491970),
            (-0.50000000, -0.16245985, 0.32491970),
        ],
        'faces': [
            (0, 1, 10), (0, 10, 14, 9), (0, 9, 15),
            (0, 15, 19, 1), (1, 2, 11, 10), (1, 19, 2),
            (2, 3, 11), (2, 19, 18, 3), (3, 4, 12, 11),
            (3, 18, 4), (4, 5, 12), (4, 18, 17, 5),
            (5, 6, 13, 12), (5, 17, 6), (6, 7, 13),
            (6, 17, 16, 7), (7, 8, 14, 13), (7, 16, 8),
            (8, 9, 14), (8, 16, 15, 9), (10, 11, 12, 13, 14), (15, 16, 17, 18, 19)
        ],
        'color_pattern': [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 2, 2],
        'normals': [
            None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)],
            [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)]
        ]
    },
    'pentagonal_cupola': {
        'vertices': [
            (-0.30722035, -0.94552702, 0.10767686),
            (-0.80431332, -0.58436784, 0.10767686),
            (-0.99418594, 0.00000000, 0.10767686),
            (-0.80431332, 0.58436784, 0.10767686),
            (-0.30722035, 0.94552702, 0.10767686),
            (0.30722035, 0.94552702, 0.10767686),
            (0.80431332, 0.58436784, 0.10767686),
            (0.99418594, -0.00000000, 0.10767686),
            (0.80431332, -0.58436784, 0.10767686),
            (0.30722035, -0.94552702, 0.10767686),
            (-0.30722035, -0.42285254, -0.21535373),
            (-0.49709297, 0.16151530, -0.21535373),
            (0.00000000, 0.52267448, -0.21535373),
            (0.49709297, 0.16151530, -0.21535373),
            (0.30722035, -0.42285254, -0.21535373)
        ],
        'faces': [
            (0, 1, 10),
            (0, 10, 14, 9),
            (0, 9, 8, 7, 6, 5, 4, 3, 2, 1),
            (1, 2, 11, 10),
            (2, 3, 11),
            (3, 4, 12, 11),
            (4, 5, 12),
            (5, 6, 13, 12),
            (6, 7, 13),
            (7, 8, 14, 13),
            (8, 9, 14),
            (10, 11, 12, 13, 14)
        ],
        'color_pattern': [0, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 3],
        'normals': [
            None, None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)],
            None, None, None, None, None, None, None, None,
            [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)]
        ]
    },
    'triaugmented_hexagonal_prism': {
        'vertices': [
            (-0.31783725, -0.55051026, 0.31783725),
            (-0.63567449, 0.00000000, 0.31783725),
            (-0.31783725, 0.55051026, 0.31783725),
            (0.31783725, 0.55051026, 0.31783725),
            (0.63567449, -0.00000000, 0.31783725),
            (0.31783725, -0.55051026, 0.31783725),
            (-0.31783725, -0.55051026, -0.31783725),
            (-0.63567449, 0.00000000, -0.31783725),
            (-0.31783725, 0.55051026, -0.31783725),
            (0.31783725, 0.55051026, -0.31783725),
            (0.63567449, -0.00000000, -0.31783725),
            (0.31783725, -0.55051026, -0.31783725),
            (-0.86602540, -0.50000000, -0.00000000),
            (0.00000000, 1.00000000, -0.00000000),
            (0.86602540, -0.50000000, -0.00000000)
        ],
        'faces': [
            (0, 6, 11, 5),
            (0, 5, 4, 3, 2, 1),
            (0, 1, 12),
            (0, 12, 6),
            (1, 2, 8, 7),
            (1, 7, 12),
            (2, 3, 13),
            (2, 13, 8),
            (3, 4, 10, 9),
            (3, 9, 13),
            (4, 5, 14),
            (4, 14, 10),
            (5, 11, 14),
            (6, 7, 8, 9, 10, 11),
            (6, 12, 7),
            (8, 13, 9),
            (10, 14, 11),
        ],
        'color_pattern': [0, 1, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 2, 1, 2, 2, 2],
        'normals': [
            None,
            [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)],
            None, None, None, None, None, None, None, None, None, None, None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)],
            None, None, None
        ]
    },
    'truncated_cuboctahedron': {
        'vertices': [
            (-0.21573941, -0.52084100, 0.82594259),
            (-0.52084100, -0.21573941, 0.82594259),
            (-0.52084100, 0.21573941, 0.82594259),
            (-0.21573941, 0.52084100, 0.82594259),
            (0.21573941, 0.52084100, 0.82594259),
            (0.52084100, 0.21573941, 0.82594259),
            (0.52084100, -0.21573941, 0.82594259),
            (0.21573941, -0.52084100, 0.82594259),
            (-0.21573941, -0.82594259, 0.52084100),
            (-0.82594259, -0.21573941, 0.52084100),
            (-0.82594259, 0.21573941, 0.52084100),
            (-0.21573941, 0.82594259, 0.52084100),
            (0.21573941, 0.82594259, 0.52084100),
            (0.82594259, 0.21573941, 0.52084100),
            (0.82594259, -0.21573941, 0.52084100),
            (0.21573941, -0.82594259, 0.52084100),
            (-0.52084100, -0.82594259, 0.21573941),
            (-0.82594259, -0.52084100, 0.21573941),
            (-0.82594259, 0.52084100, 0.21573941),
            (-0.52084100, 0.82594259, 0.21573941),
            (0.52084100, 0.82594259, 0.21573941),
            (0.82594259, 0.52084100, 0.21573941),
            (0.82594259, -0.52084100, 0.21573941),
            (0.52084100, -0.82594259, 0.21573941),
            (0.52084100, -0.82594259, -0.21573941),
            (0.21573940, -0.82594259, -0.52084100),
            (-0.21573941, -0.82594259, -0.52084100),
            (-0.52084100, -0.82594259, -0.21573941),
            (-0.82594259, -0.52084100, -0.21573941),
            (-0.82594259, -0.21573941, -0.52084100),
            (-0.82594259, 0.21573941, -0.52084100),
            (-0.82594259, 0.52084100, -0.21573941),
            (-0.52084100, 0.82594259, -0.21573941),
            (-0.21573941, 0.82594259, -0.52084100),
            (0.21573941, 0.82594259, -0.52084100),
            (0.52084100, 0.82594259, -0.21573941),
            (0.82594259, 0.52084100, -0.21573941),
            (0.82594259, 0.21573941, -0.52084100),
            (0.82594259, -0.21573941, -0.52084100),
            (0.82594259, -0.52084100, -0.21573941),
            (0.52084100, -0.21573941, -0.82594259),
            (0.52084100, 0.21573941, -0.82594259),
            (0.21573941, 0.52084100, -0.82594259),
            (-0.21573941, 0.52084100, -0.82594259),
            (-0.52084100, 0.21573941, -0.82594259),
            (-0.52084100, -0.21573941, -0.82594259),
            (-0.21573941, -0.52084100, -0.82594259),
            (0.21573940, -0.52084100, -0.82594259)
        ],
        'faces': [
            (0, 1, 9, 17, 16, 8),
            (0, 8, 15, 7),
            (0, 7, 6, 5, 4, 3, 2, 1),
            (1, 2, 10, 9),
            (2, 3, 11, 19, 18, 10),
            (3, 4, 12, 11),
            (4, 5, 13, 21, 20, 12),
            (5, 6, 14, 13),
            (6, 7, 15, 23, 22, 14),
            (8, 16, 27, 26, 25, 24, 23, 15),
            (9, 10, 18, 31, 30, 29, 28, 17),
            (11, 12, 20, 35, 34, 33, 32, 19),
            (13, 14, 22, 39, 38, 37, 36, 21),
            (16, 17, 28, 27),
            (18, 19, 32, 31),
            (20, 21, 36, 35),
            (22, 23, 24, 39),
            (24, 25, 47, 40, 38, 39),
            (25, 26, 46, 47),
            (26, 27, 28, 29, 45, 46),
            (29, 30, 44, 45),
            (30, 31, 32, 33, 43, 44),
            (33, 34, 42, 43),
            (34, 35, 36, 37, 41, 42),
            (37, 38, 40, 41),
            (40, 47, 46, 45, 44, 43, 42, 41),
        ],
        'color_pattern': [0, 1, 2, 1, 0, 1, 0, 1, 0, 2, 2, 2, 2, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2],
        'normals': [
            None,
            None,
            [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)],
            None,
            None,
            None,
            None,
            None,
            None,
            [(0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0)],
            [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0)],
            [(0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0)],
            [(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)]
        ]
    },
    'truncated_octahedron': {
        'vertices': [
            (-0.31622777, -0.54772256, 0.77459667),
            (-0.63245553, 0.00000000, 0.77459667),
            (-0.31622777, 0.54772256, 0.77459667),
            (0.31622777, 0.54772256, 0.77459667),
            (0.63245553, -0.00000000, 0.77459667),
            (0.31622777, -0.54772256, 0.77459667),
            (-0.31622777, -0.91287093, 0.25819889),
            (-0.94868330, 0.18257419, 0.25819889),
            (-0.63245553, 0.73029674, 0.25819889),
            (0.63245553, 0.73029674, 0.25819889),
            (0.94868330, 0.18257419, 0.25819889),
            (0.31622777, -0.91287093, 0.25819889),
            (-0.63245553, -0.73029674, -0.25819889),
            (-0.94868330, -0.18257419, -0.25819889),
            (-0.31622777, 0.91287093, -0.25819889),
            (0.31622777, 0.91287093, -0.25819889),
            (0.94868330, -0.18257419, -0.25819889),
            (0.63245553, -0.73029674, -0.25819889),
            (-0.31622777, -0.54772256, -0.77459667),
            (-0.63245553, 0.00000000, -0.77459667),
            (-0.31622777, 0.54772256, -0.77459667),
            (0.31622777, 0.54772256, -0.77459667),
            (0.63245553, -0.00000000, -0.77459667),
            (0.31622777, -0.54772256, -0.77459667)
        ],
        'faces': [
            (0, 6, 11, 5),
            (0, 5, 4, 3, 2, 1),
            (0, 1, 7, 13, 12, 6),
            (1, 2, 8, 7),
            (2, 3, 9, 15, 14, 8),
            (3, 4, 10, 9),
            (4, 5, 11, 17, 16, 10),
            (6, 12, 18, 23, 17, 11),
            (7, 8, 14, 20, 19, 13),
            (9, 10, 16, 22, 21, 15),
            (12, 13, 19, 18),
            (14, 15, 21, 20),
            (16, 17, 23, 22),
            (18, 19, 20, 21, 22, 23)
        ],
        'color_pattern': [2, 0, 1, 2, 1, 2, 1, 0, 0, 0, 2, 2, 2, 1],
        'normals': [
            None,
            [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)]
        ]
    },
    'cuboctahedron': {
        'vertices': [
            (-0.50000000, -0.86602540, -0.00000000),
            (-1.00000000, 0.00000000, -0.00000000),
            (-0.50000000, 0.86602540, -0.00000000),
            (0.50000000, 0.86602540, -0.00000000),
            (1.00000000, 0.00000000, -0.00000000),
            (0.50000000, -0.86602540, -0.00000000),
            (-0.50000000, -0.28867513, -0.81649658),
            (0.00000000, 0.57735027, -0.81649658),
            (0.50000000, -0.28867513, -0.81649658),
            (0.00000000, -0.57735027, 0.81649658),
            (0.50000000, 0.28867513, 0.81649658),
            (-0.50000000, 0.28867513, 0.81649658),
        ],
        'faces': [
            (0, 1, 6), (0, 6, 8, 5), (0, 5, 9), (0, 9, 11, 1),
            (1, 2, 7, 6), (1, 11, 2), (2, 3, 7), (2, 11, 10, 3),
            (3, 4, 8, 7), (3, 10, 4), (4, 5, 8), (4, 10, 9, 5),
            (6, 7, 8), (9, 10, 11)
        ],
        'color_pattern': [0, 2, 0, 1, 2, 0, 0, 2, 1, 0, 0, 2, 0, 0],
        'normals': [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    },
    'icosidodecahedron': {
        'vertices': [
            (-0.30901699, -0.95105652, -0.00000000),
            (-0.80901699, -0.58778525, -0.00000000),
            (-1.00000000, 0.00000000, -0.00000000),
            (-0.80901699, 0.58778525, -0.00000000),
            (-0.30901700, 0.95105652, -0.00000000),
            (0.30901699, 0.95105652, -0.00000000),
            (0.80901699, 0.58778525, -0.00000000),
            (1.00000000, 0.00000000, -0.00000000),
            (0.80901699, -0.58778525, -0.00000000),
            (0.30901699, -0.95105652, -0.00000000),
            (0.00000000, -0.85065081, -0.52573111),
            (-0.80901699, -0.26286556, -0.52573111),
            (-0.50000000, 0.68819096, -0.52573111),
            (0.50000000, 0.68819096, -0.52573111),
            (0.80901699, -0.26286556, -0.52573111),
            (-0.30901699, -0.42532540, -0.85065081),
            (-0.50000000, 0.16245985, -0.85065081),
            (0.00000000, 0.52573111, -0.85065081),
            (0.50000000, 0.16245985, -0.85065081),
            (0.30901699, -0.42532540, -0.85065081),
            (-0.50000000, -0.68819096, 0.52573111),
            (0.50000000, -0.68819096, 0.52573111),
            (0.80901699, 0.26286556, 0.52573111),
            (-0.00000000, 0.85065081, 0.52573111),
            (-0.80901699, 0.26286556, 0.52573111),
            (0.00000000, -0.52573111, 0.85065081),
            (0.50000000, -0.16245985, 0.85065081),
            (0.30901699, 0.42532540, 0.85065081),
            (-0.30901699, 0.42532540, 0.85065081),
            (-0.50000000, -0.16245985, 0.85065081)
        ],
        'faces': [
            (0, 1, 11, 15, 10), (0, 10, 9), (0, 9, 21, 25, 20), (0, 20, 1),
            (1, 2, 11), (1, 20, 29, 24, 2), (2, 3, 12, 16, 11), (2, 24, 3),
            (3, 4, 12), (3, 24, 28, 23, 4), (4, 5, 13, 17, 12), (4, 23, 5),
            (5, 6, 13), (5, 23, 27, 22, 6), (6, 7, 14, 18, 13), (6, 22, 7),
            (7, 8, 14), (7, 22, 26, 21, 8), (8, 9, 10, 19, 14), (8, 21, 9),
            (10, 15, 19), (11, 16, 15), (12, 17, 16), (13, 18, 17),
            (14, 19, 18), (15, 16, 17, 18, 19), (20, 25, 29), (21, 26, 25),
            (22, 27, 26), (23, 28, 27), (24, 29, 28), (25, 26, 27, 28, 29)
        ],
        'color_pattern': [
            0, 1, 0, 1,
            1, 0, 0, 1,
            1, 0, 0, 1,
            1, 0, 0, 1,
            1, 0, 0, 1,
            1, 1, 1, 1,
            1, 0, 1, 1,
            1, 1, 1, 0
        ],
        'normals': [
            None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None
        ]
    },
    'tetrahedron': {
        'vertices': [
            (-0.81649658, -0.47140452, 0.33333333),
            (0.81649658, -0.47140452, 0.33333333),
            (0.00000000, 0.00000000, -1.00000000),
            (0.00000000, 0.94280904, 0.33333333)
        ],
        'faces': [(0, 1, 3), (0, 3, 2), (0, 2, 1), (1, 2, 3)],
        'color_pattern': [0, 1, 2, 3],
        'normals': [None, None, None, None]
    },
    'octahedron': {
        'vertices': [
            (-0.70710678, -0.70710678, 0.00000000),
            (-0.70710678, 0.70710678, 0.00000000),
            (0.70710678, 0.70710678, 0.00000000),
            (0.70710678, -0.70710678, 0.00000000),
            (0.00000000, 0.00000000, -1.00000000),
            (0.00000000, 0.00000000, 1.00000000)
        ],
        'faces': [
            (0, 1, 4), (0, 4, 3), (0, 3, 5), (0, 5, 1),
            (1, 2, 4), (1, 5, 2), (2, 3, 4), (2, 5, 3)
        ],
        'color_pattern': [1, 0, 1, 0, 0, 1, 1, 0],
        'normals': [None, None, None, None, None, None, None, None]
    },
    'cube': {
        'vertices': [
            (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, -0.5, 0.5),
            (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5)
        ],
        'faces': [
            (0, 1, 5, 4), (0, 4, 7, 3), (0, 3, 2, 1),
            (1, 2, 6, 5), (2, 3, 7, 6), (4, 5, 6, 7)
        ],
        'color_pattern': [1, 1, 0, 1, 1, 0],
        'normals': [
            [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0)],
            [(0, -1, 0), (0, -1, 0), (0, -1, 0), (0, -1, 0)],
            [(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)],
            [(0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0)],
            [(1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)],
            [(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1)]
        ]
    },
    'icosahedron': {
        'vertices': [
            (-0.52573111, -0.72360680, 0.44721360),
            (-0.85065081, 0.27639320, 0.44721360),
            (-0.00000000, 0.89442719, 0.44721360),
            (0.85065081, 0.27639320, 0.44721360),
            (0.52573111, -0.72360680, 0.44721360),
            (0.00000000, -0.89442719, -0.44721360),
            (-0.85065081, -0.27639320, -0.44721360),
            (-0.52573111, 0.72360680, -0.44721360),
            (0.52573111, 0.72360680, -0.44721360),
            (0.85065081, -0.27639320, -0.44721360),
            (0.00000000, 0.00000000, 1.00000000),
            (-0.00000000, 0.00000000, -1.00000000)
        ],
        'faces': [
            (0, 1, 6), (0, 6, 5), (0, 5, 4), (0, 4, 10),
            (0, 10, 1), (1, 2, 7), (1, 7, 6), (1, 10, 2),
            (2, 3, 8), (2, 8, 7), (2, 10, 3), (3, 4, 9),
            (3, 9, 8), (3, 10, 4), (4, 5, 9), (5, 6, 11),
            (5, 11, 9), (6, 7, 11), (7, 8, 11), (8, 9, 11)
        ],
        'color_pattern': [0, 1, 2, 3, 4, 2, 1, 3, 0, 1, 4, 1, 3, 2, 3, 0, 4, 3, 4, 1],
        'normals': [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    }
}