import { readdir, readFile } from 'node:fs/promises';
import { dirname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'yaml';

// Usage: check-skills.mjs [skills-root] [skill-name ...]
// With names, only those skills are checked and only they may be named.
const [rootArgument, ...selected] = process.argv.slice(2);
const root = resolve(rootArgument ?? fileURLToPath(new URL('../skills/', import.meta.url)));
const entries = await readdir(root, { withFileTypes: true });
const names = selected.length ? selected
  : entries.filter((entry) => entry.isDirectory()).map((entry) => entry.name);
const known = new Set(names);
const errors = [];
const allowedFields = new Set([
  'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools',
]);

if (names.length === 0) errors.push('No skill directories found.');

async function files(directory) {
  const result = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    const path = join(directory, entry.name);
    if (entry.isDirectory()) result.push(...await files(path));
    else result.push(path);
  }
  return result;
}

// Code is excluded so that examples of links or names are not treated as references.
function prose(markdown) {
  return markdown.replace(/^(```|~~~)[^\n]*\n[\s\S]*?^\1[^\n]*$/gm, '').replace(/`[^`\n]*`/g, '');
}

function localTargets(markdown) {
  const targets = [];
  const text = prose(markdown);
  const patterns = [/\]\(\s*<?([^)\s>]+)>?(?:\s+["'(][^)]*)?\)/g, /^\s*\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)/gm];
  for (const pattern of patterns) {
    for (const [, target] of text.matchAll(pattern)) {
      if (/^[a-z][a-z0-9+.-]*:/i.test(target) || target.startsWith('#') || target.startsWith('//')) continue;
      targets.push(decodeURI(target.split('#')[0]));
    }
  }
  return targets;
}

for (const name of names) {
  const directory = join(root, name);
  const entry = join(directory, 'SKILL.md');
  const report = (path, message) => errors.push(`${path}: ${message}`);

  try {
    const content = await readFile(entry, 'utf8');
    const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/.exec(content);
    if (!match) {
      report(entry, 'Expected YAML frontmatter followed by skill instructions.');
      continue;
    }

    const data = parse(match[1]);
    if (!data || typeof data !== 'object' || Array.isArray(data)) {
      report(entry, 'Frontmatter must be a mapping.');
      continue;
    }

    const { name: declared, description, license, compatibility, metadata } = data;
    if (typeof declared !== 'string' || declared.length > 64 ||
        !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(declared) || declared !== name) {
      report(entry, 'name must match its directory and be a lowercase, hyphenated identifier of 1–64 characters.');
    }
    if (typeof description !== 'string' || !description.trim() || description.length > 1024) {
      report(entry, 'description must be a nonempty string of at most 1024 characters.');
    }
    if (license !== 'Proprietary. All rights reserved.') {
      report(entry, 'Include the collection’s rights-reserved license notice.');
    }
    if (compatibility !== undefined &&
        (typeof compatibility !== 'string' || !compatibility.trim() || compatibility.length > 500)) {
      report(entry, 'compatibility must be a nonempty string of at most 500 characters.');
    }
    if (metadata !== undefined && (!metadata || typeof metadata !== 'object' ||
        Array.isArray(metadata) || Object.values(metadata).some((value) => typeof value !== 'string'))) {
      report(entry, 'metadata must map keys to strings.');
    }
    if (data['allowed-tools'] !== undefined && typeof data['allowed-tools'] !== 'string') {
      report(entry, 'allowed-tools must be a string.');
    }
    for (const field of Object.keys(data)) {
      if (!allowedFields.has(field)) report(entry, `Unknown frontmatter field: ${field}`);
    }
    if (!match[2].trim()) report(entry, 'Skill instructions must not be empty.');

    // Each skill is a self-contained bundle: links stay inside its folder,
    // its resources are reachable from its entry, and siblings are named, not linked.
    const all = await files(directory);
    const links = new Map();
    for (const path of all.filter((file) => file.endsWith('.md'))) {
      const markdown = await readFile(path, 'utf8');
      const targets = [];
      for (const target of localTargets(markdown)) {
        const resolved = resolve(dirname(path), target);
        if (resolved !== directory && !resolved.startsWith(directory + sep)) {
          report(path, `Link leaves the skill folder: ${target}. Name the other skill instead.`);
        } else {
          targets.push(resolved);
        }
      }
      links.set(path, targets);
      for (const [mentioned] of markdown.matchAll(/\bluminekit-[a-z0-9]+(?:-[a-z0-9]+)*/g)) {
        if (!known.has(mentioned)) report(path, `Names an unknown or unselected skill: ${mentioned}`);
      }
    }

    const reached = new Set([entry]);
    const queue = [entry];
    while (queue.length) {
      for (const target of links.get(queue.pop()) ?? []) {
        if (!reached.has(target)) {
          reached.add(target);
          queue.push(target);
        }
      }
    }
    for (const path of all) {
      if (!reached.has(path)) {
        report(path, `Not reachable from ${relative(root, entry)} through links inside the skill.`);
      }
    }
  } catch (error) {
    report(entry, error.message);
  }
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`Validated ${names.length} skills.`);
}
