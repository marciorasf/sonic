/*
* An example of k6 test.
*/

import { Options } from "k6/options";
import { sleep } from "k6";

// These options are used by K6 to configure the test.
export const options: Options = {
	duration: "10s",
	vus: 1,
};

export default function () {
	console.log("Hello World")
	sleep(10)
}
