# Featured Assets Playbook

Use this when creating LinkedIn Featured assets, proof-of-thinking documents, carousels, one-page lead magnets, or visual proof assets for a service provider.

## Purpose

The Featured section should help a profile visitor verify competence quickly. It should answer:

```text
What does this person do?
Who is it for?
What problem do they understand?
How do they think?
What is the next step?
```

## Proof Types

- Proof of thinking: frameworks, checklists, diagnostics, teardown posts, angle maps.
- Proof of process: workflows, demos, before/after flows, implementation phases.
- Proof of results: case studies, testimonials, metrics, client screenshots, portfolio work.
- Proof of trust: philosophy, principles, public talks, certifications, recommendation excerpts.

Early-stage service providers may start with proof of thinking and process. Add proof of results as soon as it is truthful and available.

## Five-Asset System

### 1. What I Build

Use as the flagship asset.

Structure:

1. Cover: named system and outcome
2. Who it is for
3. Problem it solves
4. Method or 5-step flow
5. What clients get
6. CTA

### 2. Diagnostic Checklist

Use as a lightweight lead magnet.

Structure:

1. Cover: checklist name
2. Score the current state
3. Most common leak
4. Better path
5. CTA

### 3. Angle Map

Use to show strategic thinking around content, messaging, or buyer psychology.

Structure:

1. Cover: angle map name
2. Example buyer context
3. Problem-aware angle
4. Objection-aware angle
5. Proof-aware angle
6. Urgency-aware angle
7. Comparison-aware angle

### 4. Flow Demo

Use to show the service in motion.

Structure:

1. Cover: flow demo name
2. Sequence overview
3. Step 1 sample
4. Step 2 sample
5. Step 3 sample
6. Step 4 sample
7. Step 5 sample and CTA

### 5. Philosophy Or Manifesto

Use to make the provider feel easier to trust.

Structure:

1. Cover: principle
2. Clear beats clever
3. Automation should reassure
4. One next step
5. Human before tool
6. Easy yes

## Design Rules

- Use a consistent visual system across all assets.
- Make covers readable at small LinkedIn preview size.
- Keep one idea per page.
- Prefer diagrams, cards, checklists, and flows over dense paragraphs.
- Avoid generic AI imagery, robot cliches, and cluttered futuristic visuals.
- Use strong contrast and generous spacing.
- Keep CTA consistent across assets.

## Captions

Each Featured asset should have a caption that tells the visitor why to open it.

Examples:

```text
What I build: a simple system for turning interest into booked conversations.
```

```text
A quick diagnostic for finding where warm leads lose momentum.
```

```text
Five content angles that help service businesses create attention that is easier to follow up with.
```

```text
A simple sequence for moving a warm inquiry from first message to booked call.
```

```text
Good automation should make the buying decision easier, not make the business sound less human.
```

## Configurable Generator

When the user wants a designed blue asset kit, copy or adapt:

```text
assets/featured-assets-template/example_config.json
```

Then run:

```bash
python scripts/generate_featured_assets.py --config path/to/config.json --out path/to/output
```

The script generates:

- Square PNG pages for carousel/image use
- Multi-page PDFs for LinkedIn document uploads
- A contact sheet for review

## Privacy Rule

Do not include private resumes, personal contact details, client names, unpublished metrics, screenshots, or confidential case studies in reusable or public assets without explicit confirmation.

