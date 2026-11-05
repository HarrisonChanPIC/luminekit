import assert from 'node:assert/strict';
import { lstat, mkdtemp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, relative } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const source = fileURLToPath(new URL('../', import.meta.url));
const installer = join(source, 'node_modules/skills/bin/cli.mjs');
const remark = join(source, 'node_modules/remark-cli/cli.js');
const checkSkills = join(source, 'scripts/check-skills.mjs');
const config = join(source, '.remarkrc.json');
const agents = ['claude-code', 'codex', 'qoder'];
const destinations = ['.claude/skills', '.agents/skills', '.qoder/skills'];
const docs = [
  'luminekit-workflow', 'luminekit-docs-adopt', 'luminekit-docs-review',
  'luminekit-docs-maintain', 'luminekit-continue',
];
const authoring = ['luminekit-agent-skills-maintainence', 'luminekit-workflow', 'luminekit-arena'];
const grill = ['luminekit-grill'];
const all = (await readdir(join(source, 'skills'), { withFileTypes: true }))
  .filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
const temporary = await mkdtemp(join(tmpdir(), 'luminekit-install-'));
const env = { ...process.env, DISABLE_TELEMETRY: '1', NO_COLOR: '1' };

function run(script, args, cwd, expectedStatus = 0) {
  const result = spawnSync(process.execPath, [script, ...args], {
    cwd, env, encoding: 'utf8', timeout: 60_000,
  });
  assert.ifError(result.error);
  assert.equal(result.status, expectedStatus, `${result.stdout}\n${result.stderr}`);
  return `${result.stdout}\n${result.stderr}`;
}

async function files(directory) {
  const result = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) result.push(...await files(path));
    else result.push(path);
  }
  return result;
}

try {
  for (const [label, selection] of [['full', all], ['docs', docs], ['authoring', authoring], ['grill', grill]]) {
    for (const copy of [false, true]) {
      const project = join(temporary, `${label}-${copy ? 'copy' : 'symlink'}`);
      await mkdir(project);
      const preserved = ['AGENTS.md', 'CLAUDE.md'];
      for (const destination of destinations) {
        const directory = join(project, destination, 'unrelated');
        await mkdir(directory, { recursive: true });
        preserved.push(relative(project, join(directory, 'SKILL.md')));
      }
      for (const path of preserved) {
        await writeFile(join(project, path), `Unrelated content: ${path}\n`);
      }

      // Exercise the documented wildcard and explicit smaller selections.
      const selected = label === 'full' ? ['*'] : selection;
      const args = ['add', source, '--skill', ...selected, '-a', ...agents, '-y'];
      if (copy) args.push('--copy');
      run(installer, args, project);

      for (const destination of destinations) {
        const installed = join(project, destination);
        assert.deepEqual((await readdir(installed)).sort(), [...selection, 'unrelated'].sort());
        for (const name of selection) {
          const target = join(installed, name);
          const isLink = (await lstat(target)).isSymbolicLink();
          if (copy || destination !== '.agents/skills') {
            assert.equal(isLink, !copy, `${destination}/${name}: unexpected installation method`);
          }
          for (const file of await files(join(source, 'skills', name))) {
            const suffix = relative(join(source, 'skills', name), file);
            assert.deepEqual(await readFile(join(target, suffix)), await readFile(file),
              `${destination}/${name}/${suffix}: installed content differs`);
          }
        }
      }
      for (const path of preserved) {
        assert.equal(await readFile(join(project, path), 'utf8'), `Unrelated content: ${path}\n`);
      }
      // Each bundle is self-contained; named collection dependencies must be selected.
      const installedEntries = selection.map((name) => join('.agents/skills', name));
      const remarkArgs = [...installedEntries, '--rc-path', config, '--frail', '--no-stdout', '--quiet'];
      const checkArgs = [join(project, '.agents/skills'), ...selection];
      run(remark, remarkArgs, project);
      run(checkSkills, checkArgs, project);
      console.log(`Passed ${label} ${copy ? 'copy' : 'symlink'} install: ${selection.length} skills, 3 agents.`);

      if (label === 'docs' && copy) {
        const entry = join(project, '.agents/skills/luminekit-docs-review/SKILL.md');
        const original = await readFile(entry, 'utf8');
        await writeFile(entry, `${original}\n[Broken anchor](references/structure-and-evidence.md#missing-heading)\n`);
        assert.match(run(remark, remarkArgs, project, 1), /missing-heading-in-file/);
        await writeFile(entry, original);

        await writeFile(entry, `${original}\n[Shared artifacts](../luminekit-workflow/references/artifacts.md)\n`);
        assert.match(run(checkSkills, checkArgs, project, 1), /Link leaves the skill folder/);
        await writeFile(entry, `${original}\nUse the \`luminekit-engineering-plan\` skill.\n`);
        assert.match(run(checkSkills, checkArgs, project, 1), /unknown or unselected skill: luminekit-engineering-plan/);
        await writeFile(entry, original);

        const orphan = join(project, '.agents/skills/luminekit-docs-review/references/orphan.md');
        await writeFile(orphan, '# Orphan\n');
        assert.match(run(checkSkills, checkArgs, project, 1), /orphan\.md: Not reachable/);
        await rm(orphan);

        await rm(join(project, '.agents/skills/luminekit-docs-review/references/reading-cost.md'));
        assert.match(run(remark, remarkArgs, project, 1), /missing-file/);
        console.log('Confirmed out-of-folder links, unselected names, unreachable files, missing resources and anchors fail validation.');
      }
    }
  }
} finally {
  await rm(temporary, { recursive: true, force: true });
}
