import { readFileSync, writeFileSync, existsSync, unlinkSync } from 'fs';
import { join } from 'path';

const RALPH_STATE_FILE = join('.claude', 'ralph-loop.local.md');

function main() {
  let hookInput = '';
  try {
    hookInput = readFileSync(0, 'utf-8');
  } catch {
    // No stdin
  }

  if (!existsSync(RALPH_STATE_FILE)) {
    process.exit(0);
  }

  const stateContent = readFileSync(RALPH_STATE_FILE, 'utf-8');

  const frontmatterMatch = stateContent.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) {
    process.stderr.write('Warning: Ralph loop state file has no frontmatter. Stopping.\n');
    unlinkSync(RALPH_STATE_FILE);
    process.exit(0);
  }

  const frontmatter = frontmatterMatch[1];
  const iterationMatch = frontmatter.match(/^iteration:\s*(\d+)/m);
  const maxIterationsMatch = frontmatter.match(/^max_iterations:\s*(\d+)/m);
  const promiseMatch = frontmatter.match(/^completion_promise:\s*"?([^"\n]*)"?/m);

  if (!iterationMatch || !maxIterationsMatch) {
    process.stderr.write('Warning: Ralph loop state file corrupted. Stopping.\n');
    unlinkSync(RALPH_STATE_FILE);
    process.exit(0);
  }

  const iteration = parseInt(iterationMatch[1], 10);
  const maxIterations = parseInt(maxIterationsMatch[1], 10);
  const completionPromise = promiseMatch ? promiseMatch[1] : 'null';

  if (maxIterations > 0 && iteration >= maxIterations) {
    console.log(`Max iterations (${maxIterations}) reached.`);
    unlinkSync(RALPH_STATE_FILE);
    process.exit(0);
  }

  let transcriptPath = '';
  try {
    const parsed = JSON.parse(hookInput);
    transcriptPath = parsed.transcript_path || '';
  } catch {
    process.stderr.write('Warning: Could not parse hook input JSON. Stopping.\n');
    unlinkSync(RALPH_STATE_FILE);
    process.exit(0);
  }

  if (!transcriptPath || !existsSync(transcriptPath)) {
    process.stderr.write(`Warning: Transcript file not found: ${transcriptPath}\n`);
    unlinkSync(RALPH_STATE_FILE);
    process.exit(0);
  }

  const transcriptContent = readFileSync(transcriptPath, 'utf-8');
  const lines = transcriptContent.split('\n').filter(l => l.trim());
  const assistantLines = lines.filter(l => l.includes('"role":"assistant"'));

  if (assistantLines.length === 0) {
    process.stderr.write('Warning: No assistant messages in transcript. Stopping.\n');
    unlinkSync(RALPH_STATE_FILE);
    process.exit(0);
  }

  let lastOutput = '';
  try {
    const lastMsg = JSON.parse(assistantLines[assistantLines.length - 1]);
    const textParts = (lastMsg.message?.content || [])
      .filter(c => c.type === 'text')
      .map(c => c.text);
    lastOutput = textParts.join('\n');
  } catch {
    process.stderr.write('Warning: Failed to parse last assistant message. Stopping.\n');
    unlinkSync(RALPH_STATE_FILE);
    process.exit(0);
  }

  if (!lastOutput) {
    process.stderr.write('Warning: Assistant message had no text content. Stopping.\n');
    unlinkSync(RALPH_STATE_FILE);
    process.exit(0);
  }

  if (completionPromise && completionPromise !== 'null') {
    const promiseTagMatch = lastOutput.match(/<promise>([\s\S]*?)<\/promise>/);
    if (promiseTagMatch) {
      const promiseText = promiseTagMatch[1].trim().replace(/\s+/g, ' ');
      if (promiseText === completionPromise) {
        console.log(`Ralph loop: Detected <promise>${completionPromise}</promise>`);
        unlinkSync(RALPH_STATE_FILE);
        process.exit(0);
      }
    }
  }

  const nextIteration = iteration + 1;
  const afterFrontmatter = stateContent.replace(/^---\n[\s\S]*?\n---\n?/, '');
  const promptText = afterFrontmatter.trim();

  if (!promptText) {
    process.stderr.write('Warning: No prompt text found in state file. Stopping.\n');
    unlinkSync(RALPH_STATE_FILE);
    process.exit(0);
  }

  const updatedContent = stateContent.replace(
    /^iteration:\s*\d+/m,
    `iteration: ${nextIteration}`
  );
  writeFileSync(RALPH_STATE_FILE, updatedContent, 'utf-8');

  let systemMsg;
  if (completionPromise && completionPromise !== 'null') {
    systemMsg = `Ralph iteration ${nextIteration} | To stop: output <promise>${completionPromise}</promise> (ONLY when statement is TRUE - do not lie to exit!)`;
  } else {
    systemMsg = `Ralph iteration ${nextIteration} | No completion promise set - loop runs infinitely`;
  }

  const output = JSON.stringify({
    decision: 'block',
    reason: promptText,
    systemMessage: systemMsg
  });
  console.log(output);
  process.exit(0);
}

main();
