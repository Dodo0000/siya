var searchInput = $("#bookSearchTextInput");
var searchInputHeight = parseInt(searchInput.css("height"));
searchInput.css("height", (searchInputHeight + 2).toString() + "px");



var searchInputBody = $("#searchInputBody");
var searchInputBodyHeight = parseInt(searchInputBody.css("height"));
searchInputBody.css("height", (searchInputBodyHeight + 10).toString() + "px");

$('.initHide').hide();

function checkIfAccessionNumberExists(inputField, outputFieldSuccess,outputFieldFail)
{
  $.getJSON(
      '/head/book/does_the_accession_number_exist/'+$("#"+inputField.toString())[0].value.toString(),
      function(data){
        if (data.exists == 1)
          $("#" + outputFieldSuccess.toString()).show('slow').delay(2000).hide('fast');
        else
          $("#"+outputFieldFail.toString()).show('slow').delay(2000).hide('fast');
      }
  );
}
