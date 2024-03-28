$(document).ready(function(){

 $("#submit").click(function () {
    console.log('Нажал');
    term = $("#term").val();
    console.log(term);
    localStorage.setItem('secretIdentity', term)

  });
  let test = localStorage.getItem('secretIdentity');
  console.log(test);
  var term = "";
  var n = "0";
  $("body").removeHighlight();
  $("p.results").hide().empty();
  $("body").highlight(test);
  n = $("span.highlight").length;
  localStorage.setItem('secretIdentity', null)
 })
