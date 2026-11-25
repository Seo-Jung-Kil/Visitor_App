const SHEET_NAME = '방문자등록';
const HEADERS = ['등록일시','등록번호','학교','학번','이름','연락처','방문 목적','동의 여부'];
function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
function safeText(value) {
  return /^[=+\-@\t\r\n]/.test(value) ? "'" + value : value;
}
function doPost(e) {
  let lock;
  try {
    const props = PropertiesService.getScriptProperties();
    const d = JSON.parse(e.postData.contents);
    const token = props.getProperty('API_TOKEN');
    if (!token || d.token !== token) return reply({ok:false});
    if (!/^[a-f0-9]{32}$/.test(d.request_id) || d.consent !== true) return reply({ok:false});
    const limits = {school:100,student:30,name:50,phone:20,purpose:500};
    for (const k in limits) {
      if (typeof d[k] !== 'string' || !d[k].trim() || d[k].length > limits[k]) return reply({ok:false});
      d[k] = d[k].trim();
    }
    if (!/^01[016789]-?\d{3,4}-?\d{4}$/.test(d.phone)) return reply({ok:false});
    lock = LockService.getScriptLock();
    lock.waitLock(15000);
    const ss = SpreadsheetApp.openById(props.getProperty('SPREADSHEET_ID'));
    const sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) sheet.appendRow(HEADERS);
    const id = 'VIS-' + d.request_id;
    if (sheet.getLastRow() > 1) {
      const found = sheet.getRange(2,2,sheet.getLastRow()-1,1).createTextFinder(id).matchEntireCell(true).findNext();
      if (found) return reply({ok:true,registration_id:id,registered_at:sheet.getRange(found.getRow(),1).getDisplayValue()});
    }
    const date = Utilities.formatDate(new Date(),'Asia/Seoul','yyyy-MM-dd HH:mm:ss');
    const row = sheet.getRange(sheet.getLastRow()+1,1,1,8);
    row.setNumberFormat('@');
    row.setValues([[date,id,...['school','student','name','phone','purpose'].map(k=>safeText(d[k])), '동의']]);
    SpreadsheetApp.flush();
    return reply({ok:true,registration_id:id,registered_at:date});
  } catch (err) {
    return reply({ok:false});
  } finally {
    if (lock && lock.hasLock()) lock.releaseLock();
  }
}
