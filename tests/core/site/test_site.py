import pytest
from cifkit import CifEnsemble
from core.run.site_analysis import generate_save_site_data
import json
import os
import shutil


@pytest.mark.slow
def test_run_site_without_nested_files():
    generate_save_site_data(["tests/data/site_test"], add_nested_files=False)
    output_directory = "tests/data/site_test/output"
    with open(
        os.path.join(output_directory, "site_test_element_pairs.json"), "r"
    ) as file:
        element_pairs = json.load(file)
        assert element_pairs == {
            "Co-Co": {
                "250361": [
                    {
                        "dist": 2.529,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "rt",
                        "structure": "MgCu2",
                    }
                ],
                "1644636": [
                    {
                        "dist": 2.49,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "lt",
                        "structure": "TbFe2",
                    }
                ],
                "1644635": [
                    {
                        "dist": 2.516,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "lt",
                        "structure": "TbFe2",
                    }
                ],
            },
            "Er-Co": {
                "250361": [
                    {
                        "dist": 2.966,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "rt",
                        "structure": "MgCu2",
                    }
                ],
                "1644636": [
                    {
                        "dist": 2.926,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "lt",
                        "structure": "TbFe2",
                    }
                ],
                "1644635": [
                    {
                        "dist": 2.949,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "lt",
                        "structure": "TbFe2",
                    }
                ],
            },
        }
    shutil.rmtree(output_directory)


@pytest.mark.slow
def test_run_site_with_nested_files():
    generate_save_site_data(["tests/data/site_test"], add_nested_files=True)
    output_directory = "tests/data/site_test/output"
    with open(
        os.path.join(output_directory, "site_test_element_pairs.json"), "r"
    ) as file:
        element_pairs = json.load(file)
        assert element_pairs == {
            "Co-Co": {
                "250361": [
                    {
                        "dist": 2.529,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "rt",
                        "structure": "MgCu2",
                    }
                ],
                "1644636": [
                    {
                        "dist": 2.49,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "lt",
                        "structure": "TbFe2",
                    }
                ],
                "1644635": [
                    {
                        "dist": 2.516,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "lt",
                        "structure": "TbFe2",
                    }
                ],
            },
            "Er-Co": {
                "250361": [
                    {
                        "dist": 2.966,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "rt",
                        "structure": "MgCu2",
                    }
                ],
                "1644636": [
                    {
                        "dist": 2.926,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "lt",
                        "structure": "TbFe2",
                    }
                ],
                "1644635": [
                    {
                        "dist": 2.949,
                        "mixing": "full_occupancy",
                        "formula": "ErCo2",
                        "tag": "lt",
                        "structure": "TbFe2",
                    }
                ],
            },
            "Sm-Sm": {
                "1120297": [
                    {
                        "dist": 3.582,
                        "mixing": "full_occupancy",
                        "formula": "Sm",
                        "tag": "rt",
                        "structure": "Sm",
                    }
                ]
            },
        }
    shutil.rmtree(output_directory)


@pytest.mark.slow
def test_single_file():
    generate_save_site_data(
        ["tests/core/site/cifs/single_file_1955204"], add_nested_files=False
    )
    """
    ('Co4', 'Co4') 2.274 (Good)
    ('Co1', 'Co2') 2.46 (Good)
    ('Co1', 'Co1') 2.404 (Good)
    ('Co1', 'Co3') 2.404 (???)
    ('Co2', 'Er1') 2.776
    ('Co2', 'Er2') 2.775
    """

    """
    Co1 Co3 2.404
    Co2 Co3 2.46
    Co3 Co1 2.404
    Co4 Co4 2.274
    Er1 Co2 2.776
    Er2 Co2 2.775
    """

    output_directory = "tests/core/site/cifs/single_file_1955204/output"

    with open(
        os.path.join(
            output_directory, "single_file_1955204_element_pairs.json"
        ),
        "r",
    ) as file:
        element_pairs = json.load(file)
        assert element_pairs == {
            "Co-Co": {
                "1955204": [
                    {
                        "dist": 2.274,
                        "mixing": "full_occupancy",
                        "formula": "Er2Co17",
                        "tag": "hex",
                        "structure": "Th2Ni17",
                    }
                ]
            },
            "Er-Co": {
                "1955204": [
                    {
                        "dist": 2.775,
                        "mixing": "full_occupancy",
                        "formula": "Er2Co17",
                        "tag": "hex",
                        "structure": "Th2Ni17",
                    }
                ]
            },
        }
