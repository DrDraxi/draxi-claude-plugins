import { mkdirSync, writeFileSync } from 'fs';

function main() {
  let args = process.argv.slice(2);
  // When invoked with "$ARGUMENTS", bash passes everything as a single string.
  // Split it into words so flag parsing (--max-iterations, etc.) still works.
  if (args.length === 1 && !args[0].startsWith('-')) {
    args = args[0].split(/\s+/).filter(Boolean);
  }
  const promptParts = [];
  let maxIterations = 0;
  let completionPromise = 'null';

  let i = 0;
  while (i < args.length) {
    switch (args[i]) {
      case '-h':
      case '--help':
        console.log(`Ralph Loop - Interactive self-referential development loop

USAGE:
  /ralph-loop [PROMPT...] [OPTIONS]

OPTIONS:
  --max-iterations <n>           Maximum iterations before auto-stop (default: unlimited)
  --completion-promise '<text>'  Promise phrase (USE QUOTES for multi-word)
  -h, --help                     Show this help message

EXAMPLES:
  /ralph-loop Build a todo API --completion-promise 'DONE' --max-iterations 20
  /ralph-loop --max-iterations 10 Fix the auth bug`);
        process.exit(0);
        break;
      case '--max-iterations':
        if (!args[i + 1] || !/^\d+$/.test(args[i + 1])) {
          process.stderr.write(`Error: --max-iterations requires a positive integer, got: ${args[i + 1] || '(nothing)'}\n`);
          process.exit(1);
        }
        maxIterations = parseInt(args[i + 1], 10);
        i += 2;
        break;
      case '--completion-promise':
        if (!args[i + 1]) {
          process.stderr.write('Error: --completion-promise requires a text argument\n');
          process.exit(1);
        }
        completionPromise = args[i + 1];
        i += 2;
        break;
      default:
        promptParts.push(args[i]);
        i++;
        break;
    }
  }

  const prompt = promptParts.join(' ');

  if (!prompt) {
    process.stderr.write(`Error: No prompt provided

Ralph needs a task description to work on.

Examples:
  /ralph-loop Build a REST API for todos
  /ralph-loop Fix the auth bug --max-iterations 20
  /ralph-loop --completion-promise 'DONE' Refactor code
`);
    process.exit(1);
  }

  mkdirSync('.claude', { recursive: true });

  const promiseYaml = completionPromise !== 'null' ? `"${completionPromise}"` : 'null';
  const now = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');

  const stateContent = `---
active: true
iteration: 1
max_iterations: ${maxIterations}
completion_promise: ${promiseYaml}
started_at: "${now}"
---

${prompt}
`;

  writeFileSync('.claude/ralph-loop.local.md', stateContent, 'utf-8');

  const maxDisplay = maxIterations > 0 ? maxIterations : 'unlimited';
  const promiseDisplay = completionPromise !== 'null'
    ? `${completionPromise} (ONLY output when TRUE - do not lie!)`
    : 'none (runs forever)';

  console.log(`Ralph loop activated in this session!

Iteration: 1
Max iterations: ${maxDisplay}
Completion promise: ${promiseDisplay}

The stop hook is now active. When you try to exit, the SAME PROMPT will be
fed back to you. You'll see your previous work in files, creating a
self-referential loop where you iteratively improve on the same task.

WARNING: This loop cannot be stopped manually! It will run infinitely
    unless you set --max-iterations or --completion-promise.
`);

  console.log(prompt);

  if (completionPromise !== 'null') {
    console.log(`
===============================================================
CRITICAL - Ralph Loop Completion Promise
===============================================================

To complete this loop, output this EXACT text:
  <promise>${completionPromise}</promise>

STRICT REQUIREMENTS (DO NOT VIOLATE):
  - Use <promise> XML tags EXACTLY as shown above
  - The statement MUST be completely and unequivocally TRUE
  - Do NOT output false statements to exit the loop
  - Do NOT lie even if you think you should exit
===============================================================`);
  }
}

main();
