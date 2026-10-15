# FalconX Agent Layer — Prototype

A small Python demonstration of request classification, rule-based decisions and local JSON logging.

## What the implementation does

`agent/agent_layer.py` classifies message/action text with English keyword checks and returns an `ALLOW`, `REVIEW` or `BLOCK` label. It records the input, classification and decision in a local log. The optional `human_approval` input is a Boolean supplied by the caller.

## Run the example

```sh
python3 test_agent_layer.py
```

Python standard library only. The example prints a decision for a trading-related request and writes a local log. Despite its filename, it is a demonstration script, not an assertion-based test suite.

## Important implementation boundaries

This prototype does not invoke, intercept or authorize real tools. Its keyword checks are not a prompt-injection defense or an authentication mechanism. Unknown requests can receive an `ALLOW` label under the current rules; the label must not be used as a production authorization boundary. The caller-provided approval Boolean does not verify a human identity. Local logs may contain supplied message text and are not tamper-proof.

Production integration would need independently enforced tool permissions, argument validation, authenticated approval where required, suitable data handling and tests against the actual execution path.

## Reviewable workflow example

For a separate Python/SQLite example with explicit approval scope, transactional changes and replay checks, see the [CRM demonstration](https://github.com/albdrani37-hash/FalconX/tree/main/examples/crm-review-demo) and [selected technical portfolio](https://github.com/albdrani37-hash/FalconX/blob/main/PORTFOLIO.md).
