/**
 * Provider-neutral GitHub -> Google Drive bridge.
 * Dry-run is the default. Configure Script Properties before deployment.
 */
const CONFIG_KEYS = [
  'GITHUB_OWNER', 'GITHUB_REPOSITORY', 'GITHUB_REF', 'GITHUB_TOKEN',
  'BRIDGE_SECRET', 'DRIVE_ROOT_FOLDER_ID', 'DRY_RUN', 'ALLOWED_PATHS'
];

function properties_() {
  return PropertiesService.getScriptProperties().getProperties();
}

function json_(body, status) {
  return ContentService.createTextOutput(JSON.stringify({ ...body, statusCode: status || 200 }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return json_({ status: 'ok', service: 'workspace-bridge', dryRun: properties_().DRY_RUN !== 'false' });
}

function doPost(e) {
  const props = properties_();
  try {
    const raw = e && e.postData && e.postData.contents ? e.postData.contents : '';
    if (!raw) return json_({ status: 'error', errorCode: 'empty_body' }, 400);
    if (!verifySecret_(e, event, props.BRIDGE_SECRET)) return json_({ status: 'denied', errorCode: 'invalid_secret' }, 403);
    const event = JSON.parse(raw);
    const payload = normalizePush_(event);
    if (!payload) return json_({ status: 'manual_review', errorCode: 'unsupported_event' }, 202);
    if (!allowedRef_(payload.ref, props)) return json_({ status: 'denied', errorCode: 'unsupported_ref' }, 403);
    const files = payload.paths.filter(path => allowedPath_(path, props));
    if (!files.length) return json_({ status: 'ok', processed: 0, dryRun: true }, 200);
    const result = syncFiles_(files, props);
    return json_({ status: result.status, processed: result.processed, dryRun: result.dryRun, auditId: result.auditId }, 200);
  } catch (err) {
    console.error(err && err.stack ? err.stack : String(err));
    return json_({ status: 'error', errorCode: 'bridge_exception' }, 500);
  }
}

function verifySecret_(request, payload, secret) {
  if (!secret) return false;
  const headers = request && request.headers ? request.headers : {};
  const supplied = headers['X-Bridge-Secret'] || headers['x-bridge-secret'] || (payload && payload.bridge_secret) || (request && request.parameter && request.parameter.bridge_secret) || '';
  return supplied === secret;
}

function normalizePush_(event) {
  if (event && event.event === 'push' && event.ref) return { ref: event.ref.replace('refs/heads/', ''), paths: (event.commits || []).flatMap(c => (c.added || []).concat(c.modified || [])) };
  if (event && event.ref && event.repository) return { ref: String(event.ref).replace('refs/heads/', ''), paths: (event.commits || []).flatMap(c => (c.added || []).concat(c.modified || [])) };
  return null;
}

function allowedRef_(ref, props) {
  return ref === (props.GITHUB_REF || 'main');
}

function allowedPath_(path, props) {
  if (!path || path.indexOf('..') >= 0 || path.charAt(0) === '/') return false;
  const roots = String(props.ALLOWED_PATHS || 'brains,skills,guardrails,templates,memory').split(',').map(s => s.trim()).filter(Boolean);
  return roots.some(root => path === root || path.indexOf(root + '/') === 0);
}

function syncFiles_(paths, props) {
  const auditId = Utilities.getUuid();
  const dryRun = props.DRY_RUN !== 'false';
  if (dryRun) return { status: 'ok', processed: paths.length, dryRun: true, auditId };
  if (!props.GITHUB_TOKEN || !props.DRIVE_ROOT_FOLDER_ID) throw new Error('missing required bridge properties');
  const root = DriveApp.getFolderById(props.DRIVE_ROOT_FOLDER_ID);
  let processed = 0;
  paths.forEach(path => {
    const content = githubContent_(path, props);
    const name = path.split('/').pop().replace(/\.[^.]+$/, '');
    const doc = findOrCreateDoc_(root, path, name);
    const body = DocumentApp.openById(doc.getId()).getBody();
    body.clear();
    body.appendParagraph(content);
    processed += 1;
  });
  return { status: 'ok', processed, dryRun: false, auditId };
}

function githubContent_(path, props) {
  const url = 'https://api.github.com/repos/' + encodeURIComponent(props.GITHUB_OWNER) + '/' + encodeURIComponent(props.GITHUB_REPOSITORY) + '/contents/' + path.split('/').map(encodeURIComponent).join('/') + '?ref=' + encodeURIComponent(props.GITHUB_REF || 'main');
  const response = UrlFetchApp.fetch(url, { headers: { Authorization: 'Bearer ' + props.GITHUB_TOKEN, Accept: 'application/vnd.github+json' }, muteHttpExceptions: true });
  if (response.getResponseCode() !== 200) throw new Error('github_content_fetch_failed');
  const data = JSON.parse(response.getContentText());
  return Utilities.newBlob(Utilities.base64Decode(data.content.replace(/\n/g, ''))).getDataAsString();
}

function findOrCreateDoc_(root, path, title) {
  const files = root.getFilesByName(title);
  if (files.hasNext()) return files.next();
  const created = DocumentApp.create(title);
  DriveApp.getFileById(created.getId()).moveTo(root);
  return DriveApp.getFileById(created.getId());
}

function healthCheck() {
  const props = properties_();
  return { configured: CONFIG_KEYS.filter(k => !!props[k]), dryRun: props.DRY_RUN !== 'false', allowedPaths: props.ALLOWED_PATHS || '' };
}
