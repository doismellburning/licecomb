# licecomb

[`lice`](https://github.com/licenses/lice) is a great tool for generating license files. `licecomb` is a tool for ensuring GitHub repositories actually have a license.

## Usage

### Check a well-behaved repo

    $ licecomb doismellburning/licecomb
    $ echo $?
    0

### Check a poorly-behaved repo

    $ licecomb doismellburning/example_unlicensed_repo
    ERROR: Could not find a license file in doismellburning/example_unlicensed_repo
    $ echo $?
    1

### Authenticating to GitHub

    $ # Get a Personal Access Token from https://github.com/settings/applications
    $ export GITHUB_TOKEN=your_token_here
    $ licecomb doismellburning

### More verbose output

    $ licecomb -v doismellburning/licecomb
    SUCCESS: Found a license file in doismellburning/licecomb

### Check all of a user/organisation's repos

    $ licecomb doismellburning
    # TODO Provide sample output

### Ignore forked repositories

    $ licecomb --ignore-forks doismellburning

## Issues

* There are many ways of declaring a license; `licecomb` does not and cannot track them all (currently only looking for `/LICENSE`)
    * [License in README](https://github.com/stig/json-framework/)
    * [License in code files](https://github.com/johnezang/JSONKit/)
    * There's still the argument that having a `/LICENSE` file is A Good Thing To Do (there must be a pseudo-standard for this somewhere - it's certainly what GitHub now push at repository creation)
