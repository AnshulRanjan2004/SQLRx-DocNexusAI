CREATE TABLE default.as_providers_v1
(
    `type_1_npi` UInt64,
    `type_2_npi_names` Array(String),
    `type_2_npis` Array(UInt64),
    `first_name` String,
    `middle_name` String,
    `last_name` String,
    `gender` Enum8('M' = 1, 'F' = 2, 'O' = 3, 'U' = 4, '' = 5),
    `specialties` Array(String),
    `conditions_tags` Array(Tuple(
        String,
        String)),
    `conditions` Array(String),
    `cities` Array(String),
    `states` Array(String),
    `counties` Array(String),
    `city_states` Array(String),
    `hospital_names` Array(String),
    `system_names` Array(String),
    `affiliations` String,
    `best_type_2_npi` UInt64,
    `best_hospital_name` String,
    `best_system_name` String,
    `phone` Nullable(String),
    `email` Nullable(String),
    `linkedin` Nullable(String),
    `twitter` Nullable(String)
)
ENGINE = SharedMergeTree('/clickhouse/tables/{uuid}/{shard}', '{replica}')
PRIMARY KEY type_1_npi
ORDER BY type_1_npi
SETTINGS index_granularity = 8192;