/**
 * CPI Brand — Google Sheets native template builder.
 * Formats header row (CPI Purple fill, white Arial Bold text) and
 * alternating row bands (CPI Light Grey at 30% opacity, per the guide)
 * as REAL cell formatting + a banding rule — so it stays correct even
 * as rows are added/deleted later, instead of manually shading rows.
 *
 * HOW TO RUN: paste into your Apps Script project, then
 * Run > buildCpiSheetTemplate.
 */

var CPI_COLORS_SHEETS = {
  purple: '#41273B',
  red: '#D91E4D',
  black: '#2D2926',
  midGrey: '#948794',
  lightGrey: '#D0C4C5',
  white: '#FFFFFF'
};

function buildCpiSheetTemplate() {
  buildDepartmentSheet_('M&E', 'QReport', ['Indicator', 'Target', 'Actual', '% Achieved', 'Remarks']);
}

function buildDepartmentSheet_(code, docType, headers) {
  var fileTitle = 'CPI-BGD-' + code + '-' + docType + '-' + yyyymmSheets_() + '-v01';
  var ss = SpreadsheetApp.create(fileTitle);
  var sheet = ss.getSheets()[0];
  sheet.setName(docType);

  // Header row
  var headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setValues([headers]);
  headerRange
    .setBackground(CPI_COLORS_SHEETS.purple)
    .setFontColor(CPI_COLORS_SHEETS.white)
    .setFontWeight('bold')
    .setFontFamily('Arial')
    .setFontSize(11);
  sheet.setFrozenRows(1);

  // Column widths for readability
  for (var c = 1; c <= headers.length; c++) sheet.setColumnWidth(c, 160);

  // Alternating row banding using the brand's approved Light Grey
  // (native Sheets banding — this is a real, built-in Sheets feature,
  // not manual per-row coloring, so it updates automatically as rows
  // are added or removed)
  var dataRange = sheet.getRange(1, 1, 60, headers.length);
  var bandings = dataRange.getBandings();
  bandings.forEach(function (b) { b.remove(); });
  var banding = dataRange.applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY);
  banding.setHeaderRowColor(CPI_COLORS_SHEETS.purple);
  banding.setFirstRowColor(CPI_COLORS_SHEETS.white);
  banding.setSecondRowColor(CPI_COLORS_SHEETS.lightGrey);

  // Body font for the data area
  sheet.getRange(2, 1, 59, headers.length)
    .setFontFamily('Arial').setFontSize(11).setFontColor(CPI_COLORS_SHEETS.black);

  Logger.log('Created: ' + ss.getUrl());
  return ss;
}

function yyyymmSheets_() {
  var d = new Date();
  var m = ('0' + (d.getMonth() + 1)).slice(-2);
  return d.getFullYear() + '' + m;
}
