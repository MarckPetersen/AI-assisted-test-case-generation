# AI-assisted-test-case-generation
The basic idea is to take a set of requirements or another defined test basis and generate relevant test cases according to the test level, test objectives, product criticality and risk we want to address.

## Starter implementation

Flow: Requirements → criticality & risk → test level & objectives → AI-assisted design → test cases → traceability → results → exit criteria.

- `tcgen/risk.py` – risk score (likelihood × criticality) decides technique and depth; ISTQB level objectives.
- `tcgen/generator.py` – builds ISTQB-style prompts and creates traceable test cases. Pass a `designer` callable to plug in an LLM.
- `tcgen/traceability.py` – requirement→test matrix and exit-criteria evaluation.

Run tests: `python -m unittest discover tests`
