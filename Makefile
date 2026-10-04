# finish gate hook: the root-level pytest cannot collect the ECRYPT sieve suite (relative CSVs), so
# the shared gate calls this target instead (see scripts/test_suites.sh).
.PHONY: cover
cover:
	COVERAGE=1 scripts/test_suites.sh
