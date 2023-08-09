$('.add_student_attendance').click(function(){
      if ($(this).find('.add_student_ckbx').is(':checked')) {
        $(this).children('span').html('Present').css('background-color', '#a3e4a3');
      }
      else{
        $(this).children('span').html('Absent').css('background-color', '#fff');;
      }
    });
