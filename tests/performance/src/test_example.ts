/*
* An example of k6 test.
*/

import { sleep } from "k6";
import http from "k6/http";
import { Options } from "k6/options";

// These options are used by K6 to configure the test.
export const options: Options = {
	duration: "120s",
	vus: 1000,
};

export default function () {
	http.post(
		"http://sonic:8000/transactions",
		JSON.stringify({
			transaction: "client_id=abc-client-1;transaction_timestamp=2022-07-15T03:40:23.123;value=23.10;description=Chocolate store"
		})
	)
	sleep(0.5)
}
