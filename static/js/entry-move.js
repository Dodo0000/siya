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
      post_data.csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
      console.log(post_data);


      $.post('/book/add', post_data, function(data){
        if (data.success === true){
          max_accession_number = data.acc_no;
          $(".current_acc_no").text(max_accession_number);
          $(".input-acc_no").text(max_accession_number);
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
  if (e.keyCode == 13){
    saveBook();
  }
  if (e.keyCode == 38){
    e.preventDefault();
    cursor_accession_number -= 1;
    var tr = $("#"+cursor_accession_number).children();
    var data = [];
    var tc = $("#" + cursor_accession_number).children();
    for (i=0;i < tc.length; i++){
      console.log(cols_table[i][1][2]);
      data.push(tc[i].textContent);
      data.push();
    }
    console.log(data);
  }
  if (e.shiftKey && e.keyCode == 37){
    if (e.currentTarget.id == "1"){
      e.preventDefault();
      document.getElementById(total_cols_entry.toString()).focus();
    }
    else{
      e.preventDefault();
      document.getElementById((parseInt(e.currentTarget.id, 10)-1).toString()).focus();
    }
  }

  else if (e.shiftKey && e.keyCode == 39){
    if (e.currentTarget.id == total_cols_entry.toString()){
      e.preventDefault();
      document.getElementById("1").focus();
    }
    else{
      e.preventDefault();
      document.getElementById((parseInt(e.currentTarget.id, 10)+1).toString()).focus();
    }
  }
})


$("#"+total_cols_entry.toString()).on('keypress', function(e){
  if (e.keyCode == 9){
    e.preventDefault();
    document.getElementById("1").focus();
  }
  if ( e.shiftKey && ( e.keyCode == 9 ) ){
    e.preventDefault();
    document.getElementById((total_cols_entry - 1).toString()).focus();
  }

});

$("#1").on('keypress', function(e){
  if (e.shiftKey && ( e.keyCode == 9 ))
  {
    e.preventDefault();
    document.getElementById(total_cols_entry.toString()).focus();
  }
});
