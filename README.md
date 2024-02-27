# testall
Check basic functionality of Keck instrument systems.  
(NOTE: This is a Python port of Keck testAll instrument test scripts into one shared code base.)



## Running script

usage examples: 

    testall.py 
    testall.py --instr hires
    testall.py --instr kcwi --systems computers daemons
    testall.py --datadir /kroot/rel/default/data/

positional arguments:

    NONE

optional arguments:

    --instr     Instrument to test.  Default is INSTRUMENT environment var. 
    --datadir   Directory containing tests config files.  Default is env var $RELDIR/data/ or /data/ dir in source directory.
    --systems   List of systems groups to test.


## Config setup
Create a file named testAll-[instrument].yaml in your datadir that contains json defining groups of tests.  For example:

    {
      "computers":
      [
        {"name":"NIRES host",   "check":"ping",  "server":"niresserver1"},
        {"name":"VNC server",   "check":"ping",  "server":"vm-nires"},
      ],
      'daemons':
      [
        {"name":"nsds",  "check":"ps",   "flags":"auxww",  "pattern":"nds_service",   "excludes":["get_nires_pid", "getKeywords"],  "server":"niresserver2"},
      ]
      'keywords':
      [
        {"name":"CCR 350",              "check":"show",  "service":"nsdewar",  "keyword":"ccr350val",    "minval": 11.0,  "maxval": 19.0 },
        {"name":"SPEC ready to expose", "check":"show",  "service":"nspec",    "keyword":"ready",        "val": 1,      "errtype":"warn" },
      ]
    }


## Test types
There are four types of tests: ping, ps, show, and script.

Common params for all tests:
- "check": The type of check ['ping', 'ps', 'show', 'script']
- "name": (optional) Human readable name of test.
- "errtype": (optional) "error" or "warn".  Default is "error".
- "errmsg": (optional) Extra message to display if test does not pass.
- "fixmsg": (optional) Instructions to fix problem if test does not pass.
- "exit": (optional) "group" or "all". If set, will exit test group or all tests.


### "ping": Pings a host
  - "server": hostname of server

  examples:
  
    {"name":"NIRES host",   "check":"ping",  "server":"niresserver1"},
    {"name":"VNC server",   "check":"ping",  "server":"vm-nires"},


### "ps": Checks for running process
  - "flags": ps flags
  - "pattern": Pattern or array of patterns to match (assume AND)
  - "excludes": (optional) Array of patterns to exclude matching (assume OR)
  - "server": (optional) Server to run this check (assumes ssh key installed)
  - "num": (optional) How many instances to find to pass test.  Default passes with finding any number.

  examples:
  
    {"name":"ngs" ,  "check":"ps",   "flags":"auxww",  "pattern":"nires_service", "excludes":["get_nires_pid", "getKeywords"]},
    {"name":"nsds",  "check":"ps",   "flags":"auxww",  "pattern":"nds_service",   "excludes":["get_nires_pid", "getKeywords"],  "server":"niresserver2"},

### "show": Call KTL keyword show and check value
  - "service": KTL service to query
  - "keyword": KTL service keyword to query
  - "val": (optional) Show value to compare to pass test.  If array provided, then assume OR logic on array.  If string starts and ends with backticks then that command is executed to get val.
  - "minval": (optional) Min val of range
  - "maxval": (optional) Max val of range.
  - "thresh": (optional) If minval and maxval provided, then this range is expanded by thresh.
  - "lock": (optional) Additional lock keyword to check for value 'unlocked' in order for test to pass.
  
  (NOTE: If no val, minval, or maxval is given, the test will pass if the command returns a status of 0.)

  examples:
  
    {"name":"CCR 350",              "check":"show",  "service":"nsdewar",  "keyword":"ccr350val",    "minval": 11.0,  "maxval": 19.0 },
    {"name":"SPEC ready to expose", "check":"show",  "service":"nspec",    "keyword":"ready",        "val": 1,      "errtype":"warn" },
    {"name":"SCAM ready to expose", "check":"show",  "service":"nscam",    "keyword":"ready",        "val":"Yes",   "errtype":"warn" },
    {"name":"nscam.PSCALE",         "check":"show",  "service":"nscam",    "keyword":"pscale",       "val": [0.158, 0.0149] },
    {"name":"SPEC detector temp",   "check":"show",  "service":"nsdewar",  "keyword":"spectemp1val", "minval":"`show -s nsdewar -terse specheattrg`",  "maxval":"`show -s nsdewar -terse specheattrg`",  "thresh": 0.1,  "errtype":"warn"},


### "script": Calls any script or command and gets stdout and status.
  - "cmd": Command to execute.
  - "val": (optional) Value to compare stdout to pass test.
  - "pattern": (optional) Pattern to match in script output to pass test.
  - "status": (optional) Status value to compare status to pass test.
  - "stdout": (optional) Set to 1 to dump stdout if test fails

  examples:
  
    {"name":"H1 leachboard",  "check":"script",   "cmd":"tdl 1122 | fgrep Returned > /dev/null",    "status": 110},
    {"name":"power switches", "check":"script",   "cmd":"testRotator | fgrep ERROR",  "status": 1,  "errmsg":"Rotator is not Ready\n"},

    #NOTE: grep returns non-zero status of 1 if grep finds nothing. This can be used for tests looking for non-existance of words like 'ERROR'.


### "sshkey": Tests ssh key
  - "user": username
  - "server": hostname of server
  - "keypath": Path to ssh private key

  examples:
  
    {"check":"sshkey",  "user"":"kcwieng",   "server":"kcwiserver",  "keypath":"/home/kcwieng/.ssh/id_rsa"},


## Interpreting results
The return value is a json string of an dictionary containing the following results:

    {
      instr:      Name of instrument tested
      timestamp:  Time of test
      num_pass:   Number of tests passed
      num_warn:   Number of tests failed as warning
      num_error:  Number of tests failed as error
      tests:      Full copy of test config object with two keywords added per test:  
                    ok: Did test pass
                    err: Message if test failed  
    }

If there is a fatal error, you will only get json response like this:
    {'fatal_error': "[Error message]"}
