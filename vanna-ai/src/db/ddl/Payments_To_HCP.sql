CREATE TABLE default.as_lsf_v1
(
    `type_1_npi` UInt64 COMMENT 'This column stores the National Provider Identifier (NPI), which is a unique identification number for covered health care providers.. Samples: [{\'type_1_npi\': 1003000126}, {\'type_1_npi\': 1003000142}, {\'type_1_npi\': 1003000167}]',
    `life_science_firm_name` String COMMENT 'This column contains the names of life science firms, identifying the organizations involved in the transactions.. Samples: [{\'life_science_firm_name\': \'TEVA PHARMACEUTICALS USA, INC.\'}, {\'life_science_firm_name\': \'ABBVIE, INC.\'}, {\'life_science_firm_name\': \'AMGEN INC.\'}]',
    `product_name` String COMMENT 'This column lists the names of products associated with the life science firms, representing the items or services for which payments are made.. Samples: [{\'product_name\': \'JARDIANCE\'}, {\'product_name\': \'FISHER & PAYKEL HEALTHCARE\'}, {\'product_name\': \'EYLEA HD\'}]',
    `nature_of_payment` Nullable(String) COMMENT 'This column describes the type of payments made, such as food and beverage, travel and lodging, or education, which provides context about the nature of the transactions.. Samples: [{\'nature_of_payment\': \'Food and Beverage\'}, {\'nature_of_payment\': \'Travel and Lodging\'}, {\'nature_of_payment\': \'Education\'}]',
    `year` UInt16 COMMENT 'This column indicates the year during which the payment was made, allowing for temporal analysis of financial interactions.. Samples: [{\'year\': 2016}, {\'year\': 2017}, {\'year\': 2018}]',
    `amount` Nullable(Float32) COMMENT 'This column reflects the monetary amount of the payment made, providing quantitative data for financial analysis.. Samples: [{\'amount\': 11.800000190734863}, {\'amount\': 16.09000015258789}, {\'amount\': 17.299999237060547}]'
)
ENGINE = SharedMergeTree('/clickhouse/tables/{uuid}/{shard}', '{replica}')
ORDER BY (type_1_npi, year, life_science_firm_name, product_name)
SETTINGS index_granularity = 8192
COMMENT 'This table contains data related to life science firms, detailing their payments and associated information for various products across different years.';