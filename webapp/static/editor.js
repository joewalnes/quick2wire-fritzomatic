var editor, session;

function createEditor() {
  editor = ace.edit('editor');  
  editor.setTheme('ace/theme/clouds');
  editor.setShowPrintMargin(false);

  var session = editor.getSession();
  var JsonMode = require('ace/mode/json').Mode;
  session.setMode(new JsonMode());
  session.setTabSize(2);
  session.setUseSoftTabs(true);

  return editor;
}

function isEmpty(o) {
  for (var k in o) {
    return false;
  }
  return true;
}

function codeIsValid() {
  return isEmpty(session.getAnnotations());
}

function editorChanged() {
  if (codeIsValid()) {
    updatePreviews(JSON.parse(session.getValue()));
  } else {
    // TODO
  }
}

function updatePreviews(json) {

  // Title
  $('#component-title').text(json.title || 'Untitled');

  // Description
  if (json.description) {
    $('#description-block').show();
    $('#description').text(json.description);
  } else {
    $('#description-block').hide();
    $('#description').text('');
  }

  // Tags
  $('#tags span').not('.template').remove();
  if (json.tags) {
    $('#tags-block').show();
    json.tags.forEach(function(tag) {
      $('#tags .template').clone().removeClass('template').appendTo('#tags')
        .text(tag).attr({title:'Tag: ' + tag});
    });
  } else {
    $('#tags-block').hide();
  }
  
  // Connections
  $('#connections-block tbody tr').not('.template').remove();
  if (json.connectors && !isEmpty(json.connectors)) {
    $('#connections-block').show();
    for (var id in json.connectors) {
      var row = $('#connections-block tbody tr.template').clone().removeClass('template').appendTo('#connections-block tbody');
      var connector = json.connectors[id];
      row.find('.connection-id').text(id);
      row.find('.connection-name').text(connector.label || '');
      row.find('.connection-description').text(connector.description || '');
    }
  } else {
    $('#connections-block').hide();
  }

  // Image previews
  $.post('/encode-json', {data:JSON.stringify(json)}, function(encoded) {
    $('#icon-preview      ').attr({src:'/component/' + encoded + '/icon?size=30'});
    $('#breadboard-preview').attr({src:'/component/' + encoded + '/breadboard?size=200'});
    $('#schematic-preview ').attr({src:'/component/' + encoded + '/schematic?size=200'});
    $('#pcb-preview       ').attr({src:'/component/' + encoded + '/pcb?size=200'});
  }); // TODO: Handle XHR error
}

$(function() {
  editor = createEditor();
  session = editor.getSession();
  session.on('change', editorChanged);
  editorChanged();
});
