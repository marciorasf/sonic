#!/bin/bash

TEST_NAME=$1

npm run build

# Start py-spy on Sonic container.
docker exec --detach performance_sonic_1 py-spy record -p 1 -f speedscope -F -o /profile/profile.speedscope

docker run \
	--user 0 \
	--volume $(pwd)/build:/tests \
	--volume $(pwd)/reports:/output \
	--network performance_default \
	-i loadimpact/k6 run \
	--out json=/output/log.json \
	--summary-export=/output/summary.json \
	/tests/$TEST_NAME.js

# Stop py-spy after test is done.
docker exec performance_sonic_1 kill -SIGINT $(docker exec performance_sonic_1 ps ax | grep 'py-spy' | grep -v grep | awk '{print $1}')
