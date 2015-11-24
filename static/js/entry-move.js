// this is the javascript for the data entry page
// template at templates/head/entry.html

cursor_accession_number = max_accession_number;



var NP_EN_STRUCT = {
  "!": 1,
  '@': 2,
  '#': 3,
  '$': 4,
  '%': 5,
  '^': 6,
  '&': 7,
  '*': 8,
  '(': 9,
  ')': 0
};

$("#dataEntrySuccessful").hide();

function saveBook(){
  acc_no = $(".input-acc_no").val();
  var book_exists = false;
  $.get("/book/validate",{accNo: parseInt(acc_no)}).success(function(data){
    if (data.exists == 0)
      book_exists = true;
    console.log("book exists: " + book_exists.toString());
    if (book_exists === true || book_exists == false){
      console.log(data);
      var post_data = Object.create(null);
      for(i=0;i < cols_entry.length;i++){
        loc = cols_entry[i][1][2];
        post_data[loc] = $(".input-"+loc).val();
      }
      post_data.is_edit = is_edit;
      post_data.csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
      console.log(post_data);


      $.post('/book/add', post_data, function(data){
        if (data.success === true){
          max_accession_number = data.acc_no;
          $(".current_acc_no").text(max_accession_number);
          $(".input-acc_no").text(max_accession_number);
          $("html, body").animate({ scrollTop: 0 }, "slow");
          $("#dataEntrySuccessful").show().delay(2000).hide("slow");
          if (clear_fields == 1)
            clearInputFields();
        }
        else {
          alert("data entry unsuccessful :(");
        }
      });
    }
    else if (book_exists = null){
      console.log("accession number is invalid");
    }
  });
}

$("#saveBook").click(function(){
  saveBook();
})


$(".input").on("keypress", function(e){
  // keycode 13 - enter
  // keycode 
  if (e.keyCode == 13 && e.ctrlKey){
    console.log("save me1");
    saveBook();
  }
  else if (e.shiftKey && e.keyCode == 13){
    e.preventDefault();
    var element_id = (parseInt(e.currentTarget.id, 10)-2);
    var element = document.getElementById(element_id.toString());
    if (element == null){
      if (element_id % 2 == 0)
        document.getElementById((total_cols_entry - element_id).toString()).focus();
      else
        document.getElementById(total_cols_entry.toString()).focus();
    }
    else{
      element.focus();
    }
  }
  else if (e.keyCode == 13){
    e.preventDefault();
    var element_id = (parseInt(e.currentTarget.id, 10)+2);
    var element = document.getElementById(element_id.toString());
    if (element == null){
      if (element_id % 2 == 0)
        document.getElementById("2").focus();
      else
        document.getElementById("1").focus();
    }
    else{
      element.focus();
    }
  }
})


$("#"+total_cols_entry.toString()).on('keypress', function(e){
  if (e.shiftKey && e.keyCode == 9){
    e.preventDefault();
    $("#"+(total_cols_entry-1).toString()).focus();
  }
  else if (e.keyCode == 9){
    console.log("it is a me a mario");
    e.preventDefault();
    document.getElementById("1").focus();
  }
});

$("#1").on('keypress', function(e){
  if (e.shiftKey && e.keyCode == 9)
  {
    e.preventDefault();
    $("#"+total_cols_entry.toString()).focus();
  }
});
