---
claim: "<atomic, verifiable statement>"
sources: ["<url / file / test>"]
source_type: primary   # primary | secondary | anecdote
verified: YYYY-MM-DD
expires: YYYY-MM-DD    # only for volatile facts (versions, APIs, prices); null if not applicable
status: current        # current | disputed | superseded
superseded_by: null    # "[[note]]" if applicable
scope: general         # general | profile-<x> | project-<x>
---
Context notes (optional).
