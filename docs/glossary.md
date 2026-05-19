# Glossary

## World Ontology

The hidden causal structure of a simulated world.

Defines:
- what entities exist
- hidden and observable variables
- relationships
- systems
- causal mechanisms
- rules of the world

The world ontology represents how reality actually works inside a case.

---

## Simulated Case

A generated scenario created from the world ontology.

A case contains:
- entities
- events
- hidden state
- observable evidence
- ground truth

Example:
A company with declining customer satisfaction causes by hidden product instability.

---

## Observed  Ontology

The semantic layer exposted to the reasoner.

Defines:
- available datasets
- fields and meanings
- observable relationships
- evidence semantics
- allowed interpretations

The observed ontology may only expose part of the underyling world.

---

## Evidence

Observable records, events, or measurements produced by a simulated case.

Evidence does not explain itself.

Examples:
- support tickets
- login events
- invoices
- usage metrics
- customer records

---

## Claim

An explicit statement produced by a reasoning system.

Claims may be:
- correct
- partially correect
- incorrect
- uncertain

Example:
"Customers experiencing repeated login failures are more likely to to churn."


---

## Belief 

A confidence-weighted internal stance toward one or more claims.

Beliefs evolve as new evidence is observed.

A belief may contain:
- confidence
- supporting evidence
- contradicting evidence
- reasoning traces

---

## Reasoner

A system that investigates evidence and produces claims and beliefs.

A reasoner may:
- query evidence
- form hypotheses
- update beliefs
- evaluate uncertainty 
- construct explanations

--- 

## Ground Truth

The hidden answer key of a simulated case.

Ground truth contains:
- true causal mechanisms
- hidden variables
- true explanations
- expected outcomes

Ground truth is used for evaluation and benchmarking.

--- 

## Evaluation

The process of comparing reasoner outputs against ground truth.

Evaluation may measure:
- causal accuracy
- evidence usage
- calibration
- explanation quality
- reasoning consistency

--- 

## Observable State

State exposed to the reasoner through evidence and the observed ontology.


---

## Hidden State

State that exists in the simulated world but is not directly observable.

Hidden state often drives the true causal behavior of a case.


---

## Causal Mechanism 

A rule or process that explains how one variable influences another inside the world.

Example:
Repeated product failures increase customer frustration. 


--- 

## Reasoning Trace

A structured representation of how a reasoner arrived at a claim or belief.

May include:
- evidence references
- intermediate hypothesis 
- confidence updates 
- causal chains