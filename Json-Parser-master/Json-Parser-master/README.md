# Json-Parser
The Parser is able to validate all JSON strings and find duplicate keys and raise the error accordingly. It gives an error message in case of invalid JSON and along with it, also prints eleven charactered string starting from errored character. Given a key (or key path), it can print the corresponding value.

## Pitfalls
* Can't validate control characters
* Validation of duplicate key is implemented on whole file and not on block level

## Inside Description
The parser takes a text file as input which contains the JSON for validating and parsing There are only three public methods that are available to user. The key whose value have to be find need to be hard coded.

---

This repository is collectively maintained by
* Ayush Khopkar
* Siddhant Mehta
