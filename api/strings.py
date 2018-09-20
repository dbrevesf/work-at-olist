# KEY WORDS
CALL_ID_KEY = 'call_id'
TIMESTAMP_KEY = 'timestamp'
START_KEY = 'start'
END_KEY = 'end'
INPUT_ERROR_KEY = 'input_error'
SOURCE_KEY = 'source'
DESTINATION_KEY = 'destination'
SUCCESS_KEY = 'success'
STANDING_CHARGE_KEY = 'standing_charge'
CALL_CHARGE_KEY = 'call_charge'
PRICE_ID_KEY = 'price_id'
CREATED_DATE_KEY = 'created_date'
START_DATE_KEY = 'start_date'
START_TIME_KEY = 'start_time'
DURATION_KEY = 'duration'
PRICE_KEY = 'price'
ERROR_KEY = 'error'
PERIOD_KEY = 'period'
RESPONSE_KEY = 'response'

# LIST OF STRINGS
TRUE_VALUES = ['True', 'true', 'TRUE']
FALSE_VALUES = ['False', 'false', 'FALSE']

# ERROR MESSAGES
START_END_ERROR = 'a call must start and must end'
EQUAL_TIMESTAMPS_ERROR = 'the timestamps must be different'
SOONER_END_ERROR = 'the end must be later'
CALL_LIMIT_ERROR = 'limit of call details exceeded.'
SOURCE_EQUAL_DESTINATION_ERROR = 'source and destination must be different'
SOURCE_OR_DESTINATION_MISSED_ERROR = 'source and/or destination are missed'
END_EQUAL_START_ERROR = 'end must be different than start'
RULES_TIME_CONFLICT_ERROR = 'time conflict between the rules'
TIME_FORMAT_ERROR = 'wrong time format'
NEGATIVE_CHARGES_ERROR = 'charges must be positive'
PRICE_RULES_SAME_DATE_ERROR = 'two price rules with the same time date'
TIME_PATTERN_ERROR = 'time date must match format %s'
NO_PRICE_RULE_ERROR = 'there is no price rule for this interval'
BILLS_NOT_FOUND_ERROR = 'bills not found'
SOURCE_MISSED_ERROR = 'source is required'

# PATTERNS
COMPLETE_DATE_PATTERN = '%Y-%m-%dT%H:%M:%SZ'
YEAR_MONTH_PATTERN = '%Y-%m'
TIME_PATTERN = '%H:%M'
HOUR_MINUTE_SECOND_PATTERN = '%dh%dm%ds'
