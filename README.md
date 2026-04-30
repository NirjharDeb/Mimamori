# Mimamori
Mimamori (見守り), named after the Japanese word for watchful care and protective oversight, contains the Cursor rules and user task workflows used to evaluate human oversight and control of agentic AI behavior in AI-powered IDEs!

## Relevant Repository Contents
### Cursor Rules:
- `.cursor/rules`: Cursor Rules are instructions for the agent in the Cursor IDE that guide its responses. This folder always contains the active rule.
- `study/conditions`: These are the three different "rulesets" or "control cards" that guides how our Agent responds to the user's request to implement some functionality. Currently, we have the following control cards:
  - `baseline`: Does not show any control card, so the agent does not have any "pre-review" step prior to making code changes).
  - `light-control-card`: Shows a simple control card and then continues with code change normally.
  - `structured-review-card`: Shows a control card that shows much more information and requires the user to explicitly "acknowledge" it before the agent continues with code changes.
- `scripts`: Contains a script to automatically set which type of control card we want to set active.

### User Task:
- `seeded`: Contains a Python security authentication task (with unit tests) that has seeded traps the user must debug and resolve with the help of Cursor's LLM agent. Each user was either assigned the condition of no control card (baseline), light control card, or a strong control card (structured review card).
- `golden`: Contains the correct, perfect version of the coding task that users are given to solve. During the experiment, the LLM does NOT have access to the golden folder (otherwise it could cheat!).
