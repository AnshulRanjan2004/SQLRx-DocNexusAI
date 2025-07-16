CREATE TABLE default.as_providers_referrals_v2
(
    `primary_type_2_npi` UInt64,
    `referring_type_2_npi` UInt64,
    `primary_type_2_npi_city` String,
    `referring_type_2_npi_city` String,
    `primary_type_2_npi_state` String,
    `referring_type_2_npi_state` String,
    `primary_type_2_npi_postal_code` String,
    `referring_type_2_npi_postal_code` String,
    `primary_type_2_npi_lat` Float64,
    `referring_type_2_npi_lat` Float64,
    `primary_type_2_npi_lng` Float64,
    `referring_type_2_npi_lng` Float64,
    `primary_type_2_npi_name` String,
    `referring_type_2_npi_name` String,
    `primary_hospital_name` String,
    `referring_hospital_name` String,
    `primary_type_1_npi` UInt64,
    `referring_type_1_npi` UInt64,
    `primary_type_1_npi_name` String,
    `referring_type_1_npi_name` String,
    `primary_specialty` String,
    `referring_specialty` String,
    `date` Date,
    `diagnosis_code` String,
    `diagnosis_code_description` String,
    `procedure_code` String,
    `procedure_code_description` String,
    `total_claim_charge` Float64,
    `total_claim_line_charge` Float64,
    `patient_count` UInt64
)
ENGINE = SharedMergeTree('/clickhouse/tables/{uuid}/{shard}', '{replica}')
ORDER BY (primary_specialty, referring_specialty, primary_hospital_name, diagnosis_code)
SETTINGS index_granularity = 8192;