from postprocess.bond import strip_labels_and_remove_duplicate_atom_type_pairs

def test_strip_labels_and_remove_duplicate_atom_type_pairs():
    
    # 560709.cif
    unique_pairs_distances_test_1 =  {
        ('Ga2B', 'Ga1B'): ['2.501'],
        ('Co1A', 'Ga2B'): ['2.501'],
        ('Ga1B', 'La'): ['2.979'],
        ('Co2A', 'Ga1B'): ['2.501'],
        ('Ga1B', 'Ga2B'): ['2.501'],
        ('Co2A', 'Co1A'): ['2.501'],
        ('Co1A', 'Co2A'): ['2.501'],
        ('Co1A', 'La'): ['2.979']
    }

    adjusted_pairs_test_1 = strip_labels_and_remove_duplicate_atom_type_pairs(unique_pairs_distances_test_1)

    assert adjusted_pairs_test_1 == {
        ('Co', 'Co'): ['2.501'],
        ('Co', 'Ga'): ['2.501'],
        ('Co', 'La'): ['2.979'],
        ('Ga', 'Ga'): ['2.501'],
        ('Ga', 'La'): ['2.979']
    }
    
    # 539016.cif
    unique_pairs_distances_test_2 = {
        ('Ga1A', 'Ga1'): ['2.601'],
        ('Ga1', 'La1'): ['3.291'],
        ('Co1B', 'Ga1'): ['2.601'],
        ('Ga1', 'Ga1A'): ['2.601'],
        ('Ga1', 'Ga1'): ['2.358']
    }
        
        
    adjusted_pairs_test_2 = strip_labels_and_remove_duplicate_atom_type_pairs(unique_pairs_distances_test_2)
    
    assert adjusted_pairs_test_2 == {
        ('Ga', 'Ga'): ['2.358'],
        ('Ga', 'La'): ['3.291'],
        ('Co', 'Ga'): ['2.601']
    }

    
