CREATE TABLE default.mf_scores
(
    `id` Int32 COMMENT 'A unique identifier for each score entry, ensuring that each row can be distinctly referenced.. Samples: ["{\'id\': 4351668}", "{\'id\': 4351669}", "{\'id\': 4351670}"]',
    `score` Nullable(Float32) COMMENT 'The score value associated with a particular entry. It is represented as a nullable float, allowing for entries that may not have a score assigned.. Samples: ["{\'score\': 24.3745059967041}", "{\'score\': 23.595327377319336}", "{\'score\': 22.514259338378906}"]',
    `mf_providers_npi` Nullable(Int32) COMMENT 'The National Provider Identifier (NPI) associated with the healthcare provider linked to the score. This is also nullable, accommodating cases where provider information might not be available.. Samples: ["{\'mf_providers_npi\': 1902805740}", "{\'mf_providers_npi\': 1326251471}", "{\'mf_providers_npi\': 1871028977}"]',
    `mf_conditions_projectId` Nullable(Int32) COMMENT 'An identifier for the specific project related to the conditions assessed. This column is nullable, reflecting instances where the project ID may be absent.. Samples: ["{\'mf_conditions_projectId\': 4931}", "{\'mf_conditions_projectId\': 6074}", "{\'mf_conditions_projectId\': 6187}"]'
)
ENGINE = SharedMergeTree('/clickhouse/tables/{uuid}/{shard}', '{replica}')
ORDER BY id
SETTINGS index_granularity = 8192
COMMENT 'This table stores scores related to various providers and their associated conditions, facilitating analysis and comparisons within a healthcare context.';