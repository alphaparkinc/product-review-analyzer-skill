# product-review-analyzer-skill

> **GenPark AI Agent Skill** -- Evaluates buyer review sentiment, highlighting strengths and fixes.

## Quick Start

```python
from client import ProductReviewAnalyzerClient
client = ProductReviewAnalyzerClient()
res = client.analyze(["Works perfectly but delivery was slow", "Best quality serum!"])
print(res["pros"])
```
