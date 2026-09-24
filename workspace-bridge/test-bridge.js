#!/usr/bin/env node
/**
 * Offline behavioral test suite for Google Apps Script Workspace Bridge.
 * Tests Code.gs logic in isolation without network access or live Drive credentials.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const scriptPath = path.join(__dirname, 'Code.gs');
const code = fs.readFileSync(scriptPath, 'utf8');

const baseMockProps = {
  GITHUB_OWNER: 'cpintl-org',
  GITHUB_REPOSITORY: '.agents',
  GITHUB_REF: 'main',
  GITHUB_TOKEN: 'test-token-safe-placeholder',
  BRIDGE_SECRET: 'test-secret-cpi-bridge-12345',
  DRIVE_ROOT_FOLDER_ID: 'test-folder-id-placeholder',
  DRY_RUN: 'true',
  ALLOWED_PATHS: 'brains,skills,guardrails,templates,memory'
};

function createMockIterator(items) {
  let idx = 0;
  return {
    hasNext: () => idx < items.length,
    next: () => items[idx++]
  };
}

function createBridgeContext(customProps = {}, customConsole = console) {
  const currentProps = { ...baseMockProps, ...customProps };
  const mockDriveOps = [];

  const sandbox = {
    console: customConsole,
    Buffer,
    PropertiesService: {
      getScriptProperties: () => ({
        getProperties: () => ({ ...currentProps })
      })
    },
    ContentService: {
      createTextOutput: (text) => {
        let parsed;
        try {
          parsed = JSON.parse(text);
        } catch {
          parsed = { raw: text };
        }
        return {
          setMimeType: () => parsed
        };
      },
      MimeType: { JSON: 'application/json' }
    },
    Utilities: {
      getUuid: () => 'test-uuid-00000000',
      newBlob: (bytes) => ({
        getDataAsString: () => String(bytes)
      }),
      base64Decode: (str) => Buffer.from(str, 'base64')
    },
    DriveApp: {
      getFolderById: (id) => ({
        id,
        getFoldersByName: (name) => createMockIterator([]),
        createFolder: (name) => {
          mockDriveOps.push({ op: 'createFolder', name });
          return {
            createFolder: (sub) => {
              mockDriveOps.push({ op: 'createFolder', name: sub });
              return {};
            }
          };
        }
      })
    },
    mockDriveOps
  };

  vm.createContext(sandbox);
  vm.runInContext(code, sandbox);
  return sandbox;
}

console.log('--- Running Offline Bridge Behavioral Tests ---');

// Test 1: Empty POST body returns 400 with empty_body
{
  const ctx = createBridgeContext();
  const resNull = ctx.doPost(null);
  assert.strictEqual(resNull.statusCode, 400, 'Empty POST should return 400');
  assert.strictEqual(resNull.errorCode, 'empty_body', 'Error code should be empty_body');

  const resEmptyObj = ctx.doPost({ postData: { contents: '' } });
  assert.strictEqual(resEmptyObj.statusCode, 400);
  assert.strictEqual(resEmptyObj.errorCode, 'empty_body');
  console.log('✓ Test 1 Passed: Empty body handled correctly.');
}

// Test 2: Missing or incorrect secret returns 403 invalid_secret
{
  const ctx = createBridgeContext();
  const resNoSecret = ctx.doPost({
    postData: { contents: JSON.stringify({ event: 'push', ref: 'refs/heads/main' }) }
  });
  assert.strictEqual(resNoSecret.statusCode, 403);
  assert.strictEqual(resNoSecret.errorCode, 'invalid_secret');

  const resWrongSecret = ctx.doPost({
    postData: { contents: JSON.stringify({ bridge_secret: 'incorrect-secret', event: 'push', ref: 'refs/heads/main' }) }
  });
  assert.strictEqual(resWrongSecret.statusCode, 403);
  assert.strictEqual(resWrongSecret.errorCode, 'invalid_secret');
  console.log('✓ Test 2 Passed: Secret verification enforced correctly.');
}

// Test 3: Malformed JSON returns 500 bridge_exception (suppressing console.error during test)
{
  const silentConsole = { ...console, error: () => {} };
  const ctx = createBridgeContext({}, silentConsole);
  const resBadJson = ctx.doPost({
    postData: { contents: '{ malformed json: missing quotes }' }
  });
  assert.strictEqual(resBadJson.statusCode, 500);
  assert.strictEqual(resBadJson.errorCode, 'bridge_exception');
  console.log('✓ Test 3 Passed: Malformed JSON handled safely.');
}

// Test 4: Unsupported event returns 202 unsupported_event
{
  const ctx = createBridgeContext();
  const resBadEvent = ctx.doPost({
    postData: { contents: JSON.stringify({ bridge_secret: baseMockProps.BRIDGE_SECRET, event: 'pull_request' }) }
  });
  assert.strictEqual(resBadEvent.statusCode, 202);
  assert.strictEqual(resBadEvent.errorCode, 'unsupported_event');
  assert.strictEqual(resBadEvent.status, 'manual_review');
  console.log('✓ Test 4 Passed: Non-push events routed to manual_review.');
}

// Test 5: Unsupported ref returns 403 unsupported_ref
{
  const ctx = createBridgeContext();
  const resBadRef = ctx.doPost({
    postData: { contents: JSON.stringify({
      bridge_secret: baseMockProps.BRIDGE_SECRET,
      event: 'push',
      ref: 'refs/heads/feature-branch'
    }) }
  });
  assert.strictEqual(resBadRef.statusCode, 403);
  assert.strictEqual(resBadRef.errorCode, 'unsupported_ref');
  console.log('✓ Test 5 Passed: Non-main branches rejected.');
}

// Test 6: Allowed path filtering
{
  const ctx = createBridgeContext();
  assert.strictEqual(ctx.allowedPath_('brains/README.md', baseMockProps), true);
  assert.strictEqual(ctx.allowedPath_('skills/test-skill/SKILL.md', baseMockProps), true);
  assert.strictEqual(ctx.allowedPath_('guardrails/security-rules.yaml', baseMockProps), true);
  assert.strictEqual(ctx.allowedPath_('templates/agent-task.yaml', baseMockProps), true);
  assert.strictEqual(ctx.allowedPath_('memory/short-term.json', baseMockProps), true);

  // Traversal & absolute paths
  assert.strictEqual(ctx.allowedPath_('../secrets.json', baseMockProps), false);
  assert.strictEqual(ctx.allowedPath_('brains/../../etc/passwd', baseMockProps), false);
  assert.strictEqual(ctx.allowedPath_('/brains/root.md', baseMockProps), false);
  assert.strictEqual(ctx.allowedPath_('config/secret.yaml', baseMockProps), false);
  assert.strictEqual(ctx.allowedPath_('.github/workflows/secret.yml', baseMockProps), false);
  console.log('✓ Test 6 Passed: Path traversal and disallowed roots rejected.');
}

// Test 7: Unsafe folder segment detection in ensureFolderPath_
{
  const ctx = createBridgeContext();
  assert.throws(() => {
    ctx.ensureFolderPath_({}, ['..', 'unsafe']);
  }, /unsafe_folder_segment/);

  assert.throws(() => {
    ctx.ensureFolderPath_({}, ['.']);
  }, /unsafe_folder_segment/);

  assert.throws(() => {
    ctx.ensureFolderPath_({}, ['sub\\backslashes']);
  }, /unsafe_folder_segment/);

  assert.throws(() => {
    ctx.ensureFolderPath_({}, ['null\u0000byte']);
  }, /unsafe_folder_segment/);
  console.log('✓ Test 7 Passed: Unsafe path segments rejected with Error.');
}

// Test 8: Duplicate unidentified filename detection
{
  const ctx = createBridgeContext();
  const mockFolder = {
    getFilesByName: () => createMockIterator([
      { getDescription: () => '' } // Unidentified document without identity marker
    ])
  };

  assert.throws(() => {
    ctx.findOrCreateDoc_(mockFolder, 'skills/demo/README.md', 'README.md', baseMockProps);
  }, /duplicate_unidentified_filename/);
  console.log('✓ Test 8 Passed: Duplicate unmarked document stops execution safely.');
}

// Test 9: Path marker format verification
{
  const ctx = createBridgeContext();
  const marker = ctx.pathMarker_('cpintl-org', '.agents', 'main', 'skills/writing/SKILL.md');
  assert.strictEqual(marker, 'cpintl-bridge-path:cpintl-org/.agents/main/skills/writing/SKILL.md');
  console.log('✓ Test 9 Passed: Path identity marker correctly formatted.');
}

// Test 10: Dry run sync execution (no drive modifications)
{
  const ctx = createBridgeContext({ DRY_RUN: 'true' });
  const resDryRun = ctx.doPost({
    postData: { contents: JSON.stringify({
      bridge_secret: baseMockProps.BRIDGE_SECRET,
      event: 'push',
      ref: 'refs/heads/main',
      commits: [
        {
          added: ['brains/new-agent.md'],
          modified: ['skills/existing/SKILL.md', 'disallowed/file.txt']
        }
      ]
    }) }
  });

  assert.strictEqual(resDryRun.status, 'ok');
  assert.strictEqual(resDryRun.dryRun, true);
  assert.strictEqual(resDryRun.processed, 2, 'Should only process the 2 allowed paths');
  assert.strictEqual(resDryRun.auditId, 'test-uuid-00000000');
  assert.strictEqual(ctx.mockDriveOps.length, 0, 'Zero Drive operations in dry-run mode');
  console.log('✓ Test 10 Passed: Dry run returns 200 and performs zero Drive modifications.');
}

// Test 11: GET endpoint health status
{
  const ctx = createBridgeContext();
  const getRes = ctx.doGet();
  assert.strictEqual(getRes.status, 'ok');
  assert.strictEqual(getRes.service, 'workspace-bridge');
  assert.strictEqual(getRes.dryRun, true);

  const health = ctx.healthCheck();
  assert.strictEqual(health.dryRun, true);
  assert.strictEqual(health.configured.length, 8);
  console.log('✓ Test 11 Passed: doGet and healthCheck reported correctly.');
}

console.log('--- All 11 Offline Bridge Tests Passed Successfully ---');
