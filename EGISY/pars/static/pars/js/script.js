$(document).ready(function(){

 $("#submit").click(function () {
    console.log('Нажал');
    term = $("#term").val();
    console.log(term);
    localStorage.setItem('secretIdentity', term)

  });
  var test = localStorage.getItem('secretIdentity');
  localStorage.setItem('secretIdentity', test)
  console.log( localStorage.getItem('secretIdentity'));
  var n = "0";

  $("body").highlight(test);
  n = $("span.highlight").length;
   if($(location).attr('href')=='http://127.0.0.1:8000/')
   {
   localStorage.setItem('secretIdentity', null)

        $('body').removeHighlight();
   }
 })
