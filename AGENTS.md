# AI-TDD Working Agreement

1. Start with a test list, then implement exactly one concrete test.
2. Confirm that the new test fails for the expected behavioral reason. Import, syntax, and environment failures are not valid RED evidence.
3. Change production code only while a relevant test is failing.
4. During GREEN, never delete, skip, weaken, or rewrite the failing test.
5. Write only enough production code to make the current test pass.
6. Run the focused test first and the full suite immediately afterward.
7. Refactor only while every test is green, add no new behavior, and run the full suite afterward.
8. Record the RED, GREEN, and REFACTOR evidence for each cycle.
