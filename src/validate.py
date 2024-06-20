from great_expectations.data_context import FileDataContext


def validate_initial_data():
    # Create a FileDataContext
    context = FileDataContext(project_root_dir = "../services")

    # Connect a data source
    ds = context.sources.add_or_update_pandas(name="pandas_datasource")
    da1 = ds.add_csv_asset(name="airbnb", filepath_or_buffer="../data/samples/sample.csv")

    # Create a batch
    batch_request = da1.build_batch_request()
    batches = da1.get_batch_list_from_batch_request(batch_request)

    # Create expectations
    context.add_or_update_expectation_suite("initial_data_validation")
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name="initial_data_validation"
    )
    ex1 = validator.expect_column_values_to_not_be_null(
        column="city",
        meta={"dimension": "Completeness"}
    )
    # ex2 = validator.expect_column_values_to_be_unique(
    #     column='description',
    #     meta={"dimension": 'Uniqueness'}
    # )
    # ex3 = validator.expect_column_values_to_match_regex(
    #     column='bedrooms',
    #     regex='(\\d*.\\d)',
    #     meta={
    #         "dimension": "Validity"
    #     }
    # )
    ex4 = validator.expect_column_values_to_be_between(
        column='review_scores_rating',
        min_value=0.0,
        max_value=101.0,
        mostly=.9,
        meta={
            "dimension": 'Consistency'
        }
    )
    assert ex1['success']
    # assert ex2['success'] == False, f"Duplicate desc: {ex2['expectation_config']}"
    # assert ex3['success'] == False, print(f"Bad format: {ex3['expectation_config']}")
    assert ex4['success']

    validator.save_expectation_suite(discard_failed_expectations=False)

    checkpoint = context.add_or_update_checkpoint(
        name="initial_data_validation_checkpoint",
        validations=[
            {
                "batch_request": batch_request,
                "expectation_suite_name": "initial_data_validation"
            }
        ]
    )
    checkpoint_result = checkpoint.run()
    print(checkpoint_result.success)

    context.build_data_docs()
    context.open_data_docs()


if __name__ == "__main__":
    validate_initial_data()
