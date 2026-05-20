# LinkedIn Profile Optimizer Skill

LinkedIn is no longer just a digital resume. It is a search surface, a credibility layer, and a professional publishing channel. This skill helps Codex rebuild a LinkedIn presence with the same discipline a strong strategist, recruiter, copywriter, and content operator would bring to the work.

The goal is simple: turn scattered career history, projects, proof, and ambition into a LinkedIn profile that is easier to find, easier to trust, and easier to act on.

## Purpose

`linkedin-profile-optimizer` is a reusable Codex skill for auditing, rewriting, and operationalizing LinkedIn profiles. It is built for people who want their profile to work harder for a specific outcome: job opportunities, client leads, founder credibility, executive visibility, consulting authority, creator growth, or professional partnerships.

The skill combines four layers:

- **Positioning**: define the market category, audience, offer, and proof
- **LinkedIn SEO**: map target keywords into the right sections without stuffing
- **Trust architecture**: strengthen Featured assets, recommendations, skills, verification, and proof
- **Content strategy**: turn expertise into repeatable posts, pillars, and professional authority signals
- **Proof assets**: turn positioning into Featured carousels, checklists, diagnostics, and flow demos

## Goals

- Create LinkedIn profiles that communicate clear professional identity within seconds
- Improve recruiter, client, and partner discoverability through truthful keyword strategy
- Replace generic self-description with evidence, outcomes, and proof of work
- Build profiles that support both inbound search and outbound credibility
- Keep the process reusable, source-aware, and adaptable as LinkedIn changes
- Separate durable profile strategy from temporary algorithm tactics
- Help users move from "I need a better profile" to a complete implementation package

## Objectives

This skill is designed to produce:

- A full LinkedIn audit with scoring, gaps, and priorities
- A rebuilt headline, About section, experience section, skills strategy, and Featured plan
- A recruiter or client-facing keyword map based on target roles, job descriptions, or market briefs
- A client-flow positioning direction for service providers with tool-heavy or scattered offers
- A Featured asset kit with strategy, captions, upload order, and optional generated visuals
- Recommendation request messages that ask for specific credibility, not vague praise
- Content pillars and post ideas aligned with the user's positioning
- A profile implementation checklist that keeps facts, claims, and proof aligned
- A current-source refresh habit for LinkedIn features, skills, verification, and platform guidance

## What Makes It Different

This is not a pile of LinkedIn tips. It is an operating workflow.

The skill treats a profile as a system:

1. **Search**: Can the right people find the profile?
2. **Signal**: Can they quickly understand what the person does?
3. **Proof**: Can they verify competence without guessing?
4. **Conversion**: Do they know what action to take next?
5. **Reinforcement**: Does recent content support the same professional story?

## Repository Contents

- [`SKILL.md`](SKILL.md): the Codex workflow and triggering instructions
- [`references/official-linkedin.md`](references/official-linkedin.md): official source layer and refresh rules
- [`references/expert-stack.md`](references/expert-stack.md): expert lenses for profile writing, SEO, recruiting, and content
- [`references/profile-templates.md`](references/profile-templates.md): reusable drafting formulas and section patterns
- [`references/audit-scorecard.md`](references/audit-scorecard.md): scoring rubric and acceptance criteria
- [`references/client-flow-positioning.md`](references/client-flow-positioning.md): service-offer positioning method
- [`references/featured-assets-playbook.md`](references/featured-assets-playbook.md): Featured proof asset strategy
- [`scripts/linkedin_keyword_map.py`](scripts/linkedin_keyword_map.py): lightweight keyword gap analysis helper
- [`scripts/generate_featured_assets.py`](scripts/generate_featured_assets.py): configurable LinkedIn Featured asset generator
- [`assets/featured-assets-template/example_config.json`](assets/featured-assets-template/example_config.json): anonymized sample config
- [`agents/openai.yaml`](agents/openai.yaml): Codex/OpenAI-facing skill metadata

## How To Use

Install or place this folder where Codex can discover skills, then invoke:

```text
Use $linkedin-profile-optimizer to audit and rebuild my LinkedIn profile for my target opportunity.
```

For keyword analysis, save target job descriptions or client briefs as text files and run:

```bash
python scripts/linkedin_keyword_map.py --jobs job1.txt job2.txt job3.txt --profile profile-draft.txt
```

The script is intentionally lightweight. Its output should guide human judgment, not replace it. A keyword belongs in the profile only when it is true, relevant, and supported by evidence.

To generate a blue Featured asset kit from the included anonymized example:

```bash
python scripts/generate_featured_assets.py --config assets/featured-assets-template/example_config.json --out featured-assets-output
```

This creates:

- square PNG pages for carousel/image use
- multi-page PDFs for LinkedIn document uploads
- a contact sheet for quick review

## What To Do Next

Start with a concrete target. The skill works best when it knows what the profile is supposed to win.

Give Codex:

- A LinkedIn URL, exported profile text, screenshots, or a resume
- The primary goal: job offers, clients, consulting leads, founder credibility, executive visibility, or audience growth
- Target roles, industries, client types, or 3 to 10 job descriptions/client briefs
- Proof: metrics, projects, portfolio links, testimonials, shipped work, awards, certifications, or case studies
- Constraints: private clients, claims to avoid, tone preferences, or markets you do not want to target

Then ask for one of these outputs:

- **Audit**: score the current profile and identify the highest-impact fixes
- **Profile Rewrite**: produce copy-paste-ready LinkedIn sections
- **SEO Pack**: map target keywords into profile sections and identify gaps
- **Content Pack**: create content pillars, post ideas, and authority-building direction
- **Featured Asset Kit**: create proof assets, captions, and optional PNG/PDF exports
- **Full Rebuild**: combine audit, rewrite, SEO, Featured strategy, recommendations, and content plan

The normal flow is:

1. Audit the current profile
2. Choose the positioning direction
3. Build the keyword map
4. Rewrite the profile sections
5. Add proof assets to Featured
6. Request targeted recommendations
7. Publish content that reinforces the same positioning

## Boundary

This repository should stay generic. Do not commit private resumes, personal LinkedIn exports, client names, unpublished case studies, or confidential career documents here. Keep personal profile rebuild work in a separate private workspace.

Generated assets should also be checked before publishing. Remove private contact details, confidential metrics, client names, and anything the user has not explicitly approved.

## North Star

A strong LinkedIn profile should make the right person think:

> I understand what this person does, I believe they can do it, and I know why I should contact them.
