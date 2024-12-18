-- This query calculates average response times for managers in a chat system,
-- accounting for business hours and excluding off-hours

-- Step 1: Get chat messages and calculate the previous message time for each conversation
WITH chat_messages_with_user_message_time AS (
    SELECT
        cm.message_id,
        cm.entity_id,
        cm.created_by,
        cm.type,
        to_timestamp(cm.created_at) AT TIME ZONE 'UTC' AS manager_response_time,
        LAG(to_timestamp(cm.created_at) AT TIME ZONE 'UTC') OVER (PARTITION BY entity_id ORDER BY created_at) AS user_message_time
    FROM test.chat_messages cm
),

-- Step 2: Filter out invalid messages and ensure we have manager responses
cleared_chat_messages AS (
    SELECT
        *,
        created_by AS manager_id
    FROM chat_messages_with_user_message_time
    WHERE
        manager_response_time IS NOT NULL
        AND user_message_time IS NOT NULL
        AND created_by != 0
),

-- Step 3: Adjust user message times for business hours (9:30 AM start)
-- If user message is before business hours (9:30 AM = 570 minutes) and manager responds during the day,
-- adjust the user message time to start of business hours
fixed_user_message_time AS (
    SELECT
        *,
        CASE
            WHEN EXTRACT(HOUR FROM user_message_time) * 60 +
                 EXTRACT(MINUTE FROM user_message_time) < 570     -- Before 9:30 AM
            AND EXTRACT(HOUR FROM manager_response_time) * 60 +
                EXTRACT(MINUTE FROM manager_response_time) BETWEEN 570 AND 1440  -- Response during work hours
            THEN
                date_trunc('day', user_message_time) + INTERVAL '9 hours 30 minutes'
            ELSE
                user_message_time
        END AS new_user_message_time
    FROM cleared_chat_messages
),

-- Step 4: Calculate response times in minutes, adjusting for multi-day responses
-- by subtracting non-business hours (9.5 hours per day)
response_times AS (
    SELECT
        *,
        CASE
            WHEN EXTRACT(DAY FROM (manager_response_time - new_user_message_time)) > 0
            THEN (EXTRACT(EPOCH FROM (manager_response_time - new_user_message_time)) / 60) -
                (570 * EXTRACT(DAY FROM (manager_response_time - new_user_message_time)))
            ELSE EXTRACT(EPOCH FROM (manager_response_time - new_user_message_time)) / 60
        END AS response_time_min
    FROM fixed_user_message_time
)

-- Final step: Calculate average response time per manager
SELECT
    rt.manager_id,
    m.name_mop AS manager_name,
    ROUND(AVG(rt.response_time_min))::integer AS average_response_time_min
FROM
    response_times rt
JOIN
    test.managers m ON rt.manager_id = m.mop_id
GROUP BY
    m.name_mop, rt.manager_id
ORDER BY
    rt.manager_id;
