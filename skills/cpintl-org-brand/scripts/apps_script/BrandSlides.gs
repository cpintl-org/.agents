/**
 * CPI Brand — Google Slides native template builder.
 *
 * WHY THIS APPROACH (Google Workspace native best practice):
 * Instead of just dropping a picture of a "branded slide" into a deck,
 * this builds a real Google Slides file where the CPI colors are set as
 * actual theme/shape fills and the CPI fonts are set as actual text
 * styles — so every new slide added later, by anyone, inherits the
 * brand automatically instead of relying on people copying a picture.
 *
 * HOW TO RUN (no coding needed once this is pasted in):
 *   1. In your ai-workspace folder (see your dev-environment setup),
 *      run:  clasp create --type standalone --title "CPI Brand Kit"
 *   2. Open the project:  clasp open
 *   3. In the Apps Script editor, replace Code.gs with this file's
 *      contents (or add it as a new file called BrandSlides.gs).
 *   4. Click Run > buildCpiTitleSlideTemplate. The first time, Google
 *      will ask you to authorize — click through and Allow.
 *   5. A new Google Slides file appears in your Drive, already open-able
 *      from drive.google.com — fully native, not an uploaded image file.
 */

// Pull the same hex values used everywhere else in this skill so the
// palette only ever has to be edited in ONE place if CPI updates it.
var CPI_COLORS = {
  red: '#D91E4D',
  purple: '#41273B',
  black: '#2D2926',
  midGrey: '#948794',
  tealBlue: '#4298B5',
  secondaryPurple: '#615E9B',
  lightGrey: '#D0C4C5',
  white: '#FFFFFF'
};

var DEPARTMENTS = {
  HOP: { name: 'Health Outreach Program', theme: 'Health and Nutrition (HN)', accent: 'red' },
  HPP: { name: 'Health Post Program', theme: 'Health and Nutrition (HN)', accent: 'red' },
  HSS: { name: 'Health System Strengthening Program', theme: 'Health and Nutrition (HN)', accent: 'red' },
  WASH: { name: 'WASH', theme: 'Sustainable Development (SD)', accent: 'tealBlue' },
  CleanEnergy: { name: 'Clean Energy', theme: 'Sustainable Development (SD)', accent: 'tealBlue' },
  Education: { name: 'Education', theme: 'Sustainable Development (SD)', accent: 'tealBlue' },
  Livelihood: { name: 'Livelihood', theme: 'Sustainable Development (SD)', accent: 'tealBlue' },
  RD: { name: 'Research and Development', theme: 'Research and Development (RD)', accent: 'secondaryPurple' },
  'M&E': { name: 'Monitoring and Evaluation', theme: 'Cross-Program Department', accent: 'purple' },
  HIMS: { name: 'Health Information Management System', theme: 'Cross-Program Department', accent: 'purple' },
  Finance: { name: 'Finance', theme: 'Cross-Program Department', accent: 'purple' },
  Logistics: { name: 'Logistics', theme: 'Cross-Program Department', accent: 'purple' },
  Warehouse: { name: 'Warehouse', theme: 'Cross-Program Department', accent: 'purple' },
  HR: { name: 'Human Resource and Admin', theme: 'Cross-Program Department', accent: 'purple' },
  FieldCoordination: { name: 'Field Coordination', theme: 'Cross-Program Department', accent: 'purple' },
  MediaComms: { name: 'Media and Communication', theme: 'Cross-Program Department', accent: 'purple' }
};

/**
 * Builds ONE master title-slide template. Run this first to sanity check
 * before generating all 16 (see buildAllDepartmentDecks below).
 */
function buildCpiTitleSlideTemplate() {
  buildDepartmentDeck_('HOP');
}

/** Generates a starter deck for every department in one go. */
function buildAllDepartmentDecks() {
  for (var code in DEPARTMENTS) {
    buildDepartmentDeck_(code);
    Utilities.sleep(300); // gentle on Slides API quota
  }
}

function buildDepartmentDeck_(code) {
  var dept = DEPARTMENTS[code];
  if (!dept) throw new Error('Unknown department code: ' + code);

  var fileTitle = 'CPI-BGD-' + code + '-Presentation-' + yyyymm_() + '-v01';
  var deck = SlidesApp.create(fileTitle);
  var slide = deck.getSlides()[0];
  slide.getShapes().forEach(function (s) { s.remove(); }); // clear default placeholders

  var pageW = deck.getPageWidth();
  var pageH = deck.getPageHeight();
  var accentHex = CPI_COLORS[dept.accent];

  // Top accent bar (brand-approved color only)
  var topBar = slide.insertShape(SlidesApp.ShapeType.RECTANGLE, 0, 0, pageW, pageH * 0.05);
  topBar.getFill().setSolidFill(accentHex);
  topBar.getBorder().setTransparent();

  // Bottom purple bar
  var bottomBar = slide.insertShape(SlidesApp.ShapeType.RECTANGLE, 0, pageH * 0.95, pageW, pageH * 0.05);
  bottomBar.getFill().setSolidFill(CPI_COLORS.purple);
  bottomBar.getBorder().setTransparent();

  // Title text box — Arial Bold per the Workspace-doc typography spec
  var titleBox = slide.insertTextBox(dept.name, pageW * 0.07, pageH * 0.40, pageW * 0.86, pageH * 0.18);
  var titleStyle = titleBox.getText().getTextStyle();
  titleStyle.setFontFamily('Arial').setBold(true).setFontSize(28).setForegroundColor(CPI_COLORS.purple);

  // Subtitle / doc-type line in CPI Red per the "Heading 1" role
  var subtitleBox = slide.insertTextBox('Presentation', pageW * 0.07, pageH * 0.58, pageW * 0.86, pageH * 0.08);
  subtitleBox.getText().getTextStyle().setFontFamily('Arial').setBold(true).setFontSize(16).setForegroundColor(CPI_COLORS.red);

  // File-ID footer in CPI Mid Grey (caption role)
  var footer = slide.insertTextBox('CPI-BGD-' + code + '-Presentation-' + yyyymm_() + '-v01  |  ' + dept.theme,
    pageW * 0.07, pageH * 0.90, pageW * 0.86, pageH * 0.04);
  footer.getText().getTextStyle().setFontFamily('Arial').setItalic(true).setFontSize(9).setForegroundColor(CPI_COLORS.midGrey);

  Logger.log('Created: ' + deck.getUrl());
  return deck;
}

function yyyymm_() {
  var d = new Date();
  var m = ('0' + (d.getMonth() + 1)).slice(-2);
  return d.getFullYear() + '' + m;
}
