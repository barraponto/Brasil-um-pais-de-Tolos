$("#criar_sala").keypress(function(event) {
  if ( event.which == 13 ) {
     event.preventDefault();
     texto = $("#criar_sala").val();
     $("#criar_sala").val("");
     location.href="/sala/"+texto+"/";
   }
});

function atualizar_central() {
  $.post("atualizar", function(data){
    if(data!="0"){
      dic = JSON.parse(data);
      $('#salas').html(dic["salas"]);
      $('#participantes_central').html(dic["jogadores"]);
    }
  })
  .error(function(data) { alert("Erro ao Atualizar_Sala!"+data); });
}

setInterval('atualizar_central()', 2000);
