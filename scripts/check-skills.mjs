import { readdir, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { parse } from 'yaml';

const root = new URL('../skills/', import.meta.url);
const entries = await readdir(root, { withFileTypes: true });
const directories = entries.filter((entry) => entry.isDirectory());
const errors = [];
const allowedFields = new Set([
  'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools',
]);

if (directories.length === 0) errors.push('No skill directories found.');

for (const directory of directories) {
  const path = new URL(`${directory.name}/SKILL.md`, root);
  const report = (message) => errors.push(`${fileURLToPath(path)}: ${message}`);

  try {
    const content = await readFile(path, 'utf8');
    const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/.exec(content);
    if (!match) {
      report('Expected YAML frontmatter followed by skill instructions.');
      continue;
    }

    const data = parse(match[1]);
    if (!data || typeof data !== 'object' || Array.isArray(data)) {
      report('Frontmatter must be a mapping.');
      continue;
    }

    const { name, description, license, compatibility, metadata } = data;
    if (typeof name !== 'string' || name.length > 64 ||
        !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) || name !== directory.name) {
      report('name must match its directory and be a lowercase, hyphenated identifier of 1–64 characters.');
    }
    if (typeof description !== 'string' || !description.trim() || description.length > 1024) {
      report('description must be a nonempty string of at most 1024 characters.');
    }
    if (license !== 'Proprietary. All rights reserved.') {
      report('Include the collection’s rights-reserved license notice.');
    }
    if (compatibility !== undefined &&
        (typeof compatibility !== 'string' || !compatibility.trim() || compatibility.length > 500)) {
      report('compatibility must be a nonempty string of at most 500 characters.');
    }
    if (metadata !== undefined && (!metadata || typeof metadata !== 'object' ||
        Array.isArray(metadata) || Object.values(metadata).some((value) => typeof value !== 'string'))) {
      report('metadata must map keys to strings.');
    }
    if (data['allowed-tools'] !== undefined && typeof data['allowed-tools'] !== 'string') {
      report('allowed-tools must be a string.');
    }
    for (const field of Object.keys(data)) {
      if (!allowedFields.has(field)) report(`Unknown frontmatter field: ${field}`);
    }
    if (!match[2].trim()) report('Skill instructions must not be empty.');
  } catch (error) {
    report(error.message);
  }
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`Validated ${directories.length} skills.`);
}
