## QUESTIONS:
- What are the use cases?
  - Anyone can run anytime? Via cmd line? Via web page?
  - Monitoring?  Cron running every X minutes
  - Daycrew checkout?
- Web view?
  - All instruments panel green/yellow/red at a glance?  K1/K2
  - Click instr to get detailed list of tests pass/fail?
  - Show when last test was run (recent/old icon)?
- Are we merging ct and ctx into this as well?
- If an original testAll script has test groups commented out or ignored, should we include but comment out in config?


## TODO
- Create test configs for all instruments:
  instr    done?    who?     engacct      server          kpy3?
----------------------------------------------------------------
  NIRSPEC  [done]  (josh)     nspeceng    nirespecserver    y
  KCWI     [done]  (josh)     kcwieng     kcwiserver        y
  NIRES    [90%]   (josh)     nireseng    niresserver1      NO
  LRIS     [70%]   (josh)     lriseng     lrisserver        NO
  NIRC2            (josh)     nirc2eng    nirc2server       NO
  MOSFIRE          (lucas)    moseng      mosfireserver     NO
  ESI              (lucas)    esieng      esiserver         NO
  HIRES            (lucas)    hireseng    hiresserver       NO    
  DEIMOS           (matt)     dmoseng     deimosserver      y
  OSIRIS           (matt)     osrseng     osirisserver      NO

- NIRC2: Needs ssh key
- NIRC2: Has issues with ktl module crashing.  Needs new ktl build?
- NIRC2: Has several issues with fitting to this standardized model.
- NIRC2: Implement 'exit' test option to exit on failure?  How does this affect JSON, db, etc?
- NIRC2: Implement dependency tests for other tests that only run if the other one passed? 
- NIRES: Leach boards test in orig testAll looks incorrect to me. fgrep will not return status of 110 right? Or does it just return the status of the last failed command? https://stackoverflow.com/questions/37126964/get-exit-code-when-piping-into-grep-v
- NIRES: vm-nires cannot access 'acs' ktl service but niresserver1 can.
- LRIS: 'power' group tests is problematic.  But can be distilled to a list of show tests.  However, is the "powerNN" index dynamic?  Also, the fix is at the group level.  How would we handle auto fix?
- LRIS: look at 'test_stage' test call.  Not handling output the same way.  Need a stdout vs errout?
- LRIS: show/ktl for 3 glycol keywords not working
- LRIS: 'blue windowing' group (uses AND/OR and has parsing issues)
- HIRES: needs server specific added to ps calls

- Use glob matching with '*' for pattern matches
- Implement "fix" option (aka $act)
- Add extra level to config for instrument specific things like 
  -- KCWI's 'msg':'Please visually check Glycol flow. This script only checks glycol pump power.'  
  -- And, correct host, and user to run as. 
  -- Also, define host to ssh to for all commands if not run on that server?
- Implement "BEL" character for sound?



## ISSUES (low priority)
- Ask SAs which tests are still relevant and any new tests desired.
- Might be better to get rid of sshkey test and just handle that failure explicitily in the other tests.
- better error handling in case some typos are put in config (ie wrong backtick show val)
- KCWI: Has hard-coded -273.15 kelvin offset for 'tmp' show keywords.  I converted these in config. So output units are different.  Is this ok?
- NIRES: Revert back to 'temps' full call. ie bad idea to have temps ranges in two places in case values change?
- NIRES: get_nires_pid seems to have a bug with outval (only looking for 1 or 2 results)?  Fixed here.
- NIRES: If daemon not running, message is to start it.  If it is running incorrectly(ie ps count== 1), message is to inform the SA.  We did not not implement this level of detail.
- Some orig testAll alphabetize group tests (ie KCWI).
- Some orig testAll have server and readable name listed together (ie KCWI)
- yaml requires a '.' before 'e' in exponential notation.  Either document or switch to json parse.
- Option to write test results to DB.  Grant access issues, only run this option from vm-webtools?


## EXTERNAL SCRIPT CALLS
- NIRES: tdl, testRotator, temps*
- LRIS: tdl, test_stage


## NOTES
- Some pings only work from instrument vm so we have to use ssh.
- Some servers have different versions of ping that require different params, so we use script call in some cases.
- KCWI: ktl can't access kcwi.lastalive on vm-kcwi so we used kcwi.kt1salive.  We could fix ktl keyword config.
- psutil cannot be used for remote calls so we are not pursuing this (https://github.com/giampaolo/psutil/issues/336)
- The '-' on ps commands is important on some servers depending on OS/version
- NIRSPEC used a show command for val for currinst check. kcwi just hardcodes to 'KCWI'.  Changed NIRSPEC to match.
- NIRES: Can we avoid use of testRotators and use caget calls instead?  We'd need an OR test though.
