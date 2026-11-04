---
name: luminekit-agent-skills-maintainence
license: Proprietary. All rights reserved.
description: Create, revise, audit or retire agent skills and their supporting resources. Use for skill authoring and maintenance in any project or agent harness.
---

# Create and maintain agent skills

Follow the `luminekit-workflow` skill within this skill’s scope.

Use the target project's instructions and actual harness requirements for locations, names, metadata, licensing, installation and checks. This procedure applies to skills in any collection. Preserve existing invocation metadata; for new skills, keep the harness's normal discovery defaults unless the user chooses otherwise. Use a host-specific authoring skill only when its procedure is needed.

## Identify the useful guidance

Establish the capability, activation conditions, inputs, intended output, constraints and genuine dependencies. Inspect existing owners, resources and callers before changing them. Match depth to the task: a narrow edit needs a narrow change and relevant checks.

For a proposed behavioral rule or uncertain rewrite, observe a realistic task without the proposed guidance first. Add guidance for the demonstrated gap; a successful control supports omitting a new prescription. Existing user requirements can move to a new owner without inventing a failure or dropping the requirement. Retain the current version as the maintenance control.

## Write what changes a decision

- Assume a capable agent. Give outcomes and decision criteria; use fixed sequences or deterministic mechanics where deviation has a concrete cost. Retain non-obvious invariants and distinctions.
- Give each rule one owner. Keep only text that changes a decision; preserve information when consolidating duplicates. Prefer positive targets and observable conditions over prohibitions with exemptions.
- Name a sibling or external skill and the procedure needed at the point of dependency, in backticks rather than a link. Resolve the named dependency in the actual environment; naming it does not bundle or install it. A missing dependency leaves that part pending, while supported work continues.
- Leave skill selection, follow-on routing, work locations and project-check discovery to the agent and actual environment. Add a routing pointer only for an observed missed route.
- Make the name and description concise and discriminating: identify the capability and when it applies, with a boundary where nearby tasks could be confused. Keep detailed modes, tools and workflows in the body or relevant resources. A hard size ceiling is not an authoring target.

## Give each resource a reader task

Keep essential instructions in `SKILL.md` and conditional detail in references reachable from it, explaining when to read them. Every reference, script and asset needs an identifiable task: references supply task-specific knowledge, scripts automate demonstrably repeated mechanics or improve determinism, and assets support actual output. Create only resources that serve the task; empty scaffolds and copied manuals add no capability.

Keep one canonical skill body across harnesses, with its supporting resources in a self-contained bundle. Local resource links stay inside its folder. Check callers when changing shared resources, and ensure the reader can still reach the surviving owner after a move.

## Validate and maintain

For each meaningful removal, identify the surviving owner or evidence that the text is unnecessary. Shorter text alone does not establish preserved behavior. Preserve unrelated work and compare the actual diff, including new files and metadata.

Run the target's relevant metadata, name, resource, link and installation checks; execute affected scripts. For non-obvious deletions, guardrail rewrites, substantial new behavior or changed activation, use [behavioral checks](references/behavioral-checks.md). A small wording edit can finish with its affected content checks. Keep transient evaluation material outside the shipped bundle.

Correct causes demonstrated by use or feedback, then rerun affected checks. Update affected callers and the target's catalog, installation or development owners. For retirement, resolve callers before removing the procedure or its resources. Report structural checks, observed agent behavior and unverified coverage separately; publication and live operations retain their own authorization scope.
