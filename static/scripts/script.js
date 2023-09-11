

const drag = (event) => {
  event.dataTransfer.setData("text/plain", event.target.id);
}

const allowDrop = (ev) => {
  ev.preventDefault();
  if (hasClass(ev.target,"dropzone")) {
    addClass(ev.target,"droppable");
  }
}

const clearDrop = (ev) => {
    removeClass(ev.target,"droppable");
}

const drop = (event) => {
  event.preventDefault();
  const data = event.dataTransfer.getData("text/plain");
   const element = document.querySelector(`#${data}`);
  
  
  
   try {
    // remove the spacer content from dropzone
    event.target.removeChild(event.target.firstChild);
    // add the draggable content
    event.target.appendChild(element);
    
    // remove the dropzone parent
    unwrap(event.target);
  } catch (error) {
    console.warn("can't move the item to the same place")
  }
  updateDropzones();

  
  let newStatus=($(element).parents("div.card-body").find("h6.card-title").text());
  let id = data.replace(/[^0-9]/g, "");
  console.log
  (`Element: ${element}
  Data: ${data}`)
  console.log
 (`Data : ${data}
New Status : ${$(element).parents("div.card-body").find("h6.card-title").text()}
ID : ${id}`);

updateDb(id, newStatus);

}
// send the moved card details  to the server and update DB
const updateDb=(id, newStatus) => {
 //
  var csrfToken = $('meta[name=csrf-token]').attr('content')
// console.log(`CSRF TOKEN: ${csrfToken}`);
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
              xhr.setRequestHeader("X-CSRFToken", csrfToken)
          }
      }
  })

  var request = $.ajax({
    url: "/postmethod",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      id: id, 
      status: newStatus,
    }),  
    dataType: "json",
 })  
   .done( function (request) {
    console.log(`
    DB update Status ${request.status}
    `);
    if (request.status ==='success'){
      location.href = window.origin
      }
 })
 

// $.post( "/postmethod", {
//   updateStatusData:
//   {  id: id,
//   status: newStatus,}
// },
// (updateDbStatus) => {
// console.log(`DB update Status ${updateDbStatus}`);
// }
// );
}
const updateDropzones = () => {
    /* after dropping, refresh the drop target areas
      so there is a dropzone after each item
      using jQuery here for simplicity */

    var dz = $('<div class="dropzone rounded" ondrop="drop(event)" ondragover="allowDrop(event)" ondragleave="clearDrop(event)"> &nbsp; </div>');

    // delete old dropzones
    $('.dropzone').remove();

    // insert new dropdzone after each item
    dz.insertAfter('.card.draggable');

    // insert new dropzone in any empty swimlanes
    $(".items:not(:has(.card.draggable))").append(dz);
};

// helpers
function hasClass(target, className) {
    return new RegExp('(\\s|^)' + className + '(\\s|$)').test(target.className);
}

function addClass(ele,cls) {
  if (!hasClass(ele,cls)) ele.className += " "+cls;
}

function removeClass(ele,cls) {
  if (hasClass(ele,cls)) {
    var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
    ele.className=ele.className.replace(reg,' ');
  }
}

function unwrap(node) {
    node.replaceWith(...node.childNodes);
}

function forcePopUp(){
  jQuery('#timePopup').modal('show');
}

// Alert closing automatically

setTimeout(function () {

  // Closing the alert
  $( "div[id^='alert-']" ).alert('close');
}, 8000);




// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()