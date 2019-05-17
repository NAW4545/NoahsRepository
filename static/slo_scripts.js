var programs;
$.getJSON('/program_data', function(data){
  programs = data;
});

$('#add_program').click(function(){
  outcomeGroup = $('.outcomes_select').last();
  newOutcomeGroup = outcomeGroup.clone(true);
  newOutcomeGroup.find('.outcomes').empty();
  outcomeGroup.after(newOutcomeGroup);
});

$('.remove_program').click(function(){
  $(this).parent().remove();
});

$('.program_select').change(function(){
  let outcomes = programs[$(this).val()];
  $(this).siblings('.outcomes').empty();
  for (let outcome in outcomes) {
    let pout_id = outcomes[outcome][0];
    let pout_desc = outcomes[outcome][1];
    $(this).siblings('.outcomes').append(
      $('<input>').attr({ 'type':"checkbox", 'name': "outcome", 'id': pout_id, 'value': pout_id})
    );
    $(this).siblings('.outcomes').append(
      $('<label></label>').attr({ 'for': pout_id}).text(pout_desc)
    );
    console.log(pout_id, pout_desc);
  }
});

// progSelect = newOutcomeGroup.find('.program_select');
// for (var program in programs) {
//   progSelect.add('option').attr;
//   console.log(program);
// }
