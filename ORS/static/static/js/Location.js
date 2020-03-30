$(document).ready(function(){
        var conurl="http://127.0.0.1:8000/auth/ajax/Country";
        $.ajax({
              type :"GET",
              url : conurl,
              success: function(data){
                  for(var i =0;i<data.data.length;i++)
                  {
                      $("#country").append("<option value="+data.data[i].id+">"+data.data[i].CountryName+"</option>");
                  }
              },
              Error: function(){
                  alert("failed");
              }
        })
   });

    $("#country").change(function(){
           var action="http://127.0.0.1:8000/auth/ajax/State"
          $("#state").empty();
          $("#state").append("<option value='0'>Select State</option>");
          $("#city").empty();
          $("#city").append("<option value='0'>Select City</option>");
          //alert($("#country").val())
          //console.log($("#country").val());
          if($("#country").val() == 0)
          {
              swal({'title':'Select Country', 'text':'Fill the mandetory fields',icon: "warning"});
          }
          else
          {

                $.ajax({
                    type :"GET",
                      url : action,
                      data:{ "conid" :$(this).val() },
                      success: function(data2){
                           //alert("success");
                          for(var i =0;i<data2.State.length;i++)
                          {
                             $("#state").append("<option value="+data2.State[i].id+">"+data2.State[i].StateName+"</option>");
                          }
                      },
                      Error: function(){
                          alert("failed");
                      }
                });
          }
    });

    $("#state").change(function(){
        var action ="http://127.0.0.1:8000/auth/ajax/City";
        $("#city").empty();
        $("#city").append("<option value='0'>Select City</option>");
        if($(this).val() == 0 ){
            swal({'title':'Select State', 'text':'Fill the mandetory fields',icon: "warning"});
        }
         else
         {
            $.ajax({
                type :"GET",
                  url : action,
                  data:{ "stateid" :$(this).val() },
                  success: function(data2){
                      // alert("success");
                      for(var i =0;i<data2.City.length;i++)
                      {
                         $("#city").append("<option value="+data2.City[i].id+">"+data2.City[i].CityName+"</option>");
                      }
                  },
                  Error: function(){
                      alert("failed");
                  }
            });
         }
    });
