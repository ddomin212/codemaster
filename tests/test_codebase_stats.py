from .conftest import TEST_CODEBASE_PATH

EXPECTED_CODEBASE_STATS = {
    "num_libs": 7,
    "num_files": 22,
    "dependency_df_shape": (5, 2),
    "stats_df_shape": (1, 10),
}


def test_get_libs():
    from utils.stats.codebase import get_libs

    libs = get_libs(TEST_CODEBASE_PATH)
    assert len(libs) == EXPECTED_CODEBASE_STATS["num_libs"]


def test_get_libs_filenotfound():
    from utils.stats.codebase import get_libs

    libs = get_libs("tests/tests_static/bnb_web/req.txt")
    assert len(libs) == 0


def test_num_files(test_file_dict):
    from utils.stats.codebase import num_files

    assert num_files(test_file_dict) == EXPECTED_CODEBASE_STATS["num_files"]


def test_module_to_code_map(test_dataframes):
    from utils.stats.codebase import module_to_code_map

    _, stats_df = test_dataframes
    module_to_code = module_to_code_map(stats_df)
    assert len(module_to_code) == EXPECTED_CODEBASE_STATS["num_files"]


def test_create_dependency_df(test_code_stats_dict):
    from utils.stats.codebase import create_dependency_df

    dependency_df = create_dependency_df(test_code_stats_dict["file_names"])
    assert (
        dependency_df.shape == EXPECTED_CODEBASE_STATS["dependency_df_shape"]
    )


def test_create_stat_df(test_code_stats_dict):
    from utils.stats.codebase import create_stat_df

    stats_df = create_stat_df(**test_code_stats_dict)
    assert stats_df.shape == EXPECTED_CODEBASE_STATS["stats_df_shape"]


def test_file_stats_codebase(test_file_dict):
    from utils.stats.codebase import file_stats_codebase

    dependency_df, stats_df = file_stats_codebase(
        TEST_CODEBASE_PATH, test_file_dict
    )
    assert dependency_df.shape == (148, 2)
    assert stats_df.shape == (22, 10)
