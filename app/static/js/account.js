document.addEventListener('DOMContentLoaded', function () {
  const editForm = document.querySelector('.edit__form');
  if (editForm) {
    const gif = document.querySelector('#gif');
    if(gif) {
      editForm.addEventListener('submit', function(){
        gif.style.visibility = 'visible';
        gif.style.height = '100%';
        document.querySelectorAll(".btn-container").forEach(function(btn) {
          btn.remove();
        });
      });
    }
  }
});
