import pytest


@pytest.mark.fast
def test_remove_duplicate_pairs():
    '''
    unique_pairs_distances_test = {
        ('Ga1A', 'Ga1'): ['2.601'],
        ('Ga1', 'La1'): ['3.291'],
        ('Co1B', 'Ga1'): ['2.601'],
        ('Ga1', 'Ga1A'): ['2.601'],
        ('Ga1', 'Ga1'): ['2.358']}

    to 

    adjusted_pairs_test == {
        ('Ga1', 'Ga1A'): ['2.601'],
        ('Ga1', 'La1'): ['3.291'],
        ('Co1B', 'Ga1'): ['2.601'],
        ('Ga1', 'Ga1A'): ['2.601'],
        ('Ga1', 'Ga1'): ['2.358']}
    '''



#     # 560709.cif
#     # Mendeleev Ga	74
#     unique_pairs_distances_test_1 = {
#         ('Co1A', 'Ga2B'): ['2.501'],
#         ('La', 'Ga1B'): ['2.979'],
#         ('Co2A', 'Ga1B'): ['2.501'],
#         ('Ga1B', 'Ga2B'): ['2.501'],
#         ('Co1A', 'Co2A'): ['2.501'],
#         ('La', 'Co1A'): ['2.979']
#     }

#     adjusted_pairs_test_1 = strip_labels_and_remove_duplicate(
#         unique_pairs_distances_test_1
#     )

#     assert adjusted_pairs_test_1 == {
#         ('Co', 'Co'): ['2.501'],
#         ('Co', 'Ga'): ['2.501'],
#         ('Co', 'La'): ['2.979'],
#         ('Ga', 'Ga'): ['2.501'],
#         ('Ga', 'La'): ['2.979']
#     }

#     # 539016.cif
#     unique_pairs_distances_test_2 = {
#         ('Ga1A', 'Ga1'): ['2.601'],
#         ('Ga1', 'La1'): ['3.291'],
#         ('Co1B', 'Ga1'): ['2.601'],
#         ('Ga1', 'Ga1A'): ['2.601'],
#         ('Ga1', 'Ga1'): ['2.358']
#     }

#     adjusted_pairs_test_2 = strip_labels_and_remove_duplicate(
#         unique_pairs_distances_test_2
#     )

#     assert adjusted_pairs_test_2 == {
#         ('Ga', 'Ga'): ['2.358'],
#         ('Ga', 'La'): ['3.291'],
#         ('Co', 'Ga'): ['2.601']
#     }
