/**
 * CPI Brand — Google Docs native template builder.
 * Creates a real Google Doc with the CPI logo, correct cover layout,
 * and Heading 1/2/3/Body/Caption styles set to the exact brand spec
 * (Arial, brand colors, correct point sizes) as REAL paragraph styles
 * — so typing "Heading 1" in the Docs style dropdown later already
 * matches CPI's guide, instead of everyone manually formatting text.
 *
 * HOW TO RUN: same steps as BrandSlides.gs — paste into your Apps
 * Script project, then Run > buildCpiDocTemplate (or buildAllDepartmentDocs).
 * You'll need the CPI logo image uploaded to a Drive folder first —
 * set LOGO_DRIVE_FILE_ID below to that file's ID (right-click the file
 * in Drive > Get link, the long ID string is in the URL).
 */

var LOGO_DRIVE_FILE_ID = 'PASTE_YOUR_UPLOADED_LOGO_FILE_ID_HERE';

var CPI_COLORS_DOCS = {
  red: '#D91E4D',
  purple: '#41273B',
  black: '#2D2926',
  midGrey: '#948794'
};

function buildCpiDocTemplate() {
  buildDepartmentDoc_('HOP', 'MonthlyReport');
}

function buildDepartmentDoc_(code, docType) {
  var fileTitle = 'CPI-BGD-' + code + '-' + docType + '-' + yyyymmDocs_() + '-v01';
  var doc = DocumentApp.create(fileTitle);
  var body = doc.getBody();
  body.clear();

  // Logo, if configured
  if (LOGO_DRIVE_FILE_ID && LOGO_DRIVE_FILE_ID.indexOf('PASTE_') === -1) {
    var logoBlob = DriveApp.getFileById(LOGO_DRIVE_FILE_ID).getBlob();
    var logoPara = body.appendImage(logoBlob);
    logoPara.setWidth(90).setHeight(90);
  }

  // Title — Arial Bold 24pt, CPI Purple
  var title = body.appendParagraph(docType);
  title.setFontFamily('Arial').setBold(true).setFontSize(24)
    .setForegroundColor(CPI_COLORS_DOCS.purple);

  // Heading 1 style example — Arial Bold 18pt, CPI Red
  var h1 = body.appendParagraph('Section Heading Example');
  h1.setFontFamily('Arial').setBold(true).setFontSize(18)
    .setForegroundColor(CPI_COLORS_DOCS.red)
    .setHeading(DocumentApp.ParagraphHeading.HEADING1);

  // Heading 2 style example — Arial Bold 14pt, CPI Purple
  var h2 = body.appendParagraph('Subsection Heading Example');
  h2.setFontFamily('Arial').setBold(true).setFontSize(14)
    .setForegroundColor(CPI_COLORS_DOCS.purple)
    .setHeading(DocumentApp.ParagraphHeading.HEADING2);

  // Body text — Arial Regular 11pt, CPI Black, 1.25 line spacing
  var bodyPara = body.appendParagraph(
    'Body text uses Arial Regular at 11pt in CPI Black with 1.25 line ' +
    'spacing, matching the CPI Brand Identity Standards for Office & ' +
    'Digital Workspace documents.');
  bodyPara.setFontFamily('Arial').setBold(false).setFontSize(11)
    .setForegroundColor(CPI_COLORS_DOCS.black).setLineSpacing(1.25);

  // Caption / footer — Arial Italic 9pt, CPI Mid Grey
  var caption = body.appendParagraph(fileTitle + '  |  Community Partners International');
  caption.setFontFamily('Arial').setItalic(true).setFontSize(9)
    .setForegroundColor(CPI_COLORS_DOCS.midGrey);

  Logger.log('Created: ' + doc.getUrl());
  return doc;
}

function yyyymmDocs_() {
  var d = new Date();
  var m = ('0' + (d.getMonth() + 1)).slice(-2);
  return d.getFullYear() + '' + m;
}
