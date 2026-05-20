---
name: linkedin-profile-optimizer
description: Optimize, audit, rebuild, or create LinkedIn profiles and LinkedIn content strategy for job search, consulting, founder, executive, creator, sales, or recruiting goals. Use when rewriting a LinkedIn headline, About section, experience bullets, skills, Featured section, recommendations plan, recruiter/client SEO keyword strategy, profile audit, or content pillars/calendar.
---

# LinkedIn Profile Optimizer

## Overview

Use this skill to turn a user's career history, offers, proof, and target market into a high-signal LinkedIn profile and content system. Treat LinkedIn as three things at once: a search index, a trust surface, and a publishing channel.

Do not treat tactical algorithm advice as permanent. For current platform behavior, refresh official LinkedIn sources and label any expert or market guidance as tactical inference.

## Inputs To Collect

Collect only what is needed for the user's goal:

- Current LinkedIn URL, exported text, screenshots, resume, portfolio, or rough work history
- Target outcome: recruiters, clients, investors, partners, audience growth, sales leads, or authority
- Target roles, industries, geographies, seniority, compensation/rate, and work style
- 3 to 10 target job descriptions, client briefs, or competitor profiles when SEO matters
- Proof: metrics, projects, links, awards, shipped work, case studies, media, testimonials
- Constraints: confidentiality, tone, industries to avoid, claims that must not be made

If the user asks for direct browser editing, draft first and get confirmation before saving/publishing changes.

## Workflow

1. Define the strategic frame.
   - Name the primary audience and the action they should take.
   - Choose one positioning lane before writing: job-market candidate, consultant, founder, executive, technical expert, creator, or sales/BD operator.
   - Identify the strongest proof and the most important missing proof.

2. Build the keyword map.
   - Prefer 3 or more target job descriptions or client briefs.
   - Extract role titles, domain nouns, tools, methods, outcomes, industries, credentials, and seniority signals.
   - Use `scripts/linkedin_keyword_map.py` for a first-pass gap analysis when text files are available.
   - Place important keywords naturally across headline, About, experience, skills, projects, education, certifications, and Featured captions. Avoid keyword stuffing.

3. Audit the current profile.
   - Use `references/audit-scorecard.md`.
   - Score positioning, search relevance, proof, trust, completeness, readability, and conversion.
   - Separate factual gaps from writing gaps.

4. Rebuild the profile architecture.
   - Headline: searchable identity plus specific value and proof.
   - Banner: visual positioning signal, not generic decoration.
   - About: clear narrative, proof, specialties, credibility, and call to action.
   - Experience: outcome-first bullets with scope, tools, and business context.
   - Featured: proof assets that let the audience verify competence quickly.
   - Skills: prioritize up to 100 relevant skills, with top visible skills aligned to the target.
   - Recommendations: request specific credibility from credible people.
   - Activity/content: reinforce the same expertise the profile claims.

5. Create the content engine when requested.
   - Define 3 to 5 content pillars tied to the user's offer, expertise, proof, and point of view.
   - Mix authority posts, project breakdowns, lessons, opinionated analysis, social proof, and practical teaching.
   - Optimize for useful professional knowledge, not generic engagement bait.

6. Deliver an implementation package.
   - Provide copy-paste-ready profile sections.
   - Include a keyword placement map.
   - Include before/after rationale if useful.
   - Include a checklist for manual LinkedIn updates.
   - Include 10 to 30 post ideas if content strategy is in scope.

## Source Refresh

Read `references/official-linkedin.md` when:

- The user asks for current best practices, algorithm guidance, profile limits, or platform rules.
- The work affects skills, creator tools, verification, AI-assessed skills, or public visibility.
- You are about to state a specific LinkedIn limit, such as character counts or maximum skills.

Use official LinkedIn sources for platform rules. Use `references/expert-stack.md` for practitioner lenses and benchmark heuristics.

## Drafting Standards

- Lead with the user's strongest market category, not a vague personality claim.
- Prefer concrete nouns and proof over adjectives.
- Make the first 2 lines of About strong enough to earn the click to "see more."
- Translate responsibilities into outcomes, scope, customers, systems, money, speed, quality, risk, or growth.
- Keep claims verifiable. Do not invent metrics, credentials, clients, employers, education, endorsements, awards, or certifications.
- Write in the user's voice, but remove hedging, clutter, and generic "passionate about" phrasing.
- Build for scanability: short sections, tight bullets, and repeated keyword themes without repetition fatigue.

## Output Shapes

Choose the smallest complete output for the task:

- `Audit`: scorecard, top risks, quick wins, and rewrite priorities.
- `Profile Rewrite`: headline, About, experience, skills, Featured, recommendations, and implementation checklist.
- `SEO Pack`: keyword map, placement plan, missing proof, and job/client alignment notes.
- `Content Pack`: positioning statement, content pillars, post formats, first 10 to 30 post ideas, and engagement rules.
- `Full Rebuild`: all of the above plus a 30-day execution plan.

## References

- `references/official-linkedin.md`: official LinkedIn sources and durable takeaways.
- `references/expert-stack.md`: profile, SEO, recruiter, and content experts to synthesize.
- `references/profile-templates.md`: reusable formulas for profile copy and content.
- `references/audit-scorecard.md`: scoring rubric and acceptance criteria.

## Verification

Before claiming a rebuild is ready:

- Confirm every factual claim is supported by user-provided evidence or clearly marked as a placeholder.
- Check top keywords appear in headline, About, current experience, skills, and at least one proof asset when truthful.
- Check the profile has a clear next action for the target audience.
- Check the tone fits the user's market: recruiter-facing, client-facing, executive, founder, creator, or technical.
- Check that algorithm or SEO advice is dated and sourced when it depends on current platform behavior.
