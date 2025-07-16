CREATE TABLE default.mf_conditions
(
    `projectId` Int32 COMMENT 'A unique identifier for the project associated with the condition. This helps in linking the conditions to specific research or clinical projects.. Samples: ["{\'projectId\': 2}", "{\'projectId\': 3}", "{\'projectId\': 4}"]',
    `display` Nullable(String) COMMENT 'A human-readable name or description of the medical condition, making it easier for users to understand the condition being referenced.. Samples: ["{\'display\': \'Aagenaes Syndrome\'}", "{\'display\': \'Aase Syndrome\'}", "{\'display\': \'Aarskog Syndrome\'}"]',
    `codingType` Nullable(String) COMMENT 'Indicates the type of coding used for the condition, such as whether it pertains to a condition or a procedure. This allows for categorization of the information.. Samples: ["{\'codingType\': \'condition\'}", "{\'codingType\': \'procedure\'}"]',
    `tcSize` Nullable(Int32) COMMENT 'Represents the size of the clinical trial or data set related to the condition. This may reflect the number of cases or records available for analysis.. Samples: ["{\'tcSize\': 8069}", "{\'tcSize\': 14776}", "{\'tcSize\': 4188}"]'
)
ENGINE = SharedMergeTree('/clickhouse/tables/{uuid}/{shard}', '{replica}')
ORDER BY projectId
SETTINGS index_granularity = 8192
COMMENT 'This table stores information about various medical conditions, including their identifiers and associated descriptors.';