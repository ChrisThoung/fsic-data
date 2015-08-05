# Development

The development workflow for this project is as follows:

* The `master` branch contains the latest (fully-working and documented)
  release
* The `development` branch is a staging area to consolidate the future release
  for merging back into `master`
    * Development branches should branch from this one
	* Completed features should be merged back into this branch

## Branch naming conventions

Development branches should have name prefixes as follows:

* Feature branches: `feature/` e.g. `feature/ons`
* Fixes: `fix/` e.g. `fix/eurostat-clean-field`